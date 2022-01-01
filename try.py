import configparser

config = configparser.ConfigParser()
config.read('vipTags.inid')
print(config.sections())
