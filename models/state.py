#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.city import City
from models.base_model import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all,\
                delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """cities <=> states"""
            l_city = []
            all_instance = storage.all(City)
            for value in all_instance.value():
                if value.state_id == self.id:
                    l_city.append(value)
            return l_city
