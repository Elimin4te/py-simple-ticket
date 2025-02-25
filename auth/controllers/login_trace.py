from shared.controllers.crud import ModelController
from auth.models.login_trace import InicioDeSesion

class LoginTraceController(ModelController):
    model = InicioDeSesion
    