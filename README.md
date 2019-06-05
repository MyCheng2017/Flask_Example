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

