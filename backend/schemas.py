from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# -------- USER SCHEMAS --------
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# -------- AUCTION SCHEMAS --------
class AuctionCreate(BaseModel):
    title: str
    description: str
    start_bid: float

class FullAuctionCreate(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    base_price: float

class Bid(BaseModel):
    auction_id: int
    bid: float

class AuctionOut(BaseModel):
    id: int
    title: str
    description: str
    current_bid: float
    ends_at: datetime
    highest_bidder: Optional[str] = None

    class Config:
        from_attributes = True
