import numpy as np
from pathlib import Path
from models import MatrixFactorizationModel


dir = Path("ml/models/saved")

def save_model(users, books):
    dir.mkdir(parents=True, exist_ok=True)
    np.save(dir / "users.npy", users)
    np.save(dir/ "books.npy", books)

def load_model(users, books):
    users = np.load(dir/"users.npy")
    books = np.load(dir/ "books.npy")

    return users, books


def update(model, u, b, rating):
    for _ in range(5):
        model.step(u, b, rating)
    save_model(model.users, model.books)