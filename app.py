import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd

quotes = []
myquots = []
authors = []
books = []

async def fetch_page(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        return await response.text()

async def scrape_quotes(page):
    url = f"https://www.goodreads.com/quotes?page={page}"
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        quotes_divs = soup.find_all('div', class_='quoteText')

        for div in quotes_divs:
            quote_text = div.get_text(strip=True, separator='\n')
            quote_text = quote_text.replace('\n', ' ')  # Replace newlines with space
            quote_text = quote_text.replace('“', '')  # Remove opening quote mark
            quote_text = quote_text.replace('”', '')  # Remove closing quote mark
            quotes.append(quote_text)

async def main():
    tasks = [scrape_quotes(i) for i in range(2, 100)]  # Adjust the range as needed
    await asyncio.gather(*tasks)

    count = 0
    for quote in quotes:
        print("quote:", quote)
        author = quote.split('―')
        
        print("author: ", author[1])
        book = author[1].split(',')
        print("book: ", book[1] if len(book) > 1 else "no book found") 
        count += 1
        quote = quote.capitalize()
        author_formatted = author[1].capitalize()
        book_formatted = book[1].capitalize() if len(book) > 1 else "no book found"

        myquots.append(quote)
        authors.append(author_formatted)
        books.append(book_formatted)

    df = pd.DataFrame({
        'Quote': myquots,
        'Author': authors,
        'Book': books
    })

    # Save to a CSV file (optional)
    df.to_csv('goodreads_quotes1.csv', index=False)

# Run the asynchronous main function
asyncio.run(main())
