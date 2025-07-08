This is a simple full-stack **serverless notes app** built with:

- **AWS Lambda** – for backend logic and serving HTML
- **Amazon API Gateway** – to route HTTP requests
- **Amazon DynamoDB** – to store notes

-**Live Demo**: [Click here to try it](https://zhvqyenpqh.execute-api.ap-south-2.amazonaws.com/dev/index.html)

---

## 🚀 Features

- Create and view notes
- Frontend UI served from Lambda
- Fully serverless architecture
- Uses API Gateway + DynamoDB
- Clean and minimal UI (pure HTML + JS)

---

## 🧠 Architecture Overview

---

## 🔧 API Routes

| Method | Path            | Description              |
|--------|------------------|--------------------------|
| GET    | `/` or `/index.html` | Serves the frontend HTML UI |
| POST   | `/note`         | Create a new note        |
| GET    | `/note`         | List all notes           |

> All routes are served from the same Lambda function using proxy integration.

---

## 💻 Local Development & Testing

To test locally:

1. Package your code:
   ```bash
   zip -r serverless-website.zip lambda_function.py index.html


