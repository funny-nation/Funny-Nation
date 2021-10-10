import configparser
from src.Robot import Robot

# read env vars
config = configparser.ConfigParser()
config.read('config.ini')

# start robot
robot = Robot()
robot.run(config['private']['token'])
