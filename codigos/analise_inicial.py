# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 22:01:04 2020

@author: sergi
"""

from sompy.sompy import SOMFactory
import sompy
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_rows', 100)

# %%
df = pd.read_csv('./analisys_datasus/bases/ETLSIM.DORES_1997.csv', sep='	')

# %%
dic_variaveis = pd.read_csv(
    './analisys_datasus/documentacao/dic_variaveis.csv', sep=';').values

colunas_apagar = [dic_variaveis[i, 0] for i in range(len(dic_variaveis))
                  if dic_variaveis[i, 1] == 'x']
df = df.drop(columns=colunas_apagar)

for i in range(len(dic_variaveis)):
    coluna, _, nulo = dic_variaveis[i]
    if not np.isnan(nulo):
        df[coluna] = df[coluna].replace({nulo: np.nan})

# %%
colunas_apagar = []
total_linhas = df.shape[0]
perc_nulo_max = 0.4
for c in df:
    perc_nulo = df[c].isnull().sum() / total_linhas
    if perc_nulo > perc_nulo_max:
        print(c, perc_nulo)
        colunas_apagar.append(c)
df = df.drop(columns=colunas_apagar)
df = df.dropna()

# %%
for c in df:
    if df[c].dtype == 'object':
        encoder = OrdinalEncoder()
        df[c] = encoder.fit_transform(df[c].values.reshape(-1, 1))

# %%
sm = SOMFactory().build(df.values,
                        [20, 20],
                        mask=None, mapshape='planar',
                        lattice='rect',
                        normalization='var',
                        initialization='pca',
                        component_names=list(df.columns))

sm.train(n_job=-1, verbose='info', train_rough_len=20, train_finetune_len=20)

topographic_error = sm.calculate_topographic_error()
quantization_error = np.mean(sm._bmu[1])
print("Topographic error = {0}; Quantization error = {1}".format(
    topographic_error, quantization_error))

# %%
view2D = sompy.mapview.View2D(100, 100, "rand data", text_size=14)
view2D.show(sm, col_sz=2, which_dim="all", denormalize=True)