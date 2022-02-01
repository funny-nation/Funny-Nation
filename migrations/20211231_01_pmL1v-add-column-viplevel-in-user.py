"""
add column vipLevel in user
"""

from yoyo import step

__depends__ = {'20211223_01_g7Y82-change-comment-on-holdemgamerecord'}
__transactional__ = False
steps = [
    step("ALTER TABLE `user` ADD `vipLevel` INT(64) NOT NULL AFTER `robSince`;")
]
