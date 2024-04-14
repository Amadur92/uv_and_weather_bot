import json
from datetime import datetime

from peewee import *

db = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = db


class WeatherData(BaseModel):
    coordinates = CharField(unique=True)
    city_name = CharField()
    updated_at = IntegerField()
    temperature = CharField()
    humidity = CharField()
    uv_index = CharField()
    chance_of_rain = CharField()

    def get_coordinates(self):
        return json.loads(self.coordinates)

    def set_coordinates(self, value):
        self.coordinates = json.dumps(value)
# Определим модель, например, для пользователей
class Users(BaseModel):
    user_id = CharField(unique=True)
    username = CharField()
    city = ForeignKeyField(WeatherData, backref='users')
    subscription = IntegerField(default=1)
    join_date = DateTimeField()



class Database:
    def __init__(self):
        self.db = SqliteDatabase('db.sqlite')

    def connect(self):
        self.db.connect()

    def create_tables(self):
        self.db.create_tables([WeatherData, Users])

    def drop_tables(self):
        self.db.drop_tables([WeatherData, Users])

    def add_new_user(self, user_id, username, city, coordinates):
        user = Users.create( user_id = user_id,
                             username = username,
                             city = city,
                             coordinates = coordinates,
                             join_date = datetime.now())



# Добавление данных о погоде
weather = WeatherData.create(city_name='Moscow', updated_at=int(datetime.now().timestamp()), temperature='22°C', humidity='60%', solar_index='High', chance_of_rain='20%')

