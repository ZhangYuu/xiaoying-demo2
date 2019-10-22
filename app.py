from random import randrange
from flask import Flask, render_template, request, session, redirect, url_for, make_response, jsonify
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie,Funnel,Line,Timeline,Tab
from pyecharts.components import Table
import random, datetime, requests, json
from diagram_chart import line_datazoom_slider,funnel_sort_ascending,bar_base,table_base
from time import sleep
app = Flask(__name__)
#bootstrap = Bootstrap(app)
today=datetime.date.today()

#累积用户查询时间
date_acc=[(datetime.date.today() + datetime.timedelta(days=-30)),today]  #默认累积搜索用户时间
#活跃用户查询时间
date_active=[(datetime.date.today() + datetime.timedelta(days=-90)),today]  #默认活跃搜索用户时间
#书籍累积用户查询时间
book_acc=[(datetime.date.today() + datetime.timedelta(days=-30)),today]  #默认累积搜索用户时间
#书籍活跃用户查询时间
book_active=[(datetime.date.today() + datetime.timedelta(days=-90)),today]  #默认活跃搜索用户时间


#将日期转为datetime格式并验证
def verify_date(start_date,end_date):
  if start_date == "" or end_date == "" :
    return False
  else:
    start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    if start_date > end_date or start_date > today or end_date >today:
      return False
    else:
      return ([start_date,end_date])

#将得到的API数据转为x,y轴两个list
def transfer_data(data):
    x=[]
    y=[]
    for i in data:
        x.append(i["date"])
        y.append(i["number"])
    return ([x,y])

@app.route('/')
def index():
  return render_template('login.html')

#登陆
@app.route("/login",methods=["POST","GET"])
def login():
  error = None
  print (request.form['password'])
  if request.method == 'POST':
    if request.form['username']!="mengwei" and request.form['password']!="666666": #db.pwd.find_one()["pwd"]:
      error = '用户名或密码错误，请重新输入'
      return render_template('login.html',error=error)
    else:
      return render_template('UserChart.html')
  return render_template('login.html',error=error)

#快捷日志导航
@app.route("/qucik_date_guide/<int:num>",methods=["GET"])
def quick_date_guide(num):
  if request.method == 'GET':
    global date_acc  #获取全局变量
    if num==7:
      date_acc=[(datetime.date.today() + datetime.timedelta(days=-7)),today]
      print ("验证日期",date_acc)
      return render_template('UserChart.html')
    elif num==30:
      date_acc=[(datetime.date.today() + datetime.timedelta(days=-30)),today]
      print ("验证日期",date_acc)
      return render_template('UserChart.html')
    elif num==90:
      date_acc=[(datetime.date.today() + datetime.timedelta(days=-90)),today]
      print ("验证日期",date_acc)
      return render_template('UserChart.html')
    else:
      return render_template('UserChart.html')

#书本快捷日志导航
@app.route("/book_date_guide/<int:num>/<string:idname>",methods=["GET"])
def book_date_guide(num,idname):
  if request.method == 'GET':
    global date_acc  #获取全局变量
    id,name = idname.split("+")[0],idname.split("+")[1]
    if num==7:
      date_acc=[(datetime.date.today() + datetime.timedelta(days=-7)),today]
      return render_template('BookChart.html',book_id=id,book_name=name)
    elif num==30:
      date_acc=[(datetime.date.today() + datetime.timedelta(days=-30)),today]
      return render_template('BookChart.html',book_id=id,book_name=name)
    elif num==90:
      date_acc=[(datetime.date.today() + datetime.timedelta(days=-90)),today]
      return render_template('BookChart.html',book_id=id,book_name=name)
    else:
      return render_template('BookChart.html',book_id="xiyou",book_name="西游")

#获取用户累积日期数据
@app.route("/get_acc_date",methods=["POST"])
def get_acc_date():
  acc_error = None
  #print ("获取累积日期",request.form['start_acc_date'])
  global date_acc  #获取全局变量
  acc = verify_date(request.form['start_acc_date'],request.form['end_acc_date'])
  if acc == False:
    acc_error = "日期输入错误，请重新输入"
    return render_template('UserChart.html',acc_error=acc_error)
  else:
    date_acc = acc
    return render_template('UserChart.html')

