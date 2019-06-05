# Flask框架
## 一、项目介绍
1、本项目基于[flask](https://dormousehole.readthedocs.io/en/latest/)开发，[文档地址]:https://dormousehole.readthedocs.io/en/latest/

2、使用了蓝图、全局异常处理、sql拼接



## 二、目录介绍

### common:

公共方法

    AES：AES加密
    fun：公共方法（封装了获取前端数据的方法和统一响应的方法）
    state：状态码
    
### dao:

数据库相关

    Model：sql拼接类，模拟thinkphp数据库操作
    
    db：数据库操作，获取连接，执行语句，返回查询数据

### example:
使用示例

### exception:
异常相关（统一异常处理）


### logs:
日志文件存放位置
已经按照天进行分割


### static、templates:
静态文件

### test:
测试相关


### app.py:
程序入口

### config.py:
全局配置

### sys.db:
sqlite数据库



## Model类操作数据库

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

  
