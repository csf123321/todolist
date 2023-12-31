from sanic import Sanic
from sanic.response import text
from sanic.request import Request
import uuid

from orm.crud.Auth import get_user,create_session

app = Sanic.get_app("MyTodoList")

async def protected(request):
    token = request.token
    print(token)
    user = get_user(token,app.ctx.bind)

    path = request.path.split('/')
    method = request.method
    print(path)
    if len(path)==4 and (path[3] == 'register' or path[3] == 'login'):
        pass
    elif method=="OPTIONS":
        pass
    elif not user:
        return text('Unauthorized',status=401)
    else:
        request.ctx.user = user


