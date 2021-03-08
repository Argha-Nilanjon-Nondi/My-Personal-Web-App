import random
import os
import datetime
import builtwith
from sqlite_easy import easy as sql
from utility import user_single,users_dir,BASE_DIR

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


# if __name__=="__main__":
#	obj=Traceoute("http://localhost:8080/phpmyadmin/")
#	print(obj.find)
#
