#接口实现,负责处理用户相关的 HTTP 请求，并将请求传递到 model/user.py 进行业务逻辑的处理。
from flask import Blueprint, request, jsonify
from be.model import user

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


# 用户登录
@bp_auth.route("/login", methods=["POST"])
def login():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    terminal = request.json.get("terminal", "")
    u = user.User()
    code, message, token = u.login(user_id=user_id, password=password, terminal=terminal)

    if code == 200:
        return jsonify({"message": message, "token": token}), 200
    else:
        return jsonify({"message": message}), code


# 用户登出
@bp_auth.route("/logout", methods=["POST"])
def logout():
    user_id = request.json.get("user_id", "")
    token = request.headers.get("token")

    if not token:
        return jsonify({"message": "Missing token in headers"}), 400

    u = user.User()
    code, message = u.logout(user_id=user_id, token=token)

    return jsonify({"message": message}), code


# 用户注册
@bp_auth.route("/register", methods=["POST"])
def register():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    u = user.User()
    code, message = u.register(user_id=user_id, password=password)

    return jsonify({"message": message}), code


# 注销用户
@bp_auth.route("/unregister", methods=["POST"])
def unregister():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    token = request.headers.get("token")

    if not token:
        return jsonify({"message": "Missing token in headers"}), 400

    u = user.User()
    # 先检查 token，再执行注销操作
    code, token_message = u.check_token(user_id, token)
    if code != 200:
        return jsonify({"message": token_message}), code

    # 执行注销操作
    code, message = u.unregister(user_id=user_id, password=password)
    return jsonify({"message": message}), code


# 修改密码
@bp_auth.route("/password", methods=["POST"])
def change_password():
    user_id = request.json.get("user_id", "")
    old_password = request.json.get("oldPassword", "")
    new_password = request.json.get("newPassword", "")
    token = request.headers.get("token")

    if not token:
        return jsonify({"message": "Missing token in headers"}), 400

    u = user.User()
    # 检查 token 是否有效
    code, token_message = u.check_token(user_id, token)
    if code != 200:
        return jsonify({"message": token_message}), code

    # 执行密码修改操作
    code, message = u.change_password(
        user_id=user_id, old_password=old_password, new_password=new_password
    )
    return jsonify({"message": message}), code


def dispatch_order(self, store_id, order_id):
    # 查找商店并检查是否存在
    shop = self.shops_collection.find_one({"store_id": store_id})
    if not shop:
        return error.error_non_exist_store_id(store_id)

    # 查找商店的订单并确认状态是否为 "paid"
    order_found = False
    for order in shop.get("orders", []):
        if order["order_id"] == order_id:
            if order["state"] == "paid":
                # 更新商店订单状态为 "delivered"
                self.shops_collection.update_one(
                    {"store_id": store_id, "orders.order_id": order_id},
                    {"$set": {"orders.$.state": "delivered"}}
                )
                order_found = True
                break
            else:
                return error.error_invalid_order_state(order_id, order["state"])

    if not order_found:
        return error.error_invalid_order_id(order_id)

    # 同步更新用户订单状态为 "delivered"
    user_id = order["user_id"]
    user = self.users_collection.find_one({"user_id": user_id})
    if user:
        self.users_collection.update_one(
            {"user_id": user_id, "orders.order_id": order_id},
            {"$set": {"orders.$.state": "delivered"}}
        )
    else:
        return error.error_non_exist_user_id(user_id)

    return {"success": "Order dispatched"}
