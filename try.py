import configparser

config = configparser.ConfigParser()
config.read('vipTags.ini')
print(config.sections())

