"""
create user database
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE `funnyNationsDevelopment`.`user` ( `userID` BIGINT(255) NOT NULL , `money` BIGINT(255) NOT NULL , `lastEarnFromMessage` TIMESTAMP NOT NULL , `lastCheckIn` TIMESTAMP NOT NULL , PRIMARY KEY (`userID`)) ENGINE = InnoDB;")
]
