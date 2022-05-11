import requests
import unittest
import redis


class UserLoginCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = 'http://127.0.0.1:8000/user/login'

    @classmethod
    def tearDownClass(cls) -> None:
        '''
        还原测试环境，测试url
        :return:
        '''
        cls.client = None
        cls.url = ''

    def setUp(self) -> None:
        '''
        初始化参数
        :return:
        '''
        self.parame = {
            "username": "liwanle1i",
            "password": "123456"
        }

    def tearDown(self) -> None:
        '''最后清理参数'''
        self.parame.clear()

    def test_login_usernot_exict(self):
        parame = {
            "username": "liwanle1i33333",
            "password": "123456"
        }
        reponse = requests.post(self.url, json=parame)

        status = reponse.status_code
        reslut = reponse.json()
        self.assertEqual(status, 200)
        self.assertEqual(reslut['code'], 100205)
        self.assertEqual(reslut['message'], '用户不存在')

    def test_login_success(self):
        reponse = requests.post(self.url, json=self.parame)

        status = reponse.status_code
        reslut = reponse.json()
        self.assertEqual(status, 200)
        self.assertEqual(reslut['code'], 200)
        self.assertEqual(reslut['message'], '成功')

    def test_login_success_two(self):
        reponse = requests.post(self.url, json=self.parame)

        status = reponse.status_code
        reslut = reponse.json()
        self.assertEqual(status, 200)
        self.assertEqual(reslut['code'], 200)
        self.assertEqual(reslut['message'], '成功')

    def test_login_error(self):
        self.parame['password'] = '2222222222'
        reponse = requests.post(self.url, json=self.parame)

        status = reponse.status_code
        reslut = reponse.json()
        self.assertEqual(status, 200)
        self.assertEqual(reslut['message'], "密码错误")

    def test_log_error_big(self):
        red = redis.Redis(host='localhost', port=6379, db=0)
        red.hset("liwanle1i_password", 'num', 11)
        red.hset("liwanle1i_password", 'time', "2021-11-17 22:16:57")
        self.parame['password'] = '2222222222'
        reponse = requests.post(self.url, json=self.parame)

        status = reponse.status_code
        print(reponse.text)
        reslut = reponse.json()
        self.assertEqual(status, 200)
        self.assertEqual(reslut['code'], 100204)
        self.assertEqual(reslut['message'], "输入密码错误次数过多，账号暂时锁定，请30min再来登录")
        red.hdel("liwanle1i_password", 'num')

    def test_log_error_bigtime(self):
        red = redis.Redis(host='localhost', port=6379, db=0)
        red.hset("liwanle1i_password", 'num', '1')
        red.hset("liwanle1i_password", 'time', "2021-10-17 22:16:57")
        self.parame['password'] = '2222222222'
        reponse = requests.post(self.url, json=self.parame)

        status = reponse.status_code
        print(reponse.text)
        reslut = reponse.json()
        print(reslut)
        self.assertEqual(status, 200)
        self.assertEqual(reslut['message'], "密码错误")
        red.hdel("liwanle1i_password", 'time')

    def test_log_error_bigtime_success(self):
        red = redis.Redis(host='localhost', port=6379, db=0)
        red.hset("liwanle1i_password", 'num', '1')
        red.hset("liwanle1i_password", 'time', "2021-10-17 22:16:57")
        reponse = requests.post(self.url, json=self.parame)

        status = reponse.status_code
        print(reponse.text)
        reslut = reponse.json()
        print(reslut)
        self.assertEqual(status, 200)
        self.assertEqual(reslut['message'], "成功")
        red.hdel("liwanle1i_password", 'time')
        red.hdel("liwanle1i_password", 'num')


if __name__ == "__main__":
    unittest.main()
