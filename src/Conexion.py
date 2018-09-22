import socket
from Usuario import Usuario

"""
Clase Conexion:
    La clase conexión tiene como variables de instancia, una instancia usuario de la clase Usuario y
    una instancia enchufe de la clase Socket.
"""
class Conexion:
    """
    Constructor class Conexion:
        @param enchufe : Instancia de socket dondé se establecera la comunicacion, entre
                         el servidor y el cliente.
               usuario : Instancia de Usuario, dondé se guardara toda la información del usuario.
    """
    def __init__(self,enchufe,usuario = Usuario()):
        self.usuario = usuario
        self.enchufe = enchufe
    """
    Método setUsuario:
        Método para modificar la instancia de Usuario.
        @param nombre : El nombre con el que se instanciara el usuario.
    """
    def setUsuario(self,nombre):
        self.usuario = Usuario(nombre)
    
    """
    Método mandaMSG:
        Método que se encarga de mandar todos los mensajes salientes del enchufe.
        @param mensaje : El mensaje que se enviara.
               users : La lista de clientes a quien se les enviara el mensaje.
               nombre : Quien envia el mensaje.
               roomname : Nombre de la sala dondé se enviara el msg.
    """
    
    def mandaMSG(self,mensaje,users=None,nombre = "SERVER",roomname = ""):
        if nombre == "SERVER":
            if(users is not None):
                for conection in users:
                    conection.getEnchufe().sendall(bytes( mensaje + '\n','utf-8'))
            else:
                self.enchufe.sendall(bytes(mensaje + '\n','utf-8'))
        elif(nombre == ""):
            if(users is not None):
                for conection in users:
                    if conection == self:
                        continue
                    else:
                        conection.getEnchufe().sendall(bytes(mensaje + "\n",'utf-8'))
            else:
                self.enchufe.sendall(bytes(bytes(mensaje + "\n",'utf-8')))
        else:
            if(users is not None):
                for conection in users:
                    if conection == self:
                        continue
                    else:
                        conection.getEnchufe().sendall(bytes("..."+roomname + "-" + nombre + ": " + mensaje + "\n",'utf-8'))
            else:
                self.enchufe.sendall(bytes(nombre + ": " + mensaje + '\n' ,'utf-8'))
    
    """
    Método reciveMSG():
        Método que se encarga del Input del enchufe.
        @return el mensaje que envío el cliente al Servidor.
    """
    
    def reciveMSG(self):
        return str(self.enchufe.recv(1024),'utf-8')
    
    """
    Método getUsuario():
        @return La instancia de Usuario usuario
    """
    
    def getUsuario(self):
        return self.usuario

    """
    Método getEnchufe():
        @return La instancia de Enchufe enchufe
    """
    
    def getEnchufe(self):
        return self.enchufe
    
    """
    Método repr9(:
        @return La representación en cadena de la conexión.
    """
    
    def __repr__(self):
        return self.getUsuario().getNombre()
