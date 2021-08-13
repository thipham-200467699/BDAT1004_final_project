from db_utilities import DbUtiltity

class Car:
    def __init__(self, p_id='', p_year=0, p_brand='', p_model='', p_mileage=0, p_price=0):
        self._id = p_id
        self.year = p_year
        self.brand = p_brand
        self.model = p_model
        self.mileage = p_mileage
        self.price = p_price
    
    def serialize(self):
        return {
            '_id': self._id,
            'year': self.year,
            'brand': self.brand,
            'model': self.model,
            'mileage': self.mileage,
            'price': self.price
        }

def get_car_by_id(car_id):
    _car = None
    with DbUtiltity() as db_util:
        db_util.connect_to_db()

        result = db_util.find_one_car({"_id":car_id})
        if result:
            _car = Car( result['_id']
                    , result['year']
                    , result['brand']
                    , result['model']
                    , result['mileage']
                    , result['price'])
    return _car

def get_cars_by_filters(criteria):
    cars = []
    with DbUtiltity() as db_util:
        db_util.connect_to_db()

        #result = db_util.find_all_cars({'brand': f'/.*{car_brand}.*/i'})
        result = db_util.find_all_cars(criteria)
        for rec in result:
            cars.append(Car(
                  rec['_id']
                , rec['year']
                , rec['brand']
                , rec['model']
                , rec['mileage']
                , rec['price']
            ))
    return cars