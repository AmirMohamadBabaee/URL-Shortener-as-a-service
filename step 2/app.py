import os
import socket
import uvicorn
import requests
from redis import Redis
from typing import Dict
from fastapi import FastAPI, Request, Response, status
from typing_extensions import Annotated

SERVER_PORT = int(os.getenv('SERVER_PORT'))
EXPIRE_MINS = int(os.getenv('EXPIRE_MINS'))
ENDPOINT_NAME = os.getenv('ENDPOINT_NAME')
APILAYER_API = os.getenv('APILAYER_API')
APILAYER_URL = os.getenv('APILAYER_URL')

app = FastAPI()
redis_db = Redis(host='redis-cache', port=6379)

@app.post(f"/{ENDPOINT_NAME}")
async def endpoint(request: Request):
    req_dict = await request.json()
    url = req_dict.get('url')
    response = {}

    if not url:
        return Response(content={'error': 'at least, one url pair must be exist in request body'}, 
                        status_code=status.HTTP_400_BAD_REQUEST)

    if redis_db.exists(url) == 0:   # means the url does not exist
        apilayer_res = requests.request(method='POST',
                               url=APILAYER_URL,
                               headers={'apikey': APILAYER_API},
                               data=url)
        apilayer_dict = apilayer_res.json()

        redis_db.set(url, apilayer_dict["short_url"], ex=EXPIRE_MINS * 60)

        response["longUrl"]     = apilayer_dict["long_url"]
        response["shortUrl"]    = apilayer_dict["short_url"]
        response["hostname"]    = socket.gethostname()
        response["is_cached"]   = False
    
    else:                           # means the url already exists
        long_url = url
        if url.startswith('https'): 
            url = url[8:]  
        elif url.startswith('http'):
            url = url[7:]
        else:
            long_url = f'https://{long_url}'

        short_url = redis_db.get(url)
        response["longUrl"]     = long_url
        response["shortUrl"]    = short_url
        response["hostname"]    = socket.gethostname()
        response["is_cached"]   = True

    return response


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=SERVER_PORT)

