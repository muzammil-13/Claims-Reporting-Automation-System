from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    gcs_url = Column(String, nullable=False)
    status = Column(String, nullable=False, default="processed")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
