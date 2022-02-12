"""
new lottory table
"""

from yoyo import step

__depends__ = {'20220114_03_Heqaz-insert-default-serverinfo'}

steps = [
    step("CREATE TABLE `lottery` ( `publisherID` BIGINT NOT NULL , `msgID` BIGINT NOT NULL , `name` VARCHAR(64) NOT NULL , `quantityLeft` INT(16) NOT NULL , `price` BIGINT NOT NULL ) ENGINE = InnoDB;")
]
