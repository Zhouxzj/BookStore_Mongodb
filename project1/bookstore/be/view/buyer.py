from flask import Blueprint
from flask import request
from flask import jsonify
from be.model.buyer import Buyer

bp_buyer = Blueprint("buyer", __name__, url_prefix="/buyer")

@bp_buyer.route("/new_order", methods=["POST"])
def new_order():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    books: [] = request.json.get("books")
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


@bp_buyer.route("/payment", methods=["POST"])
def payment():
    user_id: str = request.json.get("user_id")
    order_id: str = request.json.get("order_id")
    password: str = request.json.get("password")
    if not user_id or not order_id or not password:
        return jsonify({"message": "Missing user_id, order_id, or password"}), 400

    b = Buyer()
    code, message = b.payment(user_id, password, order_id)
    return jsonify({"message": message}), code


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
