# coding=utf-8
# sql语句拼接封装类
# 类似thinkphp框架的操作方式
from dao import sqliteDb
from flask import current_app
import traceback


class Model(object):
    '''
    用于拼接sql语句的类
    不建议直接调用_开头的方法
    基本用法：
    1、增加：
        （1）插入一条记录
            Model(tableName).addData(object).add()
            Model(tableName).put(key,value).add()
        （2）插入多条记录
            Model(tableName).addList(list).insertList() 推荐
            Model(tableName).addList(list).add()
    2、删除：
        （1）删除一条记录
            指定条件where：Model(tableName).where(where).delete()
            指定条件object：Model(tableName).addData(object).delete()
            指定条件{key:value}：Model(tableName).put(key,value).delete()
        （2）删除多条记录
            指定条件fieldWhere：Model(tableName).addList(list).delete(fieldWhere=["field"])
    3、修改：
        （1）修改一条记录
            object中有id且需要使用id更新：Model(tableName).addData(object).update()
            where更新：Model(tableName).addData(object).where(where).update()
        （2）修改多条记录
            object中有id且需要使用id更新：Model(tableName).addList(list).update()
            fieldWhere更新：Model(tableName).addList(list).update(fieldWhere=["field"])
    4、查询：
        （1）查询一条记录
            Model(tableName).where(where).find()
            Model(tableName).addData(object).find()
            Model(tableName).put(key,value).find()
        （2）查询多条记录
            Model(tableName).select()
            Model(tableName).where(where).select()
            Model(tableName).addData(object).select()
            Model(tableName).put(key,value).select()
        （3）join
            Model(tableName).join("left join tableName2 on field1=field2").select()
        （4）group
            Model(tableName).group("field1,field2").select()
        （5）page
            Model(tableName).page(pageNum,pageRow).select()
            Model(tableName).where(where).page(pageNum,pageRow).select()
            Model(tableName).addData(object).page(pageNum,pageRow).select()
            Model(tableName).put(key,value).page(pageNum,pageRow).select()
        （6）limit
            Model(tableName).limit(start,end).select()
            Model(tableName).where(where).limit(start,end).select()
            Model(tableName).addData(object).limit(start,end).select()
            Model(tableName).put(key,value).limit(start,end).select()
        （7）order
            Model(tableName).order("id desc").select()
        （8）field
            Model(tableName).field("id,sum(numField)").select()
        （9）union
            Model(tableName).union("select * from tableName").select()

    '''
    testTable = "test"

    def __init__(self, table):
        self.table = table
        self._clear()

    def getCols(self):
        '''
        获取当前表的字段名，用于检查增删改查时是否有非法字段传入等（未实现）
        :return:
        '''
        conn = sqliteDb.get_db()
        conn.execute("SELECT * FROM {}".format(self.table))
        col_name_list = [tuple[0] for tuple in conn.description]
        self.cols = col_name_list
        return col_name_list

    def table(self, table):
        '''
        其他表名
        :param table:
        :return:
        '''
        self.table_a = table
        return self

    def where(self, *args):
        '''
        where条件
        支持一个参数是字符串；支持第一个参数是字符串，第二个参数是数组，用于预编译
        :param args:
        :return:
        '''
        self.whereStr = ""
        if len(args) == 1:
            self.whereStr = str(args[0])
        if len(args) > 1 and isinstance(args[0], str):
            self.whereStr = args[0]
            for i in range(args):
                if i == 0:
                    continue
                self.whereArgs.append(args[i])
        return self

    def field(self, *args):
        '''
        设置要查询的字段名
        1、可以传入一个字符串
        2、可以传入一个list
        3、可以传入（）
        :param args:
        :return:
        '''
        self.fieldStr = ""
        if len(args) == 1 and isinstance(args[0], str):
            self.fieldStr = args[0]
        if len(args) == 1 and isinstance(args[0], list):
            k = 0
            for field in args[0]:
                k += 1
                if k == len(args[0]):
                    self.fieldStr += "%s" % field
                else:
                    self.fieldStr += "%s," % field
        if len(args) > 1:
            k = 0
            for field in args:
                k += 1
                if k == len(args):
                    self.fieldStr += "%s" % field
                else:
                    self.fieldStr += "%s," % field
        return self

    def alias(self, alias):
        '''
        表的别名
        :param alias:
        :return:
        '''
        self.alias = alias
        return self

    def put(self, key=None, value=None):
        '''
        添加一个键值对数据，可作为where条件、可作为插入的数据、更新的数据
        :param key:
        :param value:
        :return:
        '''
        if key and value:
            if self.data is None:
                self.data = {}
            self.data[key] = value
        return self

    def addData(self, obj=None):
        '''
        添加一个对象数据，可作为where条件、可作为插入的数据、更新的数据
        :param obj:
        :return:
        '''
        if obj:
            self.data = obj
        return self

    # ：添加一个列表数据，可作为数据批量插入
    def addList(self, list=None):
        if list:
            self.list = list
        return self

    # ：其实直接使用where就够了
    def andLast(self, a=None, eq=None, b=None):
        if a and eq and b:
            self.whereStr += " and %s %s %s " % (a, eq, b)
        else:
            pass  # 抛出异常
        return self

    # ：其实直接使用where就够了
    def orLast(self, a=None, eq=None, b=None):
        if a and eq and b:
            self.whereStr += " or %s %s %s " % (a, eq, b)
        else:
            pass  # 抛出异常
        return self

    # ：其实直接使用where就够了
    def andFirst(self, a=None, eq=None, b=None):
        if a and eq and b:
            self.whereStr += " and (%s %s %s) " % (a, eq, b)
        else:
            pass  # 抛出异常
        return self

    # ：其实直接使用where就够了
    def orFirst(self, a=None, eq=None, b=None):
        if a and eq and b:
            self.whereStr += " or (%s %s %s) " % (a, eq, b)
        else:
            pass  # 抛出异常
        return self

    def order(self, str=None):
        '''
        只支持字符串，必须标明desc还是asc
        示例：order("id desc")
        :param str:
        :return:
        '''
        if str:
            self.orderStr = str
        return self

    def limit(self, *args):
        '''
        参数可以是字符串'1,2'，也可以是两个数字参数（1，2）,page优先limit
        :param args:
        :return:
        '''
        if len(args) == 1:
            self.limitStr = str(args[0])
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[0], int):
            self.limitStr = "%s,%s" % (args[0], args[1])
        return self

    def page(self, *args):
        '''

        参数可以是字符串'1,2'，也可以是两个数字参数（1，2）；page优先limit
        :param args:
        :return:
        '''
        if len(args) == 1:
            self.pageStr = str(args[0])
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[0], int):
            self.pageStr = "%s,%s" % ((args[0] - 1) * args[1], args[1])
            self.pageArgs = args
        return self

    def group(self, *args):
        '''
        只需传入字段名，不需要带有group by
        :param args:
        :return:
        '''
        if len(args) == 1 and isinstance(args[0], str):
            self.groupStr = args[0]
        if len(args) > 1:
            k = 0
            for field in args:
                k += 1
                if k == len(args):
                    self.groupStr += "%s" % field
                else:
                    self.groupStr += "%s," % field
        return self

    def join(self, *args):
        '''
        只支持字符串，必须带有left join 等字样，每个字符串是一个join
        :param args:
        :return:
        '''
        self.joinStr = ''
        if len(args) > 0:
            for i in range(len(args)):
                self.joinStr += " %s " % args[i]
        return self

    def union(self, *args):
        '''
        连接其他表
        只支持字符串,每个字符串是select语句
        :param args:
        :return:
        '''
        if len(args) >= 1:
            for i in args:
                self.unionStr += " %s " % i
        return self

    def distinct(self, field=None):
        '''
        同数据库distinct
        只支持字符串,字符串是字段名，可以用field代替
        :param field:
        :return:
        '''
        if field:
            self.distinctStr = field
        return self

    def add(self, clear=True):
        '''
        插入数据：
        1、使用addList传入数组，批量插入
        2、使用addData传入字典数据，单条插入
        :param clear: 插入完成是否清空addList、addData的数据
        :return: 返回成功的条数
        '''
        row = 0
        # 存在数组,优先批量插入
        if self.list and len(self.list) > 0:
            row = self.insertList(clear)
        # 存在obj，插入addData传入的数据
        elif self.data:
            try:
                row = self._insert(self.data)
            except Exception as err:
                current_app.logger.error(err)
                current_app.logger.error(self.data)
                current_app.logger.error(traceback.format_exc())
                raise Exception("add data fail!")
        if clear:
            self._clear()
        return row

    def _clear(self):
        '''
        清空所有传入的数据，外部不可调用
        :return:
        '''
        self.list = None
        self.data = None
        self.whereStr = None
        self.joinStr = None
        self.unionStr = None
        self.fieldStr = None
        self.limitStr = None
        self.pageStr = None
        self.distinctStr = None
        self.whereArgs = None
        self.pageArgs = None
        self.alias = None
        self.orderStr = None
        self.groupStr = None

    def _insert(self, data):
        '''
        插入单条数据，外部不可调用
        :param data: 需要插入的数据
        :return: 返回0表示失败，返回1成功
        '''
        kv = self._conn(data)
        key = kv["key"]
        value = kv["value"]
        sql = "insert into %s (%s) values(%s)" % (self.table, key, value)
        return sqliteDb.execute_sql(sql)

    # 批量插入
    def insertList(self):
        '''
        批量插入多条数据，配合addList方法使用
        :return:
        '''
        num = 0
        if self.list:
            # 获取数据库连接
            conn = sqliteDb.get_db()
            try:
                for item in self.list:
                    num += 1
                    # 拼接键和值
                    kv = self._conn(item)
                    key = kv["key"]
                    value = kv["value"]
                    sql = "insert into %s(%s) values(%s)" % (self.table, key, value)
                    conn.execute(sql)
                conn.commit()
            except Exception as err:
                current_app.logger.error(err)
                current_app.logger.error("error list:")
                current_app.logger.error(self.list)
                current_app.logger.error(traceback.format_exc())
                # 全部回滚
                conn.rollback()
                conn.commit()
                raise Exception("insert list fail!")
        return num

    # ：删除数据
    def delete(self, clear=True, whereField=[]):
        '''
        删除方法：
        1、可以直接调用where方法
        2、可以使用addData方法传入多个删除条件
        :param clear: 是否清空，不清空addData传入的数据不清空
        :param whereField: 使用什么字段作为删除条件，批量删除时可用
        :return:
        '''
        row = 0
        # 存在数组,优先批量删除
        if self.list:
            conn = sqliteDb.get_db()
            try:
                for item in self.list:
                    if self.whereStr:
                        where = self.whereStr
                    else:
                        # 使用当前函数的whereField作为动态条件
                        if len(whereField) > 0:
                            where = ''
                            for wf in whereField:
                                where += "%s='%s' and " % (wf, item[wf])
                            where += "1=1"
                            # 如果都没有，查看内容中是否有id，有用来更新
                        elif "id" in item:
                            where = "id='%s'" % item["id"]
                        else:
                            # 全部匹配才成功删除
                            where = self._connKv(item, "and")
                    sql = "delete from %s where %s" % (self.table, where)
                    conn.execute(sql)
                    row += 1
                conn.commit()
            except Exception as err:
                current_app.logger.error(err)
                current_app.logger.error("error list:")
                current_app.logger.error(self.list)
                current_app.logger.error(traceback.format_exc())
                conn.rollback()
                conn.commit()
                raise Exception("delete list fail！")
        # 使用addData传入的数据作为条件
        elif self.data:
            try:
                row = self._delete(self.data)
            except Exception as err:
                current_app.logger.error(err)
                current_app.logger.error("error data:")
                current_app.logger.error(self.data)
                current_app.logger.error(traceback.format_exc())
                raise Exception("delete data fail！")
        # 使用where传入的作为条件
        elif self.whereStr:
            try:
                sql = "delete from %s where %s" % (self.table, self.whereStr)
                row = sqliteDb.execute_sql(sql)
            except Exception as err:
                current_app.logger.error(err)
                current_app.logger.error("error where:")
                current_app.logger.error(self.whereStr)
                current_app.logger.error(traceback.format_exc())
                raise Exception("delete where fail！")
        if clear:
            self._clear()
        return row

    def update(self, clear=True, whereField=[]):
        '''
        修改数据
        优先更新list数据(addList)，其次更新单条数据（addData()）
        更新的条件优先级最高是。where()
        方法的条件；其次是whereField的条件
        :param
        clear: 是否清空
        :param
        whereField: 更新的where条件字段名，会从每条数据中拿数据
        :return:
        '''
        row = 0
        where = ''
        # 存在数组,优先
        if self.list:
            # 获取连接
            conn = sqliteDb.get_db()
            try:
                # 一条条遍历，批量插入
                for item in self.list:
                    # 记录插入条数
                    row += 1
                    # 键值对拼接
                    kv = self._connKv(item, ",")
                    # 优先使用where函数的条件
                    if self.whereStr:
                        where = self.whereStr
                    else:
                        # 使用当前函数的whereField作为动态条件
                        if len(whereField) > 0:
                            where = ''
                            for wf in whereField:
                                where += "%s='%s' and " % (wf, item[wf])
                                del item[wf]
                            where += "1=1"
                            # 如果都没有，查看内容中是否有id，有用来更新
                        elif "id" in item:
                            where = "id='%s'" % item["id"]
                            del item["id"]
                        else:
                            # 这里基本不会成功
                            where = self._connKv(item, "and")
                    sql = "update %s  set %s where %s " % (self.table, kv, where)
                    # 执行sql
                    current_app.logger.debug(sql)
                    conn.execute(sql)
                # 提交
                conn.commit()
            except Exception as err:
                current_app.logger.error(err)
                current_app.logger.error(self.list)
                current_app.logger.error(traceback.format_exc())
                # 出错全部回滚
                conn.rollback()
                conn.commit()
                raise Exception("update list fail！")
        # 存在obj
        elif self.data:
            try:
                row = self._update(self.data)
            except Exception as err:
                current_app.logger.error(err)
                current_app.logger.error(self.data)
                current_app.logger.error(traceback.format_exc())
                raise Exception("update data fail！")
        if clear:
            self._clear()
        return row

    def select(self, clear=True):
        '''
        查询多条数据
        :param
        clear: 是否清空传入的数据
        :return:
        '''
        field = self._getField()
        join = self._getJoin()
        group = self._getGroup()
        where = self._getWhere()
        order = self._getOrder()
        limit = self._getLimit()
        page = self._getPage()
        # 查询分页数据page方式
        if page != "":
            # 获取总数
            sqlCount = "select sum(total) as total from (select count(0) as total from %s %s %s %s)" % (
                self.table, join, where, group)
            total = sqliteDb.query_db(sqlCount, one=True)
            totalCount = total["total"]
            sql = "select %s from %s %s %s %s %s %s" % (field, self.table, join, where, group, order, page)
            listQuery = sqliteDb.query_db(sql)
            res = {"totalCount": totalCount, "listQuery": listQuery}
        # 查询分页数据limit方式
        elif limit != "":
            sql = "select %s from  %s %s %s %s %s %s" % (field, self.table, join, where, group, order, limit)
            res = sqliteDb.query_db(sql)
        # 查询多条数据
        else:
            sql = "select %s from  %s %s %s %s %s" % (field, self.table, join, where, group, order)
            res = sqliteDb.query_db(sql)
            if clear:
                self._clear()
        return res

    def find(self, clear=True):
        '''
        查询一条数据
        :param
        clear: 是否清空传入数据,
        :return: 返回一条字典数据
        '''
        field = self._getField()
        join = self._getJoin()
        group = self._getGroup()
        where = self._getWhere()
        order = self._getOrder()

        sql = "select %s from  %s %s %s %s %s limit 1" % (field, self.table, join, where, group, order)
        res = sqliteDb.query_db(sql, one=True)
        if clear:
            self._clear()
        return res

    def _delete(self, data):
        '''
        删除单条记录，外部不可调用
        :param
        data:
        :return:
        '''
        # 拼接键值对
        kv = self._connKv(data)
        sql = "delete from %s where %s" % (self.table, kv)
        return sqliteDb.execute_sql(sql)

    def _update(self, data):
        '''
        执行单条数据update操作，外部不可调用
        :param
        data: 需要update的数据
        :return:
        '''
        # 拼接键值对
        kv = self._connKv(data, ",")
        if self.whereStr:
            # 优先使用where方法的where
            where = self.whereStr
        else:
            # 没有指定where，先查看是否存在id字段
            if "id" in data:
                where = " id='%s'" % data["id"]
            else:
                # 执行了也没啥用
                where = self._connKv(data, "and")
        sql = "update %s set %s where %s " % (self.table, kv, where)
        return sqliteDb.execute_sql(sql)

    def _conn(self, args, split=","):
        '''
        将字典的所有key连接，将字典的所有值连接，分隔符为split
        :param
        args: 字典数据
        :param
        split: 分隔符
        :return: {key, value}
        '''
        k = 0
        groupStr = ""
        valueStr = ""
        for field in args:
            k += 1
            if k == len(args):
                groupStr += "%s" % field
                valueStr += "'%s'" % args[field]
            else:
                groupStr += "%s %s" % (field, split)
                valueStr += "'%s' %s" % (args[field], split)

        return {"key": groupStr, "value": valueStr}

    def _connKv(self, args, split="and"):

        '''
        拼接键值对
        :param
        args: 字典类型数据
        :param
        split: 分隔符
        :return: 返回字符串
        '''

        k = 0
        valueStr = ""

        for field in args:
            k += 1
            if k == len(args):
                valueStr += " %s='%s' " % (field, args[field])
            else:
                valueStr += " %s='%s' %s " % (field, args[field], split)
        return valueStr

    def _getField(self):
        '''
        获取field方法的拼接字符串，外部不可调用
        :return:
        '''
        if self.fieldStr:
            field = self.fieldStr
            if self.distinctStr:
                field = "%s,%s" % self.distinctStr, field
        elif self.distinctStr:
            field = self.distinctStr
        else:
            # 如果没有调用field方法
            field = "*"
        return field or "*"

    def _getJoin(self):
        '''
        获取join方法的拼接字符串，外部不可调用
        :return:
        '''
        join = ""
        if self.joinStr:
            join = self.joinStr
        return join or ""

    def _getGroup(self):
        '''
        获取group方法的拼接字符串，外部不可调用

    :return:
    '''

        group = ""
        if self.groupStr:
            group = " group by %s " % self.groupStr
        return group or ""

    def _getWhere(self):
        '''
        获取where方法的拼接字符串，外部不可调用
       :return:
       '''

        if self.whereStr:
            # where方法传入的优先级最高
            where = " where %s" % self.whereStr
        elif self.data:
            # 其次使用addData方法传入的数据作为where查询条件
            where = " where %s " % self._connKv(self.data, "and")
        else:
            where = ""
        return where

    def _getOrder(self):
        '''
        获取order方法的拼接字符串，外部不可调用
        :return:
        '''

        order = ""
        if self.orderStr:
            order = " order by %s " % self.orderStr
        return order or ""

    def _getLimit(self):
        '''
        获取limit方法的拼接字符串，外部不可调用
        :return:
        '''

        limit = ""
        if self.limitStr:
            limit = " limit %s " % self.limitStr
        return limit or ""

    def _getPage(self):
        '''
        获取page方法的拼接字符串，外部不可调用
        :return:
        '''

        page = ""
        if self.pageStr:
            page = " limit %s " % self.pageStr
        return page or ""
