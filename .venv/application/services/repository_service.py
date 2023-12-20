from typing import Optional, Iterable
from sqlalchemy.orm import Session
from application.models.dao import *
import functools
import traceback


"""

    Данный модуль является промежуточным слоем приложения, который отделяет операции 
    для работы с моделями DAO от основной бизнес-логики приложения. Создание данного 
    слоя позволяет унифицировать функции работы с источником данных, и, например, если 
    в приложении нужно будет использовать другой framework для работы с БД, вы можете 
    создать новый модуль (newframework_repository_service.py) и реализовать в нем функции 
    с аналогичными названиями (get_danger_by_station_id, и т.д.). Новый модуль можно будет
    просто импортировать в модуль с основной бизнес-логикой, практически не меняя при этом
    остальной код.
    Также отделение функций работы с БД можно сделать через отдельный абстрактный класс и 
    использовать порождающий паттерн для переключения между необходимыми реализациями.

"""


def dbexception(db_func):
    """ Функция-декоратор для перехвата исключений БД.
        Данный декоратор можно использовать перед любыми
        функциями, работающими с БД, чтобы не повторять в
        теле функции конструкцию try-except (как в функции add_danger). """
    @functools.wraps(db_func)
    def decorated_func(db: Session, *args, **kwargs) -> bool:
        try:
            db_func(db, *args, **kwargs)    # вызов основной ("оборачиваемой") функции
            db.commit()     # подтверждение изменений в БД
            return True
        except Exception as ex:
            # выводим исключение и "откатываем" изменения
            print(f'Exception in {db_func.__name__}: {traceback.format_exc()}')
            db.rollback()
            return False
    return decorated_func

def get_all_dangers(db: Session) -> Iterable[Danger]:
    """ Выборка всех записей об активности """
    result = db.query(Danger).all()
    return result

def get_danger_by_station_id(db: Session, station_id: int) -> Optional[Danger]:
    """ Выборка одной записи об активности по идентификатору (PrimaryKey) станции """
    result = db.query(Danger).filter(Danger.station == station_id).first()
    return result


def get_danger_by_station_name(db: Session, station_name: str) -> Optional[Danger]:
    """ Выборка одной записи об активности по наименованию станции """
    result = db.query(Danger).join(Station).filter(Station.name == station_name).first()
    return result

def get_all_dangers_by_station_name(db: Session, station_name: str) -> Iterable[Danger]:
    """ Выборка всех записей об активности по наименованию станции """
    result = db.query(Danger).join(Station).filter(Station.name == station_name).all()
    return result


def create_danger(db: Session, temp_m: int, temp_frequency: int, station_id: int, danger_type: int) -> bool:
    """ Создание нового объекта danger и добавление записи о погоде """
    danger = Danger(
        magnitude=temp_m,
        frequency=temp_frequency,
        station=station_id,
        type=danger_type
        )
    return add_danger(db, danger)


def add_danger(db: Session, danger: Danger) -> bool:
    """ Добавление записи о погоде (с помощью готового объекта danger) """
    try:
        db.add(danger)
        db.commit()
    except Exception as ex:
        print(traceback.format_exc())
        db.rollback()
        return False
    return True


def update_danger_magnitude_and_frequency(db: Session, temp_m: int, frequency: int, station_id: int) -> bool:
    """ Обновление значений температуры и давления для заданного населённого пункта """
    danger = get_danger_by_station_id(db, station_id)
    danger.magnitude = temp_m
    danger.frequency = frequency
    return add_danger(db, danger)


@dbexception
def delete_danger_by_station_name(db: Session, station_name: str) -> bool:
    """ Удаление записей о погоде в указанном населённом пункте """
    station_danger = get_all_dangers_by_station_name(db, station_name)
    for danger_obj in station_danger:
        db.delete(danger_obj)


@dbexception
def add_station(db: Session, station_name: str) -> None:
    """ Добавление нового населённого пункта """
    station = Station(name=station_name)
    db.add(station)


@dbexception
def add_danger_type(db: Session, danger_type_name: str) -> None:
    """ Добавление нового типа погоды """
    danger_type = DangerType(type=danger_type_name)
    db.add(danger_type)
