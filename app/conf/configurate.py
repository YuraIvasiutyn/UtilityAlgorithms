import configparser
from os.path import abspath, dirname, join


path_of_conf = join(abspath(dirname(__file__)), 'conf')
config = configparser.RawConfigParser()
config.read(path_of_conf, encoding='utf-8')
