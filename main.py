import lib
import os
import random
from validation import Validation
from datetime import timedelta
from flask import *


app=Flask(__name__)
app.debug=True
app.secret_key="r9ruchrh0dh30rjro"
app.permanent_session_lifetime = timedelta(minutes=3000)
app.host="0.0.0.0"
BASE_DIR ="""F:\\argha nondi\\codding\\avunix_assistant_web\\"""
validated=Validation()

# obj=lib.Certificate("158624666524")
# obj.input_data("hello.png","http//5869.889;png")
# obj.delete(2)


@app.route("/home/")
def home():
	if("status" in session):
		if(session["status"]=="logged"):
			return render_template("home.html")
	else:
		return redirect("/")

@app.route("/login/",methods=["GET","POST"])
@app.route("/",methods=["GET","POST"])
def login():
	"""
	session values : dbid,username,status
	"""
	code=""
	if request.method=="POST":
		email=request.form["email"]
		password=request.form["password"]
		
		if(validated.checkValue(None,email,password) or validated.checkValue("",email,password)):
			return redirect("/")
		
		obj=lib.Login(email,password)
		value=obj.check
		if (value[0]==True):
		  session.permanent = True
		  session["status"]="logged"
		  session["username"]=value[1]
		  session["dbid"]=value[2]
		  return redirect("/home/")
		else:
			code="""
<div class="alert alert-danger alert-dismissible fade show" role="alert">
  <strong>Authentication</strong> Email or password is incorrect , Try again.
  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
</div>  
			"""
			return render_template("login.html",code=code)
			
		
	return render_template("login.html",code=code)

@app.route("/money/",methods=["POST","GET"])
def money_databases():
	if("status" in session):
		if(session["status"]=="logged"):
			if request.method == "POST":
				collection = request.form["collection"]
				obj=lib.Money(session["dbid"])
				obj.add_table(collection)
			return render_template("money/money_home.html")
	else:
		return redirect("/")

@app.route("/money/tables/data/",methods=["POST","GET"])
def money_databases_data():
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.Money(session["dbid"])
			data=obj.show_databases_data()
			data={"data":data}
			return data
	else:
		return redirect("/")
	
@app.route("/money/single/<table_name_id>/",methods=["GET","POST"])
def money_single(table_name_id):
	if("status" in session):
		if(session["status"]=="logged"):
			
			obj=lib.Money(session["dbid"])
			fetch_table_name=obj.get_table_name(table_name_id)
			if request.method=="POST":
				
				date=request.form["date"]
				amount=int(request.form["amount"])
				status=int(request.form["status"])
				about=request.form["about"]
				
				if(validated.checkValue(None,date,amount,status,about) or validated.checkValue("",date,amount,status,about)):
					return redirect("/")
			
				obj.input_data(table_name_id,about,date,amount,status)
				return render_template("money/money.html",table_name_id=table_name_id,fetch_table_name=fetch_table_name)
				
			return render_template("money/money.html",table_name_id=table_name_id,fetch_table_name=fetch_table_name)
	else:
		return redirect("/")


@app.route("/money/delete/<table_name_id>/",methods=["GET","POST"])
def money_delete_database(table_name_id):
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.Money(session["dbid"])
			checl_validadion=lib.if_alreay_exist(dbid=session["dbid"],db_name="money",table_name="datas",columns=["id"],data_list=[(table_name_id,)])

			if(checl_validadion==False):
				return redirect("/logout/")
			obj.delete_table_name(table_name_id)
			return redirect("/money/")
	else:
		return redirect("/")

@app.route("/money/single/data/<table_name_id>/",methods=["GET","POST"])
def money_single_data(table_name_id):
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.Money(session["dbid"])
			data=obj.show_single_data(table_name_id)
			data={"data":data}
			return data
	else:
		return redirect("/")
		
@app.route("/money/single/signature/<table_name_id>/",methods=["GET","POST"])
def money_single_signature(table_name_id):
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.Money(session["dbid"])
			data=obj.show_signature(table_name_id)
			data={"data":data}
			return data
	else:
		return redirect("/")

@app.route("/money/single/validation/<table_name_id>",methods=["GET","POST"])
def money_single_validation_data(table_name_id):
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.Money(session["dbid"])
			data=obj.check_validation(table_name_id)
			data={"data":data}
			return data
	else:
		return redirect("/")		


@app.route("/reminder/", methods=["GET", "POST"])
def reminder():
	if ("status" in session):

		if (session["status"] == "logged"):

			obj = lib.Reminder(session["dbid"])

			if request.method == "POST":

				date = request.form["date"]
				about = request.form["about"]

				if (validated.checkValue(None, date, about) or validated.checkValue("", date, about)):
					return redirect("/")

				obj.input_data(about, date)

				return render_template("reminder.html")
			return render_template("reminder.html")
	else:
		return redirect("/")

