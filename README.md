# FastAPI Stats + Strict CORS

A lightweight FastAPI service that calculates descriptive statistics for dynamically supplied integer values and enforces a strict, origin-based CORS policy. Deployed on Render.

**Live API:** https://fastapi-stats-cors.onrender.com

## Features

- **Dynamic statistics:** Calculates count, sum, minimum, maximum, and mean from comma-separated integers.
- **Strict CORS:** Allows requests only from the assigned origin.
- **Request tracking:** Adds a unique `X-Request-ID` to every response.
- **Performance monitoring:** Adds `X-Process-Time`, reporting request processing time in seconds.
- **Preflight handling:** Supports CORS preflight requests from the allowed origin and rejects disallowed origins without returning an `Access-Control-Allow-Origin` header.
- **JSON responses:** Returns structured statistics and the configured student email.

## API Endpoint

### `GET /stats?values=1,2,3`

Accepts a comma-separated list of integers through the `values` query parameter.

**Example request:**

```bash
curl -i "https://fastapi-stats-cors.onrender.com/stats?values=1,2,3,4,5"
```

**Example response:**

```json
{
  "email": "24f2006930@ds.study.iitm.ac.in",
  "count": 5,
  "sum": 15,
  "min": 1,
  "max": 5,
  "mean": 3.0
}
```

The statistics are computed dynamically for each request; values are not hard-coded.

## CORS Policy

**Allowed origin:**

```text
https://dash-idl1i0.example.com
```

Only this origin is permitted to receive the `Access-Control-Allow-Origin` header.

- Preflight requests from the assigned origin succeed and include the appropriate CORS header.
- Preflight requests from other origins are rejected and do not include `Access-Control-Allow-Origin`.
- Wildcard origins (`*`) are not used.

## Required Response Headers

Every response includes the following middleware headers:

| Header | Purpose |
|---|---|
| `X-Request-ID` | Unique UUID identifying the request |
| `X-Process-Time` | Request processing duration in seconds |

## Testing

### 1. Test descriptive statistics

```bash
curl -i "https://fastapi-stats-cors.onrender.com/stats?values=10,20,30"
```

Expected statistics: count `3`, sum `60`, min `10`, max `30`, mean `20.0`.

### 2. Test the allowed origin

```bash
curl -i -X OPTIONS "https://fastapi-stats-cors.onrender.com/stats" \
  -H "Origin: https://dash-idl1i0.example.com" \
  -H "Access-Control-Request-Method: GET"
```

Expected: HTTP 200 with the assigned origin in `Access-Control-Allow-Origin`.

### 3. Test a disallowed origin

```bash
curl -i -X OPTIONS "https://fastapi-stats-cors.onrender.com/stats" \
  -H "Origin: https://evil.example" \
  -H "Access-Control-Request-Method: GET"
```

Expected: HTTP 400 with no `Access-Control-Allow-Origin` header.

### 4. Verify response headers

Inspect the responses above for `X-Request-ID` and `X-Process-Time`.

## Deployment

The service is deployed on [Render](https://render.com/) using a Blueprint configuration defined in `render.yaml`.

The project uses:

- **FastAPI** — API framework
- **Uvicorn** — ASGI server
- **Starlette CORSMiddleware** — CORS enforcement
- **Render** — Cloud hosting

## Project Structure

```text
fastapi-stats-cors/
├── main.py
├── requirements.txt
├── render.yaml
└── README.md
```

## Live Service

**Base URL:** https://fastapi-stats-cors.onrender.com

**Statistics endpoint:** https://fastapi-stats-cors.onrender.com/stats?values=1,2,3

The service has been manually tested for dynamic statistics, allowed and rejected CORS preflights, and the required response headers.
