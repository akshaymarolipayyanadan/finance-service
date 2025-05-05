from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app import models, schemas, crud, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_invoices(request: Request, db: Session = Depends(get_db)):
    invoices = crud.get_all_invoices(db)
    base_url = str(request.base_url).rstrip("/")

    invoice_list = []
    for inv in invoices:
        invoice_list.append({
            "id": inv.id,
            "reference": inv.reference,
            "amount": inv.amount,
            "dueDate": inv.due_date.isoformat(),
            "type": inv.type,
            "status": inv.status,
            "studentId": inv.account.student_id,
            "_links": {
                "self": {
                    "href": f"{base_url}/invoices/reference/{inv.reference}"
                },
                "pay": {
                    "href": f"{base_url}/invoices/{inv.reference}/pay"
                },
                "cancel": {
                    "href": f"{base_url}/invoices/{inv.reference}/cancel"
                }
            }
        })

    return JSONResponse(content={
        "_embedded": {
            "invoiceList": invoice_list
        },
        "_links": {
            "self": {
                "href": f"{base_url}/invoices"
            }
        }
    })


@router.get("/{invoice_id}")
def get_invoice_by_id(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    inv = crud.get_invoice_by_id(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    base_url = str(request.base_url).rstrip("/")
    return JSONResponse(content={
        "id": inv.id,
        "reference": inv.reference,
        "amount": inv.amount,
        "dueDate": inv.due_date.isoformat(),
        "type": inv.type,
        "status": inv.status,
        "_links": {
            "self": {
                "href": f"{base_url}/invoices/{inv.id}"
            },
            "reference": {
                "href": f"{base_url}/invoices/reference/{inv.reference}"
            },
            "pay": {
                "href": f"{base_url}/invoices/{inv.reference}/pay"
            },
            "cancel": {
                "href": f"{base_url}/invoices/{inv.reference}/cancel"
            }
        }
    })



@router.get("/reference/{ref}", response_model=schemas.InvoiceOut)
def get_invoice_by_reference(ref: str, db: Session = Depends(database.get_db)):
    invoice = crud.get_invoice_by_reference(db, ref)
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Flatten studentId from account relationship
    return {
        "id": invoice.id,
        "reference": invoice.reference,
        "amount": invoice.amount,
        "dueDate": invoice.due_date,
        "type": invoice.type,
        "status": invoice.status,
        "studentId": invoice.account.student_id if invoice.account else None,
        "_links": {
            "self": {"href": f"http://localhost:8081/invoices/reference/{invoice.reference}"},
            "invoices": {"href": f"http://localhost:8081/invoices"},
            "cancel": {"href": f"http://localhost:8081/invoices/{invoice.reference}/cancel"},
            "pay": {"href": f"http://localhost:8081/invoices/{invoice.reference}/pay"},
        }
    }
@router.post("/")
def create_invoice(invoice: schemas.InvoiceCreate, request: Request, db: Session = Depends(get_db)):
    inv = crud.create_invoice(db, invoice)
    base_url = str(request.base_url).rstrip("/")
    return JSONResponse(content={
        "id": inv.id,
        "reference": inv.reference,
        "amount": inv.amount,
        "dueDate": inv.due_date.isoformat(),
        "type": inv.type,
        "status": inv.status,
        "_links": {
            "self": {
                "href": f"{base_url}/invoices/reference/{inv.reference}"
            },
            "pay": {
                "href": f"{base_url}/invoices/{inv.reference}/pay"
            },
            "cancel": {
                "href": f"{base_url}/invoices/{inv.reference}/cancel"
            }
        }
    })


@router.put("/{ref}/pay")
def pay_invoice(ref: str, request: Request, db: Session = Depends(get_db)):
    inv = crud.pay_invoice(db, ref)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found or already paid/cancelled")

    base_url = str(request.base_url).rstrip("/")
    return JSONResponse(content={
        "id": inv.id,
        "reference": inv.reference,
        "amount": inv.amount,
        "dueDate": inv.due_date.isoformat(),
        "type": inv.type,
        "status": inv.status,
        "_links": {
            "self": {
                "href": f"{base_url}/invoices/reference/{inv.reference}"
            },
            "cancel": {
                "href": f"{base_url}/invoices/{inv.reference}/cancel"
            }
        }
    })


@router.delete("/{ref}/cancel")
def cancel_invoice(ref: str, request: Request, db: Session = Depends(get_db)):
    inv = crud.cancel_invoice(db, ref)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found or already paid/cancelled")

    base_url = str(request.base_url).rstrip("/")
    return JSONResponse(content={
        "id": inv.id,
        "reference": inv.reference,
        "amount": inv.amount,
        "dueDate": inv.due_date.isoformat(),
        "type": inv.type,
        "status": inv.status,
        "_links": {
            "self": {
                "href": f"{base_url}/invoices/reference/{inv.reference}"
            },
            "pay": {
                "href": f"{base_url}/invoices/{inv.reference}/pay"
            }
        }
    })
