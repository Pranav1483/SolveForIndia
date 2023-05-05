import requests

# url = "https://blockchain-88yt.onrender.com/userapp/api/product/c5ba1e92e2507be912fc02e591e46301626fa60acbbb2ce8fb6da08ad0d2c60a"
url = "http://127.0.0.1:8000/adminapp/api/admin/reports/reshma859"


resp = requests.get(url)

print(resp.text)
