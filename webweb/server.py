from flask import Flask,render_template,request,redirect,url_for,session,jsonify
# redirect 重定向
import pymysql,hashlib,math
# 连接数据库
db = pymysql.connect(host="localhost",user="root",password="",db="webweb")
# 创建游标
cur = db.cursor()

app = Flask(__name__)
# 生成密钥
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# / 代表首页
@app.route('/')
def index():
    sql = "select * from category limit 8"
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    sql1 = "select * from news limit 3"
    cur.execute(sql1)
    db.commit()
    res1 = cur.fetchall()
    return render_template("webweb-master/index.html",data=res,data1=res1)

@app.route('/business')
def business():
    return render_template("/webweb-master/business.html")
# 打开联系我们页面
@app.route('/contact')
def contact():
    return render_template("/webweb-master/contact.html")
@app.route('/addcontact',methods=['post'])
def addcontact():
    name = request.form['name']
    email = request.form['email']
    iphone = request.form['iphone']
    con = request.form['con']
    sql = "insert into contact (name,email,iphone,con) values('%s','%s',%s,'%s')" % (name, email, iphone, con)
    print(sql)
    cur.execute(sql)
    db.commit()
    return render_template("/webweb-master/contact.html")


@app.route('/aboutus')
def aboutus():
    return render_template("/webweb-master/aboutus.html")

@app.route('/news')
def news():
    sql = "select * from news limit 8"
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    sql1 = "select * from news where cid=1 order by news.id desc "
    cur.execute(sql1)
    db.commit()
    res1 = cur.fetchall()
    sql2 = "select * from news where cid=2 order by news.id desc"
    cur.execute(sql2)
    db.commit()
    res2 = cur.fetchall()
    return render_template("/webweb-master/news.html",data=res,data1=res1,data2=res2)

@app.route('/news1<id>')
def news1(id):
    sql = "select * from news where id=%s" % id
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    sql1 = "select * from news limit 8"
    cur.execute(sql1)
    db.commit()
    res1= cur.fetchall()
    return render_template("/webweb-master/news1.html",data=res,data1=res1)

@app.route('/product')
def product():
    sql = "select * from category"
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    return render_template("/webweb-master/product.html",data=res)

@app.route('/product1<id>')
def product1(id):
    # id=request.form['id']
    print(id)
    sql = "select * from category where id=%s"%id
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    return render_template("/webweb-master/product1.html",data=res)

# 后台逻辑
@app.route("/admin")
def admin():
    if 'username' in session:
        return render_template("/blue-master/index.html",level=session['level'])
    else:
        return redirect(url_for("login"))
@app.route("/login")
def login():
    return render_template("blue-master/login.html")
@app.route("/loginout")
def loginout():
    del session['username']
    del session['level']
    return render_template("blue-master/login.html")
@app.route("/checklogin",methods=['post'])
def checklogin():
    username=request.form['username']
    password = request.form['password']
    # 加密密码
    s = hashlib.md5()
    s.update(password.encode())
    password=s.hexdigest()
    #组织mysql 语句
    sql="select password,level from user where username = '%s'"%username
    # 执行sql 语句
    cur.execute(sql)
    password0=""
    # 获取查询结果
    res=cur.fetchone()

    if res!=None:
        password0 = res[0]
    if password0 == password:
        session['username']=username
        session['level'] = res[1]
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("tips",state="no",href="login",time=3))

@app.route("/tips/<state>/<href>/<time>")
def tips(state,href,time):
    return render_template("blue-master/tips.html",state=state,href=href,time=time)
@app.route("/openadduser")
def openadduser():
    if 'username' in session:
        if session['level']==1:
            return render_template("/blue-master/adduser.html")
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("tips",state="no",href="admin",time=3))

@app.route("/adduser",methods=['post'])
def adduser():
    if 'username' in session:
        username=request.form['username']
        newpass = request.form['newpass']
        renewpass = request.form['renewpass']
        if username!=""and newpass!=""and renewpass!="":
            if newpass==renewpass:
                s = hashlib.md5()
                s.update(newpass.encode())
                password = s.hexdigest()
                sql="insert into user(username,password,level) values('%s','%s',%s)"%(username,password,2)
                cur.execute(sql)
                db.commit()
                return redirect(url_for("tips",state="yes",href="openadduser",time=3))
            else:
                return redirect(url_for("tips", state="no", href="openadduser", time=3))

        else:
            return redirect(url_for("tips", state="no", href="openadduser", time=3))
    else:
        return redirect(url_for("login"))
