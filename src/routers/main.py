from fastapi import APIRouter, Request

main_router_prefix = ""
main_router = APIRouter(prefix=main_router_prefix)


@main_router.get('/')
async def hello(request: Request):
    return {'hello': 'world'}
