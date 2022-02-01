"""
add Black Jack record
"""

from yoyo import step

__depends__ = {'20211011_01_MvHgE-add-column-for-user-robsince'}
__transactional__ = False
steps = [
    step("CREATE TABLE `blackJackGameRecord` ( `userID` BIGINT NOT NULL , `money` BIGINT NOT NULL , `status` INT(2) NOT NULL COMMENT '0 represent in progress; 1 represent lose; 2 represent win' , `tableID` BIGINT NOT NULL ) ENGINE = InnoDB;")
]
