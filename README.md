# Visitor counter API

A small serverless API that counts visits to [vithu.cloud](https://vithu.cloud). The site calls it once per page load and shows the total in the footer.

![Architecture](architecture.svg)

## What it does

- An **HTTP API** on API Gateway exposes one route, `POST /hit`.
- A **Lambda** function (Python 3.12) adds one to a counter in **DynamoDB** and returns the new total.
- The update uses DynamoDB's atomic `ADD`, so visits that arrive at the same moment are all counted.
- **CORS** only allows calls from `https://vithu.cloud`.
- **Throttling** on the API caps it at 2 requests a second, so nobody can run up a bill.

## Why I built it

My other projects can only be read about. I wanted one that visitors can see working. It is also a tidy exercise in least privilege: the function's role allows one action, `dynamodb:UpdateItem`, on one table.

## Deploy

Requires the AWS SAM CLI (already installed in AWS CloudShell).

```bash
sam build
sam deploy --guided --stack-name visitor-counter
```

Copy the `ApiUrl` output into `site/assets/config.js` in the website repo:

```js
window.SITE = { counterApi: "https://abc123.execute-api.eu-west-2.amazonaws.com/hit" };
```

## Test

```bash
pip install pytest moto boto3
pytest
```

## Remove

```bash
sam delete --stack-name visitor-counter
```

## What I would add next

- Count unique visitors per day instead of raw page loads.
- A CloudWatch alarm on API 5xx errors.
- A custom domain such as `api.vithu.cloud`.

---

*Part of my AWS portfolio. More at [vithu.cloud](https://vithu.cloud).*
