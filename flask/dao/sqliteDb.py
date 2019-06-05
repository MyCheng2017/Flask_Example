# coding=utf-8
#数据库操作
import sqlite3

from flask import g, current_app

DATABASE = "sys.db"

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

#获取数据库连接并保存到全局变量
def get_db(database=DATABASE):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
        db.row_factory = make_dicts
        db.row_factory = sqlite3.Row
    return db

#查询一条或多条记录
def query_db(query, args=(), one=False):
    current_app.logger.info(query)
    cur = get_db().execute(query, args)
    columns = [column[0] for column in cur.description]
    results = []
    if one:
        rv = cur.fetchone()
        if rv:
            cur.close()
            return dict(zip(columns, rv))
    else:
        rv = cur.fetchall()
        if rv:
            for row in rv:
                results.append(dict(zip(columns, row)))
    cur.close()
    return results

#执行一条sql
def execute_sql(query, args=()):
    current_app.logger.info(query)
    conn = get_db()
    cur = conn.execute(query, args)
    cur.fetchone()
    conn.commit()
    cur.close()
    return 1

#获取表的所有字段
def getCols(tbl_name):
    conn = get_db()
    conn.execute("SELECT * FROM {}".format(tbl_name))
    col_name_list = [tuple[0] for tuple in conn.description]
    return col_name_list

