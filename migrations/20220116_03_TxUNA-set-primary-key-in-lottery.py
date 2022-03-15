"""
set primary key in lottery
"""

from yoyo import step

__depends__ = {'20220116_02_BYSb7-add-column-isopen'}

steps = [
    step("ALTER TABLE `lottery` ADD PRIMARY KEY(`name`);")
]
