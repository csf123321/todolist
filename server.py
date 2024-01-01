from sanic import Sanic
from sanic.response import text
from sanic_ext import Extend
from sqlalchemy import create_engine

from orm import *

app = Sanic("MyTodoList")


from router import register_route
from middleware import register_middleware

bind = create_engine("mysql+pymysql://root:123456@localhost/todolistdb",echo=True)

app.ctx.bind = bind
register_route(app)
register_middleware(app)

app.config.CORS_ORIGINS = ["http://8.130.123.211:5173"]
app.config.CORS_ALLOW_HEADERS = ["content-type","Authorization"]
app.config.CORS_SUPPORTS_CREDENTIALS = True
Extend(app)


if __name__ == '__main__':
    Base.metadata.create_all(bind)
    app.run(host='0.0.0.0', port=8000, access_log=False,debug=False)
