"""
Add column for user 'robSince'
"""

from yoyo import step

__depends__ = {'20211006_02_Zsic7-create-cashflow-table'}
__transactional__ = False
steps = [
    step("ALTER TABLE `user` ADD `robSince` TIMESTAMP NOT NULL AFTER `lastCheckIn`;")
]
