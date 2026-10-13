# FastAPI Stats + strict CORS


## Expected behavior

- `GET /stats?values=1,2,3` computes count, sum, min, max, and mean dynamically.
- CORS allows only `https://dash-idl1i0.example.com`.
- Request ID and process-time headers are added to responses, including CORS preflights.
- A disallowed origin receives no `Access-Control-Allow-Origin` header.

## Quick tests

```bash
curl -i 'https://YOUR-SERVICE.onrender.com/stats?values=1,2,3'
curl -i -X OPTIONS 'https://YOUR-SERVICE.onrender.com/stats' \
  -H 'Origin: https://dash-idl1i0.example.com' \
  -H 'Access-Control-Request-Method: GET'
curl -i -X OPTIONS 'https://YOUR-SERVICE.onrender.com/stats' \
  -H 'Origin: https://evil.example' \
  -H 'Access-Control-Request-Method: GET'
```
