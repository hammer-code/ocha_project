from bless.libs import database
from bless.libs import parsing_utils
from bless.libs import utils
from .setting import database_setting
from os import rename, remove


def initialize(file=None, path=None):
    obj_data = utils.yaml_read(file)
    # Create APP
    app_name =  obj_data['config']['app']['name']
    app_framework =  obj_data['config']['app']['framework']
    app_path = utils.read_app(app_name, path=path)

    if not utils.read_app(app_name, path=path):
        create_app = parsing_utils.create_app(app_name, app_framework, path=path)
    else:
        path_rm = app_path
        utils.remove_folder(path_rm)
        create_app = parsing_utils.create_app(app_name, app_framework, path=path)

    # Set App Constructor
    app_path = utils.read_app(app_name, path=path)
    driver_var = None
    try:
        driver_var = obj_data['config']['database']['driver']
    except Exception:
        driver_var = None

    if driver_var:
        driver_setting = database_setting['driver'][driver_var]
        init_src = app_path+"/app/"+driver_setting['constructor']
        init_dst = app_path+"/app/__init__.py"
        rename(init_src , init_dst)
        for driver_key in database_setting['driver']:
            if driver_key != driver_var:
                try:
                    remove(app_path+"/app/"+ database_setting['driver'][driver_key]['constructor'])
                except Exception as e:
                    print(e)

    # create environment
    if not utils.read_file(app_path+"/.env"):
        parsing_utils.create_env(obj_data['config'], app_path)
    if not utils.read_file(app_path+"/production.sh"):
        parsing_utils.create_production_env(obj_data['config'], app_path)

    # setup endpoint
    endpoint_data = obj_data['endpoint']
    parsing_utils.set_endpoint_template(endpoint_data, app_path)
    security = None
    
    for i in endpoint_data:
        try:
            security = endpoint_data[i]['auth']
        except Exception:
            security = None
        parsing_utils.create_file_controller(i, app_path, security)

    # setup routing
    parsing_utils.create_routing(endpoint_data, app_path)

    # create moduls
    nm_modul = None
    for key_i in endpoint_data:
        for end_i in endpoint_data[key_i]:
            modules_data = None
            try:
                modules_data = endpoint_data[key_i][end_i]['moduls']
            except Exception:
                modules_data = None
            if modules_data:
                for nm_moduls in modules_data:
                    if nm_modul == nm_moduls:
                        parsing_utils.add_function_moduls(nm_modul,modules_data, app_path)
                        nm_modul = nm_moduls
                    else:
                        parsing_utils.create_moduls(nm_moduls,modules_data, app_path)
                        nm_modul = nm_moduls

    # database setup
    config_database = obj_data['config']['database']
    auth_config = obj_data['auth']
    if config_database['host'] == "localhost" or config_database['host'] == "127.0.0.1":
        database.database_parse(config_database,obj_data['database'], security, auth_config)

    # execute project

    return app_path