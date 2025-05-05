from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import enum

from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String

from sqlalchemy.types import Enum as SqlEnum
from app.schemas import InvoiceType

class InvoiceType(str, enum.Enum):
    TUITION = "TUITION_FEES"
    LIBRARY_FINE = "LIBRARY_FINE"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    
    invoices = relationship("Invoice", back_populates="account")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, index=True)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    type = Column(SqlEnum(InvoiceType, name="invoicetype"), nullable=False)
    status = Column(String, default="OUTSTANDING")
    account_id = Column(Integer, ForeignKey("accounts.id"))

    account = relationship("Account", back_populates="invoices")
