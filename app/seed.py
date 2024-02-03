from random import choice, choices, sample, randint
import faker
from models import Restaurant,Restaurant_pizza,Pizza, db

fake = faker.Faker()

from app  import app

with app.app_context():
    Pizza.query.delete()
    Restaurant_pizza.query.delete()
    Restaurant.query.delete()


    for p in range(20):
        name=  fake.name()
        address= fake.address()

        restaurant = Restaurant(name=name ,address=address)
        db.session.add(restaurant)
        db.session.commit()

    pizzas= ["Veggie Delight","Meat Lovers","Four Cheese","Mediterranean","Buffalo Chicken"]
    sample_ingredients= ["Tomato sauce","Mozzarella cheese","Pepperoni","Mushrooms","Onions","Bell peppers","Sausage","Olives","Ham","Bacon","Chicken","Spinach"]

    fake_pizzas= []

    for p in range(len(pizzas)):
        other_pizz = choices(sample_ingredients , k=3)
        random_ingedients= ','.join(str(ingr) for ingr in other_pizz)
        fake_pizza= Pizza(name= choice(pizzas), ingredients= random_ingedients)
        fake_pizzas.append(fake_pizza)

    db.session.add_all(fake_pizzas)
    db.session.commit()

    for record in range(20):
        random_restaurant=choice([r.id for r in Restaurant.query.all()])
        random_pizza= choice([p.id for p in  Pizza.query.all()])
        db.session.add(Restaurant_pizza(restaurant_id=random_restaurant, pizza_id=random_pizza, price= randint(1,30)))
        db.session.commit()