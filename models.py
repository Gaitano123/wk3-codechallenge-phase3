from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, MetaData

engine = create_engine('sqlite:///restaurants.db')
Base = declarative_base()

class Restaurant(Base):
    
    __tablename__ = 'restaurants'
    
    id= Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer())
    
    review = relationship('Review', back_populates='restaurant')
    
    def __repr__(self):
        return f'Restaurant({self.id}: name="{self.name}", price={self.price})'    


class Customer(Base):
    
    __tablename__ = 'customers'
    
    id= Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    
    review = relationship('Review', back_populates='customer')
    
    def __repr__(self):
        return f'Customer(id{self.id}, first_name="{self.first_name}", last_name="{self.last_name}")'
    
    
class Review(Base):
    
    __tablename__ = 'reviews'
    
    id= Column(Integer, primary_key=True)
    star_rating=Column(Integer())
    restaurant_id=Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')
    
    def __repr__(self):
        return f'Review(id={self.id}, star_rating={self.star_rating}, restaurant_id={self.restaurant_id}, customer_id={self.customer_id})'
    
    
    
if __name__ == '__main__':
    
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind = engine)
    session = Session()