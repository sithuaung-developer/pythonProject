
import socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host= " " #enter ip address
port= 8573 #desired port no

s.bind((host,port))
s.listen(1)

con,addr=s.accept()
print("connected with", addr)


    
while True:
    messg=input("send message to client: ")
    con.send(messg.encode("utf-8"))
    print("waiting for response")
    
    c_messg=con.recv(1024)
    print("message from client: ",c_messg.decode("utf-8"))

    messg = ""
    c_messg=""
    another = input("Do you still want to send again : y/n : ")
    if another == "y":
        continue
    elif another == "n":
        messg="Path,disconnect"
        con.send(messg.encode("utf-8"))
        break
    else:
        messg="Path,disconnect"
        con.send(messg.encode("utf-8"))
        break
con.close()
