# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 22:01:04 2020

@author: sergi
"""

from sompy.sompy import SOMFactory
import sompy
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_rows', 100)

# %%
df = pd.read_csv('./analisys_datasus/bases/ETLSIM.DORES_1997.csv', sep='	')

# %%
colunas_apagar = [
    'NUMERODO',
    'def_tipo_obito',
    'DTOBITO',
    'ano_obito',
    'DTNASC',
    'ano_nasc',
    'idade_obito_anos',
    'idade_obito_meses',
    'idade_obito_dias',
    'idade_obito_horas',
    'idade_obito_mins',
    'def_sexo',
    'def_raca_cor',
    'def_est_civil',
    'def_escol',
    'def_loc_ocor',
    'def_escol_mae',
    'def_gravidez',
    'def_gestacao',
    'def_parto',
    'def_obito_parto',
    'def_obito_grav',
    'def_obito_puerp',
    'def_assist_med',
    'def_exame',
    'def_cirurgia',
    'def_necropsia',
    'LINHAA',
    'LINHAB',
    'LINHAC',
    'LINHAD',
    'LINHAII',
    'def_circ_obito',
    'def_acid_trab',
    'NUMERODV',
    'def_fonte',
    'HORAOBITO',
    'NUMSUS',
    'ESC2010',
    'ESCMAE2010',
    'NUMERODN',
    'CRM',
    'COMUNSVOIM',
    'NUMEROLOTE',
    'DTCADASTRO',
    'STCODIFICA',
    'CODIFICADO',
    'VERSAOSIST',
    'VERSAOSCB',
    'DTRECEBIM',
    'DTRECORIGA',
    'ESCMAEAGR1',
    'ESCFALAGR1',
    'STDOEPIDEM',
    'STDONOVA',
    'DIFDATA',
    'causabas_capitulo',
    'causabas_grupo',
    'causabas_categoria',
    'causabas_subcategoria',
    'res_coordenadas',
    'ocor_coordenadas']

df = df.drop(columns=colunas_apagar)

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
data = df[['idade_obito_calculado',
           'ocor_LATITUDE', 'ocor_LONGITUDE', 'ocor_ALTITUDE',
           'SEXO', 'RACACOR', 'ESTCIV', 'ESC']]
del df
# %%
sm = SOMFactory().build(data.values,
                        [100, 100],
                        mask=None, mapshape='planar',
                        lattice='rect',
                        normalization='var',
                        initialization='pca',
                        component_names=list(data.columns))

sm.train(n_job=-1, verbose='info', train_rough_len=20, train_finetune_len=20)

topographic_error = sm.calculate_topographic_error()
quantization_error = np.mean(sm._bmu[1])
print("Topographic error = {0}; Quantization error = {1}".format(
    topographic_error, quantization_error))

# %%
view2D = sompy.mapview.View2D(100, 100, "rand data", text_size=14)
view2D.show(sm, col_sz=2, which_dim="all", denormalize=True)

