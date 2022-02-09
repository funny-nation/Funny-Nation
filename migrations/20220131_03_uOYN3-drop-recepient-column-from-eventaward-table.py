"""
drop recepient column from eventaward table
"""

from yoyo import step

__depends__ = {'20220131_02_lhRKF-add-primary-key-for-eventaward-table'}

steps = [
    step("ALTER TABLE `eventAward` DROP `recipient`;")
]
