from socket import *
import sys
import os

def create404(data):
    httpHeader = 'HTTP/1.1 404 Not Found\r\n'
    httpHeader += 'Content-Type: text/html; charset=UTF-8\r\n'
    print('RESPONSE HEADER FROM PROXY TO CLIENT')
    print(httpHeader)
    print('END OF HEADER\n')
    httpHeader += '\r\n\r\n'
    httpHeader += data
    return httpHeader




if len(sys.argv) <= 1:
    print ('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    # sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
serverPort = 12000
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(("", serverPort))
tcpSerSock.listen(1)
print("Socket is listening..")
while 1:
    while 1:
        # Start receiving data from the client
        print ('\n\nReady to serve...')
        tcpCliSock, addr = tcpSerSock.accept()
        print ('Received a connection from:', addr)
        message = tcpCliSock.recv(1024)
        print(message)
        if message == b'':
            print("The given message is empty!")
            break
        # Extract the filename from the given message
        # print(message[0].split()[1].decode("utf-8"))
        # filename = message[0].split()[1].decode("utf-8").split("/")[-1]
        if message != b'':
            filename = message.split()[1].decode("utf-8").rpartition("/")[2]
            hostn= message.split()[4].decode("utf-8")
            url = message.split()[1].decode("utf-8")
        print("URL: "+ url)
        print("hostname: "+ hostn)
        print("filename: "+ filename)
        fileExist = "false"
        filetouse = "./cache/" + filename
        print(" ")
        with open('blockedUrls.txt') as f:
            for line in f:
                # print(line)
                if url in line:
                    print("Blocked URL!!")
                    flag=0
                    break
                else:
                    flag=1
        if flag==0:
            break
        print("file to use: "+ filetouse)
        try:
            # Check wether the file exist in the cache
            # print(filetouse[1:])
            f = open(filetouse[1:], "rb")
            print(f)
            # print(os.listdir("."))
            outputdata = f.readlines()
            fileExist = "true"
            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send(b'HTTP/1.1 200 OK\r\n')    
            tcpCliSock.send(b'Content-Type:text/html\r\n')
            # Fill in start.
            # Fill in end.
            print ('Read from cache')
            for line in outputdata:
                tcpCliSock.send(line)  
            f.close()
            # Error handling for file not found in cache
        except IOError:
                try:
                    if fileExist == "false":
                        # Create a socket on the proxyserver
                        c =  socket(AF_INET, SOCK_STREAM) # Fill in start. # Fill in end.
                        print(hostn)
                        
                        # Connect to the socket to port 80
                        # Fill in start.
                        c.connect((hostn, 80))
                        
                        # Fill in end.
                        # Create a temporary file on this socket and ask port 80 for the file requested by the client
                        fileobjwrite = c.makefile('w',None)
                        #request
                        # fileobjwrite.write("GET "+"http://" + hostn + " HTTP/1.0\n\n")
                        fileobjwrite.write("GET "+message.split()[1].decode("utf-8") + " HTTP/1.0\n\n")
                        # Read the response into buffer
                        # Fill in start.
                        fileobjwrite.close()
                        #read response
                        fileobj = c.makefile('rb',None)
                        buff = fileobj.readlines()
                        #print(buff)
                        # Fill in end.
                        # Create a new file in the cache for the requested file.
                        # Also send the response in the buffer to client socket and the corresponding file in the cache
                        File = open( './cache/'+filename,"wb+")
                        # Fill in start.

                        for line in buff:                                                    
                            File.write(line);                                               
                            tcpCliSock.send(line)
                        File.close()
                        c.close()
                        # Fill in end.
                except:
                    print("Illegal request")
        else:
                print('connection blocked')
                tcpCliSock.close()
                sys.exit("congrats")
    else:
        ...
        # HTTP response message for file not found
        # Fill in start.
        tcpCliSock.send("HTTP/1.0 404 sendError\r\n")                             
        tcpCliSock.send("Content-Type:text/html\r\n")
        # Fill in end.
        # Close the client and the server sockets
        tcpCliSock.close()
        print("socket closed")