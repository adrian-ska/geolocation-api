from sqlalchemy import Column, Integer, String, Float

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class GeoLocation(Base):
    __tablename__ = "geolocation"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip_or_url = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=True)
    region = Column(String, nullable=True)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    def __repr__(self):
        return (
            f"GeoLocation(id={self.id}, ip_or_url={repr(self.ip_or_url)}, "
            f"country={repr(self.country)}, region={repr(self.region)}, "
            f"city={repr(self.city)}, latitude={repr(self.latitude)}, longitude={repr(self.longitude)})"
        )