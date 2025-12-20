import asyncio
import uuid
from datetime import datetime
import httpx

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import SessionFactory
from db import models

import httpx

async def fetch_books():
    async with httpx.AsyncClient(
        headers={"User-Agent": "nous-seed-script/1.0"}
    ) as client:
        res = await client.get(
            "https://openlibrary.org/subjects/history.json",
            params={"limit": 400},
        )
        res.raise_for_status()
        return res.json()["works"]

    

async def seed_books():
    
    books = await fetch_books()

    async with SessionFactory() as db:
        for bookInfo in books:
            year = bookInfo.get("first_publish_year")
            if not year or year < 1920:
                continue
            title = bookInfo.get("title")
            authors = [a['name'] for a in bookInfo.get("authors", [])]
            cover_key = bookInfo.get("cover_edition_key")

            if not title or not authors:
                continue

            cover = (
                f"https://covers.openlibrary.org/b/olid/{cover_key}-L.jpg"
                if cover_key
                else ""
            )

            book = models.Book(
                id = uuid.uuid4(),
                title = title,
                authors = authors,
                cover = cover,
                datePublished = str(year)    
            )

            db.add(book)

        await db.commit()
            

if __name__ == "__main__":
    asyncio.run(seed_books())