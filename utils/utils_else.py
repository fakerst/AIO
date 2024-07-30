import os
import subprocess
from pathlib import Path

import numpy as np
#import pandas as pd

def normalize_path(path):
    return Path(path).resolve()

