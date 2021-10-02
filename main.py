import configparser
from src.Robot import Robot

config = configparser.ConfigParser()
config.read('config.ini')


robot = Robot()
robot.run(config['private']['token'])
