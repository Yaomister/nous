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


async def fetch_editions(client, work_key):
    res = await client.get(
        f"https://openlibrary.org{work_key}/editions.json",
        params={"limit": 20},
    )
    res.raise_for_status()
    return res.json().get("entries", [])

async def fetch_works(client, work_key):
    res = await client.get(  f"https://openlibrary.org{work_key}.json")
    res.raise_for_status()
    return res.json()

def extract_description(work):
    description = work.get("description")
    if isinstance(description, str):
        return description
    elif isinstance(description, dict):
        return description.get("value")
    return None

def extract_details(edition):
    isbn = None
    if edition.get("isbn_13"):
        isbn = edition["isbn_13"][0]
    elif edition.get("isbn_10"):
        isbn = edition["isbn_10"][0]

    pages = edition.get("number_of_pages")
    release_date = edition.get("publish_date")

    if release_date and not release_date[:4].isdigit():
        release_date = None


    language = None
    languages = edition.get("languages")
    if languages:
        key = languages[0].get("key")
        if key:
            language = key.replace("/languages/", "")  

    return isbn, pages, release_date, language

            

async def seed_books():
    
    books = await fetch_books()
    async with httpx.AsyncClient(headers = {"User-Agent": "nous-seed-script/1.0"}) as client:
        async with SessionFactory() as db:
            for bookInfo in books:
                year = bookInfo.get("first_publish_year")
                if not year or year < 1940:
                    continue
                title = bookInfo.get("title")
                authors = [a['name'] for a in bookInfo.get("authors", [])]
                cover_key = bookInfo.get("cover_edition_key")
                work_key = bookInfo.get("key")

                if not title or not authors or not work_key:
                    continue

                exists = await db.scalar(select (models.Book).where(models.Book.title == title))

                if exists: continue

                cover = (
                    f"https://covers.openlibrary.org/b/olid/{cover_key}-L.jpg"
                    if cover_key
                    else ""
                )

                
                try:
                    editions = await fetch_editions(client, work_key=work_key)
                except Exception:
                    editions = []

                isbn = language = pages = release_date = None

                for edition in editions:
                    _isbn, _pages, _release_date, _language = extract_details(edition=edition)

                    isbn = isbn or _isbn
                    pages = pages or _pages
                    release_date = release_date or _release_date
                    language = language or _language


                    if language and isbn and pages:
                        break

                description = None

                try:
                    work = await fetch_works(client, work_key)
                    description = extract_description(work)
                except Exception:
                    description = None
                
                book = models.Book(
                    language = language,
                    release_date = release_date,
                    pages = pages,
                    isbn = isbn,
                    id = uuid.uuid4(),
                    title = title,
                    authors = authors,
                    cover = cover,
                    datePublished = str(year),
                    description=description   
                )


                db.add(book)

            await db.commit()
            

if __name__ == "__main__":
    asyncio.run(seed_books())