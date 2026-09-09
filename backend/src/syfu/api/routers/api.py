from fastapi import APIRouter

from syfu.api.routers.tasks import tasks_router

api_router = APIRouter(prefix='/api')

api_router.include_router(tasks_router)

@api_router.get('/health')
def health():
    return {'status': 'ok'}
