import configparser
from src.Robot import Robot


def run():

    config = configparser.ConfigParser()
    config.read('config.ini')

    robot = Robot()
    robot.run(config['private']['token'])

