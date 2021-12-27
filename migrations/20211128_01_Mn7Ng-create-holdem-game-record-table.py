"""
Create holdem game record table
"""

from yoyo import step

__depends__ = {'20211109_01_xKblp-change-comments-on-black-jack-record'}

steps = [
    step("CREATE TABLE `holdemGameRecord` ( `userID` BIGINT NOT NULL , `moneyInvested` BIGINT NOT NULL , `status` INT NOT NULL COMMENT '0 represent in progress; 1 represent lose or fold; 2 represent win;' , `tableID` BIGINT NOT NULL , `time` TIMESTAMP NOT NULL , `tableUUID` VARCHAR(64) NOT NULL ) ENGINE = InnoDB;")
]