@app.route("/listuser<page>")
def listuser(page):
    page = int(page)
    if 'username' in session:
        sql = "select count(*) from user"
        cur.execute(sql)
        length=cur.fetchone()[0]
        #  a,b 每一页从a 开始显示b条
        sql = "select id,username,level from user limit %s,2" % ((page-1)*2)
        cur.execute(sql)
        res = cur.fetchall()
        pages = range(1, math.ceil(length/2)+1)
        return render_template("/blue-master/listuser.html", data=res, pages=pages, now=page)
    else:
        return redirect(url_for("login"))
# 修改
@app.route("/openedituser<id>_<username>")
def openedituser(id,username):
    if 'username' in session and session['level']==1:
        return render_template("/blue-master/edituser.html",id=id,username=username)
@app.route("/edituser",methods=['post'])
def edituser():
    if 'username' in session and session['level'] == 1:
        id=request.form['id']
        username = request.form['username']
        mpass=request.form['mpass'] #原始密码
        newpass=request.form['newpass'] #新密码

        s = hashlib.md5()
        s.update(mpass.encode())
        mpass = s.hexdigest()
        sql="select password from user where id=%s"%id
        cur.execute(sql)
        res=cur.fetchone()[0]

        if res==mpass:
            h = hashlib.md5()
            h.update(newpass.encode())
            newpass = h.hexdigest()
            sql="update user set password='%s' where id=%s"%(newpass,id)
            cur.execute(sql)
            db.commit()
            return redirect(url_for("tips",state="yes",href="listuser1",time=3))
        else:
            return redirect(url_for("tips",state="no",href="openedituser%s_%s"%(id,username),time=3))
#  删除
@app.route("/deluser<name>")
def deluser(name):
    if name != "admin":#超级管理员不能删除
        try:
            sql = "delete from users where username='%s'" % (name)
            cur.execute(sql)
            db.commit()
            return redirect(url_for("tips", state="yes", href="listuser1", time=3))
        except:
            db.rollback()#数据回滚 提交错误时 返回到提交时
            return redirect(url_for("tips",state="no",href="listuser1",time=3))
    else:
        return redirect(url_for("tips", state="no", href="listuser1", time=3))


@app.route("/openpcategory")
def openpcategory():
    sql = "select id,name from pcategory  "
    cur.execute(sql)
    res = cur.fetchall()
    return render_template("/blue-master/addpcategory.html",data=res)
# 添加产品分类
@app.route("/addpcategory",methods=['post'])
def addpcategory():
    name=request.form['name']
    sql="insert into pcategory (name) values ('%s')"%name
    cur.execute(sql)
    db.commit()
    sql="select id from pcategory where name='%s'"%name
    cur.execute(sql)
    id=cur.fetchone()[0]
    rep={'info':'ok','id':id}
    print(rep)
    return jsonify(rep)

# 判断添加蔬菜种类不重复
@app.route("/selectpcategory",methods=['post'])
def selectpcategory():
    name = request.form['name']
    sql="select count(*) from pcategory where name='%s'"%name
    cur.execute(sql)
    length = cur.fetchone()[0]
    print(length)
    if length>0:
        return "no"
    else:
        return "yes"

# 打开修改页面
@app.route("/openeditpcategory<id>_<name>")
def openeditpcategory(id,name):
    return render_template("/blue-master/editpcategory.html",id=id,name=name)
# 修改种类名称
@app.route("/editpcategory",methods=['post'])
def editpcategory():
    id=request.form['id']
    name=request.form['name']
    newname = request.form['newname']
    sql = "update pcategory set name='%s' where name='%s'" % (newname,name)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("tips", state="yes", href="openpcategory", time=3))
