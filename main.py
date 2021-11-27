import configparser
from src.Robot import Robot


def run():

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    robot = Robot()
    robot.run(config['private']['token'])

run()
