import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from be.model import store
from model import store
from pymongo import MongoClient, TEXT

class DBConn:
    def __init__(self):
        self.db = self.get_db()
        self.create_indexes()  # 创建所需索引

    def get_db(self):
        #########这里要改成我们自己的数据库###############
        client = MongoClient("mongodb://localhost:27017/")
        return client["your_database_name"]  # 替换为你的数据库名称
         #########这里要改成我们自己的数据库###############

    def create_indexes(self):
        """
        创建索引，包括唯一索引、复合索引和全文索引。
        """
        # 创建 isbn 的唯一索引
        self.db.books.create_index("isbn", unique=True, name="isbn_unique_index")

        # 创建作者和书名的复合索引
        self.db.books.create_index(
            [("author", 1), ("title", 1)], name="author_title_compound_index"
        )

        # 创建全文索引以支持关键字搜索（如需支持标题和内容搜索）
        self.db.books.create_index(
            [("title", TEXT), ("author", TEXT)],
            name="books_text_index"
        )

    def user_id_exist(self, user_id):
        return self.db.users.find_one({"user_id": user_id}) is not None

    def book_id_exist(self, store_id, isbn):
        return self.db.shops.find_one({"store_id": store_id, "books.isbn": isbn}) is not None

    def store_id_exist(self, store_id):
        return self.db.store.find_one({"store_id": store_id}) is not None