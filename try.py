# import configparser
#
# config = configparser.ConfigParser()
# config.read('giftConfig.ini')
# for keys in config.sections():
#     print(keys)

import glob
from pathlib import Path

for i in glob.glob('*'):
    print(Path(i).stem)