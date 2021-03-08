import os
import datetime
from sqlite_easy import easy as sql
from utility import user_single,BASE_DIR,users_dir,if_alreay_exist
from block_chain.block import Block
import random

class Reminder:
    def __init__(self, database):
        self.database = database

    def input_data(self, about, time):
        self.time = time
        self.about = about
        dt = datetime.datetime.strptime(self.time, "%Y-%m-%dT%H:%M")
        get_year = str(dt.year)
        get_month = str(dt.month)
        get_day = str(dt.day)
        get_hour = str(dt.hour)
        get_minutes = str(dt.minute)
        get_second = "00"

        time = "{0}/{1}/{2} {3}:{4}:{5}".format(get_month, get_day, get_year, get_hour, get_minutes, get_second)

        print(time)

        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)

        code = "SELECT no FROM reminder ORDER BY no DESC LIMIT 1;"
        no = sql.sqlite_run("reminder", code)
        if (len(no) == 0):
            no = "1"
        else:
            no = str(no[0][0] + 1)

        try:
            sql.db_insert("reminder", "reminder", [["about", self.about], ["time", time], ["no", no]])
        except Exception as a:
            print(a)

    def delete(self, no):

        self.no = tuple([int(no)])

        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)

        code = "SELECT no FROM reminder;"

        record = sql.sqlite_run("reminder", code)

        if (self.no in record):

            print(str((self.no)[0]))

            sql.row_delet("reminder", "reminder", "no", str((self.no)[0]))

        else:
            pass

    @property
    def show_data(self):
        data = []

        user_dir_single = user_single(self.database)
        os.chdir(user_dir_single)

        code = """
		Select * from reminder;
		"""

        record = sql.sqlite_run("reminder", code)
        record.reverse()
        for i in record:
            data.append([i[0], i[1], str(i[2])])
        return data


# obj=Reminder("44433280239")
# print(obj.show_data)
# obj.input_data("a","2016-04-10T08:07")
# print(obj.show_data)
# obj.delete("1")
# print(obj.show_data)
