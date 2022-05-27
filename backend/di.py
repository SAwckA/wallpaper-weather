"""Display Interface, шаблонизатор"""
from starlette.templating import Jinja2Templates


class DI:
    """Определение шаблонизатора"""
    templates = Jinja2Templates(directory='templates')
