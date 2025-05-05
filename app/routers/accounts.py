from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app import crud, schemas, database
from fastapi import Request
import json


router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/")
def get_all_accounts(request: Request, db: Session = Depends(get_db)):
    accounts = crud.get_all_accounts(db)
    base_url = str(request.base_url).rstrip("/")

    account_list = []
    for account in accounts:
        has_outstanding = any(invoice.status == "OUTSTANDING" for invoice in account.invoices)
        account_list.append({
            "id": account.id,
            "studentId": account.student_id,
            "hasOutstandingBalance": has_outstanding,
            "_links": {
                "self": {
                    "href": f"{base_url}/accounts/student/{account.student_id}"
                },
                "accounts": {
                    "href": f"{base_url}/accounts"
                }
            }
        })

    return JSONResponse(content={
        "_embedded": {
            "accountList": account_list
        },
        "_links": {
            "self": {
                "href": f"{base_url}/accounts"
            }
        }
    })



@router.post("/")
async def create_account(account: schemas.AccountCreate, request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    print("📥 Incoming POST /accounts body:", body)

    acc = crud.create_account(db, account.studentId)
    base_url = str(request.base_url).rstrip("/")
    has_outstanding = any(invoice.status == "OUTSTANDING" for invoice in acc.invoices)
    return JSONResponse(content={
        "id": acc.id,
        "studentId": acc.student_id,
        "hasOutstandingBalance": has_outstanding,
        "_links": {
            "self": {
                "href": f"{base_url}/accounts/student/{acc.student_id}"
            },
            "accounts": {
                "href": f"{base_url}/accounts"
            }
        }
    })



@router.get("/student/{student_id}")
def get_account_by_student_id(student_id: str, request: Request, db: Session = Depends(get_db)):
    acc = crud.get_account_by_student_id(db, student_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    base_url = str(request.base_url).rstrip("/")
    has_outstanding = any(invoice.status == "OUTSTANDING" for invoice in acc.invoices)
    return JSONResponse(content={
        "id": acc.id,
        "studentId": acc.student_id,
        "hasOutstandingBalance": has_outstanding,
        "_links": {
            "self": {
                "href": f"{base_url}/accounts/student/{acc.student_id}"
            },
            "accounts": {
                "href": f"{base_url}/accounts"
            }
        }
    })


@router.get("/{account_id}")
def get_account_by_id(account_id: int, request: Request, db: Session = Depends(get_db)):
    acc = crud.get_account_by_id(db, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    base_url = str(request.base_url).rstrip("/")
    has_outstanding = any(invoice.status == "OUTSTANDING" for invoice in acc.invoices)
    return JSONResponse(content={
        "id": acc.id,
        "studentId": acc.student_id,
        "hasOutstandingBalance": has_outstanding,
        "_links": {
            "self": {
                "href": f"{base_url}/accounts/student/{acc.student_id}"
            },
            "accounts": {
                "href": f"{base_url}/accounts"
            }
        }
    })
