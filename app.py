from flask import Flask, jsonify, request, render_template
from data_accquiring import start_data_accquiring
from apscheduler.schedulers.background import BackgroundScheduler
import car
import sys
import threading
import time
import atexit

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=start_data_accquiring, trigger="interval", hours=24)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    # Get brand statistics
    brand_statistics = car.get_car_brand_statistics()
    data1 = {'Brands':'Count'}
    data1.update(brand_statistics)

    # Get average price by car brand
    price_statistics = car.get_avg_price_by_brand()
    data2 = {'Brands':'Avg_Price'}
    data2.update(price_statistics)

    # Get average mileage by year of manufacture
    mileage_statistics = car.get_avg_mileage_by_year()
    data3 = {'Year':'Avg_Mileage'}
    data3.update(mileage_statistics)

    # build final data
    data = {'brand_statistics': data1
            , 'price_statistics': data2
            , 'mileage_statistics': data3}

    return render_template('dashboard.html', data=data)

@app.route('/api/v1/cars/importdata', methods=['GET'])
def import_car_data():
    threading.Thread(target=start_data_accquiring).start()
    return "OK", 200

@app.route('/api/v1/cars/all', methods=['GET'])
def get_all_cars():
    cars = car.get_cars_by_filters({})
    return jsonify([c.serialize() for c in cars])

@app.route('/api/v1/cars/<_id>', methods=['GET'])
def get_car_by_id(_id):
    _car = car.get_car_by_id(_id)
    return jsonify(_car.serialize() if _car else {})

@app.route('/api/v1/cars/filter', methods=['GET'])
def get_cars_by_filter():
    criteria = {}
    cars = []
    
    try:
        if 'brand' in request.args:
            car_brand = request.args['brand']
            criteria.update({'brand' : {'$regex': f'.*{car_brand}.*', '$options': 'i'}})

        if 'model' in request.args:
            model = request.args['model']
            criteria.update({'model' : {'$regex': f'.*{model}.*', '$options': 'i'}})

        if 'years' in request.args:
            _year = request.args['years']
            criteria.update({'year' : {"$in":list(map(int, _year.split(',')))}})

        max_mileage = sys.maxsize
        min_mileage = 0
        if 'max_mileage' in request.args:
            max_mileage = int(request.args['max_mileage'])

        if 'min_mileage' in request.args:
            min_mileage = int(request.args['min_mileage'])

        criteria.update({'mileage' : {'$gte': min_mileage, '$lte': max_mileage}})

        max_price = sys.maxsize
        min_price = 0
        if 'max_price' in request.args:
            max_price = int(request.args['max_price'])

        if 'min_price' in request.args:
            min_price = int(request.args['min_price'])

        criteria.update({'price' : {'$gte': min_price, '$lte': max_price}})

        cars = car.get_cars_by_filters(criteria)
    except Exception as e:
        print(e)

    return jsonify([c.serialize() for c in cars])


if __name__ == "__main__":
    app.run()