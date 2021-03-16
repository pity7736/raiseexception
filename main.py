import uvicorn

from raiseexception import settings

if __name__ == '__main__':
    uvicorn.run(
        app='raiseexception:app',
        host='0.0.0.0',
        port=8000,
        reload=settings.DEBUG
    )
