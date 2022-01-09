import configparser

vipTagsConfig = configparser.ConfigParser()
vipTagsConfig.read('vipTags.ini')

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini')

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini')

majorConfig = configparser.ConfigParser()
majorConfig.read('config.ini')

adminListConfig = configparser.ConfigParser()
adminListConfig.read('admins.ini')


def getVipTagsConfig():
    if len(vipTagsConfig.sections()) == 0:
        return None
    return vipTagsConfig


def getLanguageConfig():
    return languageConfig


def getMajorConfig():
    return majorConfig


def getAdminListConfig():
    if len(adminListConfig.sections()) == 0:
        return None
    return adminListConfig

