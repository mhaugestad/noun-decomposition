import pickle, os, json
from importlib_resources import files
from .models import DecompoundingModel

path = files('Secos.models')
path = os.path.dirname(os.path.abspath(__file__))

def load(model_name):
    # open(path.joinpath(f"/data/{model_name}.pkl"), "rb")
    with open(path + f"/data/{model_name}.json", "r") as f:
        model = json.loads(f.read())
    return DecompoundingModel(**model)