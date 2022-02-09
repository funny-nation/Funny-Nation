from src.Robot import Robot
from src.checkBeforeRun.checkBeforeRun import checkBeforeRun
from src.utils.readConfig import getMajorConfig


def run():
    checkBeforeRun()
    config = getMajorConfig()
    robot = Robot()
    robot.run(config['private']['token'])


run()
