import numpy as np
from ml.models import MatrixFactorizationModel
from ml.helper import load_model

model = None

def load_recommender():
    global model
    users, books = load_model()
    model = MatrixFactorizationModel(users.shape[0], books.shape[0], users.shape[1])
    model.users = users
    model.books = books