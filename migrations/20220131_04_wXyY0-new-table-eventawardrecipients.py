"""
new table eventAwardRecipients
"""

from yoyo import step

__depends__ = {'20220131_03_uOYN3-drop-recepient-column-from-eventaward-table'}
__transactional__ = False

steps = [
    step("CREATE TABLE `eventAwardRecipients` ( `eventMsgID` BIGINT NOT NULL , `recipientID` BIGINT NOT NULL , `approvePrivateMSGID` BIGINT NOT NULL , `status` INT(4) NOT NULL COMMENT '0 represent just created; 1 represent rejected; 2 represent approved' ) ENGINE = InnoDB;")
]
