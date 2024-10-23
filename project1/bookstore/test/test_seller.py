import unittest
from flask import Flask
from be.view.seller import bp_seller  # 确保这个路径与项目的 view 结构匹配
from be.model.user import User  # 假设有用户模块进行测试数据准备
from be.model.seller import Seller  # 假设有卖家模块进行测试数据准备

class SellerTestCase(unittest.TestCase):
    def setUp(self):
        # 创建一个 Flask 应用并注册 seller 蓝图
        self.app = Flask(__name__)
        self.app.register_blueprint(bp_seller)
        self.client = self.app.test_client()

        # 创建用户和商店用于测试
        self.user_model = User()
        self.seller_model = Seller()

        # 注册测试用户并创建商店
        self.user_id = "test_user"
        self.password = "test_password"
        self.store_id = "test_store"
        self.user_model.register(self.user_id, self.password)
        self.seller_model.create_store(self.user_id, self.store_id)

    def tearDown(self):
        # 注销用户并删除商店，清理数据
        self.seller_model.delete_store(self.user_id, self.store_id)  # 假设有删除商店的功能
        self.user_model.unregister(self.user_id, self.password)

    # 测试创建商店的接口
    def test_create_store(self):
        # 测试成功创建商店
        response = self.client.post("/seller/create_store", json={
            "user_id": "test_user",
            "store_id": "new_test_store"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)  # 检查返回的 JSON 是否为 None
        self.assertEqual(response.json["message"], "ok")

        # 测试商店已存在的情况
        response = self.client.post("/seller/create_store", json={
            "user_id": "test_user",
            "store_id": "test_store"  # 已存在的 store_id
        })
        self.assertEqual(response.status_code, 514)
        self.assertIn("exist store id", response.json["message"])

        # 测试用户不存在的情况
        response = self.client.post("/seller/create_store", json={
            "user_id": "nonexistent_user",
            "store_id": "new_store"
        })
        self.assertEqual(response.status_code, 511)
        self.assertIn("non exist user id", response.json["message"])

    # 测试添加书籍的接口
    def test_add_book(self):
        # 测试成功添加书籍
        response = self.client.post("/seller/add_book", json={
            "user_id": "test_user",
            "store_id": "test_store",
            "book_info": {
                "id": "book1",
                "title": "Test Book",
                "author": "Author"
            },
            "stock_level": 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "ok")

        # 测试书籍已存在的情况
        response = self.client.post("/seller/add_book", json={
            "user_id": "test_user",
            "store_id": "test_store",
            "book_info": {
                "id": "book1",  # 已存在的 book_id
                "title": "Duplicate Book",
                "author": "Author"
            },
            "stock_level": 10
        })
        self.assertEqual(response.status_code, 516)
        self.assertIn("exist book id", response.json["message"])

    # 测试增加库存的接口
    def test_add_stock_level(self):
        # 测试成功增加库存
        response = self.client.post("/seller/add_stock_level", json={
            "user_id": "test_user",
            "store_id": "test_store",
            "book_id": "book1",
            "add_stock_level": 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "ok")

        # 测试书籍不存在的情况
        response = self.client.post("/seller/add_stock_level", json={
            "user_id": "test_user",
            "store_id": "test_store",
            "book_id": "nonexistent_book",
            "add_stock_level": 5
        })
        self.assertEqual(response.status_code, 515)
        self.assertIn("non exist book id", response.json["message"])


if __name__ == "__main__":
    unittest.main()
