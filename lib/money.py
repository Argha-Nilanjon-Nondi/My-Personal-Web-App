import os
import datetime
from sqlite_easy import easy as sql
from utility import user_single,BASE_DIR,users_dir,if_alreay_exist
from block_chain.block import Block
import random

class Money:
    def __init__(self, database) -> object:
        self.database = database

    def delete_table_name(self, table_id):
        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)
        sql.sqlite_run("money", """DROP TABLE "{0}";""".format(table_id))
        sql.row_delet("money","datas","id",table_id)
        return "true"

    def get_table_name(self, table_id):
        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)
        table = sql.sqlite_run("money", """SELECT name FROM datas WHERE id={0};""".format(table_id))[0][0]
        return table

    def add_table(self, table_name):

        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)

        code = """SELECT no FROM "datas" ORDER BY no DESC LIMIT 1;"""

        no = sql.sqlite_run("money", code)
        if (len(no) == 0):
            no = "1"
        else:
            no = str(no[0][0] + 1)

        try:
            id = str(random.randrange(6887)) + str(random.randrange(6887)) + str(random.randrange(6887))
            sql.db_insert("money", "datas", [
                ["id", id],
                ["name", table_name],
                ["no", no]
            ])

            code = """ CREATE TABLE "{0}" (
                	"no"	INTEGER NOT NULL UNIQUE,
                 	"about"	TEXT NOT NULL,
                 	"entery_date"	TEXT NOT NULL,
                	"event_date"	TEXT NOT NULL,
	                 "status"	INTEGER,
                   	"hash"	TEXT NOT NULL,
	                "previous_hash"	TEXT NOT NULL,
                	"amount"	INTEGER NOT NULL,
                	PRIMARY KEY("no" AUTOINCREMENT)); """.format(id)
            sql.sqlite_run("money", code)

            sql.db_insert("money",id, [
                ["about","AAAAAAAA"],
                ["entery_date","2021-01-10"],
                ["event_date","1000/1/1 12:0:00"],
                ["status",0],
                ["amount", 0],
                ["no", 1],
                ["hash","7e51e0a656a0805298ddf453ea1a2a714a2ba5362df89ad9f498a670a4ab1911"],
                ["previous_hash","AAAAAAA"]
            ])

            return "true"

        except Exception as a:
            return "false"

    def show_databases_data(self):
        data = []
        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)
        code = """Select no,id,name from datas;"""
        record = sql.sqlite_run("money", code)
        record.reverse()
        for i in record:
            data.append([i[0], i[1], i[2]])
        return data

    def show_single_data(self, table_name):
        data = []
        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)
        code = """Select about,entery_date,event_date,status,amount,previous_hash,hash from '{0}';""".format(table_name)
        record = sql.sqlite_run("money", code)
        record.reverse()
        for i in record:
            data.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6]])
        return data

    def input_data(self, table_name, about, time, amount, status):
        self.time = time
        self.about = about
        self.amount = amount
        self.status = status
        self.today = str(datetime.date.today())
        dt = datetime.datetime.strptime(self.time, "%Y-%m-%dT%H:%M")
        get_year = str(dt.month)
        get_month = str(dt.year)
        get_day = str(dt.day)
        get_hour = str(dt.hour)
        get_minutes = str(dt.minute)
        get_second = "00"
        time = "{0}/{1}/{2} {3}:{4}:{5}".format(get_month, get_day, get_year, get_hour, get_minutes, get_second)

        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)

        code = "SELECT no FROM '{0}' ORDER BY no DESC LIMIT 1;".format(table_name)

        no = sql.sqlite_run("money", code)
        if (len(no) == 0):
            no = "1"
        else:
            no = str(no[0][0] + 1)

        previous_hash = sql.sqlite_run("money", """SELECT hash FROM '{0}' order by no desc  limit 1;""".format(table_name))[0][0]


        blo = Block()

        blo.data = {"about": self.about, "time": time, "status":self.status, "amount": self.amount}

        blo.ts = self.today
        blo.ph = previous_hash

        try:
            sql.db_insert("money", table_name, [
                ["about", self.about],
                ["entery_date", self.today],
                ["event_date", time],
                ["status", self.status],
                ["amount",self.amount],
                ["no", no],
                ["hash", blo.mh()],
                ["previous_hash", previous_hash]
            ])
            return "true"
        except Exception as a:
            return "false"

    def check_validation(self, table_name):
        chain = self.show_single_data(table_name).copy()
        chain.reverse()

        for i in range(1, len(chain)):

            previous = chain[i - 1]
            current = chain[i]

            # current block info start
            cu_about = current[0]
            cu_hash = current[6]
            cu_phash = current[5]
            cu_enterdate = current[1]
            cu_eventdate = current[2]
            cu_amount = current[4]
            cu_status = current[3]
            # current block info end

            # previous block info start
            pre_hash = previous[6]
            # previous block info start

            block = Block()
            block.data = {
                "about": cu_about,
                "time": cu_eventdate,
                "status":cu_status,
                "amount":cu_amount}
            block.ts = cu_enterdate
            block.ph = cu_phash

            if (cu_hash != block.mh()):
                return "false"

            if (pre_hash != cu_phash):
                return "false"

        return "true"

    def show_signature(self, table_name):
        code = """
		Select hash FROM '{0}' Order By no DESC LIMIT 1;
		""".format(table_name)
        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)

        record = sql.sqlite_run("money", code)
        data = record[0][0]
        return data[0:20]


# #input=7e51e0a656a0805298ddf453ea1a2a714a2ba5362df89ad9f498a670a4ab1911
# obj = Money("574511571705")
# # print(obj.get_table_name(420610565563))
# # # obj.add_table("hacktaberfestpopo")
# print(obj.show_databases_data())
# obj.input_data(table_name="183655255662",about="AAAAAiyhlukAAA",time="1000-01-01T12:00",amount=0,status=0)
# print(obj.check_validation("183655255662"))
# 000000000000
#
# # 	#print(obj.show_signature)
