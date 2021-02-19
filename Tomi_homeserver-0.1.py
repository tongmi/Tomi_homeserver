#!/bin/python3
# -*- coding: UTF-8 -*-
# Import some modules.
import sys
import os
import socket
import time
import json
import threading
import shutil
# ERROR_CODE
NO_ERROR = 0
UNABLE_TO_DO = -1

# Initialize the vars.
Started_Time = time.time()
Program_name = "Tomi_homeserver"
Program_version = 0.1
Program_logs = True
Program_ssh = False
Program_plugins = True
Program_ssh_password = "031317"
information_backup = {"hostname": "0.0.0.0", "port": 31313, "version": 0}
information = information_backup
keys = list(information.keys())
server_tcp_listen = 5
server_mode = socket.SOCK_STREAM
server = socket.socket(socket.AF_INET, server_mode)
loaded_plugins = []

# Help information var define.
help_infomation = """

Tomi_homeserver 0.1 Help

选项：
-h/-help/-Help      获取帮助.
-v/-version/-Version        获取版本信息
-hostname/-h/-ip <hostname>     修改使用的主机名（不修改config.json的配置）
-port/-Port/-p <port>     修改使用的端口（不修改config.json的配置）
-ssh/-s/-S      启用远程ssh连接服务器
-unlog/-ul      关闭日志流(实验功能)
-unplugin/-upg   关闭插件功能(实验功能)

"""

# Define classes


class socket_server:
    error = NO_ERROR
    hostname = ""
    port = 520
    listen = 5
    mode = socket.SOCK_STREAM
    server = None
    server_is_running = False

    def __init__(self, ip="", p=520, lis=5, m=socket.SOCK_STREAM):
        self.hostname = ip
        self.port = p
        self.listen = lis
        self.mode = m
        try:
            self.server = socket.socket(socket.AF_INET, self.mode)
            self.server.bind((self.hostname, self.port))
            self.server.listen(self.listen)
            self.server_is_running = True
        except Exception as buf:
            self.error = UNABLE_TO_DO
            err(str(buf))

    def __del__(self):
        self.close()

    def close(self):
        if self.server_is_running is True:
            self.server.close()
            self.server_is_running = False
            return NO_ERROR
        else:
            return UNABLE_TO_DO


class socket_client:
    error = NO_ERROR
    hostname = ""
    port = None
    mode = socket.SOCK_STREAM
    client = None
    client_is_running = False

    def __init__(self, ip="", p=None, m=socket.SOCK_STREAM):
        self.mode = m
        try:
            self.client = socket.socket(socket.AF_INET, self.mode)
            if type(p) == int:
                self.client.bind((self.hostname, self.port))
            self.client_is_running = True
            self.hostname, self.port = self.client.getsockname()
        except Exception as buf:
            self.error = UNABLE_TO_DO
            err(str(buf))

    def __del__(self):
        self.close()

    def close(self):
        if self.client_is_running is True:
            self.client.close()
            self.client_is_running = False
            return NO_ERROR
        else:
            return UNABLE_TO_DO


class thread_server_ssh(threading.Thread):
    def run(self):
        ssh()

# Define some kernel functions.


def info(_str):
    str_type = if_main_thread()+"/"+"INFO"
    write_screen(str_type, "\033[1;32m" + _str + "\033[0m")

def info_nc(_str):
    str_type = if_main_thread()+"/"+"INFO"
    write_screen(str_type, _str)


def warn(_str):
    str_type = if_main_thread()+"/"+"WARN"
    write_screen(str_type, "\033[1;33m" + _str + "\033[0m")


def warn_nc(_str):
    str_type = if_main_thread()+"/"+"WARN"
    write_screen(str_type, _str)


def err(_str):
    str_type = if_main_thread()+"/"+"ERROR"
    write_screen(str_type, "\033[1;31m" + _str + "\033[0m")

def err_nc(_str):
    str_type = if_main_thread()+"/"+"ERROR"
    write_screen(str_type, _str)



def if_main_thread():
    if threading.current_thread().name == "MainThread":
        return "Main"
    else:
        return "Thread"


def write_screen(str_class, str):
    out = time.strftime("[%H:%M:%S]"+" ["+str_class+"]:"+str+"\n",time.localtime())
    print(out, end="")
    write_logs(out)


def write_logs(string):
    global logs
    if Program_logs is True:
        logs.write(string)
        logs.flush()
        return NO_ERROR
    else:
        return UNABLE_TO_DO

