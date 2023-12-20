from typing import Optional, List
from application.config import SessionLocal
from application.models.dao import Danger
from application.models.dto import DangerDTO, StationDTO, DangerTypeDTO
import application.services.repository_service as repository_service


"""

    Данный модуль содержит программный слой с реализацией дополнительной бизнес-логики, 
    выполняемой перед или после выполнения операций над хранилищем данных (repository), 
    например: маппинг атрибутов из DAO в DTO, применение дополнительных функций к атрибутам DTO.
    
    ВАЖНО! Реализация данного слоя приведена в качестве демонстрации полной структуры RESTful веб-сервиса.
           В небольших проектах данный слой может быть избыточен, в таком случае, из контроллера ваших маршрутов 
           (Router в FastAPI или View в Django) можно напрямую работать с функциями хранилища данных (repository_service).

"""


class DangerService:
        
    def get_all_dangers_in_danger(self) -> List[DangerDTO]:
        danger_data: List[DangerDTO] = []
        with SessionLocal() as session:
           result = repository_service.get_all_dangers(session)
           for w in result:
               danger_data.append(self.map_danger_data_to_dto(w))
        return danger_data
    
    def get_danger_by_station_id(self, station_id: int) -> Optional[DangerDTO]:
        with SessionLocal() as session:     # конструкция with позволяет автоматически завершить сессию после выхода из блока
            danger_data = repository_service.get_danger_by_station_id(session, station_id)
        if danger_data is not None:
            return self.map_danger_data_to_dto(danger_data)
        else:
            return None
        
    def get_danger_by_station_name(self, station_name: str) -> Optional[DangerDTO]:
        with SessionLocal() as session:     # конструкция with позволяет автоматически завершить сессию после выхода из блока
            danger_data = repository_service.get_danger_by_station_name(session, station_name)
        if danger_data is not None:
            return self.map_danger_data_to_dto(danger_data)
        else:
            return None

    def add_danger_info(self, danger: DangerDTO) -> bool:
        with SessionLocal() as session:
            return repository_service.create_danger(session,
                                                     temp_m=danger.magnitude,
                                                     temp_frequency=danger.frequency,
                                                     station_id=danger.station,
                                                     danger_type=danger.type)

    def update_danger_info(self, danger: DangerDTO) -> bool:
        with SessionLocal() as session:
            return repository_service.update_danger_magnitude_and_frequency(session,
                                                                       temp_m=danger.magnitude,
                                                                       frequency=danger.frequency,
                                                                       station_id=danger.station)

    def delete_danger_info_by_station_name(self, station_name: str) -> bool:
        with SessionLocal() as session:
            return repository_service.delete_danger_by_station_name(session, station_name)

    def add_station(self, station: StationDTO) -> bool:
        if station.name != "":
            with SessionLocal() as session:
                return repository_service.add_station(session, station_name=station.name.upper())
        return False
    
    def add_type(self, danger_type: DangerTypeDTO) -> bool:
        if danger_type.type != "":
            with SessionLocal() as session:
                return repository_service.add_danger_type(session, danger_type_name=danger_type.type.upper())
        return False

    def map_danger_data_to_dto(self, danger_dao: Danger):
        """ Метод для конвертирования (маппинга) Danger DAO в DangerDTO """
        return DangerDTO(id=danger_dao.id,
                          magnitude=danger_dao.magnitude,
                          frequency=danger_dao.frequency,
                          type=danger_dao.type,
                          station=danger_dao.station,
                          updated_on=danger_dao.updated_on)
