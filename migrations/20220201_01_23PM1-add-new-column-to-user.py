"""
add new column to user
"""

from yoyo import step

__depends__ = {'20220131_06_5bdgX-add-primary-key-for-eventawardrecipients-table'}
steps = [
    step("ALTER TABLE `user` ADD `lastAnonymousMsg` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER `vipLevel`;")
]
