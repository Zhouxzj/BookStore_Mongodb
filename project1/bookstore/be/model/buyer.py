from pymongo import MongoClient, errors
import uuid
import json
import logging
from datetime import datetime
from be.model import db_conn
from be.model import error
import traceback


class Buyer(db_conn.DBConn):
    def __init__(self):
        super().__init__()
        self.store_col = self.get_store_col()
        self.user_col = self.get_user_col()
        self.book_col = self.get_book_col()

    def new_order(
        self, user_id: str, store_id: str, id_and_count: [(str, int)]
    ) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            for book_id, count in id_and_count:
                store_data = list(self.store_col.find(
                    {"store_id": store_id, "books": {"$elemMatch": {"book_id": book_id}}},
                    {"books.$": 1}
                ))
                if not store_data or not store_data[0].get("books"):
                    return error.error_non_exist_book_id(book_id) + (order_id,)

                book_data  = store_data[0]["books"][0]
                stock_level = book_data.get("num", 0)

                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                self.store_col.update_one(
                    {"store_id": store_id, "books.book_id": book_id},
                    {"$inc": {"books.$.num": -count}}
                )

                updated_store_data = self.store_col.find_one(
                    {"store_id": store_id, "books.book_id": book_id},
                    {"books.$": 1}
                )

                if not updated_store_data or updated_store_data['books'][0]['num'] < 0:
                    return error.error_stock_level_low(book_id) + (order_id,)

                price_data = self.book_col.find_one(
                    {"book_id": book_id},
                    {"price": 1, "_id": 0}
                )
                price = price_data['price'] if price_data else 0
                user = self.user_col.find_one({"user_id": user_id})
                if user is None:
                    return error.error_non_exist_user_id(user_id) + (order_id,)
                address = user.get("address", "")
                order_data_u = {
                    "order_id": uid,
                    "store_id": store_id,
                    "book_id": book_id,
                    "num": count,
                    "state": "ordered",
                    "address": address,
                }
                self.user_col.update_one(
                    {"user_id": user_id},
                    {"$push": {"order": order_data_u}}
                )

                order_time = datetime.now().isoformat()
                order_data_s = {
                    "order_id": uid,
                    "user_id": user_id,
                    "book_id": book_id,
                    "count": count,
                    "address": address,
                    "state": "ordered",
                    "order_time": order_time
                }
                self.store_col.update_one(
                    {"store_id": store_id},
                    {"$push": {"order": order_data_s}}
                )
            order_id = uid

        except errors.PyMongoError as e:
            print("Error Type:", type(e))
            print("Traceback:", traceback.format_exc())
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            print("Error Type:", type(e))
            print("Traceback:", traceback.format_exc())
            return 530, "{}".format(str(e)), ""
        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            order_info = self.store_col.find_one(
                {"order.order_id": order_id},
                {"order": {"$elemMatch":{"order_id": order_id}}}
            )
            buyer = order_info["order"][0]["user_id"]
            if buyer != user_id:
                return  error.error_authorization_fail()

            user = self.user_col.find_one({"user_id": user_id})
            if user is None:
                return error.error_non_exist_user_id(user_id)
            if password != user.get("passwd"):
                return error.error_authorization_fail()

            order_buyer = self.user_col.find_one({"user_id": user_id, "order.order_id": order_id})
            if order_buyer is None:
                return error.error_invalid_order_id(order_id)

            store_data = self.user_col.aggregate([
                {"$unwind": "$order"},
                {"$match": {"order.order_id": order_id}},
                {"$project": {"store_id": 1}}
            ])

            if not store_data:
                return error.error_invalid_order_id(order_id)
            print("3")
            store_id = store_data[0]["store_id"]
            store = self.store_col.find_one({"store_id": store_id})
            if store is None:
                return error.error_non_exist_store_id(store_id)

            seller_id = store["user_id"]

            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            order_book_info = list(self.user_col.aggregate([
                {"$unwind": "$order"},
                {"$match": {"order.order_id": order_id}},
                {"$project": {"num": "$order.num", "book_id": "$order.book_id"}}
            ]))

            if not order_book_info:
                return error.error_invalid_order_id(order_id)
            order_num = order_book_info[0]["num"]
            order_book_id = order_book_info[0]["book_id"]

            price_data = self.book_col.find_one({"book_id": order_book_id}, {"price": 1, "_id": 0})
            if price_data is None:
                return  error.error_non_exist_book_id(order_book_id)

            price = price_data["price"]
            total_price = int(price) * int(order_num)

            if user["account"] < total_price:
                return error.error_not_sufficient_funds(order_id)

            self.user_col.update_one(
                {"user_id": user_id},
                {"$inc": {"account": -total_price}}
            )
            self.user_col.update_one(
                {"user_id": user_id,"order.order_id": order_id},
                {"$set": {"order.$.state": "paid"}}
            )
            self.user_col.update_one(
                {"user_id": seller_id},
                {"$inc": {"account": total_price}}
            )
            self.store_col.update_one(
                {"user_id": seller_id, "order.order_id": order_id},
                {"$set": {"order.$.state": "paid"}}
            )

        except errors.PyMongoError as e:
            print("Error Type:", type(e))
            print("Traceback:", traceback.format_exc())
            return 528, "{}".format(str(e))
        except BaseException as e:
            print("Error Type:", type(e))
            print("Traceback:", traceback.format_exc())
            return 530, "{}".format(str(e))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            user = self.user_col.find_one({"user_id": user_id})
            if user is None:
                return error.error_non_exist_user_id(user_id)

            if password != user.get("passwd"):
                return error.error_authorization_fail(user_id)

            self.user_col.update_one(
                {"user_id": user_id},
                {"$inc": {"account": add_value}}
            )
        except errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    # 新增的搜索功能代码
    def search_books(self, keyword, store_id=None, page=1, per_page=10):
        """
        搜索书籍，支持分页查询
        :param keyword: 搜索关键字
        :param store_id: 可选的商店ID，如果提供则限制在该商店内搜索
        :param page: 当前页码
        :param per_page: 每页显示的书籍数量
        :return: 包含结果列表和分页信息的字典
        """
        query = {"$text": {"$search": keyword}}  # 使用全文索引进行关键字搜索

        if store_id:
            query["store_id"] = store_id  # 如果提供 store_id，则只搜索该商店的书籍

        # 查询并进行分页
        cursor = self.book_col.find(query).skip((page - 1) * per_page).limit(per_page)
        total_count = self.book_col.count_documents(query)  # 计算总匹配书籍数量

        results = list(cursor)

        if total_count == 0:
            return error.error_no_books_found(keyword)  # 返回错误信息

        # 返回搜索结果和分页信息
        return {
            "results": [{"book_id": book.get("book_id"), "title": book.get("title"), "author": book.get("author")} for
                        book in results],
            "total_count": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page  # 计算总页数
        }

    def receive(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            # 查找用户并验证
            user = self.user_col.find_one({"user_id": user_id})
            if user is None:
                return error.error_non_exist_user_id(user_id)

            if user.get("passwd") != password:
                return error.error_authorization_fail()

            # 检查订单是否存在于用户的订单列表中
            order_data = self.user_col.find_one(
                {"user_id": user_id, "order.order_id": order_id},
                {"order.$": 1}
            )
            if not order_data or not order_data.get("order"):
                return error.error_invalid_order_id(order_id)

            # 更新订单状态为 "received"
            self.user_col.update_one(
                {"user_id": user_id, "order.order_id": order_id},
                {"$set": {"order.$.state": "received"}}
            )

        except errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"
