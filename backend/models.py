from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    start_bid = Column(Float)
    current_bid = Column(Float)
    is_active = Column(Boolean, default=True)
    ends_at = Column(DateTime)
    host_id = Column(Integer, ForeignKey("users.id"))
    highest_bidder_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    highest_bidder = relationship("User", foreign_keys=[highest_bidder_id])
