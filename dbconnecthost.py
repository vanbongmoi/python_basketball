import mysql.connector
import datetime
def Savereporthost(ctcode,zcode,score,ticket):
    mydbh = mysql.connector.connect(
        host = '103.130.216.111',
        user = 'hardware_tini',
        passwd='tiniworld1@3',
        database='hardware_nkidiot'
    )
    mycusorh = mydbh.cursor()
    sqlh = 'insert into basketballreport (playday,score,ticket,centercode,zonecode) values(%s,%s,%s,%s,%s)'
    valh = (datetime.datetime.now(),score,ticket,ctcode,zcode)
    mycusorh.execute(sqlh,valh)
    mydbh.commit()
    return 1
#Savereporthost('3333','vbvbvb',40,15)