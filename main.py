from fastapi import FastAPI, Request
from tensorflow import keras
import uvicorn
import pandas as pd
import os

bird_dex = pd.read_csv("dict_liste_oiseaux.csv")
app = FastAPI()
model = keras.models.load_model('complete_model_81.h5')


@app.get('/')
def home():
    return({"Bienvenue" : "bienvenue"})

@app.get('/predict')
async def get_prediction(request : Request):
    
    mat = await request.json()
    mat = eval(mat)
    predict = model.predict(mat['Image'])
    predict = predict.argmax() + 1

    return({"result" : bird_dex[bird_dex['number'] == predict]["name"].values[0]})

if __name__ == '__main__':

    uvicorn.run(app, host='127.0.0.1', port=4000, debug=True)