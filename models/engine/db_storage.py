#!/usr/bin/python3
"""
New engine DBStorage
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy import create_engine, Integer
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models.user import User
from os import getenv


class DBStorage:
    """class DBStorage and his methods"""
    __engine = None
    __session = None

    def __init__(self):
        """ public instance method for contructor"""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        MY_DB = "mysql+mysqldb://{}:{}@{}/{}".format(user, passwd, host, db)
        self.__engine = create_engine(MY_DB, pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ all objects depending of the class name"""
        classes = ['State', 'City', 'User', 'Place', 'Review', 'Amenity']
        objects = {}
        if cls and cls in classes:
            for obj in self.__session.query(eval(cls)):
                objects.update({obj.id: obj})
        elif cls is None:
            for class_name in classes:
                for obj in self.__session.query(eval(class_name)):
                    objects.update({obj.id: obj})
        return objects

    def new(self, obj):
        """the new object"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database sessio"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        re_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(re_session)
        self.__session = Session()

    def close(self):
        """ calling remove method"""
        self.__session.close_all()
