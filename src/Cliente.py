import socket,sys,threading

"""
Funcion manejaOut(sock):
    Maneja la salida de la instancia sock de Socket.
    @param sock : instancia de Sock, en donde se enviara según lo que escriba el
                  cliente.
"""

def manejaOut(sock):
    while True:
        msg = str(input(""))
        sock.sendall(bytes(msg,"utf-8"))
        if msg == "DISCONNECT":
            break

"""
Funcion manejaIn(sock):
    Escucha la entrada de la instancia sc de Socket.
    Todo lo recivido se imprimira en la pantalla.
    @param sc : instancia de Sock
"""

def manejaIn(sc):
    while True:
        data = str(sc.recv(1024),'utf-8')
        if(data == "DISCONNECTING"):
            break
        elif not data:
            break
        else:
            print(data)

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print("Especifica el host y el puerto en donde se establecera la comunicación")
        sys.exit(-1)
    sc = socket.socket()
    host = str(sys.argv[1])
    port = int(sys.argv[2])
    sc.connect((host,port))
    salida_thread = threading.Thread(target=manejaOut,args=(sc,))
    entrada_thread = threading.Thread(target=manejaIn,args=(sc,))
    salida_thread.start()
    entrada_thread.start()
    