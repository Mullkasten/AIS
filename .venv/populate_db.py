from application.config import SessionLocal
from application.services.repository_service import *
import random


""" Данный скрипт заполняет БД тестовыми данными """


Station = ['Kurils', 'Kamchatka', 'Kavkaz']

SeismicDanger = ['Safe', 'Unsafe', 'Danger', 'Very Danger']


def populate_station(db: Session) -> None:
    for station_name in Station:
        add_station(db, station_name)


def populate_danger_type(db: Session) -> None:
    for danger_type_name in SeismicDanger:
        add_danger_type(db, danger_type_name)


if __name__ == "__main__":
    with SessionLocal() as session:
        populate_station(session)
        populate_danger_type(session)
        create_danger(session, temp_m=random.randint(1, 12), temp_frequency=random.randint(20, 800), station_id=1, danger_type=2)