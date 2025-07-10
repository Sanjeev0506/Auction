from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend.database import SessionLocal
from backend.models import Auction, User
from backend.schemas import FullAuctionCreate, AuctionOut, Bid
from backend.utils import get_current_user

router = APIRouter()

# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Host Auction ----------------
@router.post("/host-auction", response_model=AuctionOut)
def host_auction(
    auction: FullAuctionCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if auction.end_time <= auction.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    new_auction = Auction(
        title=auction.title,
        description=auction.description,
        start_bid=auction.base_price,
        current_bid=auction.base_price,
        is_active=True,
        ends_at=auction.end_time,
        host_id=user["id"]
    )
    db.add(new_auction)
    db.commit()
    db.refresh(new_auction)
    return AuctionOut(
        id=new_auction.id,
        title=new_auction.title,
        description=new_auction.description,
        current_bid=new_auction.current_bid,
        ends_at=new_auction.ends_at,
        highest_bidder=None
    )

# ---------------- Get Ongoing Auctions ----------------
@router.get("/get-auctions", response_model=List[AuctionOut])
def get_auctions(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    auctions = db.query(Auction).filter(Auction.ends_at > now, Auction.is_active == True).all()

    result = []
    for a in auctions:
        result.append(AuctionOut(
            id=a.id,
            title=a.title,
            description=a.description,
            current_bid=a.current_bid,
            ends_at=a.ends_at,
            highest_bidder=a.highest_bidder.email if a.highest_bidder else None
        ))
    return result

# ---------------- Join Auction ----------------
@router.post("/join-auction/{auction_id}")
def join_auction(
    auction_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")

    return {"message": f"{user['email']} joined auction #{auction_id}"}

# ---------------- Place a Bid ----------------
@router.post("/api/bid")
def bid_on_auction(
    bid: Bid,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    auction = db.query(Auction).filter(Auction.id == bid.auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")

    if bid.bid <= auction.current_bid:
        raise HTTPException(status_code=400, detail="Bid must be higher than current bid")

    auction.current_bid = bid.bid
    auction.highest_bidder_id = user["id"]
    db.commit()
    db.refresh(auction)

    return {
        "message": "Bid placed successfully",
        "current_bid": auction.current_bid,
        "highest_bidder": user["email"]
    }
