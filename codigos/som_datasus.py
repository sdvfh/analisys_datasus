# -*- coding: utf-8 -*-
"""som_datasus.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iK49Tblp4-736B13qkbfUZLGoOAiUugP
"""

!pip install git+https://github.com/sevamoo/SOMPY.git

import glob
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
import sompy
from sompy.sompy import SOMFactory
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_rows', 100)

path_bases = '/content/drive/My Drive/ICFernando/Microdados_DATASUS/ETLSIM/Dados'
all_files = glob.glob(path_bases + "/ETLSIM.DORES_*.csv")
all_files = all_files[-10:]

dic_variaveis = pd.read_csv(
    '/content/drive/My Drive/ICFernando/Microdados_DATASUS/dic_variaveis.csv', sep=';').values

colunas_apagar = [dic_variaveis[i, 0] for i in range(len(dic_variaveis))
                  if dic_variaveis[i, 1] == 'x']

for i, path_base in enumerate(all_files):
    print(path_base)
    df_temp = pd.read_csv(path_base, sep='	')
    df_temp = df_temp.drop(columns=colunas_apagar)
    if i == 0:
        df = df_temp.copy()
    else:
        df = pd.concat((df, df_temp))

for i in range(len(dic_variaveis)):
    coluna, _, nulo = dic_variaveis[i]
    if not np.isnan(nulo):
        df[coluna] = df[coluna].replace({nulo: np.nan})

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

for c in df:
    if df[c].dtype == 'object':
        encoder = OrdinalEncoder()
        try:
            df[c] = encoder.fit_transform(df[c].values.reshape(-1, 1))
        except TypeError:
            print('apagar ', c)
            df = df.drop(columns=c)

sm = SOMFactory().build(df.values,
                        [50, 50],
                        mask=None, mapshape='planar',
                        lattice='rect',
                        normalization='var',
                        initialization='pca',
                        component_names=list(df.columns))

sm.train(n_job=2, verbose='info', train_rough_len=30, train_finetune_len=20)

with open(
    '/content/drive/My Drive/IC_Cristine/SOM/som_primeiro.pkl',
    'wb') as arq:
    pickle.dump(sm, arq)

view2D = sompy.mapview.View2D(100, 100, "rand data", text_size=14)
view2D.show(sm, col_sz=5, which_dim="all", denormalize=True)

topographic_error = sm.calculate_topographic_error()
quantization_error = np.mean(sm._bmu[1])
print("Topographic error = {0}; Quantization error = {1}".format(
    topographic_error, quantization_error))

colunas_apagar = [
    'TIPOBITO',
    'data_obito',
    'data_nasc',
    'res_MSAUDCOD',
    'res_RSAUDCOD',
    'ocor_MSAUDCOD',
    'ocor_RSAUDCOD',
    'res_SIGLA_UF',
    'res_NOME_UF',
    'ocor_SIGLA_UF',
    'ocor_NOME_UF',
    'causabas_subcategoria',
    ]
df = df.drop(columns=colunas_apagar)

sm = SOMFactory().build(df.values,
                        [50, 50],
                        mask=None, mapshape='planar',
                        lattice='rect',
                        normalization='var',
                        initialization='pca',
                        component_names=list(df.columns))

sm.train(n_job=2, verbose='info', train_rough_len=30, train_finetune_len=20)

with open(
    '/content/drive/My Drive/IC_Cristine/SOM/som_segundo.pkl',
    'wb') as arq:
    pickle.dump(sm, arq)

topographic_error = sm.calculate_topographic_error()
quantization_error = np.mean(sm._bmu[1])
print("Topographic error = {0}; Quantization error = {1}".format(
    topographic_error, quantization_error))

view2D = sompy.mapview.View2D(100, 100, "rand data", text_size=14)
view2D.show(sm, col_sz=5, which_dim="all", denormalize=True)

cl = sm.cluster(n_clusters=4)

h = sompy.hitmap.HitMapView(10, 10, 'hitmap', text_size=8, show_text=True)
h.show(sm)

u = sompy.umatrix.UMatrixView(50, 50, 'umatrix', show_axis=True, text_size=8, show_text=True)
UMAT = u.build_u_matrix(sm, distance=1, row_normalized=False)
UMAT = u.show(sm, distance2=1, row_normalized=False, show_data=True, contooor=True, blob=False)