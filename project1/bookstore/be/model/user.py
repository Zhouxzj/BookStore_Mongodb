#编写用户注册、登录、登出等具体的业务逻辑，并与数据库交互，确保用户数据的完整性。
import jwt
import time
import logging
import sqlite3 as sqlite
from be.model import error
from be.model import db_conn

# JWT 解码
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded

class User(db_conn.DBConn):
    token_lifetime: int = 3600  # Token lifetime in seconds (1 hour)

    def __init__(self):
        super().__init__()

    # 检查 token 是否有效
    # 修改 check_token 方法的返回类型
    def check_token(self, user_id: str, token: str) -> tuple[int, str]:
        try:
            cursor = self.conn.execute(
                "SELECT token FROM user WHERE user_id = ?", (user_id,)
            )
            db_token = cursor.fetchone()
            if db_token is None or not self.__check_token(user_id, db_token[0], token):
                return error.error_authorization_fail()
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        return 200, "ok"

    # 私有方法：内部检查 token 逻辑
    def __check_token(self, user_id: str, db_token: str, token: str) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
        return False

    # 检查密码的方法，减少代码重复
    # 修改 check_password 方法的返回类型
    def check_password(self, user_id: str, password: str) -> tuple[int, str]:
        try:
            cursor = self.conn.execute(
                "SELECT password FROM user WHERE user_id = ?", (user_id,)
            )
            stored_password = cursor.fetchone()
            if stored_password is None:
                return error.error_non_exist_user_id(user_id)
            if stored_password[0] != password:
                return error.error_invalid_password(user_id)
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        return 200, "ok"

    # 用户注册
    def register(self, user_id: str, password: str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            self.conn.execute(
                "INSERT INTO user(user_id, password, balance, token, terminal) "
                "VALUES (?, ?, ?, ?, ?);",
                (user_id, password, 0, token, terminal),
            )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        return 200, "ok"

    # 用户注销
    def unregister(self, user_id: str, password: str):
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            cursor = self.conn.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
            if cursor.rowcount == 1:
                self.conn.commit()
            else:
                return error.error_authorization_fail()
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        return 200, "ok"

    # 用户登录
    def login(self, user_id: str, password: str, terminal: str):
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            token = jwt_encode(user_id, terminal)
            self.conn.execute(
                "UPDATE user SET token = ?, terminal = ? WHERE user_id = ?",
                (token, terminal, user_id),
            )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        return 200, "ok", token

    # 修改密码
    def change_password(self, user_id: str, old_password: str, new_password: str):
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            cursor = self.conn.execute(
                "UPDATE user SET password = ?, token= ?, terminal = ? WHERE user_id = ?",
                (new_password, token, terminal, user_id),
            )
            if cursor.rowcount == 0:
                return error.error_authorization_fail()

            self.conn.commit()
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        return 200, "ok"

    # 用户登出
    def logout(self, user_id: str, token: str):
        try:
            cursor = self.conn.execute(
                "SELECT token FROM user WHERE user_id = ?", (user_id,)
            )
            stored_token = cursor.fetchone()
            if stored_token is None or stored_token[0] != token:
                return error.error_authorization_fail()

            self.conn.execute("UPDATE user SET token = NULL WHERE user_id = ?", (user_id,))
            self.conn.commit()
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        return 200, "ok"

    def confirm_receipt(self, user_id, order_id, store_id):
        # 查找用户并检查是否存在
        user = self.users_collection.find_one({"user_id": user_id})
        if not user:
            return error.error_non_exist_user_id(user_id)

        # 查找用户的订单并确认状态是否为 "delivered"
        order_found = False
        for order in user.get("orders", []):
            if order["order_id"] == order_id and order["store_id"] == store_id:
                if order["state"] == "delivered":
                    # 更新用户订单状态为 "received"
                    self.users_collection.update_one(
                        {"user_id": user_id, "orders.order_id": order_id},
                        {"$set": {"orders.$.state": "received"}}
                    )
                    order_found = True
                    break
                else:
                    return error.error_invalid_order_state(order_id, order["state"])

        if not order_found:
            return error.error_invalid_order_id(order_id)

        # 同步更新商店订单状态为 "received"
        shop = self.shops_collection.find_one({"store_id": store_id})
        if shop:
            self.shops_collection.update_one(
                {"store_id": store_id, "orders.order_id": order_id},
                {"$set": {"orders.$.state": "received"}}
            )
        else:
            return error.error_non_exist_store_id(store_id)

        return {"success": "Order confirmed as received"}
