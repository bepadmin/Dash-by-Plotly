# -*- coding: utf-8 -*-
"""
Created on Thu May 27 13:04:40 2021

@author: wlim
"""

import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../webids").resolve()
print(DATA_PATH)