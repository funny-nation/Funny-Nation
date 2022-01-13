"""
add new column whoTake
"""

from yoyo import step

__depends__ = {'20220113_01_uTmuw-new-lucky-money-table'}

steps = [
    step("ALTER TABLE `luckyMoney` ADD `whoTake` TEXT NOT NULL AFTER `senderMsgID`;")
]
