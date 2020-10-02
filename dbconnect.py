import mysql.connector
import datetime
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'tini',
    passwd='tini123',
    database='tnpbasketball'
    )
mycusor = mydb.cursor()
def excutemyquery(sql):
    mycusor.execute(sql)
    mydb.commit()
    return 1

def getallconfig():
    lsconfig = []
    sql = 'select * from Config'
    mycusor.execute(sql)
    myresult = mycusor.fetchall()
    for rs in myresult:
        lsconfig.append(rs)
    return lsconfig
def getcentercode():
    lscofig=''
    sql = 'select centercode,zonecode from Config'
    mycusor.execute(sql)
    myresult = mycusor.fetchall()
    for rs in myresult:
        lsconfig =rs
    return lsconfig
def Gethighscore():
    highscore = 0
    sql = 'select max(score) as highscore from Report'
    mycusor.execute(sql)
    myresult = mycusor.fetchall()
    mycount = myresult[0][0]
    if mycount>0:
        hscore = myresult[0][0]
        if hscore>0:
            highscore = hscore
        else:
            highscore = 0
    return highscore
def Savereport(ctcode,zcode,score,ticket):
    dt = datetime.datetime.now()
    #current = dt.strftime('%x')    
    sql = 'insert into Report (playday,score,ticket,centercode,zonecode) values(%s,%s,%s,%s,%s)'
    val = (dt,score,ticket,ctcode,zcode)
    mycusor.execute(sql,val)
    mydb.commit()
    return 1