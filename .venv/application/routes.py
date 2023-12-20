from fastapi import APIRouter, HTTPException, status, Request, Response
from starlette.responses import RedirectResponse
from application.models.dto import *
from application.services.danger_service import DangerService


"""

    Данный модуль отвечает за маршрутизацию доступных API URI (endpoints) сервера

"""


router = APIRouter(prefix='/api', tags=['Seismic activity assessment API'])       # подключаем данный роутер к корневому адресу /api
service = DangerService()              # подключаем слой с дополнительной бизнес-логикой


@router.get('/')
async def root():
    """ Переадресация на страницу Swagger """
    return RedirectResponse(url='/docs', status_code=307)


@router.get('/seismicactivity/', response_model=List[DangerDTO])
async def get_all_seismicactivity():
    """ Получение всех записей о сейсмической активности """
    return service.get_all_dangers_in_danger()

@router.get('/seismicactivity/{station_name}', response_model= DangerDTO)
async def get_seismicactivity_by_station_name(station_name: str):
    """ Получение записи о сейсмической активности из определенной станции (необходим параметр ?station_name=) """
    danger_data=service.get_danger_by_station_name(station_name)
    if danger_data is None:
        raise HTTPException(status_code=404, detail="Сейсмическая активность не найдена")
    return danger_data

@router.post('/seismicactivity', status_code=201)
async def post_seismicactivity(danger: DangerDTO):
    """ Добавить новую запись об активности """
    if service.add_danger_info(danger):
        return Response(status_code=201)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't add new Danger data",
        )


@router.put('/seismicactivity', status_code=202)
async def put_seismicactivity(danger: DangerDTO):
    """ Обновить запись об активности по id станции """
    if service.update_danger_info(danger):
        return Response(status_code=202)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't update Danger data",
        )


@router.delete('/seismicactivity/{station_name}', status_code=200)
async def del_seismicactivity(station_name: str):
    """ Удаление записи об активности """
    if service.delete_danger_info_by_station_name(station_name):
        return Response(status_code=200)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't delete Danger data",
        )


@router.post('/station', status_code=201)
async def create_station(station: StationDTO) -> Response:
    """ Добавить новую станцию """
    if service.add_station(station):
        return Response(status_code=201)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't add new Station data",
        )
    
@router.post('/danger_type', status_code=201)
async def create_danger_type(danger_type: DangerTypeDTO) -> Response:
    """ Добавить новый тип погоды """
    if service.add_type(danger_type):
        return Response(status_code=201)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't add new Type data",
        )
