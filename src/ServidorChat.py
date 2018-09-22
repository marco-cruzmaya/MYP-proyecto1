import socketserver
import socket
import threading
from threading import Thread, Lock
from Conexion import Conexion
from EventosChat import EventoChat
from Chat import Chat
from Usuario import Usuario
from Room import Room
from Status import Status
import sys


"""
Clase Servidor
    Clase que extiende a las clases ThreadindMixIn y TCPServer del modulo socketserver.
    Esta clase se encarga de conectarse, escuchar las conexiones entrantes y solo llamara
    al método serverforever(), en dondé se manejara los request de las coneciones entrantes.

    Su constructor tiene como parametros el host, port y la clase Handler.
    La clase Handler es necesaria, ya que en la clase Handler se especificara como se 
    manajaran los request de las conexiones, con el método handle()

"""


class Servidor(socketserver.ThreadingMixIn, socketserver.TCPServer): pass

"""
Clase ServidorChatHAndler:
    Clase Handler. En esta clase se especificara el método handle() el cual se encargara de
    todos los request, es decir es dondé se especificara el manejo de conexiones.
    Tiene como variables de clase, una instancia de la clase Chat y una instancia de la
    clase Conexion.
"""
class ServidorChatHandler(socketserver.BaseRequestHandler):
    chat = Chat()
    conexion = None
    """
    Método handle()
        En este método se manejara la conexion. En terminos del proyecto, se manejaran los
        diferentes eventos que se presentar según el protocolo especificado.
    """
    def handle(self):
        print("Connection from ", self.client_address)
        enchufe = self.request
        self.conexion = Conexion(enchufe)
        lock = Lock()
        self.manejaConexion(lock)
    
    """
    Método auxiliar manejaConexion():
        Método donde se manejara cada evento.
    """
    def manejaConexion(self,lock):
        finalizara = False
        identificado = False
        while(not finalizara):
            mensaje = self.manejaMSG()
            if(not identificado):
                if(mensaje[0] == EventoChat.UNKNWON):
                    self.eventoDesconocido()
                elif(mensaje[0] == EventoChat.DISCONNECT):
                    finalizara = True
                    self.desconectar(identificado,lock)
                elif(mensaje[0] == EventoChat.IDENT):
                    if(len(mensaje) > 1):
                        repetido = self.identificar(mensaje[1])
                        if(repetido):
                            identificado = False
                        else:
                            identificado = True
                            lock.acquire()
                            self.chat.añadirCliente(self.conexion)
                            lock.release()
                    else:
                        self.eventoDesconocido()
                else:
                    self.conexion.mandaMSG("...MUST IDENTIFY FIRST\n...TO IDENTIFY: IDENTIFY USERNAME")
            else:
                if(mensaje[0] == EventoChat.UNKNWON):
                    self.eventoDesconocido()
                if(mensaje[0] == EventoChat.IDENT):
                    if(len(mensaje) > 1):
                        lock.acquire()
                        repetido = self.identificar(mensaje[1])
                        lock.release()
                    else:
                        self.eventoDesconocido()
                elif(mensaje[0] == EventoChat.STATUS):
                    if(len(mensaje) > 1):
                        lock.acquire()
                        self.conexion.getUsuario().setState(mensaje[1])
                        self.conexion.mandaMSG(self.conexion.getUsuario().getNombre() + " " + mensaje[1],
                                                    self.chat.getClientes(),"")
                        lock.release()
                    else:
                        self.eventoDesconocido()
                elif(mensaje[0] == EventoChat.USERS):
                    self.conexion.mandaMSG(self.mandarUSERS())
                elif(mensaje[0] == EventoChat.MSG):
                    if(len(mensaje) > 1):
                        self.mandarPrivado(mensaje[1],lock)
                    else:
                        self.eventoDesconocido()
                elif(mensaje[0] == EventoChat.PUBLICMSG):
                    if(len(mensaje) > 1):
                        self.conexion.mandaMSG("...MESSAGE SENT")
                        self.conexion.mandaMSG(mensaje[1],
                                self.chat.getClientes(),self.conexion.getUsuario().getNombre(),"PUBLIC")
                    else:
                        self.eventoDesconocido()
                elif(mensaje[0] == EventoChat.CREATEROOM):
                    if(len(mensaje) > 1):
                        lock.acquire()
                        self.chat.añadirRoom(mensaje[1],[],self.conexion)
                        lock.release()
                        self.conexion.mandaMSG("...ROOM CREATED")
                    else:
                        self.eventoDesconocido()
                elif(mensaje[0] == EventoChat.ROOMSG):
                    if(len(mensaje) > 1):
                        self.mandaMSGRoom(mensaje[1])
                    else:
                        self.eventoDesconocido()
                elif(mensaje[0] == EventoChat.INVITE):
                    if(len(mensaje) > 1):
                        self.invitacion(mensaje[1],lock)
                    else:
                        self.eventoDesconocido()
                elif(mensaje[0] == EventoChat.JOINROOM):
                    if(len(mensaje) > 1):
                        self.joinRoom(mensaje[1],lock)
                    else:
                        self.eventoDesconocido()
                elif(mensaje[0] == EventoChat.DISCONNECT):
                    finalizara = True
                    self.desconectar(identificado,lock)
        self.conexion.mandaMSG("DISCONNECTING...")
                
    """
    Método ManejaMSG():
        Método que se encargara del input del socket del servidor.
        @return Tupla, dondé el primer elemento es el evento especificado por el protocolo.
    """
    def manejaMSG(self):
        mensaje = self.conexion.reciveMSG()
        mensaje = mensaje.strip()
        mensaje = mensaje.split(" ",1)
        evento = EventoChat.get(EventoChat,mensaje[0])
        if(len(mensaje) == 2):
            return (evento,mensaje[1])
        return (evento,)
    
    """
    Método auxiliar eventoDesconocido():
        Método que se encarga de hacerle conocer al cliente que el evento no esta especificado
        en el protocolo.
    """
    
    def eventoDesconocido(self):
        self.conexion.mandaMSG("...INVALID MESSAGE TRY")
        self.conexion.mandaMSG("...VALID MESSAGE ARE:")
        for representacion in EventoChat.listaEventos(EventoChat):
            if(representacion is not None):
                if representacion == "IDENTIFY":
                    self.conexion.mandaMSG("..." + representacion + " NAME")
                elif representacion == "STATUS":
                    self.conexion.mandaMSG("..." + representacion + " ACTIVE/AWAY/BUSY")
                elif representacion == "USERS":
                    self.conexion.mandaMSG("..." + representacion)
                elif representacion == "MESSAGE":
                    self.conexion.mandaMSG("..." + representacion + " USERNAME messageContent")
                elif representacion == "PUBLICMESSAGE":
                    self.conexion.mandaMSG("..." + representacion + " messageContent")
                elif representacion == "CREATEROOM":
                    self.conexion.mandaMSG("..." + representacion + " roomName")
                elif representacion == "INVITE":
                    self.conexion.mandaMSG("..." + representacion + " roomName user1 user2...")
                elif representacion == "JOINROOM":
                    self.conexion.mandaMSG("..." + representacion + " roomName")
                elif representacion == "ROOMESSAGE":
                    self.conexion.mandaMSG("..." + representacion + " roomName messageContent")
                elif representacion == "DISCONNECT":
                    self.conexion.mandaMSG("..."+representacion)
    

    """
    Método auxiliar joinRoom():
        Método auxiliar que se encarga del evento JOINROOM especificado en el protocolo.
        @param room_name: El nombre de la sala al que el cliente se quiere unir.
               lock : Instancia de la clase Lock() del módulo threading, necesaria para
                      poder sincronizar la lista de conexiones la sala.
        
    """
    def joinRoom(self,room_name,lock):
        room = self.chat.getRoom(room_name)
        if room is None:
            self.conexion.mandaMSG("...ROOM NOT EXISTS")
            return
        if(self.conexion in room.getInvitados() and not(self.conexion in room.getUsers())):
            lock.acquire()
            room.agregarUser(self.conexion)
            room.eliminarInvitado(self.conexion)
            lock.release()
            self.conexion.mandaMSG("...SUCCESFULLY JOINED TO ROOM")
        elif(self.conexion in room.getInvitados() and (self.conexion in room.getUsers())):
            lock.acquire()
            room.eliminarInvitado(self.conexion)
            lock.release()
            self.conexion.mandaMSG("...ALREADY EXISTS IN ROOM")
        else:
            self.conexion.mandaMSG("...TOU ARE NOT INVITED TO ROOM "+room.getName())
    
    """
    Método auxiliar invitacion():
        Método auxiliar que se encarga del evento INVITE especificado en el protocolo.
        @param msg: Mensaje donde se sacara el nombre de la sala y el nombre del cliente
                    a quien se le esta invitando.
               lock : Instancia de la clase Lock() del módulo threading, necesaria para
                      poder sincronizar la lista de conexiones de invitados de la sala.
    """
    
    def invitacion(self,msg,lock):
        msg = msg.split(" ")
        room = self.chat.getRoom(msg[0])
        if(room is None):
            self.conexion.mandaMSG("...ROOM NOT EXIST")
            return
        if(room.getCreador() !=  self.conexion):
            self.conexion.mandaMSG("...YOU ARE NOT THE OWNER OF THE ROOM")
            return
        invitado = self.chat.getCliente(msg[1])
        if(invitado is None):
            self.conexion.mandaMSG("...USER " + msg[1] + " NOT FOUND")
            return
        lock.acquire()
        room.agregarInvitado(invitado)
        lock.release()
        nombre = self.conexion.getUsuario().getNombre()
        self.conexion.mandaMSG("...INVITATION SENT TO " + invitado.__repr__())
        self.conexion.mandaMSG("...INVITATION TO JOIN ROOM "+room.getName()+" FROM BY "+nombre,[invitado])
        self.conexion.mandaMSG("...TO JOIN: JOINROOM "+room.getName(),[invitado])
    
    """
    Método auxiliar identificar():
        Método auxiliar que se encarga del evento IDENTIFY especificado en el protocolo.
        Se modificara o se entrudicira el nombre del cliente.
        Si el nombre entrante es repetido, se mandara un mensaje al cliente , para que se le
        haga saber este hecho.
        @param nombre: nombre para modificar el nombre del cliente.
    """
    
    def identificar(self,nombre):
        nombre_repetido = False
        for cliente in self.chat.getClientes():
            if(cliente.getUsuario().getNombre() == nombre):
                nombre_repetido = True
                break
        if(nombre_repetido):
            self.conexion.mandaMSG("...NOMBRE OCUPADO...")
            return nombre_repetido
        else:
            self.conexion.setUsuario(nombre)
            self.conexion.mandaMSG("...SUCCESFUL IDENTIFICATION")
            return nombre_repetido
    
    """
    Método auxiliar mandarUSERS():
        Método auxiliar que se encarga del evento USERS especificado en el protocolo.
        Se envia la lista de clientes del chat.
    """
    
    def mandarUSERS(self):
        s = ""
        for cliente in self.chat.getClientes():
            s = s + cliente.__repr__() + "   "
        return s
    
    """
    Método auxiliar mandaMSG():
        Método auxiliar que se encarga del evento ROOMESSAGE especificado en el protocolo.
        Se modificara o se entrudicira el nombre del cliente.
        @param msg : mensaje en donde se sacara el nombre de la sala, y el mensaje que se
                     enviara en el room especificado.
    """
    
    def mandaMSGRoom(self,msg):
        msg = msg.split(" ")
        if(len(msg) < 2):
            self.eventoDesconocido()
            return
        room = self.chat.getRoom(msg[0])
        nombre = self.conexion.getUsuario().getNombre()
        if(room is None):
            self.conexion.mandaMSG("...ROOM NOT EXISTS")
            return
        self.conexion.mandaMSG("...MESSAGE SENT")
        self.conexion.mandaMSG(msg[1],room.getUsers(),nombre,msg[0])

    """
    Método auxiliar desconectar():
        Método auxiliar que se encarga del evento DISCONNECT especificado en el protocolo.
        Se eliminara de todas las listas donde este contenida la conexion que se desconectara.
        @param identificado: bool; True si la conexion ya esta indentificada, False otherwise.
               lock : Instancia de la clase Lock() del módulo threading, necesaria para
                      poder sincronizar la lista de conexiones de invitados de la sala,
                      lista de conexiones del chat y la lista de conexiones de las salas.
    """
    
    def desconectar(self,identificado,lock):
        if(not identificado):
            return
        if(identificado):
            self.chat.eliminarCliente(self.conexion,lock)

    """
    Método auxiliar mandarPrivado():
        Método auxiliar que se encarga del evento INVITE especificado en el protocolo.
        Se establecera la comunicación privada en una sala. Si es la primera vez que se
        establece comunicación entre los dos clientes se creara una sala, en donde se
        establecera la conversación. Sino solo se mandara  la sala privada entre los clientes.
        @param mensaje: Mensaje donde se sacara el nombre del cliente emisario y 
                        del cliente  remitente.
               lock : Instancia de la clase Lock() del módulo threading, necesaria para
                      poder sincronizar la lista de salas del chat.
    """

    def mandarPrivado(self,mensaje,lock):
        mensaje = mensaje.split(" ")
        nombre = self.conexion.getUsuario().getNombre()
        remitente = self.chat.getCliente(mensaje[0])
        if(remitente is None):
            self.conexion.mandaMSG("...USER " + mensaje[0] + " NO FOUND")
            return
        private_roomName = "$$" + nombre + "-" + mensaje[0] + "$$"
        if(private_roomName in self.chat.getRooms()):
            self.conexion.mandaMSG("...MESSAGE SENT")
            self.conexion.mandaMSG(mensaje[1],
                                    self.chat.getRoom(private_roomName).getClientes(),nombre)
        else:
            user1 = self.chat.getCliente(nombre)
            user2 = self.chat.getCliente(mensaje[0])
            lock.acquire()
            self.chat.añadirRoom(private_roomName,[user1,user2])
            lock.release()
            self.conexion.mandaMSG("...MESSAGE SENT")
            self.conexion.mandaMSG(mensaje[1],
                                    self.chat.getRoom(private_roomName).getUsers(),nombre)
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Especifica el puerto.")
        sys.exit(-1)
    server = Servidor(('', int(sys.argv[1])),ServidorChatHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()