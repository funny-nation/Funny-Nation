"""
New Column uuid on black jack record
"""

from yoyo import step

__depends__ = {'20211103_02_9SaYA-new-column-time-on-black-jack-record'}
__transactional__ = False
steps = [
    step("ALTER TABLE `blackJackGameRecord` ADD `uuid` VARCHAR(64) NOT NULL AFTER `time`, ADD PRIMARY KEY (`uuid`);")
]
