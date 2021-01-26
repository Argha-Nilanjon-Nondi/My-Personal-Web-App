import os
import datetime
from sqlite_easy import easy as sql
from utility import user_single,BASE_DIR,users_dir,if_alreay_exist
from block_chain.block import Block
import random

class Certificate:
    def __init__(self, database):
        self.database = database

    def input_data(self, img_name, url):
        self.img_name = img_name
        self.url = r"""{0}""".format(url)

        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)

        code = "SELECT no FROM certificate ORDER BY no DESC LIMIT 1;"

        no = sql.sqlite_run("certificate", code)
        if (len(no) == 0):
            no = "1"
        else:
            no = str(no[0][0] + 1)

        try:
            sql.db_insert("certificate", "certificate", [["url", self.url], ["img_name", self.img_name], ["no", no]])
            return "true"
        except Exception as a:
            return "false"

    def delete(self, no):

        self.no = tuple([int(no)])

        code = "SELECT no FROM certificate;"

        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)

        record = sql.sqlite_run("certificate", code)

        if (self.no in record):

            sql.row_delet("certificate", "certificate", "no", str((self.no)[0]))
            return "true"
        else:
            return "false"

    @property
    def show_data(self):
        data = []
        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)
        code = """Select url,img_name,no from certificate;"""
        record = sql.sqlite_run("certificate", code)
        record.reverse()
        for i in record:
            data.append([i[0], i[1], i[2]])

        return data


# obj=Certificate("158624666524")
# obj.input_data("hello.png","http//5869.889;png")
# obj.delete(2)