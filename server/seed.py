#!/usr/bin/env python3

from app import app, db
from models import Restaurant, Pizza, RestaurantPizza

if __name__ == '__main__':
    with app.app_context():

        # Delete existing data
        print("Deleting data...")
        RestaurantPizza.query.delete()
        Restaurant.query.delete()
        Pizza.query.delete()
        db.session.commit()

        print("Creating restaurants...")
        shack = Restaurant(name="Karen's Pizza Shack", address='address1')
        bistro = Restaurant(name="Sanjay's Pizza", address='address2')
        palace = Restaurant(name="Kiki's Pizza", address='address3')
        restaurants = [shack, bistro, palace]

        print("Creating pizzas...")
        cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
        pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
        california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
        pizzas = [cheese, pepperoni, california]

        print("Creating RestaurantPizza associations...")
        pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=1)
        pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=4)
        pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=5)
        restaurant_pizzas = [pr1, pr2, pr3]

        # Add all to session and commit
        db.session.add_all(restaurants)
        db.session.add_all(pizzas)
        db.session.add_all(restaurant_pizzas)
        db.session.commit()

        print("Seeding done!")
        print(f"Created {len(restaurants)} restaurants")
        print(f"Created {len(pizzas)} pizzas")
        print(f"Created {len(restaurant_pizzas)} restaurant-pizza associations")