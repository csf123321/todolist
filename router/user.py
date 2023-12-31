from sanic.views import HTTPMethodView
from sanic import Blueprint,Sanic,HTTPMethod
from sanic.response import text,json,HTTPResponse

from orm.crud import user

app = Sanic.get_app("MyTodoList")

class Register(HTTPMethodView):
    async def post(self, request):
        # print(request.form)
        email = request.form['email'][0]
        username = request.form['username'][0]
        password = request.form['password'][0]
        res_code = await user.sign_up(email,username,password,bind=request.app.ctx.bind)
        if res_code == 1:
            return json({'code':1,'message':'用户已存在'})
        elif res_code == 2:
            return json({'code':2,'message':'邮箱已注册'})
        else:
            return json({'code':0,'message':'注册成功'})

class Login(HTTPMethodView):
    async def post(self,request):
        email = request.form['email'][0]
        password = request.form['password'][0]
        res_code = await user.sign_in(email,password,request.app.ctx.bind)
        if res_code==1:
            return json({'code':1,'message':'用户不存在'})
        elif res_code==2:
            return json({'code':2,'message':'密码错误'})
        token = res_code

        res = json({'code':0,'message':"登录成功",'token':token})
        return res

class InfoView(HTTPMethodView):
    async def get(self,request):
        user = request.ctx.user
        userInfo = {
            'username':user.username,
            'email':user.email
        }
        return json({
            'code':0,
            'data':userInfo
        })

async def Logout(request):
    the_user = request.ctx.user
    await user.logout(the_user.id,app.ctx.bind)
    return json({'code':0,'message':'登出成功'})


user_bp = Blueprint('users',url_prefix='/users')
user_bp.add_route(Register.as_view(), "/register")
user_bp.add_route(Login.as_view(),"/login")
user_bp.add_route(InfoView.as_view(),'/info')
user_bp.add_route(Logout,'/logout',[HTTPMethod.PUT])
