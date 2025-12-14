from  models import MatrixFactorizationModel

def train(ratings, epochs = 100): 
    rows, columns = ratings.shape
    model = MatrixFactorizationModel(rows, columns, degree = 10, learning_rate = 0.01)
    for epoch in range(epochs):
        prediction = model.predict(ratings["user_id"], ratings["book_id"])


