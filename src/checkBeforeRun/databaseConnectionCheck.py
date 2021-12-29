from src.model.makeDatabaseConnection import makeDatabaseConnection


def databaseConnectionCheck():
    db = makeDatabaseConnection()
    if db is None:
        return False
    db.close()
    return True
