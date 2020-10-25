#Import some modules.
import sys,os,socket,time,json,_thread

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
Program_ssh=False
Program_ssh_password="123456"
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
-ssh/-s/-S      启用远程ssh连接服务器

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
    global information,keys,information_backup,server,server_mode,server_tcp_listen,Program_ssh
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
        if sys.argv[i]=="-ssh" or sys.argv[i]=="-s" or sys.argv[i]=="-S":
            Program_ssh=True
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
    #If ssh service is on,run this codes.
    if Program_ssh==True:
        _thread.start_new_thread(ssh,())

#Initialize sh mode to run some commands that you send.
def ssh():
    global information
    server_ssh_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_ssh_socket.bind((information["hostname"],information["port"]+1))
    server_ssh_socket.listen(server_tcp_listen)
    info("Ssh service of the server("+information["hostname"]+") was running at the port "+str(information["port"]+1)+".")
    while True:
        c,addr=server_ssh_socket.accept()
        connected_admin_connected(addr)
        c.send("Please send the admin password to the server！(UTF-8)".encode("utf-8"))
        recv_password=c.recv(1024).decode("utf-8")
        if recv_password==Program_ssh_password:
            connected_admin_logined(addr)
            c.send("Login successful.You can send some commands to the server and the server will run this codes.Type \'exit\' can cut the connecting.(UTF-8)".encode("utf-8"))
            while True:
                recv_code=c.recv(1029).decode("utf-8")
                if recv_code=="exit":
                    connected_admin_exit(addr)
                    break
                exec(recv_code)
        else:
            connected_admin_loginfail(addr,recv_password)
            c.send("Password error.Cut the connecting.".encode("utf-8"))
            c.close()

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
def connected_admin_connected(addr):
    global logs
    out=time.strftime("%Y-%m-%d %H:%M:%S"+" The admin "+addr[0]+" "+str(addr[1])+" has connected."+"\n",time.localtime())
    print(out,end="")
    logs.write(out)
    logs.flush()
def connected_admin_logined(addr):
    global logs
    out=time.strftime("%Y-%m-%d %H:%M:%S"+" The admin "+addr[0]+" "+str(addr[1])+" has login."+"\n",time.localtime())
    print(out,end="")
    logs.write(out)
    logs.flush()
def connected_admin_loginfail(addr,recv_password):
    global logs
    out=time.strftime("%Y-%m-%d %H:%M:%S"+" The admin "+addr[0]+" "+str(addr[1])+" login failed.He typed password is \'"+recv_password+"\'.\n",time.localtime())
    print(out,end="")
    logs.write(out)
    logs.flush()
def connected_admin_exit(addr):
    global logs
    out=time.strftime("%Y-%m-%d %H:%M:%S"+" The admin "+addr[0]+" "+str(addr[1])+" exited."+"\n",time.localtime())
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


