import discord

from src.Robot import Robot
from src.checkBeforeRun.checkBeforeRun import checkBeforeRun
from src.utils.readConfig import getMajorConfig


def run():
    checkBeforeRun()
    config = getMajorConfig()
    intents = discord.Intents().all()
    robot = Robot(intents=intents)
    robot.run(config['private']['token'])


run()
