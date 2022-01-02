"""
set 0 default value for vip level
"""

from yoyo import step

__depends__ = {'20211231_01_pmL1v-add-column-viplevel-in-user'}

steps = [
    step("ALTER TABLE `user` CHANGE `vipLevel` `vipLevel` INT NOT NULL DEFAULT '0';")
]
