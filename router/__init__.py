from sanic import Blueprint
from router.user import user_bp
from router.task import tasks_bp


def register_route(app):
    api_route = Blueprint.group(user_bp,tasks_bp,url_prefix='/api')
    app.blueprint(api_route)
