# coding=utf-8
import unittest
from app import app
import json
from common import fun


class TestExample(unittest.TestCase):
    '''
    定义测试案例
    '''

    # 测试代码执行之前调用 (方法名固定)
    def setUp(self):
        '''
        在执行具体的测试方法前，先被调用
        :return:
        '''
        app.config.from_object('config.TestingConfig')
        # 可以使用python的http标准客户端进行测试
        # urllib  urllib2  requests
        #app.config['TESTING'] = True  # 指定app在测试模式下运行
        app.testing = True  # 指定app在测试模式下运行。 (测试模式下,视图中的意外异常可以正常打印显示出来)
        # 使用flask提供的测试客户端进行测试 (Flask客户端可以模拟发送请求)
        self.client = app.test_client()

    # 测试代码。 (方法名必须以"test_"开头)
    def test_list_user(self):
        '''
        测试模拟场景
        :return:
        '''
        # 使用Flask客户端向后端发送post请求, data指明发送的数据，会返回一个响应对象
        response = self.client.get("/example/list", data={})

        # respoonse.data是响应体数据
        resp_json = response.data

        # 按照json解析
        resp_dict = json.loads(resp_json)
        app.logger.debug(resp_dict)

        # 使用断言进行验证
        self.assertIn("status", resp_dict)
        status = resp_dict.get("status")
        self.assertEqual(status, 200)


 # 测试代码。 (方法名必须以"test_"开头)
    def test_add_user(self):
        '''
        测试模拟场景
        :return:
        '''
        # 使用Flask客户端向后端发送post请求, data指明发送的数据，会返回一个响应对象
        response = self.client.get("/example/add", data={"username":"testAdd","update_time":fun.intTime(),"create_time":fun.intTime()})

        # respoonse.data是响应体数据
        resp_json = response.data

        # 按照json解析
        resp_dict = json.loads(resp_json)
        app.logger.debug(resp_dict)

        # 使用断言进行验证
        self.assertIn("status", resp_dict)
        status = resp_dict.get("status")
        self.assertEqual(status, 200)

if __name__ == '__main__':
    unittest.main()  # 进行测试
