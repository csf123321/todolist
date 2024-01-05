import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from orm.model import ToDoList

def change_string_to_time(t):
    print("时间戳：",t)
    return datetime.datetime.fromtimestamp(int(t))

async def to_do_info(user,bind):
    """
    获取用户的todo信息
    Parameters
    ----------
    user:用户对象
    bind:数据库连接对象

    Returns
    -------

    """
    with Session(bind) as db:
        todolist = db.query(ToDoList).filter(ToDoList.user_id==user.id).all()
        list_result = []
        for i in todolist:
            temp_object = {}
            temp_object['id'] = i.id
            temp_object['name'] = i.name
            temp_object['description'] = i.description
            temp_object['createDate'] = int(i.createDate.timestamp())
            temp_object['deadline'] = int(i.deadline.timestamp())
            temp_object['state'] = "已完成" if i.state else "未完成"
            list_result.append(temp_object)
        return list_result

async def add_todo(user,todo,bind):
    """
    添加用户的todo信息
    Parameters
    ----------
    user:用户
    bind:数据库连接对象

    Returns
    -------

    """

    with Session(bind) as db:
        new_todo = ToDoList(name=todo['name'],
                            description=todo['description'],
                            createDate=datetime.datetime.today(),
                            deadline=change_string_to_time(todo['deadline']),
                            state=0,
                            user_id=user.id)

        db.add(new_todo)
        db.commit()

async def change_todo(user,todo,bind):
    """
    修改todo的信息
    Parameters
    ----------
    user:用户
    todo:todo的信息
    bind:数据库连接

    Returns
    -------

    """
    with Session(bind) as db:
        old_todo = db.query(ToDoList).filter(ToDoList.id==todo['id']).one()
        if user.id != old_todo.user_id:
            return 1
        if todo['name'] != '':
            old_todo.name = todo['name']
        if todo['description'] != '':
            old_todo.description = todo['description']
        if todo.get('deadline',None):
            old_todo.deadline = change_string_to_time(todo['deadline'])
        if type(todo.get('state',None))==int:
            old_todo.state = todo['state']
        db.add(old_todo)
        db.commit()
        return 0


async def delete_todo(user,id,bind):
    """
    删除指定的todo
    Parameters
    ----------
    user:用户
    id:todo的id
    bind:数据库连接

    Returns
    -------

    """
    with Session(bind) as db:
        target_todo = db.query(ToDoList).filter(ToDoList.id==id).one()
        if user.id != target_todo.user_id:
            return 1

        db.delete(target_todo)
        db.commit()
        return 0