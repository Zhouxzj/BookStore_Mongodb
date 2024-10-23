import unittest
from flask import Flask
from be.view.buyer import bp_buyer
from be.model.buyer import Buyer

class BuyerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(bp_buyer)
        self.client = self.app.test_client()
        self.buyer_model = Buyer()

        # 创建测试数据
        self.user_id = "test_buyer"
        self.password = "test_password"
        self.store_id = "test_store"
        self.buyer_model.add_funds(self.user_id, self.password, 10000)

    def tearDown(self):
        # 清理测试数据
        pass

    # 测试下单
    def test_new_order(self):
        response = self.client.post("/buyer/new_order", json={
            "user_id": self.user_id,
            "store_id": self.store_id,
            "books": [{"id": "book1", "count": 1}]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("order_id", response.json)

    # 测试付款
    def test_payment(self):
        order_response = self.client.post("/buyer/new_order", json={
            "user_id": self.user_id,
            "store_id": self.store_id,
            "books": [{"id": "book1", "count": 1}]
        })
        order_id = order_response.json["order_id"]

        payment_response = self.client.post("/buyer/payment", json={
            "user_id": self.user_id,
            "order_id": order_id,
            "password": self.password
        })
        self.assertEqual(payment_response.status_code, 200)

    # 测试充值
    def test_add_funds(self):
        response = self.client.post("/buyer/add_funds", json={
            "user_id": self.user_id,
            "password": self.password,
            "add_value": 5000
        })
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
