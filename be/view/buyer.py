import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from be.model.buyer import Buyer

from flask import Blueprint, request, jsonify
from be.model import store  # 新增导入 store 模块

bp_buyer = Blueprint("buyer", __name__, url_prefix="/buyer")

# 买家下单
@bp_buyer.route("/new_order", methods=["POST"])
def new_order():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    books: list = request.json.get("books")  # 确保 books 是一个列表
    if not user_id or not store_id or not books:
        return jsonify({"message": "Missing user_id, store_id, or books"}), 400

    id_and_count = []
    for book in books:
        book_id = book.get("id")
        count = book.get("count")
        if not book_id or count is None:  # 进一步检查 book_id 和 count 是否为空
            return jsonify({"message": "Invalid book format"}), 400
        id_and_count.append((book_id, count))

    b = Buyer()
    code, message, order_id = b.new_order(user_id, store_id, id_and_count)
    return jsonify({"message": message, "order_id": order_id}), code


# 买家付款
@bp_buyer.route("/payment", methods=["POST"])
def payment():
    user_id: str = request.json.get("user_id")
    order_id: str = request.json.get("order_id")
    password: str = request.json.get("password")
    if not user_id or not order_id or not password:
        return jsonify({"message": "Missing user_id, order_id, or password"}), 400

    b = Buyer()
    code, message = b.payment(user_id, order_id, password)
    return jsonify({"message": message}), code


# 买家充值
@bp_buyer.route("/add_funds", methods=["POST"])
def add_funds():
    user_id = request.json.get("user_id")
    password = request.json.get("password")
    add_value = request.json.get("add_value")
    if not user_id or not password or add_value is None:
        return jsonify({"message": "Missing user_id, password, or add_value"}), 400

    b = Buyer()
    code, message = b.add_funds(user_id, password, add_value)
    return jsonify({"message": message}), code

# 新增的图书搜索接口（实现分页搜索）
@bp_buyer.route("/search_books", methods=["GET"])
def search_books():
    keyword = request.args.get("keyword", "")
    store_id = request.args.get("store_id")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    
    s = store.Store("")
    search_results = s.search_books(keyword, store_id, page, per_page)
    return jsonify(search_results)