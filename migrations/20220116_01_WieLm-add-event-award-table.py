"""
add event award table
"""

from yoyo import step

__depends__ = {'20220114_03_Heqaz-insert-default-serverinfo'}

steps = [
    step("CREATE TABLE `eventAward` ( `eventID` VARCHAR(64) NOT NULL , `eventManagerID` BIGINT NOT NULL , `eventMsgID` BIGINT NOT NULL , `money` BIGINT NOT NULL , `eventName` VARCHAR(32) NOT NULL , `recipient` TEXT NOT NULL , PRIMARY KEY (`eventID`)) ENGINE = InnoDB;")
]
