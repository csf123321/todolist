from sanic.views import HTTPMethodView
from sanic import Sanic
from sanic import Blueprint
from sanic.response import text,json,HTTPResponse

from orm.crud import tasks

app = Sanic.get_app("MyTodoList")

class ListInfo(HTTPMethodView):
    async def get(self,request):
        user = request.ctx.user
        tasksList = await tasks.to_do_info(user,app.ctx.bind)
        print(tasksList)
        res = json({
            'code':0,
            'data':tasksList
        })

        return res

    async def post(self,request):
        user = request.ctx.user
        todo = request.json['todo']
        await tasks.add_todo(user,todo,app.ctx.bind)

        res = json({
            'code':0,
            'message':"添加成功"
        })

        return res

    async def put(self,request):
        user = request.ctx.user
        todo = request.json['todo']
        res_code = await tasks.change_todo(user,todo,app.ctx.bind)

        if res_code==1:
            res = json({
                'code':1,
                "message":"无权限更改"
            })
        elif res_code==0:
            res = json({
                'code':0,
                "message":"更改成功"
            })

        return res

    async def delete(self,request):
        user = request.ctx.user
        todo_id = request.json['id']

        res_code = await tasks.delete_todo(user,todo_id,app.ctx.bind)
        if res_code==1:
            res = json({
                'code':1,
                'message':"无权限"
            })
        else:
            res = json({
                'code':0,
                'message':"删除成功"
            })

        return res

tasks_bp = Blueprint('list',url_prefix='/list')
tasks_bp.add_route(ListInfo.as_view(), "/info")