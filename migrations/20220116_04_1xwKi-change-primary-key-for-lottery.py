"""
change primary key for lottery
"""

from yoyo import step

__depends__ = {'20220116_03_TxUNA-set-primary-key-in-lottery'}

steps = [
    step("ALTER TABLE `lottery` DROP PRIMARY KEY, ADD PRIMARY KEY(`msgID`);")
]
