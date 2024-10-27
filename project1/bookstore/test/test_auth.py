import unittest
from flask import Flask
from be.view.auth import bp_auth  # 确保路径与项目结构一致
from be.model.user import User
from pymongo import MongoClient

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


class TestOrderFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 初始化 MongoDB 连接和测试数据
        cls.client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.client['bookstore']
        cls.users_collection = cls.db['users']
        cls.shops_collection = cls.db['shops']

        # 插入测试数据
        cls.user_id = "test_user"
        cls.store_id = "test_store"
        cls.order_id = "test_order"

        cls.users_collection.insert_one({
            "user_id": cls.user_id,
            "orders": [{"order_id": cls.order_id, "store_id": cls.store_id, "state": "paid"}]
        })
        cls.shops_collection.insert_one({
            "store_id": cls.store_id,
            "orders": [{"order_id": cls.order_id, "user_id": cls.user_id, "state": "paid"}]
        })

        cls.user = User()
        cls.auth = Auth()

    def test_dispatch_order_success(self):
        # 测试发货成功
        response = self.auth.dispatch_order(self.store_id, self.order_id)
        self.assertEqual(response, {"success": "Order dispatched"})

        # 验证用户和商店中的订单状态是否已更新为 "delivered"
        user_order = self.users_collection.find_one({"user_id": self.user_id, "orders.order_id": self.order_id})
        shop_order = self.shops_collection.find_one({"store_id": self.store_id, "orders.order_id": self.order_id})

        self.assertEqual(user_order['orders'][0]['state'], "delivered")
        self.assertEqual(shop_order['orders'][0]['state'], "delivered")

    def test_dispatch_order_invalid_state(self):
        # 设置订单状态为 "delivered" 以触发无效状态错误
        self.shops_collection.update_one(
            {"store_id": self.store_id, "orders.order_id": self.order_id},
            {"$set": {"orders.$.state": "delivered"}}
        )

        # 测试无效状态下的发货
        with self.assertRaises(Exception) as context:
            self.auth.dispatch_order(self.store_id, self.order_id)
        self.assertEqual(context.exception.args[0], error.error_invalid_order_state(self.order_id, "delivered"))

    def test_confirm_receipt_success(self):
        # 设置订单状态为 "delivered" 以便测试收货
        self.users_collection.update_one(
            {"user_id": self.user_id, "orders.order_id": self.order_id},
            {"$set": {"orders.$.state": "delivered"}}
        )
        self.shops_collection.update_one(
            {"store_id": self.store_id, "orders.order_id": self.order_id},
            {"$set": {"orders.$.state": "delivered"}}
        )

        # 测试收货成功
        response = self.user.confirm_receipt(self.user_id, self.order_id, self.store_id)
        self.assertEqual(response, {"success": "Order confirmed as received"})

        # 验证用户和商店中的订单状态是否已更新为 "received"
        user_order = self.users_collection.find_one({"user_id": self.user_id, "orders.order_id": self.order_id})
        shop_order = self.shops_collection.find_one({"store_id": self.store_id, "orders.order_id": self.order_id})

        self.assertEqual(user_order['orders'][0]['state'], "received")
        self.assertEqual(shop_order['orders'][0]['state'], "received")

    def test_confirm_receipt_invalid_state(self):
        # 设置订单状态为 "paid" 以触发无效状态错误
        self.users_collection.update_one(
            {"user_id": self.user_id, "orders.order_id": self.order_id},
            {"$set": {"orders.$.state": "paid"}}
        )

        # 测试无效状态下的收货
        with self.assertRaises(Exception) as context:
            self.user.confirm_receipt(self.user_id, self.order_id, self.store_id)
        self.assertEqual(context.exception.args[0], error.error_invalid_order_state(self.order_id, "paid"))

    @classmethod
    def tearDownClass(cls):
        # 清理测试数据
        cls.users_collection.delete_many({"user_id": cls.user_id})
        cls.shops_collection.delete_many({"store_id": cls.store_id})
        cls.client.close()

if __name__ == "__main__":
    unittest.main()
