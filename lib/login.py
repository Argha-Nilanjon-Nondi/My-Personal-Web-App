import os
from sqlite_easy import easy as sql
from utility import BASE_DIR


class Login:
    """
	Used for user's login
	"""

    def __init__(self, email, password):
        self.email = email
        self.password = password
        print("worked=9999")

    @property
    def check(self):
        code = """
			SELECT email FROM user;
			"""
        email = tuple([self.email])
        os.chdir(BASE_DIR)
        record = sql.sqlite_run("users", code)
        if (email in record):
            code = "SELECT password FROM user where email='{0}';".format(self.email)
            db_password = sql.sqlite_run("users", code)[0][0]
            if (self.password == db_password):
                code = "SELECT username FROM user where email='{0}';".format(self.email)

                username = sql.sqlite_run("users", code)[0][0]

                code = "SELECT dbid FROM user where email='{0}';".format(self.email)

                dbid = sql.sqlite_run("users", code)[0][0]

                return [True, username, dbid]
        else:
            return [False]


# obj=Login("pcic098u88009b5@gmail.com","avunix9143")
# print(obj.check)
