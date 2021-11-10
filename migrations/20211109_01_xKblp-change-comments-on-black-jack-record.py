"""
change comments on black jack record
"""

from yoyo import step

__depends__ = {'20211103_04_Y0xbO-remove-uuid-s-primary-key-on-black-jack-record'}

steps = [
    step("ALTER TABLE `blackJackGameRecord` CHANGE `status` `status` INT NOT NULL COMMENT '0 represent in progress; 1 represent lose; 2 represent win; 3 represent draw; 4 represent closed; ';")
]
