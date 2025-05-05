from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class InvoiceType(str, Enum):
    TUITION_FEES = "TUITION_FEES"
    LIBRARY_FINE = "LIBRARY_FINE"

# -------------------- Account Schemas --------------------

class AccountCreate(BaseModel):
    studentId: str


class AccountOut(BaseModel):
    id: int
    student_id: str

    class Config:
        orm_mode = True


# -------------------- Invoice Schemas --------------------

class InvoiceCreate(BaseModel):
    amount: float
    dueDate: date
    type: InvoiceType
    account: AccountCreate


class InvoiceOut(BaseModel):
    id: int
    reference: str
    amount: float
    dueDate: date
    type: InvoiceType
    status: str
    studentId: str  # <-- ADD THIS
    _links: dict

    class Config:
        from_attributes = True  # For SQLAlchemy -> Pydantic