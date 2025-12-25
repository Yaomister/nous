import numpy as np
from pathlib import Path

dir = Path("ml/models/saved")

def save_model(users, books):
    dir.mkdir(parents=True, exist_ok=True)
    np.save(dir / "users.npy", users)
    np.save(dir/ "books.npy", books)

def load_model(users, books):
    users = np.load(dir/"users.npy")
    books = np.load(dir/ "books.npy")

    return users, books