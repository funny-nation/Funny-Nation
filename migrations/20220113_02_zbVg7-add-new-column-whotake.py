"""
add new column whoTake
"""

from yoyo import step

__depends__ = {'20220113_01_uTmuw-new-lucky-money-table'}
__transactional__ = False
steps = [
    step("ALTER TABLE `luckyMoney` ADD `whoTake` TEXT NOT NULL AFTER `senderMsgID`;")
]
