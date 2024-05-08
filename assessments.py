"""Question 1: Asynchronous I/O with Memory Optimization (15 minutes)
 
Task: Develop a Python script that efficiently downloads a list of URLs concurrently while minimizing memory usage. The script should:
 
Accept a list of URLs as input.
Use asynchronous I/O techniques (e.g., asyncio, aiohttp) to download the content of each URL concurrently.
Employ techniques to limit the number of concurrent downloads to prevent overwhelming system resources. Consider using a semaphore or similar mechanism.
Print the downloaded content for each URL or an error message if the download fails.

"""


import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()


async def download_content(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

def main():
    urls = [
        "http://www.testingmcafeesites.com/index.html",
        "http://www.testingmcafeesites.com/testcat_ac.html"
    ]

    loop = asyncio.get_event_loop()
    content = loop.run_until_complete(download_content(urls))
    
    for index, text in enumerate(content, start=1):
        print(text)
    
if __name__ == '__main__':
    main()



"""
Question 2: Advanced Decorator Design with Caching and Metaprogramming (15 minutes)
 
Task: Create a decorator in Python that:
 
Caches the results of a function based on its arguments.
Leverages metaprogramming techniques (e.g., inspect module) to automatically determine the function's signature (argument names) for cache key generation.
Provides a configuration option to specify the maximum cache size or a time-based expiration for cached values.
Optionally integrates with a persistent cache storage mechanism (e.g., Redis, in-memory database) for scalability.

"""

import functools
import time

class Cache:
    def __init__(self, expiration, max_size, persistent_cache) -> None:
        self.max_size = max_size
        self.expiration = expiration
        self.persistent_cache = persistent_cache
    
    def __call__(self, *args: functools.Any, **kwds: functools.Any) -> functools.Any:
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = self._generate_key(func.__name__, args, kwargs)

            if key in cache:
                if self.expiration and time.time() - cache[key]['timestamp'] > self.expiration:
                    del cache[key]
                else:
                    return cache[key]['value']
            
            result = func(*args, **kwargs)

            cache[key] = {"value": "result", "timestamp": time.time()}

            if self.max_size and len(cache) > self.max_size:
                cache.pop(next(iter(cache)))
            
            if self.persistent_cache:
                self.persistent_cache[key] = result
            
            return result
        
        return wrapper
    
    def _generate_key(self, func_name, args, kwargs):
        arg_list = [str(arg) for arg in args]
        kwarg_list = [f"{key} = {value}" for key, value in kwargs.items()]
        signature = ",".join(arg_list+kwarg_list)
        return f"{func_name}({signature})"


persistant_cache = {}

@Cache(max_size=10, expiration=60, persistent_cache=persistant_cache)
def add(x,y):
    return x + y

print(add(2,3))

print(add(2,3))

time.sleep(61)

print(add(2,3))

print(persistant_cache)

