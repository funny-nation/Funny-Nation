from discord import Member, Role


def checkIfMessagerIsBooster(boostedRole: Role, user: Member) -> bool:
    """
    Function would be called by Robot class
    :param boostedRole: Role for who boosted the server
    :param user: instance from Discord.User
    :return: True if user is a booster
    """
    for role in user.roles:
        if role == boostedRole:
            return True
    return False
