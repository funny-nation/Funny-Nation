"""
Remove lastAnonymousMsg column
"""

from yoyo import step

__depends__ = {'20220116_01_WieLm-add-event-award-table', '20220116_06_3APs6-change-column-name', '20220201_01_23PM1-add-new-column-to-user'}

steps = [
    step("ALTER TABLE `user` DROP `lastAnonymousMsg`;")
]
