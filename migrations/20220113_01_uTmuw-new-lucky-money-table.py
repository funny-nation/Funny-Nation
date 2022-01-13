"""
new lucky money table
"""

from yoyo import step

__depends__ = {'20211231_02_zOlGp-set-0-default-value-for-vip-level'}

steps = [
    step("CREATE TABLE `luckyMoney` ( `uuid` VARCHAR(64) NOT NULL , `sender` BIGINT NOT NULL , `moneyLeft` BIGINT NOT NULL , `quantityLeft` INT(8) NOT NULL , `senderMsgID` BIGINT NOT NULL , PRIMARY KEY (`uuid`)) ENGINE = InnoDB;")
]
