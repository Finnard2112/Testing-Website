import requests

url = "http://192.168.41.243:8000/loctust/api/create"
form_data = {'abc': 'abc'}

print(form_data)
payload={'data': "\"" + str(form_data) + "\""}
files=[

]
headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6ImtxQ041NXQ3bkJMeDlNajh3cEVESWhuN3hPOFFDcEsyIn0.eyJuYW1lIjoiaHV5bnEiLCJleHAiOjE2NTYzMDQ2NDB9.BAo2ifJodIeKvvh6ydOOH7GRF8e8iwq7nUD4KulOa5E'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

print(response.status_code)
print(response.text)
