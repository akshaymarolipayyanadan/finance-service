from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.routers import accounts, invoices
from app.database import engine, Base, SessionLocal
from app import crud  # Needed for accessing invoice by reference

# Create DB tables
Base.metadata.create_all(bind=engine)

# FastAPI app setup
app = FastAPI(title="Finance Microservice")

# Mount static and template folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def datetimeformat(value, format='%d-%b-%Y'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value  # fallback if not a datetime

templates.env.filters['datetimeformat'] = datetimeformat
# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root portal page
@app.get("/", response_class=HTMLResponse)
def portal(request: Request):
    return templates.TemplateResponse("portal.html", {"request": request})

# Invoice view route from form
@app.post("/portal/invoice", response_class=HTMLResponse)
def view_invoice(
    reference: str = Form(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    invoice = crud.get_invoice_by_reference(db, reference)
    if not invoice:
        return templates.TemplateResponse("portal.html", {
            "request": request,
            "message": f"No invoice found with reference: {reference}"
        }, status_code=404)

    return templates.TemplateResponse("invoice.html", {
        "request": request,
        "invoice": invoice
    })

@app.get("/portal", response_class=HTMLResponse)
def portal_alias(request: Request):
    return templates.TemplateResponse("portal.html", {"request": request})

@app.post("/portal/pay")
def pay_invoice(reference: str = Form(...), request: Request = None, db: Session = Depends(get_db)):
    invoice = crud.pay_invoice(db, reference)
    if not invoice:
        return templates.TemplateResponse("portal.html", {
            "request": request,
            "message": f"Invoice with reference {reference} not found or already paid."
        })
    
    return templates.TemplateResponse("invoice.html", {
        "request": request,
        "invoice": invoice,
        "message": "Invoice marked as paid successfully."
    })


# Log all HTTP requests with body
@app.middleware("http")
async def log_request_body(request: Request, call_next):
    body = await request.body()
    print(f"\n📨 {request.method} {request.url.path}")
    print("Headers:", dict(request.headers))
    print("Raw body:", body.decode())
    response = await call_next(request)
    return response

# Register routers
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
