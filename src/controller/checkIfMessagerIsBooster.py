
def checkIfMessagerIsBooster(self, user):
    """
    Function would be called by Robot class
    :param self: instance from Robot
    :param user: instance from Discord.User
    :return: True if user is a booster
    """
    for role in user.roles:
        if role == self.boostedRole:
            return True
    return False
