import concurrent.futures

def worker(n):
    print(f"Worker thread running\{n}")

pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

pool.submit(worker, 1)
pool.submit(worker, 2)

pool.shutdown(wait=True)

print("Main thread continuing to run")
