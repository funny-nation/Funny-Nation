"""
New Column time on black jack record
"""

from yoyo import step

__depends__ = {'20211103_01_zW2CR-add-black-jack-record'}

steps = [
    step("ALTER TABLE `blackJackGameRecord` ADD `time` TIMESTAMP NOT NULL AFTER `tableID`;")
]
