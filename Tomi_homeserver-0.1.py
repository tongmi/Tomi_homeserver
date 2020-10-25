#Import some modules.
import sys,os,socket,time,json

#Initialize logs.
if os.path.exists("logs")==True:
    if os.path.isdir("logs")==False:
        os.mkdir("logs")
else:
    os.mkdir("logs")
logs_name=time.strftime(r"logs/"+"%Y-%m-%d_%H-%M-%S.log", time.localtime())
logs=open(logs_name,"w+")

#Initialize the vars.
Program_name="Tomi_homeserver"
Program_version=0.1
information_backup={"hostname":"localhost","port":31317,"version":0}
information={"hostname":"localhost","port":31317,"version":0}
keys=list(information.keys())
server_tcp_listen=5
server_mode=socket.SOCK_STREAM
server=socket.socket(socket.AF_INET,server_mode)

#Help information var define.
help_infomation="""

Tomi_homeserver 0.1 Help

选项：
-h/-help/-Help      获取帮助.
-v/-version/-Version        获取版本信息
-hostname/-h/-ip <hostname>     修改使用的主机名（不修改config.json的配置）
-port/-Port/-p <port>     修改使用的端口（不修改config.json的配置）

"""

#Initialize the program.
def init():
    #Helpful infomation and information of the version.
    for i in range(0,len(sys.argv)):
        if sys.argv[i]=="-h" or sys.argv[i]=="-help" or sys.argv[i]=="-Help":
            info(help_infomation)
            os._exit(0)
        if sys.argv[i]=="-v" or sys.argv[i]=="-version" or sys.argv[i]=="-Version":
            info(Program_name+" "+str(Program_version))
            os._exit(0)
    #Print some infomation before initializing.
    info("The programs started,initializing...")
    #Import some objects.
    global information,keys,information_backup,server,server_mode,server_tcp_listen
    #Initialize config.json file.
    if os.path.exists("config.json")==True:
        if os.path.isfile("config.json")==True:
            with open("config.json","r") as f:
                try:
                    information=json.load(f)
                except:
                    information={}
        else:
            err("Please remove the directory \'config.json\'.")
            os._exit(0)
    else:
        with open("config.json","w") as f:
            json.dump(information,f)
            info("Initialized config.json.")
    #Check infomation.
    keys_now=list(information.keys())
    for i in keys:
        if (i in keys_now) == False:
            information=information_backup
            with open("config.json","w") as f:
                json.dump(information,f)
            warn("Config was reset.Because the config was not correct.")
            break
    #Reset some configs and be for some helps.
    for i in range(0,len(sys.argv)):
        if sys.argv[i]=="-hostname" or sys.argv[i]=="-h" or sys.argv[i]=="-ip":
            information["hostname"]=sys.argv[i+1]
            info("Reset the hostname("+sys.argv[i+1]+") successfully.")
        if sys.argv[i]=="-port" or sys.argv[i]=="-Port" or sys.argv[i]=="-p":
            try:
                information["port"]=int(sys.argv[i+1])
                info("Reset the port("+sys.argv[i+1]+") successfully.")
            except:
                err("The port("+sys.argv[i+1]+") was not correct.Please reset.")
                os._exit(0)
    #Initialize the socket of server.
    try:
        server.bind((information["hostname"],information["port"]))
    except socket.gaierror:
        err("The hostname("+str(information["hostname"])+") was not correct.")
        os._exit(0)
    except OSError:
        err("The port("+str(information["port"])+") may be used.Please edit \'config.json\' to reset or free the port.")
        os._exit(0)
    else:
        info("The server("+information["hostname"]+") was running at the port "+str(information["port"])+".")
    if server_mode==socket.SOCK_DGRAM:
        pass
    else:
        server.listen(server_tcp_listen)

#Define some functions.
def info(str):
    global logs
    out=time.strftime("%Y-%m-%d %H:%M:%S"+" [Info]:"+str+"\n",time.localtime())
    print(out,end="")
    logs.write(out)
    logs.flush()
def warn(str):
    global logs
    out=time.strftime("%Y-%m-%d %H:%M:%S"+" [Warning]:"+str+"\n",time.localtime())
    print(out,end="")
    logs.write(out)
    logs.flush()
def err(str):
    global logs
    out=time.strftime("%Y-%m-%d %H:%M:%S"+" [Error]:"+str+"\n",time.localtime())
    print(out,end="")
    logs.write(out)
    logs.flush()
def connected(addr):
    global logs
    out=time.strftime("%Y-%m-%d %H:%M:%S"+" "+addr[0]+" "+str(addr[1])+" has connected."+"\n",time.localtime())
    print(out,end="")
    logs.write(out)
    logs.flush()

#Main codes.
init()
while True:
    c,addr=server.accept()
    connected(addr)
    send_info=time.strftime("It is %Y-%m-%d %H:%M:%S now.", time.localtime())
    c.send(send_info.encode("utf-8"))
    c.close()


