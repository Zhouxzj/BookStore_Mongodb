import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from be.model import error

import logging
import os
import sqlite3 as sqlite
import threading




class Store:
    database: str

    def __init__(self, db_path):
        self.database = os.path.join(db_path, "be.db")
        self.init_tables()

    def init_tables(self):
        try:
            conn = self.get_db_conn()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS user ("
                "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
                "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS user_store("
                "user_id TEXT, store_id, PRIMARY KEY(user_id, store_id));"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS store( "
                "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
                " PRIMARY KEY(store_id, book_id))"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order( "
                "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT)"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order_detail( "
                "order_id TEXT, book_id TEXT, count INTEGER, price INTEGER,  "
                "PRIMARY KEY(order_id, book_id))"
            )

            conn.commit()
        except sqlite.Error as e:
            logging.error(e)
            conn.rollback()

    def get_db_conn(self) -> sqlite.Connection:
        return sqlite.connect(self.database)
    
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
        query = "SELECT book_id, book_info FROM store WHERE book_info LIKE ?"
        params = [f"%{keyword}%"]
        
        if store_id:
            query += " AND store_id = ?"
            params.append(store_id)
        
        query += " LIMIT ? OFFSET ?"
        params.extend([per_page, (page - 1) * per_page])

        conn = self.get_db_conn()
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        
        # 计算总数以便于分页
        count_query = "SELECT COUNT(*) FROM store WHERE book_info LIKE ?"
        count_params = [f"%{keyword}%"]
        if store_id:
            count_query += " AND store_id = ?"
            count_params.append(store_id)
        
        cursor.execute(count_query, tuple(count_params))
        total_count = cursor.fetchone()[0]
        
        if total_count == 0:
            return error.error_no_books_found(keyword)
        
        return {
            "results": [{"book_id": row[0], "book_info": row[1]} for row in results],
            "total_count": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }


database_instance: Store = None
# global variable for database sync
init_completed_event = threading.Event()


def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()
