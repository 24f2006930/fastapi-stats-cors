# FastAPI Stats + strict CORS

## Deploy on Render

1. Create a new **public or private GitHub repository** and upload `main.py`, `requirements.txt`, and `render.yaml`.
2. In Render, choose **New → Blueprint** and connect that repository (or create a Web Service using the same build/start commands).
3. Wait for deployment and copy the service's base URL, e.g. `https://your-service.onrender.com`.
4. Open `https://your-service.onrender.com/stats?values=1,2,3` to test the endpoint.
5. If your logged-in IITM email is not `24f2006930@ds.study.iitm.ac.in`, update the `STUDENT_EMAIL` environment variable in Render to the exact address shown by the assignment page and redeploy.

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
