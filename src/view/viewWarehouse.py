class viewWarehouse : 

    def __init__(self, screenX,screenY,idWarehouse=None):
        """
        Initializes on the canva a warehouse at coordinates screenX & screenY 
        
        :param self: Description
        :param screenX: Description
        :param screenY: Description
        :param idWarehouse: Description
        """
        
        self.screenX = screenX
        self.screenY = screenY
        self.idWarehouse = idWarehouse
        self.r = 25

    def getIdWarehouse(self): 
        return self.idWarehouse


 


