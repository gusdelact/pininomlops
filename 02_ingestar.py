import pandas as pd
from sklearn.model_selection import train_test_split

#cargar dataset

dataset = pd.read_csv("sample.csv")
dataset.head(20)

#dividir en datos de entranmiento y de prueba
(dataset_feature0_train, dataset_feature0_test,dataset_label_train, dataset_label_test ) = train_test_split(dataset['feature0'],dataset['label'],test_size=0.3,train_size=0.7)

dataset_train = pd.DataFrame({ 'feature0': dataset_feature0_train , 'label': dataset_label_train  })
dataset_train.to_csv('train.csv',index=False)
print("Dataset train.csv listo ...")

dataset_test = pd.DataFrame({ 'feature0': dataset_feature0_test , 'label': dataset_label_test })
dataset_test.to_csv('test.csv',index=False)
print("Dataset test.csv listo ...")
