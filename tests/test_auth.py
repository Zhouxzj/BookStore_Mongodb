import unittest
from flask import Flask
from be.view.auth import bp_auth  # 确保路径与项目结构一致
from be.model.user import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # 设置 Flask 测试客户端
        self.app = Flask(__name__)
        self.app.register_blueprint(bp_auth)
        self.client = self.app.test_client()
        self.user_model = User()

        # 创建测试用户
        self.user_id = "test_user"
        self.password = "test_password"
        self.terminal = "test_terminal"
        self.user_model.register(self.user_id, self.password)

    def tearDown(self):
        # 清理测试用户（如果已经注销，就跳过这个步骤）
        try:
            self.user_model.unregister(self.user_id, self.password)
        except:
            pass  # 用户可能已经在测试过程中注销

    # 测试用户注册
    def test_register(self):
        response = self.client.post("/auth/register", json={
            "user_id": "new_user",
            "password": "new_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "ok")

    # 测试用户登录
    def test_login(self):
        response = self.client.post("/auth/login", json={
            "user_id": self.user_id,
            "password": self.password,
            "terminal": self.terminal
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)
        self.token = response.json["token"]

    # 测试登录失败（密码错误）
    def test_login_wrong_password(self):
        response = self.client.post("/auth/login", json={
            "user_id": self.user_id,
            "password": "wrong_password",
            "terminal": self.terminal
        })
        self.assertEqual(response.status_code, 521)  # 假设 521 是用户名或密码错误
        self.assertIn("message", response.json)

    # 测试用户登出
    def test_logout(self):
        # 首先需要登录获取 token
        login_response = self.client.post("/auth/login", json={
            "user_id": self.user_id,
            "password": self.password,
            "terminal": self.terminal
        })
        token = login_response.json["token"]

        # 测试登出
        response = self.client.post("/auth/logout", json={
            "user_id": self.user_id,
        }, headers={"token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "ok")

    # 测试用户注销
    def test_unregister(self):
        # 登录获取 token
        login_response = self.client.post("/auth/login", json={
            "user_id": self.user_id,
            "password": self.password,
            "terminal": self.terminal
        })
        token = login_response.json["token"]

        # 测试注销用户
        response = self.client.post("/auth/unregister", json={
            "user_id": self.user_id,
            "password": self.password
        }, headers={"token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "ok")

    # 测试修改密码
    def test_change_password(self):
        # 登录获取 token
        login_response = self.client.post("/auth/login", json={
            "user_id": self.user_id,
            "password": self.password,
            "terminal": self.terminal
        })
        token = login_response.json["token"]

        # 测试修改密码
        response = self.client.post("/auth/password", json={
            "user_id": self.user_id,
            "oldPassword": self.password,
            "newPassword": "new_password"
        }, headers={"token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "ok")

        # 验证修改后的密码登录
        new_login_response = self.client.post("/auth/login", json={
            "user_id": self.user_id,
            "password": "new_password",
            "terminal": self.terminal
        })
        self.assertEqual(new_login_response.status_code, 200)
        self.assertIn("token", new_login_response.json)

    # 测试修改密码失败（旧密码错误）
    def test_change_password_wrong_old_password(self):
        # 登录获取 token
        login_response = self.client.post("/auth/login", json={
            "user_id": self.user_id,
            "password": self.password,
            "terminal": self.terminal
        })
        token = login_response.json["token"]

        # 测试修改密码，旧密码错误
        response = self.client.post("/auth/password", json={
            "user_id": self.user_id,
            "oldPassword": "wrong_password",  # 错误的旧密码
            "newPassword": "new_password"
        }, headers={"token": token})
        self.assertEqual(response.status_code, 520)  # 假设 520 是密码错误的状态码
        self.assertIn("message", response.json)


if __name__ == "__main__":
    unittest.main()
