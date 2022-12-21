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
tcpSerSock.listen(5)
print("Socket is listening..")
while 1:
    # Start receiving data from the client
    print ('\n\nReady to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('Received a connection from:', addr)
    message = tcpCliSock.recv(1048576)
    print(message)
    # Extract the filename from the given message
    # print(message[0].split()[1].decode("utf-8"))
    # filename = message[0].split()[1].decode("utf-8").split("/")[-1]
    filename = message.split()[1].decode("utf-8").rpartition("/")[2]
    # message[0].split()[1].decode("utf-8").split("/")[1]
    print("########")
    # hostname=message[0].split()[1].decode("utf-8").split("/")[1].split(".")[1:]
    # hostname='.'.join(hostname)
    # hostname=message[0].split()[1].decode("utf-8").split("/")[2]
    hostn= message.split()[4].decode("utf-8")
    print("hostname: "+ hostn)
    print("filename: "+ filename)
    fileExist = "false"
    filetouse = "./cache/" + filename
    print(" ")
    print("file to use: "+filetouse)
    # if filename in os.listdir("."):
    #     f=open(filename,"r")
    #     print(f)
    try:
        # Check wether the file exist in the cache
        # print(filetouse[1:])
        f = open(filetouse, "rb")
        # f=open(filename,"r")
        print(f)
        # print(os.listdir("."))
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(b'HTTP/1.1 200 OK\r\n')    
        tcpCliSock.send(b'Content-Type:text/html\r\n')
        print("Ba3atna el response")
        # Fill in start.
        # Fill in end.
        print ('Read from cache')
        for line in outputdata:
            tcpCliSock.send(line)  
        # for i in range(0, len(outputdata)):
        #     tcpCliSock.send(bytes(outputdata[i],"utf-8"))
        #     print("The output data is: " + outputdata[i])
        #     print ('Read from cache')
        f.close()
        # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM) 
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn,80))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                print("premake")
                fileobjwrite = c.makefile('w', None)
                fileobjwrite.write("GET "+"http://" + hostn + " HTTP/1.0\n\n")
                fileobjwrite.close()
                print("postmake")
                # Read the response into buffer
                # Fill in start.
                # Fill in end.
                # Create a new file in the cache for the requested file.
                fileobj=c.makefile('rb', None)
                buff = fileobj.readlines()
                print(buff)
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./cache/" + filename,"wb+")
                for line in buff:
                    tmpFile.write(line)
                    tcpCliSock.send(line) 
                # Fill in start.
                tmpFile.close()
                c.close()
                # Fill in end.
            except:
                print ("Illegal request")
                # print(os.listdir("."))
        else:
            print("HTTP response Not found")
            create404()
            # HTTP response message for file not found
            # Fill in start.
            # Fill in end.
            # Close the client and the server sockets
    tcpCliSock.close()
            # Fill in start.
            # Fill in end