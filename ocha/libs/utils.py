import yaml
import os
import shutil
import git
import requests
import zipfile
import coloredlogs
import logging
from dotenv import load_dotenv
from urllib.request import urlopen


APP_HOME = os.path.expanduser("~")
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def question(word):
    answer = False
    while answer not in ["y", "n"]:
        answer = input("{} [y/n]? ".format(word)).lower().strip()

    if answer == "y":
        answer = True
    else:
        answer = False
    return answer

def report(head = None, value = None):
    if not value:
        value = ""
    coloredlogs.install()
    logging.info(head+value)


def log_warn(stdin):
    coloredlogs.install()
    logging.warn(stdin)


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)


def check_keys(obj, keys):
    chek = None
    try:
        chek = obj[keys]
    except Exception:
        log_warn(Exception)
        exit()
    else:
        return chek


def template_git(url, dir):
    try:
        chk_repo = os.path.isdir(dir)
        if chk_repo:
            shutil.rmtree(dir)
        git.Repo.clone_from(url, dir)
        return True
    except Exception as e:
        print(e)
        return False


def yaml_parser(stream):
    try:
        data = yaml.load(stream)
        return data
    except yaml.YAMLError as exc:
        print(exc)


def yaml_create(stream, path):
    with open(path, 'w') as outfile:
        try:
            yaml.dump(stream, outfile, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)
        else:
            return True

def yaml_writeln(stream, path):
    with open(path, '+a') as outfile:
        try:
            yaml.dump(stream, outfile, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)
        else:
            return True


def yaml_read(path):
    with open(path, 'r') as outfile:
        try:
            data = yaml.load(outfile)
        except yaml.YAMLError as exc:
            print(exc)
        else:
            return data


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def copyfile(src, dest):
    try:
        shutil.copyfile(src, dest)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def read_file(file):
    if os.path.isfile(file):
        return True
    else:
        return False

def read_app(app_name, path=None):
    if path is None:
        app_path = APP_HOME+"/BLESS/"+app_name
    else:
        app_path = path+"/"+app_name
    if not os.path.exists(app_path):
        return None
    else:
        return app_path

def create_file(file, path=None, value=None):
    default_path = APP_HOME
    if path:
        default_path = path
    f=open(default_path+"/"+file, "a+")
    f.write(value)
    f.close()

    try:
        return read_file(default_path+"/"+file)
    except Exception as e:
        print(e)

def check_internet():
    try:
        urlopen("https://raw.githubusercontent.com")
    except Exception as e:
        print(e)
    else:
        return True


def download(url):
    try:
        response = urlopen(url)
    except Exception as e:
        print(e)
    else:
        return response


def check_folder(path):
    return os.path.isdir(path)


def create_folder(path):
    return os.makedirs(path)


def remove_folder(path):
    return shutil.rmtree(path)


def read_value(file):
    value = open(file)
    return value.read()


# for login deploy
def check_env():
    return os.path.isfile("{}/.ocha.env".format(APP_HOME))


def load_env_file():
    return load_dotenv("{}/.ocha.env".format(APP_HOME), override=True)

def get_env_values():
    if check_env():
        load_env_file()
        ocha_env = {}
        ocha_env['username'] = os.environ.get('OS_USERNAME')
        ocha_env['password'] = os.environ.get('OS_PASSWORD')
        ocha_env['project_url'] = os.environ.get('OS_PROJECT_URL')
        ocha_env['project_port'] = os.environ.get('OS_PROJECT_PORT')
        return ocha_env
    else:
        print("Can't find ocha.env")

def send_http(url, data = None, headers=None):
    send = requests.post(url, json=data, headers=headers)
    respons = send.json()
    return respons

def sign_to_project(url, username, password):
    post_data = {
        "username": username,
        "password": password
    }
    resp = send_http(url, data=post_data)
    return resp


def list_dir(dirname):
    listdir = list()
    for root, dirs, files in os.walk(dirname):
        for file in files:
            data = {
                "index": file,
                "file": os.path.join(root, file)
            }
            listdir.append(data)
    return listdir

def get_http(url, headers=None):
    send = requests.get(url, headers=headers)
    respons = send.json()
    return respons

def make_archive(name, path):
    shutil.make_archive(name,"zip",path)


