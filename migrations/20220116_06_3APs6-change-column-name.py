"""
change column name
"""

from yoyo import step

__depends__ = {'20220116_05_UQsPj-new-table-lotteryrecipient'}

steps = [
    step("ALTER TABLE `lottery` CHANGE `quantityLeft` `quantity` INT NOT NULL;")
]
