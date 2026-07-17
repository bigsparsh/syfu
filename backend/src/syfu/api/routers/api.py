from fastapi import APIRouter

api_router = APIRouter(prefix='/api')

@api_router.get('/health')
def health():
    return {'status': 'ok'}
