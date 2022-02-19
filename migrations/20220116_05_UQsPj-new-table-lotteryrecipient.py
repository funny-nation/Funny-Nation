"""
new table lotteryRecipient
"""

from yoyo import step

__depends__ = {'20220116_04_1xwKi-change-primary-key-for-lottery'}

steps = [
    step("CREATE TABLE `lotteryRecipient` ( `recipientID` BIGINT NOT NULL , `msgID` BIGINT NOT NULL ) ENGINE = InnoDB;")
]
