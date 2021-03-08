import os
from sqlite_easy import easy as sql

BASE_DIR = os.getcwd()

users_dir =os.path.join(BASE_DIR,"users")

def user_single(dbid):
    return os.path.join(users_dir,dbid)


def if_alreay_exist(dbid,db_name,table_name,columns,data_list):
    user_dir_single = user_single(dbid)
    os.chdir(user_dir_single)
    #Add all column to column_collection start
    column_collection=""
    for i in columns:
        column_collection+=(i+",")
    column_collection=column_collection[0:-1]
    ##Add all column to column_collection end

    #Run a sql query and load all data start
    code = """
    		Select {0} from {1};
    		""".format(column_collection,table_name)

    record = sql.sqlite_run(db_name, code)
    #Run a sql query and load all data end

    #Check all data_list in record variable start
    for j in data_list:
        if(j not in record):
            return False
    # Check all data_list in record variable end
    return True