"""
add primary key for eventAwardRecipients table
"""

from yoyo import step

__depends__ = {'20220131_05_J51LT-add-status-column-to-eventaward-table'}

steps = [
    step("ALTER TABLE `eventAwardRecipients` ADD PRIMARY KEY(`approvePrivateMSGID`);")
]
