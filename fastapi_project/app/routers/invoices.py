'''from fastapi import APIRouter
from models.invoice import Invoice

router = APIRouter(tags=["Invoices"])

@router.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data'''