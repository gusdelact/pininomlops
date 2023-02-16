import pandas as pd
import numpy as np
import torch
import sklearn
from sklearn.model_selection import train_test_split
import pickle

#cargar dataset

dataset = pd.read_csv("train.csv")
dataset.head(20)

#dividir en datos de entrenamiento y de prueba

(dataset_feature0_train, dataset_feature0_test,dataset_label_train, dataset_label_test ) = train_test_split(dataset['feature0'],dataset['label'],test_size=0.3,train_size=0.7)

#funciones de aprendizaje

#estimacion
def estimate(x,w_1,b_1) :
  return w_1*x + b_1
  
#perdida o costo
def loss(y,y_fit):
  return torch.mean((y - y_fit)**2)
  

#entrenamiento  
def train(features,target,etha,debug=False,iter=100) :
   loss_list = []

   w_1 = torch.randn(1, requires_grad=True)
   b_1 = torch.randn(1, requires_grad=True)

   
   for i in range(iter):
     if debug :
       print( i,(w_1.item(),b_1.item()))
     
     y_fit = estimate(features,w_1,b_1)
     if debug:
       print( i,y_fit)
     L=loss(y_fit,target)
     loss_list.append(L.item())
     L.backward() 
     if debug:
      print("Iteracion {}: Perdida {} : Parametros {}",i,L.item(),(w_1.grad.item(),b_1.grad.item()))
     w_1.data = w_1.data -  w_1.grad.data*etha
     b_1.data = b_1.data -  b_1.grad.data*etha
     w_1.grad.zero_()
     b_1.grad.zero_()
   return (w_1.item(),b_1.item(),loss_list) 
   
def MSE_score( y_observada , y_estimada):
   return ((y_observada - y_estimada)**2).mean().item()
   
def R2_score( y_observada , y_estimada):
    numerador = ((y_observada - y_estimada)**2).sum()
    y_promedio = y_observada.mean()
    denominador = ((y_observada - y_promedio)**2).sum()
    return (1 - (numerador/denominador)).item()
   
x_feature = torch.from_numpy(  dataset_feature0_train.to_numpy() )
y_label = torch.from_numpy(  dataset_label_train.to_numpy() )


(e_w_1,e_b_1,e_L)=train(x_feature,y_label,0.00001,debug=False,iter=10000)

mse=MSE_score(y_label,estimate(x_feature,e_w_1,e_b_1))
r2=R2_score(y_label,estimate(x_feature,e_w_1,e_b_1))


print((e_w_1,e_b_1))
print((mse,r2))

ml_params= {
    "w_1" : e_w_1,
    "b" : e_b_1
}

pickle.dump(ml_params,open("mlparams", 'wb') )
print("Parametros escritos en archivo mlparams")
