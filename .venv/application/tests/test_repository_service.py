import unittest
import random
import sys
sys.path.append("C:\\Users\\adeli\\Downloads\\AIS2\\AIS2\\.venv") #без этого у меня выходит ошибка, но может это только у меня
from application.config import SessionLocal
from application.services.repository_service import *


"""
   Данный модуль реализует "тестовые случаи/ситуации" для модуля repository_service.
   Для создания "тестового случая" необходимо создать отдельный класс, который наследует 
   базовый класс TestCase. Класс TestCase предоставляется встроенным 
   в Python модулем для тестирования - unittest.
   
   Более детально см.: https://pythonworld.ru/moduli/modul-unittest.html
"""


STATION = ['KURILS', 'KAMCHATKA', 'KAVKAZ']

SEISMIC_DANGER = ['SAFE', 'UNSAFE', 'DANGER', 'VERY DANGER']


class TestDangerRepositoryService(unittest.TestCase):
    """ Все тестовые методы в классе TestCase (по соглашению)
        должны начинаться с префикса test_* """

    def setUp(self):
        """ Наследуемый метод setUp определяет инструкции,
            которые должны быть выполнены ПЕРЕД тестированием """
        self.session = SessionLocal()       # создаем сессию подключения к БД
        try:
            for station_name in STATION:
                add_station(self.session, station_name)
            for seismic_danger_type in SEISMIC_DANGER:
                add_danger_type(self.session, seismic_danger_type)
        except:
            print('Test data already created')

    def test_create_danger(self):
        """ Тест функции создания записи Danger """
        result = create_danger(self.session,
                                temp_m=random.uniform(20, 29),
                                temp_frequency=random.randint(735, 755),
                                danger_type=1,
                                station_id=1)
        self.assertTrue(result)     # валидируем результат (result == True)

    def test_get_danger(self):
        """ Тест функции поиска записи Danger по наименованию населённого пункта """
        weather_in_kurils_rows = get_all_dangers_by_station_name(self.session, station_name='KURILS')
        for row in weather_in_kurils_rows:
            self.assertIsNotNone(row)           # запись должна существовать
            self.assertTrue(row.station == 1)   # идентификатор station_id == 1 (т.е. город KURILS в таблице station)
            self.assertTrue(row.station.name == 'KURILS')  # проверка связи (relation) по FK

    def test_delete_danger(self):
        """ Тест функции удаления записи Danger по наименованию населённого пункта """
        delete_danger_by_station_name(self.session, station_name='KURILS')
        result = get_danger_by_station_id(self.session, station_id=1)        # ищем запись по идентификатору города KURILS
        self.assertIsNone(result)       # запись не должна существовать

    def tearDown(self):
        """ Наследуемый метод tearDown определяет инструкции,
            которые должны быть выполнены ПОСЛЕ тестирования """
        self.session.close()        # закрываем соединение с БД


if __name__ == '__main__':
    unittest.main()