@app.route("/reminder/data/",methods=["GET","POST"])
def reminder_data():
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.Reminder(session["dbid"])
			data=obj.show_data
			data={"data":data}
			return data
	else:
		return redirect("/")	
										
@app.route("/certificate/data/",methods=["GET","POST"])
def certificate_data():
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.Certificate(session["dbid"])
			data=obj.show_data
			data={"data":data}
			return data
	else:
		return redirect("/")										
									

@app.route("/reminder/delete/<int:no>/",methods=["POST","GET"])
def reminder_delete(no):
	no=no
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.Reminder(session["dbid"])
			
			if(validated.checkValue(None,no) or validated.checkValue("",no)):
				return redirect("/")
				
			obj.delete(str(no))
			return redirect("/reminder/")	
	else:
		return redirect("/")	
		
						
@app.route("/certificate/",methods=["GET","POST"])
def certificate():
	if("status" in session):
		if(session["status"]=="logged"):
			if(request.method=="POST"):
				
				url=request.form["url"]
				image=request.files["image"]
				
				if(validated.checkValue(None,url,image) or validated.checkValue("",url,image)):
								return redirect("/")
								
				random_file_name=str(random.randrange(7007))+str(random.randrange(706607))+str(random.randrange(78907))+".pdf"
				
				users_dir=os.path.join(BASE_DIR,"static","users",session["dbid"],"certificate")
				
								
				obj=lib.Certificate(session["dbid"])
				
				obj.input_data(random_file_name,url)			
				
				image.save(os.path.join(users_dir, (random_file_name) ))
				
				return render_template("certificate.html")
			return render_template("certificate.html")
	else:
		return redirect("/")

@app.route("/certificate/delete/<int:no>/",methods=["POST","GET"])
def certificate_delete(no):
	no=no
	if("status" in session):
		if(session["status"]=="logged"):
				if(validated.checkValue(None,no) or validated.checkValue("",no)):
					return redirect("/")			
		obj=lib.Certificate(session["dbid"])			
		obj.delete(str(no))
		return redirect("/certificate/")	
	else:
		return redirect("/")	

@app.route("/logout/")
def logout():
	if("status" in session):
		if(session["status"]=="logged"):
			session.pop("status",None)
			return redirect("/")
	else:
		return redirect("/")	
		
@app.route("/dbid/",methods=["GET","POST"])		
def dbid():
	if("status" in session):
		if(session["status"]=="logged"):
			return {"data":session["dbid"]}
	else:
		return redirect("/")

@app.route("/trace/data/",methods=["GET","POST"])
def trace_data():
	if("status" in session):
		if(session["status"]=="logged"):
			url=request.args.get("url");
			if(validated.checkValue(None,url) or validated.checkValue("",url)):
				return redirect("/")			
			obj=lib.Traceoute(url)
			return obj.find;
	else:
		return redirect("/")

@app.route("/trace/",methods=["GET","POST"])
def trace():
	if("status" in session):
		if(session["status"]=="logged"):
			return render_template("traceoute.html")
	else:
		return redirect("/")

		
@app.route("/chatroom/data/",methods=["GET","POST"])
def chatroom_data():
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.ChatRoom(own="",other="")
			data={"data":obj.show_list()}
			return data
	else:
		return redirect("/")
		
		
@app.route("/chatroom/",methods=["GET","POST"])
def chatroom():
	if("status" in session):
		if(session["status"]=="logged"):
			return render_template("chatroom.html")
	else:
		return redirect("/")		
		
@app.route("/chat_me/<id>/<name>/",methods=["GET","POST"])
def chat_me(id,name):
  if(validated.checkValue(None,id,name) or validated.checkValue("",id,name)):
    return redirect("/")
  if("status" in session):
    if(session["status"]=="logged"):
      return render_template("chat_me.html",id=id,name=name)
  else:
    return redirect("/")		
		
@app.route("/chat_me/talk/<own>/<other>/",methods=["GET","POST"])
def chat_talk(own,other):
	if(validated.checkValue(None,own,other) or validated.checkValue("",own,other)):
		return redirect("/")
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.ChatRoom(own,other)
			data={"data":obj.show_msg()}
			return data
	else:
		return redirect("/")		
		
@app.route("/chat_me/enter/<own>/<other>/<msg>/",methods=["GET","POST"])
def chat_enter(own,other,msg):
	if(validated.checkValue(None,own,other,msg) or validated.checkValue("",own,other,msg)):
		return redirect("/")
	if("status" in session):
		if(session["status"]=="logged"):
			obj=lib.ChatRoom(own,other);
			obj.send_msg(msg);			
			return "true";
	else:
		return redirect("/")


@app.route("/money/home")
def money_home():
	if("status" in session):
		if(session["status"]=="logged"):
			print("*****")
			return render_template("money/money_home.html")
	else:
		return redirect("/")

"""
@app.route("/home")
def home():
	if("status" in session):
		if(session["status"]=="logged"):
			print("*****")
			return "******"
	else:
		return redirect("/")
"""
if __name__=="__main__":
	app.run()