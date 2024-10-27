import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from be.model import user, store

#接口实现,负责处理用户相关的 HTTP 请求，并将请求传递到 model/user.py 进行业务逻辑的处理。
from flask import Blueprint, request, jsonify

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


# 新增的图书搜索接口(分页查询)
@bp_auth.route("/search_books", methods=["GET"])
def search_books():
    keyword = request.args.get("keyword", "")
    store_id = request.args.get("store_id")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    
    s = store.Store("")
    search_results = s.search_books(keyword, store_id, page, per_page)
    return jsonify(search_results)
