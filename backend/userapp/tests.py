import requests
from requests.structures import CaseInsensitiveDict
import json
import os

url = "https://blockchain-88yt.onrender.com/userapp/api/user/login/"
# url = "http://127.0.0.1:8000/adminapp/api/admin/product/"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
data = {"pd_id": "101", "batch_id": "001", "product_details": {"Item": "Shirt", "Size": "38", "Colour": "Grey"}}
data = json.dumps(data)
# data = '{"username": "reshma859", "first_name": "Reshma", "last_name": "Suresh", "email": "reshmadundu@gmail.com", "password": "xyz123", "mobile": "+91-9446013859"}'
# data = '{"username": "Reshma859", "hash": "c0f89613cea3282a13d4b99e6051b9b0b36a10dd3a3a49b365823750545f47ff"}'
data = '{"username": "pranav1483", "password": "abc321"}'
# data = '{"username": "reshma859", "location": "India", "report": "Fake Shorts"}'
# data = '{"otp_from_user": "123", "otp": "124"}'
# data = '{"email": "pranavp1483@gmail.com", "otp": "123"}'


resp = requests.post(url, headers=headers, data=data)

print(resp.text)

