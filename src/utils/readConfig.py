import configparser

vipTagsConfig = configparser.ConfigParser()
vipTagsConfig.read('vipTags.ini', encoding='utf-8')

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

majorConfig = configparser.ConfigParser()
majorConfig.read('config.ini', encoding='utf-8')

giftConfig = configparser.ConfigParser()
giftConfig.read('giftConfig.ini', encoding='utf-8')

cashFlowMsgConfig = configparser.ConfigParser()
cashFlowMsgConfig.read('cashFlowMsg.ini', encoding='utf-8')

generalConfig = configparser.ConfigParser()
generalConfig.read('generalConfig.ini', encoding='utf-8')

adminListConfig = configparser.ConfigParser()
adminListConfig.read('admins.ini', encoding='utf-8')

def getVipTagsConfig():
    if len(vipTagsConfig.sections()) == 0:
        return None
    return vipTagsConfig


def getLanguageConfig():
    return languageConfig


def getMajorConfig():
    return majorConfig

def getCashFlowMsgConfig():
    return cashFlowMsgConfig

def getGeneralConfig():
    return generalConfig


def getAdminListConfig():
    if len(adminListConfig.sections()) == 0:
        return None
    return adminListConfig

def getGiftConfig():
    return giftConfig

