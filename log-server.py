from fastapi import FastAPI, Request
import getpass
import platform
import logging
import uvicorn
from datetime import datetime
import time

app = FastAPI()

logging.basicConfig(
    filename='info_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("fastapi")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware for incoming requests"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host,
        "status_code": response.status_code,
        "process_time": round(process_time, 4)
    }
    
    logger.info(f"{log_data['method']} {log_data['path']} from {log_data['client_ip']} "
                f"- Status: {log_data['status_code']} - {log_data['process_time']}s")
    
    return response

@app.get("/")
async def get_system_info():
    """Return username and OS version"""
    return {
        "username": getpass.getuser(),
        "os_version": platform.platform()
    }

if __name__ == "__main__":
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=9100,
        log_level="info",
        access_log=True
    )
    server = uvicorn.Server(config)
    
    server.run()
