import configparser
from src.Robot import Robot
import os

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/config.ini')


robot = Robot()
robot.run(config['private']['token'])
