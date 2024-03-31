import logging
from io import BytesIO

from PIL import Image
from fastapi import FastAPI, UploadFile

from src.model import ConvNet
from src.predict import get_test_score, classify_image
from src.train import fit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/train")
def train():
    fit(ConvNet())
    return {"message": "Model successfully saved!"}


@app.get("/health")
def health_check():
    return {"status": "Server is running"}


@app.get("/validate")
def validate():
    loss = get_test_score()
    return {"Loss": f"{loss}"}


@app.post("/predict")
def predict(file: UploadFile):
    img = Image.open(BytesIO(file.file.read()))
    prediction = classify_image(img)
    return {"prediction": prediction}
