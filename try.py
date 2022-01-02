import configparser

config = configparser.ConfigParser()
config.read('vipTags.ini')
print(config.has_option('1', 'df'))


