"""
change activityStat column
"""

from yoyo import step

__depends__ = {'20220217_01_ZAQ5Y-remove-lastanonymousmsg-column'}

steps = [
    step("ALTER TABLE `activityStat` CHANGE `activityValue` `activityPoint` INT NOT NULL DEFAULT '0';")
]
