# -*- coding: utf-8 -*-
"""Aula 28/08/2023.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YMWbcocTBdzPRZCVZ32I6mh3OIJAmXQK

Importando bibliotecas
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# %matplotlib inline

"""Analisando base de dados"""

#dados = pd.read_csv("Banana.csv")
#dados = pd.read_csv("Mammo.csv")
dados = pd.read_csv("Faults.csv")

dados.head()

dados.info()

df_dados = pd.DataFrame(dados)
df_dados.info()
#figura = df_dados.plot.scatter(x='A1',y='A2',c='Class',colormap='viridis')

"""Separando a base para os conjuntos de treino, validação e teste"""

from sklearn.model_selection import train_test_split
x_treino,x_temp,y_treino,y_temp=train_test_split(df_dados,dados['Class'],test_size=0.5,stratify=dados['Class'])
x_validacao,x_teste,y_validacao,y_teste=train_test_split(x_temp,y_temp,test_size=0.5, stratify = y_temp)
print("Treino")
x_treino.info()
y_treino.info()
print("\nValidação")
x_validacao.info()
y_validacao.info()
print("\nTeste")
x_teste.info()
y_teste.info()

"""Executando o KNN"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

KNN = KNeighborsClassifier(n_neighbors=30,weights="distance")
KNN.fit(x_treino,y_treino)
opiniao = KNN.predict(x_validacao)
print("Acc: ",accuracy_score(y_validacao, opiniao))
confusion_matrix(y_validacao, opiniao)

"""Descobrindo o melhor K"""

for i in range (1,50,2):
  KNN = KNeighborsClassifier(n_neighbors=i,weights="distance")
  KNN.fit(x_treino,y_treino)
  opiniao = KNN.predict(x_validacao)
  print("K: ",i," Acc: ",accuracy_score(y_validacao, opiniao))

"""Usando a regra do cotovelo para determinar melhor k"""

tx_erro = []
for i in range (1,50):
    KNN = KNeighborsClassifier(n_neighbors=i)
    KNN.fit(x_treino,y_treino)
    pred = KNN.predict(x_validacao)
    tx_erro.append(np.mean(pred!=y_validacao))
tx_erro

plt.figure (figsize=(11,7))
plt.plot(range(1,50),tx_erro,color='blue',linestyle='dashed',marker='o')
plt.xlabel('K')
plt.ylabel('Erro')

print("Melhor k: ",np.argmin(tx_erro)+1)

"""Tentando encontrar a melhor configuração para o modelo"""

maior = -1
for j in ("distance","uniform"):
  for i in range (1,50):
    KNN = KNeighborsClassifier(n_neighbors=i,weights=j)
    KNN.fit(x_treino,y_treino)
    opiniao = KNN.predict(x_validacao)
    Acc = accuracy_score(y_validacao, opiniao)
    print("K: ",i," Métrica: ",j," Acc: ",Acc)
    if (Acc > maior):
      maior = Acc
      Melhor_k = i
      Melhor_metrica = j

print("\nMelhor configuração para o KNN")
print("K: ",Melhor_k," Métrica: ",Melhor_metrica," Acc: ",maior)

"""Executando uma árvore de decisão"""

from sklearn import tree
DT = tree.DecisionTreeClassifier()
DT.fit(x_treino,y_treino)
opiniao = KNN.predict(x_validacao)
print("Acc: ",accuracy_score(y_validacao, opiniao))
confusion_matrix(y_validacao, opiniao)

"""Ajustando os melhores parâmetros para o modelo

criterion{“gini”, “entropy”, “log_loss”}, default=”gini”
splitter{“best”, “random”}, default=”best”
max_depth :int, default=None
min_samples_split :int or float, default=2
min_samples_leaf :int or float, default=1
"""

from sklearn import tree

for i in ("gini","entropy"):
  DT = tree.DecisionTreeClassifier(criterion=i)
  DT.fit(x_treino,y_treino)
  opiniao = DT.predict(x_validacao)
  print("Acc: ",accuracy_score(y_validacao, opiniao))

for i in ("gini","entropy"):
  for j in ("best","random"):
    DT = tree.DecisionTreeClassifier(criterion=i,splitter=j)
    DT.fit(x_treino,y_treino)
    opiniao = DT.predict(x_validacao)
    print("Acc: ",accuracy_score(y_validacao, opiniao))

for i in ("gini","entropy"):
  for j in ("best","random"):
    for k in range (3,10):
      DT = tree.DecisionTreeClassifier(criterion=i,splitter=j,max_depth=k)
      DT.fit(x_treino,y_treino)
      opiniao = DT.predict(x_validacao)
      print("Acc: ",accuracy_score(y_validacao, opiniao))

for i in ("gini","entropy"):
  for j in ("best","random"):
    for k in range (3,10):
      for l in range (1,5):
        DT = tree.DecisionTreeClassifier(criterion=i,splitter=j,max_depth=k,min_samples_leaf=l)
        DT.fit(x_treino,y_treino)
        opiniao = DT.predict(x_validacao)
        print("Acc: ",accuracy_score(y_validacao, opiniao))

maior = -1
for i in ("gini","entropy"):
  for j in ("best","random"):
    for k in range (3,10):
      for l in range (1,5):
        DT = tree.DecisionTreeClassifier(criterion=i,splitter=j,max_depth=k,min_samples_leaf=l)
        DT.fit(x_treino,y_treino)
        opiniao = DT.predict(x_validacao)
        Acc = accuracy_score(y_validacao, opiniao)
        print("Acc: ",Acc," Critério: ",i," Split: ",j," Profundidade: ",k," Mínimo por folha: ",l)
        if (Acc > maior):
          maior = Acc
          Crit = i
          Split = j
          Prof = k
          MPF = l

print("\A melhor configuração para a AD")
print("Critério: ",Crit," Split: ",Split," Profundidade: ",Prof," Mínimo por folha: ",MPF)

from sklearn.ensemble import RandomForestClassifier
maior = -1
for i in ("gini","entropy"):
  for j in (50,100,150,200):
    for k in range (3,10):
      for l in range (1,5):
        DT = RandomForestClassifier(criterion=i,n_estimators=j,max_depth=k,min_samples_leaf=l)
        DT.fit(x_treino,y_treino)
        opiniao = DT.predict(x_validacao)
        Acc = accuracy_score(y_validacao, opiniao)
        print("Acc: ",Acc," Critério: ",i," Estimadores: ",j," Profundidade: ",k," Mínimo por folha: ",l)
        if (Acc > maior):
          maior = Acc
          Crit = i
          Estim = j
          Prof = k
          MPF = l

print("\A melhor configuração para a AD")
print("Critério: ",Crit," n_estimators: ",Estim," Profundidade: ",Prof," Mínimo por folha: ",MPF)