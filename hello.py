# from flask import Flask
from flaskext.mysql import MySQL
from flask import Flask,jsonify, render_template, json, request,url_for, redirect
from datetime import datetime

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ssss'
app.config['MYSQL_DATABASE_DB'] = 'buildathon'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def hello():
    # return "Welcome to Python Flask App!"
    return redirect(url_for('index'))
    # return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/showSignUp")
def showSignUp():
    return render_template("signup.html")

@app.route("/status", methods=['POST'])
def status():
    if request.method == 'POST':
        _name = request.form['inputName']
        # _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _role=request.form['inputRole']

        print(_name)
        print(_password)
        print(_role)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT * from login where Username='" + _name + "' and Password='" + _password + "'")
            data = cursor.fetchone()
            # con.commit()
            if data is None:

                cursor.execute("insert into login values(default,'"+_name+"','"+_password+"','"+_role+"')")
                # conn.commit()
                print("we need to signup")
            else:
                print("user already exist")
            conn.commit()

            #retieve userid and roleid from database
            cursor.execute("select * from login where Username='"+_name+"' and Role='"+_role+"'")
            data = cursor.fetchone()
            print("retrive from database ",data[0],data)

            if _role!="Admin":
                # result ='user/'+str(data[0])
                result = {'url': 'user/'+str(data[0])}
                # result = {'url': url_for('user',data[0])}
            else:
                result ={'url':'admin/'+str(data[0])}
                # result = {'url': url_for('admin',data[0])}
            return jsonify(result)
        except conn.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('hello')
        finally:
            conn.close() # close the connection

@app.route('/user/<string:id>', methods=['GET'])
def user(id):
    # date = request.args.get('date', None)
    print("user page")
    #retrieve the user name and send it
    #select * from user where Id = id
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from user where Id = " + id )
    data = cursor.fetchone()
    Username=data[1]
    #retrieve all notification from database and send
    #create notification based on rules
    cursor.execute("select * from scorebased where Id = " + id )
    data = cursor.fetchone()
    #create notification based on scorebased
    if data[1]<0.05*data[2]:
        cursor.execute("insert into notification values('dafault','"+id+"','"+"'red','"+now()+")")
    else if data[1]>0.05*data[2] and data[1]<0.08*data[2]:
        cursor.execute("insert into notification values('dafault','"+id+"','"+"'amber','"+now()+")")
    else:
        cursor.execute("insert into notification values('dafault','"+id+"','"+"'green','"+now()+")")

    #create notification based on time based notification
    #in 2 hour we have 120 min to set up notification
    cursor.execute("select * from timebased where Id="+id)
    data = cursor.fetchone()
    if now()-data[1]<120:
        #create notification for daily assessmenttimeline
        cursor.execute("insert into notification values('dafault','"+id+"','"+"'Alert for assessmenttimeline','"+now()+")")
    else if now()-data[1]<60:
        #create notification for daily dailyupdateTimeline
        cursor.execute("insert into notification values('dafault','"+id+"','"+"'Alert for dailyupdateTimeline','"+now()+")")

    #create notification based on event based notification before 2 days
    #in 2 days we have 2880 min to set up notification
    cursor.execute("select * from eventbased where Id="+id)
    data = cursor.fetchone()
    if now()-data[1]<2880:
        #create notification for daily assessmenttimeline
        cursor.execute("insert into notification values('dafault','"+id+"','"+"'Alert for event ','"+now()+")")

    #create notification based on participation
    cursor.execute("select * from participation where Id="+id)
    data = cursor.fetchone()
    if data[2]=="NO":
        #create notification for daily assessmenttimeline
        cursor.execute("insert into notification values('dafault','"+id+"','"+"'not yet participated','"+now()+")")

    #create notification based on rolebased
    cursor.execute("select * from rolebased where Id="+id)
    data = cursor.fetchone()
    if data[1]=="MANAGER":
        #create notification for daily assessmenttimeline
        cursor.execute("insert into notification values('dafault','"+id+"','"+"'Hello manager how are you','"+now()+")")
    else if data[1]=="EMPLOYEE":
        #create notification for daily assessmenttimeline
        cursor.execute("insert into notification values('dafault','"+id+"','"+"'Hello employee how are you','"+now()+")")

    #select * from  notification where Id=id
    cursor.execute("select * from  notification where Id=" +id+"order by time desc")
    data = cursor.fetchone()
    notifications={}
    for ele in data:
        notifications[data[0]]=data[3]

    # updatethe time of login of user in user table
    cursor.execute("update user set Lastlogin="+now()+" where Id = "+Id)

    # return redirect(url_for("user"))
    return render_template("user.html",id=id,Username=Username,notifications=notifications)


