from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship, sessionmaker
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, MetaData, desc

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
    
    @property
    def restaurant_reviews(self):
        return [review for review in self.reviews]  
    
    @property
    def restaurant_customers(self):
        return [review.customer for review in self.reviews]
    
    @classmethod
    def fanciest(self):
        fancy = session.query(Restaurant).order_by(desc(Restaurant.price)).first()
        return fancy
    
    @property
    def all_reviews(self):
        reviews = []
        for review in self.review:   
            review_str = f'Review for {self.name} by {review.customer.first_name} {review.customer.last_name}: {review.star_rating} stars.'
            reviews.append(review_str)
        return reviews 


class Customer(Base):
    
    __tablename__ = 'customers'
    
    id= Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    
    review = relationship('Review', back_populates='customer')
    
    def __repr__(self):
        return f'Customer(id{self.id}, first_name="{self.first_name}", last_name="{self.last_name}")'
    
    @property
    def customer_reviews(self):
        return [review for review in self.reviews]
    
    @property
    def customer_restaurants(self):
        return [review.restaurant for review in self.reviews]
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def favourite_restaurant(self):
        favourite = max(self.reviews, key=lambda review: review.star_rating)
        return favourite.restaurant
    
    def add_review(self, restaurant, rating):
        new_review = Review(restaurant=restaurant, customer = self, star_rating = rating)
        session.add(new_review)
        session.commit()
        
    def delete_reviews(self, restaurant):
        reviews_to_delete = session.query(Review).filter(Review.restaurant == restaurant, Review.customer == self).all()
        
        for review in reviews_to_delete:
            session.delete(review)
            
        session.commit()
        
    
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
    
    @property
    def customer(self):
        return self.customer
    
    @property
    def restaurant(self):
        return self.restaurant
    
    @property
    def full_review(self):
        return f'Review for {self.restaurant.name} by {self.customer.first_name} {self.customer.second_name}: {self.star_rating} starts.'
    
if __name__ == '__main__':
    
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind = engine)
    session = Session()