#获取用户活跃日期数据
@app.route("/get_date",methods=["POST"])
def get_date():
  active_error = None
  #print ("获取活跃日期",request.form['start_date'])
  global date_active  #获取全局变量
  act = verify_date(request.form['start_date'],request.form['end_date'])
  if act == False:
    active_error = "日期输入错误，请重新输入"
    return render_template('UserChart.html',active_error=active_error)
  else:
    date_active = act
    return render_template('UserChart.html')

#获取书本累计日期数据
@app.route("/book_acc_date",methods=["POST"])
def book_acc_date():
  acc_error = None
  #print ("获取累积日期",request.form['start_acc_date'])
  global book_acc  #获取全局变量
  acc = verify_date(request.form['book_start_acc_date'],request.form['book_end_acc_date'])
  book_id = request.form['book_id']
  name = request.form['book_name']
  if acc == False:
    acc_error = "日期输入错误，请重新输入"
    return render_template('BookChart.html',acc_error=acc_error,book_id=book_id,book_name=name)
  else:
    book_acc = acc
    return render_template('BookChart.html',book_id=book_id,book_name=name)

#获取书本活跃日期数据
@app.route("/book_get_date",methods=["POST"])
def book_get_date():
  active_error = None
  #print ("获取活跃日期",request.form['start_date'])
  global book_active  #获取全局变量
  act = verify_date(request.form['start_date'],request.form['end_date'])
  book_id = request.form['book_id']
  name = request.form['book_name']
  if act == False:
    active_error = "日期输入错误，请重新输入"
    return render_template('BookChart.html',active_error=active_error,book_id=book_id,book_name=name)
  else:
    book_active = act
    return render_template('BookChart.html',book_id=book_id,book_name=name)

#页面跳转
@app.route('/skip/<int:num>',methods=['GET'])
def skip(num):
  if request.method == 'GET':
    if num==1:
      return render_template('UserList.html')
    elif num==2:
      return render_template('UserBehavior.html')
    elif num==3:
      return render_template('UserChart.html')
    elif num==4:
      return render_template('BookChart.html',book_id="xiyou",book_name="西游")
    elif num==5:
      return render_template('BookChart.html',book_id="xiyou2",book_name="西游配音版")
    elif num==6:
      return render_template('BookChart.html',book_id="qinzi",book_name="亲子关系")
    elif num==7:
      return render_template('BookChart.html',book_id="qinzi2",book_name="亲子关系配音版")
    else:
      return render_template('home.html')

#用户页面
@app.route("/userlist")
def UserList():
  return render_template("UserList.html")

#用户列表数据
@app.route('/userlist_get_data')
def ul_getdata():
  url_userlist="http://13.125.241.222:8080/api/user/list"
  user_data=json.loads(requests.get(url_userlist).text)
  for user in user_data:
      if user["avatar"] is None:
          user["avatar"]="/static/img/portfolio/empty_avatar.png"
          #print(user["name"])
  data={"data":user_data}
  return jsonify(data)

#获取用户行为统计数据发送前端
@app.route('/userbehaviour_get_data')
def stuff2():
  url_userbehaviour="http://13.125.241.222:8080/api/user/record"
  data={"data":json.loads(requests.get(url_userbehaviour).text)}
  return jsonify(data)

#累积折线图 用户/书本通用
@app.route("/accu_line_chart/<string:id>",methods=["GET"])
def accu_line_chart(id):
    #print("累积用户表",date_acc)
    if id=="user":
      url = "http://13.125.241.222:8080/api/user/total"
      d = {"startdate": str(date_acc[0]), "enddate": str(date_acc[1])}
      print(url)
    else:
      url = "http://13.125.241.222:8080/api/user/total/" + id
      d = {"startdate": str(book_acc[0]), "enddate": str(book_acc[1])}
      print("#############",url)
    acc_data=requests.get(url,data=d).text #这里需要写data=XXX而不是直接给
    acc_data=json.loads(acc_data)
    trans_data=transfer_data(acc_data)
    d = line_datazoom_slider(trans_data[0],trans_data[1],"累积用户")
    return d.dump_options_with_quotes()

