from enum import Enum

"""
Class EventoChat:
    Enumeración donde se especifica cada evento del protocolo.
"""
class EventoChat(Enum):
    IDENT = "IDENTIFY"
    STATUS = "STATUS"
    USERS = "USERS"
    MSG = "MESSAGE"
    PUBLICMSG = "PUBLICMESSAGE"
    CREATEROOM = "CREATEROOM"
    INVITE = "INVITE"
    JOINROOM = "JOINROOM"
    ROOMSG = "ROOMESSAGE"
    DISCONNECT = "DISCONNECT"
    UNKNWON = "UNKNWON"

    """
    Método listaEventos():
        @return Lista con la representación de cada evento.
    """

    def listaEventos(self):
        listR = []
        for evento in EventoChat:
            listR.append(evento.value)
        return listR
    
    """
    Método get():
        @param evento : Cádena con el evento a especificar.
        @return El evento que se pide.
    """

    def get(self, evento):
        if(evento == "IDENTIFY"):
            return self.IDENT
        elif(evento == "STATUS"):
            return self.STATUS
        elif(evento == "USERS"):
            return self.USERS
        elif(evento == "MESSAGE"):
            return self.MSG
        elif(evento == "PUBLICMESSAGE"):
            return self.PUBLICMSG
        elif(evento == "CREATEROOM"):
            return self.CREATEROOM
        elif(evento == "INVITE"):
            return self.INVITE
        elif(evento == "JOINROOM"):
            return self.JOINROOM
        elif(evento == "ROOMESSAGE"):
            return self.ROOMSG
        elif(evento == "DISCONNECT"):
            return self.DISCONNECT
        else:
            return self.UNKNWON
