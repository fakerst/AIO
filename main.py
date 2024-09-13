import sys

from AIO import *
from utils.utils_else import *
from utils.feature import *

if __name__ == "__main__":
    cmd = get_cmd(sys.argv)
    aio = AIO(cmd)
    aio.run()