from src.checkBeforeRun.databaseConnectionCheck import databaseConnectionCheck
from loguru import logger

def checkBeforeRun():
    if not databaseConnectionCheck():
        logger.error("Database connection error")
        exit(1)