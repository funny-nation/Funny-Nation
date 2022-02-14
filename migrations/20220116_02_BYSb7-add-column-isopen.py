"""
add column isOpen
"""

from yoyo import step

__depends__ = {'20220116_01_HKwbd-new-lottory-table'}

steps = [
    step("ALTER TABLE `lottery` ADD `isOpen` INT(2) NOT NULL AFTER `price`;")
]
