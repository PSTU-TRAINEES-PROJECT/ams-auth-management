from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logging.basicConfig(level=logging.INFO)

class LogRequestPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Foreground Colors
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        WHITE = "\033[37m"
        CYAN = "\033[96m"
        
        # Background Colors
        BLACK_BG = "\033[40m"
        RED_BG = "\033[41m"
        GREEN_BG = "\033[42m"
        YELLOW_BG = "\033[43m"
        BLUE_BG = "\033[44m"
        MAGENTA_BG = "\033[45m"
        CYAN_BG = "\033[46m"
        WHITE_BG = "\033[47m"
        
        RESET = "\033[0m"
        
        logging.info(f"{GREEN_BG}Request path: {request.url.path}{RESET}")
        
        response = await call_next(request)
        
        return response