from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning Rules!"}
    
    if model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    if model_name.value == "resnet":
        return {"model_name": model_name, "message": "Have some residuals"}