# ---#############CUTING##############---#
def connected_admin_connected(addr):
    out = "The admin "+addr[0]+" "+str(addr[1]) + " has connected."
    info(out)


def connected_admin_logined(addr):
    out = "The admin "+addr[0]+" "+str(addr[1]) + " has login."
    info(out)


def connected_admin_loginfail(addr, recv_password):
    out = "The admin " + addr[0] + " " + str(addr[1]) + " login failed.He typed password is \"" + recv_password + "\"."
    info(out)


def connected_admin_exit(addr):
    out = "The admin "+addr[0] + " "+str(addr[1]) + " exited."
    info(out)
# Helpful infomation and information of the version.


def help_and_so_on():
    global Program_logs
    for i in range(0, len(sys.argv)):
        if sys.argv[i] == "-unlog" or sys.argv[i] == "-ul":
            if Program_logs is True:
                Program_logs = False
        if sys.argv[i] == "-h" or sys.argv[i] == "-help" \
                or sys.argv[i] == "-Help":
            print(help_infomation)
            os._exit(0)
        if sys.argv[i] == "-v" or sys.argv[i] == "-version" or \
                sys.argv[i] == "-Version":
            print(Program_name+" "+str(Program_version))
            os._exit(0)
# Initialize logs.


def start_logs():
    global logs
    if Program_logs is True:
        if os.path.exists("logs") is True:
            if os.path.isdir("logs") is False:
                os.mkdir("logs")
        else:
            os.mkdir("logs")
        logs_name = time.strftime(r"logs/"+"%Y-%m-%d_%H-%M-%S.log", time.localtime())
        logs = open(logs_name, "w+")
        buffer = time.strftime("[%H:%M:%S]" + " [Main/KERNEL]:Create " + "the log \"" + logs_name + "\".\n", time.localtime())
        print(buffer, end="")
        logs.write(buffer)
        logs.flush()
        del buffer
    else:
        print(time.strftime("[%H:%M:%S]"+" [Main/KERNEL]:The stream of logs " + "closed.", time.localtime()))
# Initialize the program.


def init():
    # Print some infomation before initializing.
    info("The programs started,initializing...")
    # Import some objects.
    global information, keys, information_backup, server, server_mode, \
        server_tcp_listen, Program_ssh, Program_plugins, loaded_plugins
    # Initialize config.json file.
    if os.path.exists("config.json") is True:
        if os.path.isfile("config.json") is True:
            with open("config.json", "r") as f:
                try:
                    information = json.load(f)
                except Exception:
                    information = {}
        else:
            err("Please remove the directory \'config.json\'.")
            os._exit(0)
    else:
        with open("config.json", "w") as f:
            json.dump(information, f)
            info("Initialized config.json.")
    # Check infomation.
    keys_now = list(information.keys())
    for i in keys:
        if (i in keys_now) is False:
            information = information_backup
            with open("config.json", "w") as f:
                json.dump(information, f)
            warn("Config was reset.Because the config was not correct.")
            break
    # Reset some configs and be for some helps.
    for i in range(0, len(sys.argv)):
        if sys.argv[i] == "-hostname" or sys.argv[i] == "-h" or \
                sys.argv[i] == "-ip":
            information["hostname"] = sys.argv[i+1]
            info("Reset the hostname("+sys.argv[i+1]+") successfully.")
        if sys.argv[i] == "-port" or sys.argv[i] == "-Port" or \
                sys.argv[i] == "-p":
            try:
                information["port"] = int(sys.argv[i+1])
                info("Reset the port("+sys.argv[i+1]+") successfully.")
            except Exception:
                err("The port(" + sys.argv[i+1] +
                    ") was not correct.Please reset.")
                os._exit(0)
        if sys.argv[i] == "-ssh" or sys.argv[i] == "-s" or sys.argv[i] == "-S":
            Program_ssh = True
        if sys.argv[i] == "-unplugin" or sys.argv[i] == "-upg":
            Program_plugins = False
            info("The plugins function closed.")
    try:
        server.bind((information["hostname"], information["port"]))
    except socket.gaierror:
        err("The hostname("+str(information["hostname"])+") was not correct.")
        os._exit(0)
    except OSError:
        err("The port("+str(information["port"])+") may be used.Please edit \'\
config.json\' to reset or free the port.")
        os._exit(0)
    else:
        info("The server("+information["hostname"] +
             ") was running at the port "+str(information["port"])+".")
    if server_mode == socket.SOCK_DGRAM:
        # Wait...
        pass
    else:
        server.listen(server_tcp_listen)
    # If ssh service is on,run this codes.
    if Program_ssh is True:
        # Wait to be perfect Use the new threads. 2.6
        t_ssh = thread_server_ssh()
        t_ssh.start()
    # Plugins Function
    if Program_plugins is True:
        try:
            shutil.rmtree("./plugins/__pycache__")
            info("Cleaned the \"__pycache__\".")
        except Exception:
            info("Have not cleaned the \"__pycache__\".")
            pass
        try:
            datanames = os.listdir("./plugins")
            for dataname in datanames:
                # 下次加入多线程
                if os.path.splitext(dataname)[1] == '.py' or os.path.splitext(dataname)[1] == '.pyc': # 目录下包含.py .pyc的文件
                    plugin_name = os.path.splitext(dataname)[0]
                    info("Loading the plugin \"" + plugin_name + "\".")
                    try:
                        __import__("plugins." + plugin_name)
                        loaded_plugins.append(plugin_name)
                    except Exception as tmp:
                        err("At the plugin \"" + plugin_name + "\".")
                        err("Error happened: " + str(tmp))
                    continue
                if os.path.splitext(dataname)[1] == '.tomi': # 目录下包含.tomi的文件
                    plugin_name = os.path.splitext(dataname)[0]
                    info("Loading the plugin \"" + plugin_name + "\".")
                    try:
                        with open("./plugins/" + dataname, "r") as f:
                            exec(f.read(-1))
                        loaded_plugins.append(plugin_name)
                    except Exception as tmp:
                        err("At the plugin \"" + plugin_name + "\".")
                        err("Error happened: " + str(tmp))
                    continue
        except Exception:
            warn("No plugins are loaded.")
    info("The server started successfully," + " took " + str(time.time()-Started_Time) +"s!")


