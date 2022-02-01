"""
insert default serverInfo
"""

from yoyo import step

__depends__ = {'20220114_02_lHBKM-new-table-serverinfo'}
__transactional__ = False
steps = [
    step("INSERT INTO `serverInfo` (`onlineMinute`) VALUES (0);")
]
