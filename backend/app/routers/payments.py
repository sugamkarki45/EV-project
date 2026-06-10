from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/initiate")
async def initiate_payment(amount: float, gateway: str):
    # Simulation: return eSewa/Khalti form data or checkout URL
    return {"checkout_url": "https://esewa.com.np/mock-checkout"}

@router.get("/wallet-balance")
async def get_wallet_balance():
    return {"balance_npr": 1500.50}
