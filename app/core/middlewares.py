from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import traceback


class CatchExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            print(f"REQUEST: {request.method} {request.url}", flush=True)
            return await call_next(request)

        except IntegrityError as e:
            if "foreign key constraint" in str(e.orig).lower():
                return JSONResponse(status_code=404, content={"detail": "Связанный объект не найден"})
            elif "unique constraint" in str(e.orig).lower():
                return JSONResponse(status_code=409, content={"detail": "Запись с такими данными уже существует"})
            else:
                return JSONResponse(status_code=400, content={"detail": "Ошибка целостности данных"})

        except ValueError as e:
            return JSONResponse(status_code=400, content={"detail": str(e)})

        except Exception:
            print("🔥 Exception caught:", traceback.format_exc(), flush=True)
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
