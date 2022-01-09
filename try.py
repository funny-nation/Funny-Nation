import configparser

config = configparser.ConfigParser()
config.read('admins.ini')
l = []
for section in config.sections():
    l.append(int(config[section]['id']))
print(l)
