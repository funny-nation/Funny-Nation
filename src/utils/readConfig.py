import configparser

vipTagsConfig = configparser.ConfigParser()
vipTagsConfig.read('vipTags.ini', encoding='utf-8')

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

majorConfig = configparser.ConfigParser()
majorConfig.read('config.ini', encoding='utf-8')

adminListConfig = configparser.ConfigParser()
adminListConfig.read('Admins.ini', encoding='utf-8')

eventListConfig = configparser.ConfigParser()
eventListConfig.read('eventAdmins.ini', encoding='utf-8')

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
def getEventAdminListConfig():
    if len(eventListConfig.sections()) == 0:
        return None
    return eventListConfig

