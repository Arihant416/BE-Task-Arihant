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

# I Setup a redis server on my local system and tried a couple of things.
```

10. Design decisions that I've took
    1. Segregated models (giving the MVC feel a little, but not exactly)
    2. Used Redis for in-memory caching (performance, ease and simple for our use-case)
    3. Maintained a custom root logger for the entire journey
    4. Segregated my db logic, notification, logging, utilities, models to keep my code loosely coupled!
    5. Created an AbstractCrawler(which is sort of an overkill in our case but still!!)
    6. Have not tried to find some other ways to capture data if one out of some product fails to be scraped!! for now.

For Anyone who wishes to use this automation script!
Please follow the below steps

1. Set up redis server (Local, EC2, etc)
2. Clone this repo, and create a python virtual-env to avoid package conflicts on any system. (Commands are shared above)
3. The entry point is the ```main.py``` file which basically is run using the following command

```bash
uvicorn main:app --reload --port <<PORT_NO>>
# All this command does is instructs uvicorn to open up a asgi server to listen to the requests sent on the fastapi's endpoint /crawl
```

4. You can increase the expiration time for saving data(current time 60 seconds) while setting it on cache.

Thanks!!
