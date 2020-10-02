import requests
import dbconnect
import subprocess
import psutil
import time
import socket
data = dbconnect.getcentercode()
centercode=data[0]
zonecode=data[1]
myurl = 'http://hardwarenkid.com/rest/'
def Callshutdown(): 
    subprocess.call(['shutdown','0'])
def Autosendreport():    
    try:        
        s = requests.get(url='http://localhost/autosendreport.php',params={'report':1},timeout=1)        
    except:
        pass
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
def Sendrequest():
    ipv4 = get_ip_address()    
    cpu = psutil.cpu_percent()       
    mem = psutil.virtual_memory().percent      
    temp1 = psutil.sensors_temperatures()
    temp=temp1['cpu-thermal'][0][1]
    uptime = time.time() -psutil.boot_time()
    mydata={"temperture":temp,"usage":cpu,"memory":mem,"uptime":uptime,"centercode":centercode,"zonecode":zonecode,"ipv4":ipv4}
    try:       
        d = requests.post(url = myurl,data=mydata,auth=('admin','tini123'),timeout=1)
        data = d.json()        
        if len(data['sql'])>0:
            if data['centercode'] == centercode and data['zonecode']==zonecode:
                rs=dbconnect.excutemyquery(data['sql'])
        if len(data['command'])>0:
            if data['command'] =='reboot':
               subprocess.run("reboot")
            if data['command'] =='shutdown':
               Callshutdown()
    except:
        pass