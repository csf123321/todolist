import datetime
import asyncio

import sqlalchemy.orm
from sqlalchemy.exc import NoResultFound
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as dbSession
from orm.model import Session,Users
import uuid

namespace = uuid.NAMESPACE_URL

def create_session(user,bind):
    """
    获取token
    Parameters
    ----------
    user:用户对象
    bind:数据库连接

    Returns:token
    -------

    """
    name = user.username + user.email + str(datetime.datetime.today())
    token = uuid.uuid3(namespace,name)
    token = str(token)

    with dbSession(bind) as db:
        user = db.query(Users).filter(Users.id==user.id).one()
        sess = Session(session=token)
        if user.session:
            user.session.session = token
        else:
            user.session = sess
        db.add(user)
        db.commit()
    return token

def get_user(token,bind):
    """
    获取用户
    Parameters
    ----------
    token:用户的验证token
    bind:数据库连接对象

    Returns:用户对象
    -------

    """
    with dbSession(bind) as db:
        try:
            sess = db.query(Session).filter(Session.session==token).one()
        except NoResultFound:
            return 0
        return sess.user

