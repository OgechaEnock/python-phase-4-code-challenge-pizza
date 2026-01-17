#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Initialize db with app
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-RESTful API
api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


class Restaurants(Resource):
    """GET /restaurants - Returns all restaurants without nested data"""
    
    def get(self):
        restaurants = Restaurant.query.all()
        return [restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants], 200


class RestaurantById(Resource):
    """GET and DELETE /restaurants/<int:id>"""
    
    def get(self, id):
        """Returns a single restaurant with nested restaurant_pizzas and pizza data"""
        restaurant = Restaurant.query.filter_by(id=id).first()
        
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        
    
        return restaurant.to_dict(), 200
    
    def delete(self, id):
        """Deletes a restaurant and cascades to delete associated restaurant_pizzas"""
        restaurant = Restaurant.query.filter_by(id=id).first()
        
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        
        db.session.delete(restaurant)
        db.session.commit()
        
    
        return '', 204


class Pizzas(Resource):
    """GET /pizzas - Returns all pizzas without nested data"""
    
    def get(self):
        pizzas = Pizza.query.all()
        
        return [pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas], 200


class RestaurantPizzas(Resource):
    """POST /restaurant_pizzas - Creates a new RestaurantPizza"""
    
    def post(self):
        try:
            data = request.get_json()
            
            # Validate that data exists
            if not data:
                return {'errors': ['validation errors']}, 400
            
            # Validate required fields
            required_fields = ['price', 'pizza_id', 'restaurant_id']
            if not all(field in data for field in required_fields):
                return {'errors': ['validation errors']}, 400
            
            # Create new RestaurantPizza
            
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )
            
            db.session.add(restaurant_pizza)
            db.session.commit()
            
            # Return the created RestaurantPizza with nested restaurant and pizza data
            return restaurant_pizza.to_dict(), 201
            
        except ValueError as e:
          
            db.session.rollback()
            return {'errors': ['validation errors']}, 400
        except Exception as e:
            
            db.session.rollback()
            return {'errors': ['validation errors']}, 400


# Register resources with their routes
api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantById, '/restaurants/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')


if __name__ == "__main__":
    app.run(port=5555, debug=True)