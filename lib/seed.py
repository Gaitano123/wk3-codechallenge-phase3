from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Customer, Review

fake = Faker()

print("Beginning")

if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()
    session.commit()

    print("seeding restaurant info...")

    restaurants = [
        Restaurant(
            name=fake.name(),
            price=random.randint(1000, 100000)
        )
        for _ in range(10)
    ]

    session.add_all(restaurants)
    session.commit()

    print("seeding customers info...")

    customers = [
        Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        for _ in range(10)
    ]

    session.add_all(customers)
    session.commit()

    print("seeding reviews info...")

    for restaurant in restaurants:
        for _ in range(random.randint(1, 10)):
            customer = random.choice(customers)
            review = Review(
                star_rating=random.randint(1, 10),
                restaurant_id=restaurant.id,
                customer_id=customer.id
            )
            session.add(review)

    session.commit()
    session.close()
