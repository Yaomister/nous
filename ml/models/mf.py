
import numpy as np

class MatrixFactorizationModel():
    def __init__(self, num_users, num_books, degree, learning_rate = 0.01):
        self.num_users = num_users
        self.num_books = num_books
        self.degree = degree
        self.learning_rate = learning_rate

        self.users = np.random.normal(0, 1, size = (num_users, degree))
        self.books = np.random.normal(0, 1, size = (num_books, degree))

    def predict(self, user_id, book_id):
        user_vector = self.users[user_id]
        book_vector = self.books[book_id]
        return 
        return np.dot(user_vector, book_vector)
    

    def calculate_loss(self, predicted_rating, actual_rating):
        return (predicted_rating - actual_rating) ** 2


    def step(self, user_id, book_id, rating):
        prediction = self.predict(user_id, book_id)

        error = self.calculate_loss(prediction, rating)

        gradient_user = self.users[user_id] - 2 * (rating - prediction) * self.books[book_id] 
        gradient_book = self.books[book_id] - 2 * (rating - prediction) * self.users[user_id] 

        self.users[user_id] = self.users[user_id] - self.learning_rate * gradient_user
        self.books[book_id] = self.books[book_id] - self.learning_rate * gradient_book

        