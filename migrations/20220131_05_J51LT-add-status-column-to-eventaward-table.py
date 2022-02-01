"""
add status column to eventaward table
"""

from yoyo import step

__depends__ = {'20220131_04_wXyY0-new-table-eventawardrecipients'}

steps = [
    step("ALTER TABLE `eventAward` ADD `status` INT(2) NOT NULL COMMENT '0 represent open; 1 represent closed' AFTER `eventName`;")
]
