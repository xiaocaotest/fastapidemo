import uuid
import requests
import unittest

from config import testplan


class FastApiTestUserCreate(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        '''
        初始化测试环境
        :return:
        '''
        cls.client = requests
        cls.testurl = testplan+"/user/create"

    @classmethod
    def tearDownClass(cls) -> None:
        '''
        还原测试环境，测试url
        :return:
        '''
        cls.client = None
        cls.testurl = ''

    def setUp(self) -> None:
        """
        初始化参数
        :return:
        """
        self.parame = {"username": "liwanle1i",
                       "password": "123456",
                       "role": "学生",
                       "age": 19,
                       'studentnum': 20332}

    def tearDown(self) -> None:
        """最后清理参数"""
        self.parame.clear()

    def test_create_user(self):
        """重复的添加一个数据"""
        response = self.client.post(self.testurl, json=self.parame)
        code = response.status_code
        reslut = response.json()
        self.assertEqual(code, 200)
        self.assertEqual(reslut['message'], '用户名重复')
        self.assertEqual(reslut['code'], 100104)

    def test_create_user_new(self):
        """添加一个新的学生"""
        self.parame['username'] = str(uuid.uuid1())[:9]
        response = self.client.post(self.testurl, json=self.parame)
        code = response.status_code
        reslut = response.json()
        self.assertEqual(code, 200)
        self.assertEqual(reslut['code'], 200)
        self.assertEqual(reslut['message'], 'success')

    def test_create_user_new_tearcher(self):
        """添加一个新的教师"""
        self.parame['username'] = str(uuid.uuid1())[:9]
        self.parame['role'] = "教师"
        self.parame['jobnum'] = 93928
        self.parame['sex'] = "女"
        response = self.client.post(self.testurl, json=self.parame)
        code = response.status_code
        reslut = response.json()
        self.assertEqual(code, 200)
        self.assertEqual(reslut['code'], 200)
        self.assertEqual(reslut['message'], 'success')

    def test_create_user_new_one(self):
        """测试学生没有填写学籍号"""
        self.parame['username'] = str(uuid.uuid1())[:9]
        self.parame.pop("studentnum")
        response = self.client.post(self.testurl, json=self.parame)
        code = response.status_code
        reslut = response.json()
        self.assertEqual(code, 200)
        self.assertEqual(reslut['code'], 100102)
        self.assertEqual(reslut['message'], '身份和对应号不匹配')

    def test_create_user_new_tearcher_one(self):
        """
        测试老师的工作号不填写
        """
        self.parame['username'] = str(uuid.uuid1())[:9]
        self.parame['role'] = "教师"
        self.parame['sex'] = "女"
        response = self.client.post(self.testurl, json=self.parame)
        code = response.status_code
        reslut = response.json()
        self.assertEqual(code, 200)
        self.assertEqual(reslut['code'], 100102)
        self.assertEqual(reslut['message'], '身份和对应号不匹配')


if __name__ == "__main__":
    unittest.main()
