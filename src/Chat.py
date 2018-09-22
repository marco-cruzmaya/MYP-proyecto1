from Room import Room
from Conexion import Conexion
from Usuario import Usuario

"""
Clase Chat:
    Clase que tiene como variables de clase, un dictionario de salas y una lista de clientes.
"""
class Chat:
    """
    Constructor class Chat:
        Se inicializa la lista de clientes y el dictionario de salas.
        Se añade la sala publica, donde se enviaran todos los mensajes especificados por
        el evento PUBLICMESSAGE especificado en el protocolo.
    """

    def __init__(self):
        self.clientes = []
        self.rooms = {}
        self.rooms["publico"] = Room("publico",self.clientes)
    
    """
    Método getClientes():
        @return La lista de clientes en el chat.
    """
    
    def getClientes(self):
        return self.clientes
    
    """
    Método getRoom():
        @param nombre_room : el nombre de room a buscar.
        @return instancia de Room que tiene nombre nombre_room
    """
    
    def getRoom(self,nombre_room):
        if(nombre_room in self.rooms):
            return self.rooms[nombre_room]
        return None
    
    """
    Método añadirCLiente():
        Se añade un nuevo cliente a la lista de clientes
        @param cliente : cliente a añadir a la lista de clientes
    """
    
    def añadirCliente(self,cliente):
        self.clientes.append(cliente)

    """
    Método añadirRoom():
        Se añade una nueva sala al dictionario de salas.
        @param nombre_room : el nombre de la nueva sala.
               lista_user : la lista de usuario que abra en la nueva sala.
               cliente_creador : el cliente que hizo la nueva sala.
    """
    
    def añadirRoom(self,nombre_room,lista_user = [],cliente_creador=None):
        if(cliente_creador is None):
            self.rooms[nombre_room] = Room(nombre_room,lista_user)
        else:
            self.rooms[nombre_room] = Room(nombre_room,lista_user,cliente_creador)
        
    """
    Método eliminarCliente():
        Elimina el cliente tanto en la lista de clintes como en todas las salas 
        que lo contengan.
        @param cliente : el cliente a eliminar
               lock : intancia de clasee Lock(), para poder sincronizar la lista de
                      clientes y el arbol de salas.
    """
    
    def eliminarCliente(self,cliente,lock):
        lock.acquire()
        self.clientes.remove(cliente)
        lock.release()
        for room in self.rooms:
            if self.rooms[room].contiene(cliente):
                era_creador = cliente == self.rooms[room].getCreador()
                lock.acquire()
                self.rooms[room].eliminarUser(cliente)
                lock.release()
                if(era_creador):
                    if(len(self.rooms[room].getUsers()) > 0):
                        lock.acquire()
                        self.rooms[room].setCreador(self.rooms[room].getUsers()[0])
                        lock.release()
                    else:
                        lock.acquire()
                        del self.rooms[room]
                        lock.release()
                        break
                elif(cliente in self.rooms[room].getInvitados()):
                    lock.acquire()
                    self.rooms[room].eliminarInvitado(cliente)
                    lock.release()
    
    """
    Método getRooms():
        @return el arbol de salas.
    """
    
    def getRooms(self):
        return self.rooms
    
    """
    Método getRoom():
        Se regresa el cliente que tenga el nombre especificado.
        @param nombre : el nombre del cliente a buscar.
        @return el cliente que coincide con el nombre especificado.
    """
    
    def getCliente(self,nombre):
        for cliente in self.clientes:
            if(cliente.getUsuario().getNombre() == nombre):
                return cliente
        return None