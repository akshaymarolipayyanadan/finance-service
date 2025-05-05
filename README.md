# 💰 Finance Service Microservice

A FastAPI-based microservice for handling student invoice generation, payments, and account linking. Built as part of a modular university management system.

---

## 🚀 Features

- View invoice details by reference
- Pay and cancel invoices
- Link invoices to student accounts
- RESTful API with HATEOAS-style links
- Template-based frontend (Jinja2)
- Logs incoming HTTP requests
- Containerized using Docker

---

## 🧱 Tech Stack

- **Python 3.11**
- **FastAPI** - web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - database
- **Jinja2** - templating engine
- **Docker** - containerization

---

## 📁 Project Structure

finance-service/
├── app/
│ ├── crud.py
│ ├── database.py
│ ├── models.py
│ ├── routers/
│ │ ├── accounts.py
│ │ └── invoices.py
│ └── schemas.py
├── templates/
│ ├── invoice.html
│ ├── portal.html
│ └── fragments/
│ ├── header.html
│ └── nav.html
├── static/
│ └── css/
├── requirements.txt
├── Dockerfile
├── main.py
└── README.md


---

## ⚙️ Running the Service

### 🔧 Option 1: Local (Dev Mode)

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload --port 8081


# Build Docker image
docker build -t finance-service .

# Run container
docker run -p 8081:8081 finance-service

📬 API Endpoints (Sample)

    GET /invoices/reference/{ref} - Get invoice by reference

    POST /portal/invoice - View invoice via form

    PUT /invoices/{ref}/pay - Pay an invoice

    DELETE /invoices/{ref}/cancel - Cancel an invoice

👤 Author

Akshay Maroli Payyanadan

📄 License

This project is licensed for academic and educational use.
