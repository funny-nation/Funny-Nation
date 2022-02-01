"""
new table activityStat
"""

from yoyo import step

__depends__ = {'20220113_02_zbVg7-add-new-column-whotake'}
__transactional__ = False
steps = [
    step("CREATE TABLE `activityStat` ( `userID` BIGINT NOT NULL , `activityValue` INT(64) NOT NULL , PRIMARY KEY (`userID`)) ENGINE = InnoDB;")
]
