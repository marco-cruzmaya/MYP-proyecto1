from Status import Status

class Usuario:
    """
    Constructor class Usuario:
        @param nombre : el nombre del usuario
    """
    def __init__(self,nombre = ""):
        self.nombre = nombre
        self.state = Status.ACTIVE

        
    def setNombre(self,nombre):
        self.nombre = nombre
    
    def setState(self,state):
        self.state = state
    
    def getNombre(self):
        return self.nombre
    
    def getState(self):
        return self.state

    

    

