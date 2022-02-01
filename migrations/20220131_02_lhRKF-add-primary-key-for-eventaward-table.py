"""
add primary key for eventaward table
"""

from yoyo import step

__depends__ = {'20220131_01_z5vIT-remove-eventaward-s-eventid'}
__transactional__ = False

steps = [
    step("ALTER TABLE `eventAward` ADD PRIMARY KEY(`eventMsgID`);")
]
