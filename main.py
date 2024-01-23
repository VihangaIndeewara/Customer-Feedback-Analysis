

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse , RedirectResponse
from fastapi.staticfiles import StaticFiles

import logging
from pipeline import preprocessing ,vectorizer,get_prediction

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

logging.info('FastAPI server started')

data = dict()
reviews = []
positive = 0
negative = 0

@app.get("/" , response_class=HTMLResponse)
def read_root(request:Request):
    data['reviews'] = reviews
    data['positive'] = positive
    data['negative'] = negative

    logging.info('========== Open home page ============')

    return templates.TemplateResponse("index.html",{"request": request, "data": data})

@app.post("/")
async def submit(request: Request, text: str=Form()):
    logging.info(f'Text : {text}')

    preprocessedText=preprocessing(text)
    logging.info(f'Preprocessed Text : {preprocessedText}')
    
    vectorizedText=vectorizer(preprocessedText)
    logging.info(f'Vectorized Text : {vectorizedText}')

    prediction=get_prediction(vectorizedText)
    logging.info(f'Prediction : {prediction}')

    

    if prediction == 'negative':
        global negative
        negative += 1
    else:
        global positive
        positive += 1

    reviews.insert(0, text)
            
    return RedirectResponse("/", status_code=303)
 