# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:14:11 2020

@author: sergi
"""
import pandas as pd

df_1 = pd.read_csv(r'D:\repositorios\analisys_datasus\PIBIC_2020_2021\base\com_anomalia.csv')

df_2 = pd.read_csv(r'D:\repositorios\analisys_datasus\PIBIC_2020_2021\base\sem_anomalia.csv')


df = pd.concat((df_1, df_2))
del df_1, df_2

df['IDANOMAL'.lower()].value_counts()
