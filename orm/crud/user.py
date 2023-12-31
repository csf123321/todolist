import hashlib
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from orm.model import Users
from orm.model import Session as dbsession
import asyncio
from sqlalchemy import create_engine
from orm.crud.Auth import create_session



def hash_data(data: str):
    """
    用于进行用户的密码加密
    Parameters
    ----------
    data：用户的数据

    Returns
    -------
    加密的数据
    """
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    result = sha256.hexdigest()
    return result


async def sign_up(email:str,username: str, password: str,bind):
    """
    注册的数据库写入操作
    Parameters
    ----------
    email:邮箱
    username:用户名
    password:密码
    bind:数据库连接

    Returns
    -------

    """
    with Session(bind=bind) as db:
        #检测用户名有无重复
        try:
            user = db.query(Users).filter(Users.username == username).one()
            return 1
        except NoResultFound:
            pass
        #重复邮箱
        try:
            user = db.query(Users).filter(Users.email == email).one()
            return 2
        except NoResultFound:
            pass

        #添加用户
        password = hash_data(password)
        new_user = Users(email=email,username=username,password=password)
        db.add(new_user)

        db.commit()
        return 0

async def sign_in(email:str,password:str,bind):
    """
    处理登录的数据库逻辑
    Parameters
    ----------
    email:邮箱
    password:密码

    Returns
    -------

    """
    with Session(bind) as db:
        try:
            user = db.query(Users).filter(Users.email==email).one()
        except NoResultFound:
            return 1
        password = hash_data(password)
        if user.password != password:
            return 2
        token = create_session(user,bind)
        return token

async def logout(user_id,bind):
    with Session(bind) as db:
        sess = db.query(dbsession).filter(dbsession.user_id==user_id).one()
        sess.session = ""
        db.commit()
        return 0

if __name__ == '__main__':
    bind = create_engine("mysql+pymysql://root:123456@localhost/todolistdb",echo=True)
    asyncio.run(sign_in('2050203751@qq.com','123',bind))