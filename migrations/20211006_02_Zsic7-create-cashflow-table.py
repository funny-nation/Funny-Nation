"""
create cashflow table
"""

from yoyo import step

__depends__ = {'20211006_01_gSl3C-create-user-database'}
__transactional__ = False
steps = [
    step("CREATE TABLE `cashFlow` ( `flowID` BIGINT(255) NOT NULL AUTO_INCREMENT , `userID` BIGINT(255) NOT NULL , `amount` BIGINT(255) NOT NULL , `message` TEXT NOT NULL , `date` TIMESTAMP NOT NULL , PRIMARY KEY (`flowID`)) ENGINE = InnoDB;")
]