# Initialize sh mode to run some commands that you send.
def ssh():
    # Waiting to be perfect. 2021.1.27
    global information
    server_ssh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ssh_socket.bind((information["hostname"], information["port"]+1))
    server_ssh_socket.listen(server_tcp_listen)
    info("Ssh service of the server("+information["hostname"] +
         ") was running at the port "+str(information["port"]+1)+".")
    try:
        while True:
            c, addr = server_ssh_socket.accept()
            connected_admin_connected(addr)
            c.send("Please send the admin password to the server " +
                   "in 30 seconds！(UTF-8)".encode("utf-8"))
            c.settimeout(29.9)
            try:
                recv_password = c.recv(1024).decode("utf-8")
            except Exception:
                c.send("Sorry,timeout.".encode("utf-8"))
                c.close()
                connected_admin_loginfail(addr, "China  NB,timeout")
                continue
            c.settimeout(None)
            if recv_password == Program_ssh_password:
                connected_admin_logined(addr)
                c.send("Login successful.You can send the server codes to run.\
Type \'exit\' can cut the connecting.(UTF-8)".encode("utf-8"))
                while True:
                    # Waiting to be perfect. 2021.2.05 下次加入多线程运行
                    recv_code = c.recv(2048+4).decode("utf-8")
                    info("Command: "+recv_code)
                    if recv_code == "exit":
                        connected_admin_exit(addr)
                        c.close()
                        break
                    try:
                        exec(recv_code)
                    except Exception as buf:
                        err(str(buf))
            else:
                connected_admin_loginfail(addr, recv_password)
                c.send("Password error.Cut the connecting.".encode("utf-8"))
                c.close()
    except KeyboardInterrupt:
        server_ssh_socket.close()
        info("Ssh service is exiting.")
    except Exception as buf:
        server_ssh_socket.close()
        err(buf)
        info("Ssh service is exiting.")


def main():
    help_and_so_on()
    start_logs()
    init()

# Main codes.
if __name__ == "__main__":
    main()
    time.sleep(0.3)
    try:
        while True:
            code = input("tomi>")
            if code == "exit" or code == "Exit" or code == "EXIT":
                raise(KeyboardInterrupt)
            elif code == "list":
                print(loaded_plugins)
            else:
                try:
                    exec(code)
                except Exception as buf:
                    err("语句执行时有错误产生："+str(buf))
    except KeyboardInterrupt:
        server.close()
        info("Program is exiting.")
        os._exit(0)




