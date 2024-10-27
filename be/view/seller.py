from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import seller
import json

#定义了用于卖家操作的 API 路由

bp_seller = Blueprint("seller", __name__, url_prefix="/seller")

#创建商铺接口 (/seller/create_store)：处理商铺的创建请求
@bp_seller.route("/create_store", methods=["POST"])
def seller_create_store():
    try:
        user_id: str = request.json.get("user_id")
        store_id: str = request.json.get("store_id")
        if not user_id or not store_id:
            return jsonify({"message": "user_id or store_id is missing"}), 400

        s = seller.Seller()
        code, message = s.create_store(user_id, store_id)
        return jsonify({"message": message}), code
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500

#添加书籍接口 (/seller/add_book)：处理书籍添加请求，接收书籍信息并调用 add_book 方法
@bp_seller.route("/add_book", methods=["POST"])
def seller_add_book():
    try:
        user_id: str = request.json.get("user_id")
        store_id: str = request.json.get("store_id")
        book_info: dict = request.json.get("book_info")
        stock_level = request.json.get("stock_level", 0)

        # 参数校验
        if not user_id or not store_id or not book_info:
            return jsonify({"message": "Missing required fields"}), 400

        s = seller.Seller()
        code, message = s.add_book(
            user_id, store_id, book_info.get("id"), json.dumps(book_info), int(stock_level)
        )
        return jsonify({"message": message}), code
    except ValueError:
        return jsonify({"message": "Invalid stock level value"}), 400
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500

#增加库存接口 (/seller/add_stock_level)：处理库存增加的请求
@bp_seller.route("/add_stock_level", methods=["POST"])
def add_stock_level():
    try:
        user_id: str = request.json.get("user_id")
        store_id: str = request.json.get("store_id")
        book_id: str = request.json.get("book_id")
        add_num = request.json.get("add_stock_level", 0)

        # 参数校验
        if not user_id or not store_id or not book_id:
            return jsonify({"message": "Missing required fields"}), 400

        s = seller.Seller()
        code, message = s.add_stock_level(user_id, store_id, book_id, int(add_num))
        return jsonify({"message": message}), code
    except ValueError:
        return jsonify({"message": "Invalid stock level value"}), 400
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500
    
#修改点总结：
#参数校验：在所有接口中，检查是否传递了必要的字段，并确保 stock_level 和 add_stock_level 是有效的整数值。
#异常处理：为每个接口添加了通用的异常处理逻辑，如果出现任何意外错误，都会返回服务器错误信息。
#统一的返回格式：所有接口的返回信息格式化为 {"message": message} 形式，确保一致性。