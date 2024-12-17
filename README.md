# Task: Create a Scraping Tool

I'm penning down whatever steps I've followed throughout the task in this markdown file.

Steps:

1. Since I need to create a basic automation tool which will scrape data and do couple of things (not relevant now).
I need an environment to setup fastapi and scraping library

```bash
python -m venv .

pip install fastapi requests beautifulSoup4
```

2. Defined my model based on the model described in the assignment requirements. Nothing to change there, a straight forward Product model.
  
3. Create a basic blueprint (class) for what my crawler's going to accept!

4. Crawled the site for the first page and generated data for the 1st page products successfully to understand what challenges could be posed!!

* For Now: Continuing if any product data is not scraped or an exception occurs while scraping a specific product.
  
5. So fastAPI will need a ASGI server to run. Uvicorn serves the purpose well for fastAPI based services.

```bash
pip install uvicorn
```

6. retries = 3  

* This retry can be dynamic in nature in an actual scenario based on various factors
  
7. timeout = 2

* Same goes for timeout this can be dynamic and increasing with retries (exponential backoff)

> I am assuming server has  increased load and it's taking time for the server to process a request hence exponential backoff.

* this could have been other way, if server is permanently down I'd decresed timeout with increasing retries.

8. Writing all product details in a json file for now, it could be a sqlite based storage too nothing too fancy but sticking to the current scope.

9. Now, the thing about in-memory caching! Going with Redis
    * Assumptions:
      * I'll use my product title as key and assume there's one product with one name.

```bash
pip install redis
```
