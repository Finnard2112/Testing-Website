import jwt

print(jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6ImtxQ041NXQ3bkJMeDlNajh3cEVESWhuN3hPOFFDcEsyIn0.eyJuYW1lIjoiaHV5bnEiLCJleHAiOjE2NTcxODExMjJ9.AmMvmzA10yT9OX-5iOQOO4w9xR1hdNYnXSqgLnpTrhga",algorithms=["HS256"], options={"verify_signature": False}))
