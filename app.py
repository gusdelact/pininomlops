from flask import Flask
from flask import request
import pickle
import logging
import sys
def predict(x,w_1,b_1) :
  return w_1*x + b_1
  
print(__name__)
app = Flask(__name__)
api_mlparams=pickle.load(open("mlparams", 'rb'))

logging.info(api_mlparams)

@app.route('/infer')
def infer():
   w_1 = api_mlparams['w_1']
   b = api_mlparams['b']
   reqX = request.args.get('x')
   x = float(reqX)
   print((x,type(x)),file=sys.stderr)
   return {'y':w_1*x  + b}

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)