from sqlalchemy.orm import Session
from datetime import date
from . import models, schemas
import uuid
import random
import string
from sqlalchemy.orm import joinedload

# -------------------- Account Operations --------------------


def generate_reference(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_account_id_by_student_id(db: Session, student_id: str) -> int:
    account = db.query(models.Account).filter(models.Account.student_id == student_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Finance account not found for student")
    return account.id

def get_all_accounts(db: Session):
    return db.query(models.Account).all()


def create_account(db: Session, student_id: str):
    existing = db.query(models.Account).filter(models.Account.student_id == student_id).first()
    if existing:
        return existing
    new_account = models.Account(student_id=student_id)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


def get_account_by_student_id(db: Session, student_id: str):
    return db.query(models.Account).filter(models.Account.student_id == student_id).first()


def get_account_by_id(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()


# -------------------- Invoice Operations --------------------

def get_all_invoices(db: Session):
    return db.query(models.Invoice).all()


def get_invoice_by_id(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()


def get_invoice_by_reference(db: Session, reference: str):
    return (
        db.query(models.Invoice)
        .options(joinedload(models.Invoice.account))  # Ensures account is available
        .filter(models.Invoice.reference == reference)
        .first()
    )

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    # Explicitly normalize type here
    invoice_type = invoice.type
    if invoice_type == "TUITION_FEES":
        invoice_type = "TUITION"

    db_invoice = models.Invoice(
        amount=invoice.amount,
        due_date=invoice.dueDate,
        type=invoice_type,
        status="OUTSTANDING",
        reference=generate_reference(),
        account_id=get_account_id_by_student_id(db, invoice.account.studentId)
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice



def pay_invoice(db: Session, reference: str):
    invoice = get_invoice_by_reference(db, reference)
    if invoice and invoice.status == "OUTSTANDING":
        invoice.status = "PAID"
        db.commit()
    return invoice


def cancel_invoice(db: Session, reference: str):
    invoice = get_invoice_by_reference(db, reference)
    if invoice and invoice.status == "OUTSTANDING":
        invoice.status = "CANCELLED"
        db.commit()
    return invoice