#  删除产品种类/数据库
# @app.route("/delpcategory<name>")
# def delpcategory(name):
#     try:
#         sql="delete from pcategory where name='%s'"%name
#         cur.execute(sql)
#         db.commit()
#     except:
#         db.rollback()  #回滚，出现错误信息的时候回滚到出错之前
#         return redirect(url_for("tips",state="no", href="openpcategory", time=3))
#     return redirect(url_for("tips",state="yes",href="openpcategory",time=3))
# 删除产品分类 ajax方式
@app.route("/delpcategory",methods=['post'])
def delpcategory():
    id = request.form['id']
    print(id)
    sql="delete from pcategory where id='%s'"%id
    cur.execute(sql)
    db.commit()
    return "ok"

# 产品管理:打开添加产品页面，获取产品分类
@app.route("/openaddpcategory")
def openaddpcategory():
    sql="select * from pcategory"
    cur.execute(sql)
    db.commit()
    res=cur.fetchall()
    return render_template("/blue-master/addcategory.html",data=res)
# 产品管理：添加产品，插入到数据库
@app.route("/addcategory",methods=['post'])
def addcategory():
    imgurl = request.form['imgurl1']
    name = request.form['title']
    star = request.form['star']
    cid = request.form['cid']
    con = request.form['con']
    sql = "insert into category (imgurl,name,star,cid,con) values('%s','%s',%s,%s,'%s')"%(imgurl,name,star,cid,con)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("tips", state="yes", href="openaddpcategory", time=3))
# 查看产品列表
@app.route("/listcategory<page>")
def listcategory(page):
    page = int(page)
    sql = "select count(*) from category"
    cur.execute(sql)
    length=cur.fetchone()[0]
    sql="select category.*,pcategory.name from category left join pcategory on category.cid=pcategory.id order by category.id desc limit %s,2" % ((page-1)*2)
    cur.execute(sql)
    res = cur.fetchall()
    print(sql)
    print(res)
    pages = range(1, math.ceil(length/2)+1)
    return render_template("/blue-master/listpcategory.html", data=res, pages=pages, now=page)

#  删除某个产品
@app.route("/delcategory<name>")
def delcategory(name):
    try:
        sql="delete from category where name='%s'"%name
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()  #回滚，出现错误信息的时候回滚到出错之前
        return redirect(url_for("tips",state="no", href="listcategory1", time=3))
    return redirect(url_for("tips",state="yes",href="listcategory1",time=3))
# 打开修改产品详情页面
@app.route("/openeditcategory<id>_<name>")
def openeditcategory(id,name):
    sql = "select * from pcategory"
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    return render_template("/blue-master/editcategory.html",id=id,name=name,data=res)
# 修改产品详情页
@app.route("/editcategory",methods=['post'])
def editcategory():
    id = request.form['id']
    print(id)
    name = request.form['title']
    imgurl = request.form['imgurl1']
    con=request.form['con']
    cid=request.form['cid']
    sql = "update category set name='%s',imgurl='%s',con='%s',cid=%s where id=%s" % (name,imgurl,con,cid,id)
    print(sql)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("tips", state="yes", href="openeditcategory%s_%s"%(id,name), time=3))
@app.route("/uploadPimg",methods=['post'])
def uploadPimg():
    f=request.files['imgurl']
    imgurl="static/upload/img/"+f.filename
    print(imgurl)
    f.save(imgurl)
    rep={'info':'ok','imgurl':'/'+imgurl}
    return jsonify(rep)
# 打开新闻
@app.route("/opennewscategory")
def opennewscategory():
    sql = "select id,name from newscategory  "
    cur.execute(sql)
    res = cur.fetchall()
    return render_template("/blue-master/addnewscategory.html",data=res)
# 添加新闻种类
@app.route("/addnewscategory",methods=['post'])
def addnewscategory():
    name=request.form['name']
    sql="insert into newscategory (name) values ('%s')"%name
    cur.execute(sql)
    db.commit()
    sql="select id from newscategory where name='%s'"%name
    cur.execute(sql)
    id=cur.fetchone()[0]
    rep={'info':'ok','id':id}
    print(rep)
    return jsonify(rep)
