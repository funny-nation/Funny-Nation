"""
change comment on holdemGameRecord
"""

from yoyo import step

__depends__ = {'20211128_01_Mn7Ng-create-holdem-game-record-table'}
__transactional__ = False
steps = [
    step("ALTER TABLE `holdemGameRecord` CHANGE `status` `status` INT NOT NULL COMMENT '0 represent in progress; 1 represent lose or fold; 2 represent win; 3 represent game close';")
]