#日活折线图
@app.route("/day_line_chart/<string:id>",methods=["GET"])
def line_day_chart(id):
    #print("日活用户表", date_active)
    if id=="user":
      url = "http://13.125.241.222:8080/api/user/active/daily"
      d = {"startdate": str(date_active[0]), "enddate": str(date_active[1])}
    else:
      url = "http://13.125.241.222:8080/api/user/active/daily/" + id
      d = {"startdate": str(book_active[0]), "enddate": str(book_active[1])}
    act_data=requests.get(url,data=d).text #这里需要写data=XXX而不是直接给
    act_data=json.loads(act_data)
    trans_data=transfer_data(act_data)
    d = line_datazoom_slider(trans_data[0],trans_data[1],"日活跃用户")
    return d.dump_options_with_quotes()

#周活折线图
@app.route("/week_line_chart/<string:id>",methods=["GET"])
def line_week_chart(id):
    if id=="user":
      url = "http://13.125.241.222:8080/api/user/active/weekly"
      d = {"startdate": str(date_active[0]), "enddate": str(date_active[1])}
    else:
      url = "http://13.125.241.222:8080/api/user/active/weekly/" + id
      d = {"startdate": str(book_active[0]), "enddate": str(book_active[1])}
    act_data=requests.get(url,data=d).text #这里需要写data=XXX而不是直接给
    act_data=json.loads(act_data)
    trans_data=transfer_data(act_data)
    d = line_datazoom_slider(trans_data[0],trans_data[1],"周活跃用户")
    return d.dump_options_with_quotes()

#月活折线图
@app.route("/month_line_chart/<string:id>",methods=["GET"])
def line_month_chart(id):
    if id=="user":
      url = "http://13.125.241.222:8080/api/user/active/monthly"
      d = {"startdate": str(date_active[0]), "enddate": str(date_active[1])}
    else:
      url = "http://13.125.241.222:8080/api/user/active/monthly/" + id
      d = {"startdate": str(book_active[0]), "enddate": str(book_active[1])}
    act_data=requests.get(url,data=d).text
    print(type(act_data))
    act_data=json.loads(act_data)
    trans_data=transfer_data(act_data)
    d = line_datazoom_slider(trans_data[0],trans_data[1],"月活跃用户")
    return d.dump_options_with_quotes()

#书本柱状图表格
@app.route("/barChart")
def get_bar_chart():
    url = "http://13.125.241.222:8080/api/user/list/book"
    book_data=requests.get(url).text
    book_data=json.loads(book_data)
    book_list=[]
    book_user=[]
    for i in book_data:
        book_list.append(i["name"])
        book_user.append(i["number"])
    #print(book_list,book_user)
    c = bar_base(book_list,book_user)
    return c.dump_options_with_quotes()

#书本漏斗图
@app.route("/funnelchart/<string:id>",methods=["GET"])
def get_funnel_chart(id):
    url = "http://13.125.241.222:8080/api/user/progress/"+id
    study_progress=[]
    book_data=requests.get(url).text
    book_data=json.loads(book_data)
    for book in book_data:
        study_progress.append((book['name'],book['number']))
    d = funnel_sort_ascending(study_progress)
    return d.dump_options_with_quotes()

#书本表格
@app.route('/booktable_get_data')
def stuff3():
  url = "http://13.125.241.222:8080/api/user/list/book"
  book_data=requests.get(url).text
  book_data=json.loads(book_data)
  table_data=[]
  for i in book_data:
      table_data.append([i["name"],i["number"],i["id"]])  
  d = table_base(["课程名称","用户数量","课程ID"],table_data)
  return d.render_embed()


#书本表格
@app.route('/result',methods = ['POST', 'GET'])
def result():
  url = "http://13.125.241.222:8080/api/user/list/book"
  book_data=requests.get(url).text
  book_data=json.loads(book_data)
  list = book_data
  print(json.dumps(list))
  return render_template("UserChart.html",book_data = json.dumps(list))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)

