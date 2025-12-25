


from sqlalchemy.ext.asyncio import AsyncSession, async_session
from  db import models, SessionFactory
from .models.mf import MatrixFactorizationModel
import numpy as np
from .helper import save_model
import asyncio
from sqlalchemy import text

async def train():
    async with SessionFactory() as db:
        rows = await db.execute(text("""
            SELECT posts.user_id, posts.book_id, ratings.rating
            FROM ratings JOIN posts ON posts.id = ratings.post_id
"""))
        data = rows.fetchall()

        users = {u for u, _, _ in data}
        books = {b for _, b, _ in data}

        users_map = {u: i for i, u in enumerate(users)}
        books_map = {b: i for i, b in enumerate(books)}

        for u, i in users_map.items():
            await db.merge(models.UserMLIndex(user_id = u, user_index = i))

        for b, i in books_map.items():
            await db.merge(models.BookMLIndex(book_id = b, book_index = i))

        await db.commit()

        model = MatrixFactorizationModel(num_users=len(users_map), num_books=len(books_map), degree=32 )

        for _ in range(30):
            np.random.shuffle(data)
            for u, b, r  in data:
                model.step(user_id=users_map[u], book_id=books_map[b], rating=r)

        save_model(model.users, model.books)




if __name__ == "__main__":
    asyncio.run(train())
