import configparser

vipTagsConfig = configparser.ConfigParser()
vipTagsConfig.read('vipTags.ini')



def vipTagsConfig():
    if len(vipTagsConfig.sections()) == 0:
        return None
    return vipTagsConfig