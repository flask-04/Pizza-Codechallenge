#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db, Restaurant, Pizza, Restaurant_pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api= Api(app)

@app.errorhandler(NotFound)
def handle_not_found(e):
    response= make_response("NotFound: The requested resource not found", 404)
    return response

@app.route('/')
def home():
    return "<h1>Welcome to Michael Korir Pizza Code Challenge</h1>"

class Restaurants(Resource):
    def get(self):
        response_dict= [n.to_dict() for n in Restaurant.query.all()]
        response= make_response(response_dict, 200)
        return  response

api.add_resource(Restaurants, '/restaurants')

class RestaurantById(Resource):
    def get(self, id):
        restraurant= Restaurant.query.filter_by(id=id).first()
        if restraurant is None:
            response= make_response(jsonify({'error':'Restaurant not found'}),404)
            return response
        else:
            record_dict= restraurant.to_dict()
            response = make_response(record_dict, 200)
            return response
        
    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant is None:
            response= make_response(jsonify({'error':'Restaurant not found'}),404)
            return response
        db.session.delete(restaurant)
        db.session.commit()

api.add_resource(RestaurantById, '/restaurants/<int:id>')    

class Pizza(Resource):
    def get(self):
        response_dict= [n.to_dict() for n in Pizza.query.all()]
        if len(response_dict)==0:
            response= make_response("Restaurant not found", 404)
            return response
        else :
            response= make_response(jsonify(response_dict), 200)
            return response
        
api.add_resource(Pizza, '/pizzas')
    
class RestaurantPizzas(Resource):
        def post(self):
            try:
                data= request.get_json()
                price= data.get('price')
                pizza_id= data.get('pizza_id')
                restaurant_id=  data.get('restaurant_id')
                pizza= Pizza.query.get(pizza_id)
                restaurant=  Restaurant.query.get(restaurant_id)

                if not pizza and restaurant:
                    return make_response(jsonify({"message":["Pizza and Restaurant does not exist"]}),404)
                # If price not between 1-30 return message
                if not 1<= price <=30:
                    return make_response(jsonify({"Error": ['validation error']}))
                else:
                    newpizza= Restaurant_pizza(price=price, pizza_id=pizza_id,  restaurant_id=restaurant_id )
                    db.session.add(newpizza)
                    db.session.commit()

                return make_response(jsonify(newpizza.to_dict()), 201)
            
            except:
                err_dict= {"errors" : ["validation errors"]}
                response= make_response(err_dict, 404)
                db.session.rollback()
                return response

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
