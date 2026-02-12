import requests, json

url = "https://jsonplaceholder.typicode.com/todos/1"

response = requests.get(url)
data = response.json()
done = "☐"

print(f"Tittel: {data["title"]}")
if data["completed"]: 
done = "☑"
print(f"Status: ")

print(response.status_code) 
print(response.text) 