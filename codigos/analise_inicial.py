# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 22:01:04 2020

@author: sergi
"""

import sompy
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_rows', 100)

# %%
df = pd.read_csv('./bases/ETLSIM.DORES_1997.csv', sep='	')
df.shape
