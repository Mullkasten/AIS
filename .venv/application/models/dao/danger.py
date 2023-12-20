from sqlalchemy import Column, ForeignKey, Boolean, Integer, Numeric, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from datetime import datetime


# Объявление декларативного (описательного) метода представления БД
Base = declarative_base()


class Danger(Base):
    """ Описание сущности (таблицы) Danger """
    __tablename__ = "danger"

    id = Column(Integer, primary_key=True)      # объявление первичного ключа
    _magnitude = Column('magnitude', Integer, nullable=False)       # поле не может быть пустым (NULL)
    #magnitude_f = Column(Integer)
    frequency = Column(Integer)
    # связь полей type и station через внешние ключи
    type = Column(Integer, ForeignKey('danger_type.id'), nullable=False)   # объявление ограничения по внешнему ключу
    """ 
     При использовании конструкции relationship("ИМЯ_СВЯЗАННОГО_ОБЪЕКТА") по соответствующему имени атрибута можно
     будет получить свзязанный объект (в данном примере, если после SELECT мы получили объект w типа Danger, то
     связанный с ним объект объект DangerType можно будет получить через атрибут w.Danger_type, а необходимое
     значение, соответственно: w.Danger_type.type). Подробнее см.: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
    """
    danger_type = relationship('DangerType')
    station = Column(Integer, ForeignKey('station.id'), nullable=False)
    station_name = relationship('Station')
    created_on = Column(DateTime(), default=datetime.now)      # в поле автоматически генерируется метка времени при создании записи
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)    # в поле автоматически генерируется метка времени при создании записи, метка обновляется при каждой операции UPDATE

    @hybrid_property
    def magnitude(self):
        """ Декоратор @hybrid_property позволяет добавить какую-нибудь бизнес-логику или проверку
            при установке данному полю какого-либо значения. Подробнее см.:
            https://docs.sqlalchemy.org/en/14/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property """
        return self._magnitude

    @magnitude.setter
    def magnitude(self, magnitude: float):
        """ При установке значения полю magnitude будет автоматически рассчитано значение magnitude_f """
        self.magnitude_f = 32.0 + (magnitude / 0.5556)
        self._magnitude = magnitude

    def __repr__(self):
        """ Переопределяем строковое представление объекта (см. python magic methods)"""
        return f'{self.__dict__}'


class DangerType(Base):
    """ Тип погоды ("Ясно", "Облачно" и т.п.) """
    __tablename__ = "danger_type"

    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)      # значение этого поля не может повторяться


class Station(Base):
    """ Таблица с наименованиями населённых пунктов """
    __tablename__ = "station"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