@app.route('/admin/<string:id>', methods=['GET'])
def admin(id):
    # date = request.args.get('date', None)
    print("admin page")
    # return redirect(url_for("admin"))
    #retrieve the list of all userid
    #select * from user
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from user")
    data = cursor.fetchone()
    userid={}
    for ele in data:
        userid[ele[0]]=ele[1]

    conn.close()
    print(data)
    print(userid)
    return render_template("admin.html",id=id,userid=userid)

@app.route('/createmapping', methods=['POST'])
def createmapping():
    # date = request.args.get('date', None)
    if request.method == 'POST':
        _adminid=request.form['adminid']
        _trigger = request.form['trigger']
        _users = request.form['users']
        conn = mysql.connect()
        cursor = conn.cursor()
        if _trigger=="scorebased":
            nooftransaction=request.form['nooftransaction']
            monthlyachievement=request.form['monthlyachievement']
            cursor.execute("insert into"+ scorebased+"(default,'"+nooftransaction+"','"+monthlyachievement+"','"+_users+"')")
        else if _trigger=="eventbased":
            eventTimeline=request.form['eventTimeline']
            cursor.execute("insert into"+ eventbased+"(default,'"+eventTimeline+"','"+_users+"')")
        else if _trigger=="statusbased":
            activeinactive=request.form['activeinactive']
            cursor.execute("insert into"+ statusbased+"(default,'"+activeinactive+"','"+_users+"')")
        else if _trigger=="participation" :
            activityName=request.form['activityName']
            cursor.execute("insert into"+ participation+"(default,'"+activityName+"','"+_users+"')")
        else if _trigger=="randomtrigger":
            cursor.execute("insert into"+ randomtrigger+"(default,'"+nooftransaction+"','"+monthlyachievement+"','"+_users+"')")
        else if _trigger=="rolebased":
            roleName=request.form['roleName']
            cursor.execute("insert into"+ rolebased+"(default,'"+roleName+"','"+_users+"')")
        else:
            assessmenttimeline=request.form['assessmenttimeline']
            dailyupdatetimeline=request.form['dailyupdatetimeline']
            cursor.execute("insert into"+ timebased+"(default,'"+assessmenttimeline+"','"+dailyupdatetimeline+"','"+_users+"')")
        conn.close()
        # _role=request.form['inputRole']
    print(_adminid)
    print(_trigger)
    print(_users)
    #create the mapping and store in database
    # "insert into"+ _trigger+"(default,'"+ +")"
    print("mapping created")
    return render_template("admin.html")
    # return redirect(url_for("admin"))
    # return render_template("admin.html")


if __name__ == "__main__":
    conn = mysql.connect()
    cursor = conn.cursor()
    #create notification based on statusbased notification whether the user has logged in or not
    cursor.execute("select * from user where Id")
    data = cursor.fetchone()
    # set the utc date time 5:30
    time_in_utc = datetime.utcnow()
    if now()==time_in_utc:
        for eachuser in data:
            # time_in_utc = datetime.utcnow()
            if time_in_utc-date[3]>0:
                #create notification for daily assessmenttimeline
                cursor.execute("insert into notification values('dafault','"+id+"','"+"'Alert user has not logged in today ','"+now()+")")

    # schedule randomtrigger
    cursor.execute("select * from randomtrigger")
    data = cursor.fetchone()
    # set the utc date time 5:30 for random trigger
    time_in_utc = datetime.utcnow()
    if now()==time_in_utc:
        for eachuser in data:
            # # time_in_utc = datetime.utcnow()
            # if time_in_utc-date[3]>0:
            #     #create notification for daily assessmenttimeline
            cursor.execute("insert into notification values('dafault','"+id+"','"+"'Hello ,how are you ','"+now()+")")

    app.run(debug=True)
