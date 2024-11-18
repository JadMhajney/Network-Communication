from socket import *
import sys
import errno

def start_client():
    host = '127.0.0.1' #host is localhost
    port = 1337
    if len(sys.argv)==3:
        host=sys.argv[1]
        port=(int)(sys.argv[2]) 
    elif len(sys.argv)==2:
        if is_integer(sys.argv[1]): # if its only port 
            print_error("invalid input")
        else:
            host=sys.argv[1]
    
    try:
        with socket.socket(AF_INET , SOCK_STREAM) as clientSoc:
            clientSoc.connect((host , port))
            print(clientSoc.recv(23).decode())
            
            while(True):
                #check format
                user_name = input()
                if("User: " in user_name):
                    if(len(user_name.split(' '))==2):
                        clientSoc.send(user_name.encode())
                    else:
                        print_error("failed to login")
                        continue
                password = input()
                if("Password: " in user_name):
                    if(len(user_name.split(' '))==2):
                        clientSoc.send(user_name.encode())
                    else:
                        print_error("failed to login")
                        continue
                else:
                    print_error("failed to login")
                    continue
                msg=clientSoc.recv(1024).decode()
                print(msg)
                if(msg=="failed to login"):
                    continue
                elif("good to see you" in msg):
                    break
            

            while True :
                func=input()
                clientSoc.send(func.encode())
                response=clientSoc.recv(1024).decode()
                if(response=="quit"):
                    return 
                print(response)

                
                      
    except :
        print_error("an error has occured")
    

    



def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def print_error(message):
    print(message)


if __name__ == '__main__':
    start_client()