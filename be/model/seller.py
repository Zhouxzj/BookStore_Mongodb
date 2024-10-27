import sqlite3 as sqlite
from be.model import error
from be.model import db_conn

#负责与数据库交互，实现业务逻辑
class Seller(db_conn.DBConn):
    def __init__(self):
        super().__init__()

    # 创建商铺的方法
    def create_store(self, user_id: str, store_id: str):
        try:
            # 检查用户是否存在
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            
            # 检查商铺是否已经存在
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            # 如果检查通过，创建新商铺
            self.conn.execute(
                "INSERT INTO user_store (store_id, user_id) VALUES (?, ?)",
                (store_id, user_id)
            )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        except Exception as e:
            return 530, f"Unknown Error: {str(e)}"
        return 200, "ok"

    # 添加书籍到商铺
    def add_book(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        book_json_str: str,
        stock_level: int,
    ):
        try:
            # 检查用户、商铺和书籍是否存在
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            # 添加书籍到商铺
            self.conn.execute(
                "INSERT INTO store (store_id, book_id, book_info, stock_level) "
                "VALUES (?, ?, ?, ?)",
                (store_id, book_id, book_json_str, stock_level)
            )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        except Exception as e:
            return 530, f"Unknown Error: {str(e)}"
        return 200, "ok"

    # 增加库存的逻辑
    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            # 检查用户、商铺和书籍是否存在
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            # 更新书籍库存
            self.conn.execute(
                "UPDATE store SET stock_level = stock_level + ? WHERE store_id = ? AND book_id = ?",
                (add_stock_level, store_id, book_id)
            )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, f"SQLite Error: {str(e)}"
        except Exception as e:
            return 530, f"Unknown Error: {str(e)}"
        return 200, "ok"
