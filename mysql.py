#! /usr/bin/env python
# coding=utf-8
import mysql.connector
from config import cfg
from logger import get_debug_logger


class MySQL:
    def __init__(self):
        self.mydb = None
        self.cursor = None
        self.mysqlM_logger = get_debug_logger('sql', f'logs/mysql.log')
        self.connect_db()

    def connect_db(self):
        try:
            self.mydb = mysql.connector.connect(
                host=cfg.mysql.host,
                user=cfg.mysql.user,
                password=cfg.mysql.password,
                database=cfg.mysql.database
            )
            self.cursor = self.mydb.cursor()
        except mysql.connector.Error as e:
            self.mysqlM_logger.error(f'Failed to connect to DB | Error: {e}')

    def query(self, sql_query, values):
        self.mysqlM_logger.info(f"Executing query: {sql_query} | Values: {values}")
        try:
            self.cursor.execute(sql_query, values)
            self.mydb.commit()
            ID = self.cursor.lastrowid
            return ID
        except mysql.connector.Error as e:
            self.mysqlM_logger.error(f'Query Failed | {sql_query} | Error: {e}')
            if not self.mydb.is_connected():
                self.reconnect()

    def fetch_data(self, sql_query, values=None):
        self.mysqlM_logger.info(f"Executing query: {sql_query} | Values: {values}")
        try:
            self.cursor.execute(sql_query, values)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            self.mysqlM_logger.error(f'Fetch Failed | {sql_query} | Error: {e}')
            self.reconnect()

    def reconnect(self):
        self.close()
        self.connect_db()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.mydb and self.mydb.is_connected():
            self.mydb.close()


if __name__ == "__main__":
    mysql_ = MySQL()
    # sample queries
    # id = '2'
    # sql = "SELECT name FROM part WHERE id = %s"
    # ret = mysql_.fetch_data(sql, (job_id,))
    # out = ret[0][0]

