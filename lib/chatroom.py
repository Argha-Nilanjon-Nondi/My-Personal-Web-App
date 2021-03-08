import os
import datetime
from sqlite_easy import easy as sql
from utility import user_single,BASE_DIR,users_dir,if_alreay_exist
from block_chain.block import Block
import random

class ChatRoom:

    def __init__(self, own, other):
        self.me = own
        self.other = other

    def tuple_list(self, data):
        list_record = []
        for i in data:
            list_record.append(list(i))
        return list_record

    def show_list(self):
        """
			gives the list of users including username and dbid
			"""
        code = """SELECT username,dbid FROM user """;
        os.chdir(BASE_DIR)
        record = sql.sqlite_run("users", code)
        return self.tuple_list(record)

    def show_msg(self):

        limit_no = "90"  # limit of msg
        code1 = """SELECT time,msg FROM chatroom WHERE dbid = '{0}' Limit {1}""".format(self.me, limit_no)
        user_dir_single = user_single(self.other)
        os.chdir(user_dir_single)
        record1 = sql.sqlite_run("chatroom", code1)
        user_dir_single = user_single(self.me)
        os.chdir(user_dir_single)
        code2 = """SELECT time,msg FROM chatroom WHERE dbid = '{0}' Limit {1}""".format(self.other, limit_no)
        record2 = sql.sqlite_run("chatroom", code2)

        total = []

        for i in record1:
            date = datetime.datetime.strptime(i[0],
                                              '%Y-%m-%d %H:%M:%S.%f'
                                              )
            msg = i[1]
            mark = "U"
            to_d = [date, msg, mark]
            total.append(to_d)

        for i in record2:
            date = datetime.datetime.strptime(i[0],
                                              '%Y-%m-%d %H:%M:%S.%f'
                                              )
            msg = i[1]
            mark = "O"
            to_d = [date, msg, mark]
            total.append(to_d)

        total.sort()
        return total

    def send_msg(self, msg):
        code = """SELECT no FROM chatroom ORDER BY no DESC LIMIT 1;"""
        user_dir_single = user_single(self.other)
        os.chdir(user_dir_single)
        no = sql.sqlite_run("chatroom", code)
        if (len(no) == 0):
            no = "1"
        else:
            no = str(no[0][0] + 1)

        try:
            time = str(datetime.datetime.now());
            sql.db_insert("chatroom" ,"chatroom", [["no", no], ["msg", msg], ["dbid", self.me], ["time", time]])
            return "true"
        except Exception as a:
            return "false"

# obj=ChatRoom(own="33859112054",#other="46312894429")
# print(obj.show_list())
# print(obj.show_msg())
# print(obj.send_msg("Hi there lol"))