# 判断添加新闻种类不重复
@app.route("/selectnewscategory",methods=['post'])
def selectnewscategory():
    name = request.form['name']
    sql="select count(*) from newscategory where name='%s'"%name
    cur.execute(sql)
    length = cur.fetchone()[0]
    print(length)
    if length>0:
        return "no"
    else:
        return "yes"
# 打开修改新闻种类页面
@app.route("/openeditnewscategory<id>_<name>")
def openeditnewscategory(id,name):
    return render_template("/blue-master/editnewscategory.html",id=id,name=name)
# 修改新闻种类
@app.route("/editnewscategory",methods=['post'])
def editnewscategory():
    id=request.form['id']
    name=request.form['name']
    newname = request.form['newname']
    sql = "update newscategory set name='%s' where name='%s'" % (newname,name)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("tips", state="yes", href="opennewscategory", time=3))
# 删除新闻分类 ajax方式
@app.route("/delnewscategory",methods=['post'])
def delnewscategory():
    id = request.form['id']
    print(id)
    sql="delete from newscategory where id='%s'"%id
    cur.execute(sql)
    db.commit()
    return "ok"
# 打开添加新闻页面
@app.route("/openaddnews")
def openaddnews():
    sql="select * from newscategory"
    cur.execute(sql)
    db.commit()
    res=cur.fetchall()
    return render_template("/blue-master/addnews.html",data=res)
# 添加新闻
@app.route("/addnews",methods=['post'])
def addnews():
    imgurl = request.form['imgurl1']
    name = request.form['title']
    cid = request.form['cid']
    con = request.form['con']
    before = request.form['before']
    next=request.form['next']
    sql = "insert into news (imgurl,name,cid,con,before,next) values ('%s','%s',%s,'%s','%s','%s')"%(imgurl,name,cid,con,before,next)
    print(sql)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("tips", state="yes", href="openaddnews", time=3))
# 新闻图片
@app.route("/uploadNewsimg",methods=['post'])
def uploadNewsimg():
    f=request.files['imgurl']
    imgurl="static/upload/newsimg/"+f.filename
    print(imgurl)
    f.save(imgurl)
    rep={'info':'ok','imgurl':'/'+imgurl}
    return jsonify(rep)
# 查看新闻列表
@app.route("/listnews<page>")
def listnews(page):
    page = int(page)
    sql = "select count(*) from news"
    cur.execute(sql)
    length=cur.fetchone()[0]
    sql="select news.*,newscategory.name from news left join newscategory on news.cid=newscategory.id order by news.id desc limit %s,2" % ((page-1)*2)
    cur.execute(sql)
    res = cur.fetchall()
    pages = range(1, math.ceil(length/2)+1)
    return render_template("/blue-master/listnews.html", data=res, pages=pages, now=page)
# 删除新闻
#  删除某个产品
@app.route("/delnews<name>")
def delnews(name):
    try:
        sql="delete from news where name='%s'"%name
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()  #回滚，出现错误信息的时候回滚到出错之前
        return redirect(url_for("tips",state="no", href="listnews1", time=3))
    return redirect(url_for("tips",state="yes",href="listnews1",time=3))
# 打开修改产品详情页面
@app.route("/openeditnews<id>_<name>")
def openeditnews(id,name):
    sql = "select * from newscategory"
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    return render_template("/blue-master/editnews.html",id=id,name=name,data=res)
# 修改新闻详情页
@app.route("/editnews",methods=['post'])
def editnews():
    id = request.form['id']
    print(id)
    name = request.form['title']
    imgurl = request.form['imgurl1']
    con=request.form['con']
    cid=request.form['cid']
    print(cid)
    sql = "update news set name='%s',imgurl='%s',con='%s',cid=%s where id=%s" % (name,imgurl,con,cid,id)
    print(sql)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("tips", state="yes", href="openeditnews%s_%s"%(id,name), time=3))
# 联系我们 客户列表
@app.route("/listcontact")
def listcontact():
    sql = "select * from contact"
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    return render_template("/blue-master/listname.html",data=res)
# 删除用户列表
@app.route("/delcontact")
def delcontact():
    sql = "select * from contact"
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    return render_template("/blue-master/listname.html",data=res)
if __name__ == '__main__':
        app.run(debug=True)
        # debug=True 自动调适程序