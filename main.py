import configparser
from src.Robot import Robot
from src.checkBeforeRun.checkBeforeRun import checkBeforeRun

def run():
    checkBeforeRun()
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    robot = Robot()
    robot.run(config['private']['token'])

run()
