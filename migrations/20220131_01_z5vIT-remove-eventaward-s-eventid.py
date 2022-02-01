"""
remove eventAward's eventID
"""

from yoyo import step

__depends__ = {'20220114_03_Heqaz-insert-default-serverinfo'}
__transactional__ = False

steps = [
    step("ALTER TABLE `eventAward` DROP `eventID`;")
]
