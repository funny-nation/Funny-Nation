"""
new table serverInfo
"""

from yoyo import step

__depends__ = {'20220114_01_YcLdG-new-table-activitystat'}

steps = [
    step("CREATE TABLE `serverInfo` ( `onlineMinute` BIGINT NOT NULL ) ENGINE = InnoDB;")
]
