import pandas as pd
import numpy as np
import torch


#generar una línea recta con ruido
data_x=np.arange(-5,5,0.1,dtype=float)
(n_x) = data_x.size
in_w1 = 1.5
in_b = 1.33
ruido = np.random.randn(n_x)
data_y = data_x*in_w1 + in_b #*ruido

#guardar al archivo
salida = pd.DataFrame( )
salida['feature0'] = pd.DataFrame(data_x)
salida['label'] = pd.DataFrame(data_y)
salida.set_index('feature0')
salida.info()

salida.to_csv("sample.csv", index=False)