from Usuario import Usuario
from Conexion import Conexion


"""
class Room:
    Clase que tiene como variables de instancia, una lista de clientes que son miembros
    de la sala, una instancia creador de Conexion() sera el creador de la sala, una lista
    de los clientes que han sido invitados a la sala.
"""
class Room:
    """
    Constructor class Room:
        @param nomre : nombre de la sala.
               lista_users : lista de clientes que estaran en la sala.
               creador : el creador de la sala.
    """
    def __init__(self,nombre,lista_users = [],creador = None):
        self.usuarios = lista_users
        self.creador = creador
        self.invitados = []
        if creador is not None:
            self.usuarios.append(creador)
        self.nombre = nombre
    
    """
    Método agregaUser():
        Se agregara un nuevo cliente a la lista de clientes.
        @param user : el cliente a añadir.
    """
    
    def agregarUser(self,user):
        self.usuarios.append(user)
    
    """
    Método eliminaUser():
        Se eliminara el cliente especificado de la lista de clientes.
        @param user : el cliente a eliminar en la lista de clientes.
    """
    
    def eliminarUser(self,user):
        self.usuarios.remove(user)
    
    """
    Método eliminarInvitado():
        Se eliminara el cliente especificado de la lista de invitados.
        @param invitado : el cliente a eliminar en la lista de invitados.
    """
    
    def eliminarInvitado(self,invitado):
        self.invitados.remove(invitado)
    
    """
    Método getUsers():
        @return la lista de clientes.
    """
    
    def getUsers(self):
        return self.usuarios
    
    """
    Método agregarInvitado():
        Se agregara el cliente que fue invitado a la sala a la lista de invitados.
        @param invitado : el cliente que se añadira ala lista de invitados.
    """
    
    def agregarInvitado(self,invitado):
        self.invitados.append(invitado)
    
    """
    Método getInvitados():
        @return la lista de invitados.
    """
    
    def getInvitados(self):
        return self.invitados
    
    """
    Método getName():
        @return el nombre de la sala.
    """
    
    def getName(self):
        return self.nombre
    
    """
    Método contien:
        @param cliente : el cliente a saber si esta contenido en la lista de clientes.
        @return bool; True si el cliente es miembro de la sala. False otherwise.
    """

    def contiene(self,cliente):
        return cliente in self.usuarios
    
    """
    Método getUser():
        @param nombre : el nombre de cliente a buscar.
        @return el cliente que tiene el mismo nombre que se especifico.
    """
    
    def getUser(self,nombre):
        for cliente in self.usuarios:
            if(cliente.getUser().getName() == nombre):
                return cliente
            else:
                return None
    
    """
    Método setCreador():
        Se modifica el creador en caso de que el creador deje la sala.
        @param nuevo_creador : el nuevo dueño de la sala.
    """

    def setCreador(self,nuevo_creador):
        self.creador = nuevo_creador
    
    """
    Método getCreador():
        @return el dueño de la sala.
    """
    
    def getCreador(self):
        return self.creador
        