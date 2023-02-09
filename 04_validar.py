import pandas as pd
import numpy as np
import torch
import pickle

def estimate(x,w_1,b_1) :
  return w_1*x + b_1
  
def MSE_score( y_observada , y_estimada):
   return ((y_observada - y_estimada)**2).mean().item()
   
def R2_score( y_observada , y_estimada):
    numerador = ((y_observada - y_estimada)**2).sum()
    y_promedio = y_observada.mean()
    denominador = ((y_observada - y_promedio)**2).sum()
    return (1 - (numerador/denominador)).item()

  
dataset = pd.read_csv("test.csv")

print(dataset.head())

ml_param_validate=pickle.load(open("mlparams", 'rb'))

print(ml_param_validate)

x_test = torch.from_numpy(  dataset['feature0'].to_numpy() )
y_fit_test= estimate(x_test,ml_param_validate['w_1'],ml_param_validate['b'])
y_test = torch.from_numpy(  dataset['label'].to_numpy() )


print(R2_score(y_test,y_fit_test))
print(MSE_score(y_test,y_fit_test))


