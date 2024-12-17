# Task: Create a Scraping Tool

I'm penning down whatever steps I've followed throughout the task in this markdown file.

## Steps

### 1. Setting Up the Environment

I need an environment to set up FastAPI and scraping library.

```bash
python -m venv .
pip install fastapi requests beautifulsoup4
```

### 2. Defining the Model

Defined my model based on the model described in the assignment requirements. This is a straightforward Product model.

### 3. Creating the Basic Blueprint

Create a basic blueprint (class) for what my crawler is going to accept.

### 4. Initial Crawling

Crawled the site for the first page and generated data for the 1st page products successfully to understand potential challenges.

For now: Continuing if any product data is not scraped or an exception occurs while scraping a specific product.

### 5. Setting Up FastAPI with Uvicorn

FastAPI needs an ASGI server to run. Uvicorn serves the purpose well for FastAPI-based services.

```bash
pip install uvicorn
```

### 6. Retry Mechanism

1. Set up retries:
    - retries = 3
    - This retry can be dynamic in nature in an actual scenario based on various factors.
  
2. Set up timeout:
   - timeout = 2
   - The timeout can be dynamic and increasing with retries (exponential backoff).
   - Assumption: The server has increased load and it's taking time for the server to process a request hence exponential backoff.
   - This could have been the other way: if the server is permanently down, I’d decrease timeout with increasing retries.

### 7. Saving Data

Writing all product details to a JSON file for now. It could be a SQLite-based storage too.

### 8. In-Memory Caching with Redis

```bash
pip install redis
# Set up a Redis server on my local system and tried a couple of things.
```

> Assumption: I’ll use my product title as key and assume there's one product with one name.

## Design Decisions

- Segregated Models: Giving an MVC feel, but not exactly.

- Used Redis: For in-memory caching (performance, ease, and simple for our use-case).

- Custom Logger: Maintained a custom root logger for the entire journey.

- Modular Structure: Segregated db logic, notification, logging, utilities, models to keep code loosely coupled.

- AbstractCrawler: Created an AbstractCrawler class.

- Error Handling: Have not tried to find some other ways to capture data if one out of some product fails to be scraped for now. Just tried to gracefully handle the rest of the scraping.

Try it out on your system??

1. Set Up Redis Server
(Local, EC2, etc.)

2. Clone the Repository
Create a Python virtual environment to avoid package conflicts.

```bash
python -m venv .
source ./bin/activate
pip install -r requirements.txt
#. Run the Application The entry point is the 'main.py' file, which is run using:

uvicorn main:app --reload --port 8080

# This command instructs Uvicorn to open up an ASGI server to listen to requests sent to FastAPI's endpoint /crawl.
```



3. Configure Cache Expiration
Increase the expiration time for saving data (current time 60 seconds) while setting it in the cache.

Thanks
