import asyncio
import random
import aiohttp
import time
import argparse
import sys
from datetime import datetime

def generate_random_data():
    return {
        "data": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=20)),
        "value": random.randint(1, 1000),
        "timestamp": datetime.now().isoformat()
    }

async def send_request(session, url, method="GET", data=None):
    start_time = time.monotonic()
    try:
        if method == "GET":
            async with session.get(url) as response:
                status = response.status
                if status == 200:
                    await response.text()
        elif method == "POST":
            async with session.post(url, json=data) as response:
                status = response.status
        elif method == "PUT":
            async with session.put(url, json=data) as response:
                status = response.status
        elif method == "DELETE":
            async with session.delete(url) as response:
                status = response.status
                
        duration = time.monotonic() - start_time
        return {"status": "success", "code": status, "duration": duration}
        
    except Exception as e:
        duration = time.monotonic() - start_time
        return {"status": "error", "message": str(e), "duration": duration}

async def load_test(target_url, num_requests, concurrent_workers):
    endpoints = ["/", "/redoc", "/docs", "/user/profile"]
    connector = aiohttp.TCPConnector(limit=0) 
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        request_counter = 0
        success_count = 0
        error_count = 0
        total_duration = 0
        
        while request_counter < num_requests:
            method = random.choices(
                ["GET", "POST", "PUT", "DELETE"],
                weights=[0.5, 0.3, 0.15, 0.05] 
            )[0]

            endpoint = random.choices(endpoints,
                weights=[0.5, 0.3, 0.15, 0.05] 
            )[0]

            full_url = f"{target_url}{endpoint}"
            
            data = generate_random_data() if method in ["POST", "PUT"] else None
            
            task = asyncio.create_task(
                send_request(session, full_url, method, data)
            )
            
            tasks.append(task)
            request_counter += 1
            
            if len(tasks) >= concurrent_workers:
                done, pending = await asyncio.wait(
                    tasks, 
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                for task in done:
                    result = task.result()
                    total_duration += result["duration"]
                    if result["status"] == "success":
                        success_count += 1
                    else:
                        error_count += 1
                    with open("results.csv", "a") as f:
                        f.write(f"{method},{result['code'] if 'code' in result else 0},{result['duration']}\n")
                
                tasks = list(pending)
                
                sys.stdout.flush()
        
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                total_duration += result["duration"]
                if result["status"] == "success":
                    success_count += 1
                else:
                    error_count += 1
    print("\n\n📊 Load testing results:")
    print(f"✅ Successful requests: {success_count} ({success_count/num_requests:.1%})")
    print(f"❌ Failure requests: {error_count} ({error_count/num_requests:.1%})")
    print(f"⏱️ Total time: {total_duration:.2f} s")
    print(f"⚡ Requests per second: {num_requests/total_duration:.2f}")
    print(f"⏳ Average response time: {total_duration/num_requests:.4f} s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='Target URL (for example: http://localhost:9100)')
    parser.add_argument('-r', '--requests', type=int, default=100, 
                        help='Total requests (default: 100)')
    parser.add_argument('-c', '--concurrency', type=int, default=10,
                        help='Count of simultaneous requests (default: 10)')
    
    args = parser.parse_args()
    print()
    print("=" * 50)
    print(f"🛠️ Settings:")
    print(f"  Target URL: {args.url}")
    print(f"  Total requests: {args.requests}")
    print(f"  Parallel requests: {args.concurrency}")
    print("=" * 50)
    
    start_time = time.monotonic()
    asyncio.run(load_test(args.url, args.requests, args.concurrency))
    print(f"\n🕒 Total test execution time: {time.monotonic() - start_time:.2f} s")
    
