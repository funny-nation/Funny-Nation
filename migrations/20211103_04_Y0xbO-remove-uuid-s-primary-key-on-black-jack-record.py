"""
Remove uuid's primary key on black jack record
"""

from yoyo import step

__depends__ = {'20211103_03_gjqVL-new-column-uuid-on-black-jack-record'}

steps = [
    step("ALTER TABLE `blackJackGameRecord` DROP PRIMARY KEY;")
]
