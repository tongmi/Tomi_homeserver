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

#Initialize the program.
def init():
    #Print some infomation.
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
            info("Config reset.Because the config was not correct.")
            break
    #Initialize the socket of server.
    try:
        server.bind((information["hostname"],information["port"]))
    except:
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


