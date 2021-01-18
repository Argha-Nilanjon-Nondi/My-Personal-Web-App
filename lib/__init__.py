import random
import os
import datetime
import builtwith
from sqlite_easy import easy as sql


#print(if_alreay_exist(dbid="574511571705",db_name="money",table_name="datas",columns=["id","name"],data_list=[('547265204017', 'Full money')]))


class CreatAccount:
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password
        self.db = str(random.randrange(688987)) + str(random.randrange(6568887)) + str(random.randrange(647887))

    def create(self):
        code = """
			SELECT email FROM user;
			"""
        email = tuple([self.email])
        os.chdir(BASE_DIR)
        record = sql.sqlite_run("users", code)
        if (email in record):
            return False
        else:
            sql.db_insert("users", "user", [["email", self.email], ["username", self.name], ["password", self.password],
                                            ["dbid", self.db]])
            os.path.join(BASE_DIR, "static", "users", self.db, "certificate")
            os.chdir(users_dir)
            os.mkdir(self.db)
            os.chdir(self.db)

            folder = ["certificate"]  # folders which will be create in static directory
            databases_dict = {
                "reminder": ["""CREATE TABLE "reminder" 
				               ("about" TEXT Not null ,
				                "time" TEXT Not null ,
				                 "no" int Not null   Primary Key);"""],
                "money": ['''CREATE TABLE "datas" (
	                       "no"	INTEGER NOT NULL UNIQUE,
	                       "id"	TEXT NOT NULL,
	                       "name"	TEXT NOT NULL,
	                        PRIMARY KEY("no")); '''],
                "certificate": ["""CREATE TABLE "certificate" 
				                ("no" INTEGER Not null  Primary Key ,
				                  "img_name" TEXT Not null ,
				                   "url" TEXT Not null )"""],
                "chatroom": ["""CREATE TABLE chatroom(
				               no INT,
		                       msg Varchar(200),
		                       dbid Varchar(200),
		                    time Varchar(200))"""]
            }  # database's names and sql code which will be create in users/dbid

            for x in databases_dict:
                db_name = x
                sql.db_create(db_name)
                sql_code = databases_dict[db_name]

                for item_code in sql_code:
                    sql.sqlite_run(db_name, item_code)

            # sql.db_insert(self.db,"money",[
            # ["about","AAAAA"],
            # ["hash","000040d6883880da2a96fce37c89d449fcc2666c5bfb96c73c368cacab1bf091"],
            # ["previous_hash","AAAAAAA"],
            # ["entery_date","00/00/00"],
            # ["event_date","00/00/00"],
            # ["amount",0],
            # ["status","1"],
            # ["no","1"]
            # ])

            os.chdir(BASE_DIR + r"/static/" + r"/users/")
            os.mkdir(self.db)
            os.chdir(BASE_DIR + r"/static/" + r"/users/" + self.db)

            for f in folder:
                os.mkdir(f)
            return True
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


class Traceoute:
    def __init__(self, url):
        self.url = url

    @property
    def find(self):
        return builtwith.parse(self.url)


class Music:
    def __init__(self, database):
        self.database = database

    def input_data(self, music_name, url, image):
        self.image = image
        self.music_name = music_name
        self.url = r"""{0}""".format(url)
        os.chdir(users_dir)

        code = "SELECT no FROM music ORDER BY no DESC LIMIT 1;"

        os.chdir(users_dir)

        no = sql.sqlite_run(self.database, code)
        if (len(no) == 0):
            no = "1"
        else:
            no = str(no[0][0] + 1)

        try:
            sql.db_insert(self.database, "music",
                          [["url", self.url], ["music", self.music_name], ["no", no], ["image", self.image]])
        except Exception as a:
            print(a)

    def delete(self, no):

        self.no = tuple([int(no)])

        code = "SELECT no FROM music;"

        os.chdir(users_dir)

        record = sql.sqlite_run(self.database, code)

        if (self.no in record):

            os.chdir(users_dir)

            sql.row_delet(self.database, "music", "no", str((self.no)))

            code = "SELECT music FROM music WHERE no ={0} ;".format((self.no)[0])

            file_name = sql.sqlite_run(self.database, code)[0][0]

            os.chdir(os.path.join(BASE_DIR, 'static', "users", self.database, "music"))

            os.remove(file_name)

        else:
            pass

    @property
    def show_data(self):
        data = []
        code = """
		Select music,url,no,image from music;
		"""
        os.chdir(users_dir)
        record = sql.sqlite_run(self.database, code)
        record.reverse()
        for i in record:
            data.append([i[0], i[1], i[2], i[3]])

        return data


# obj=Music("30345821341")
# obj.input_data("hello","5869","999.png")
# print(obj.show_data)


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


# if __name__=="__main__":
#	obj=Traceoute("http://localhost:8080/phpmyadmin/")
#	print(obj.find)
#
