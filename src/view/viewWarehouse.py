"""
Main author: Benoit Boulard
"""

class viewWarehouse : 
    """
    Visual representation of a warehouse.

    Stores screen-space coordinates and display parameters
    for rendering on a Tkinter canvas.
    """

    def __init__(self, screenX,screenY,idWarehouse=None):
        """
        Initialize a warehouse at given screen coordinates.

        Parameters
        ----------
        screenX : float
            X coordinate in screen space (canvas).
        screenY : float
            Y coordinate in screen space (canvas).
        idWarehouse : int, optional
            Identifier linking this view object to the model.
        """
        
        self.screenX = screenX
        self.screenY = screenY
        self.idWarehouse = idWarehouse
        self.r = 25

    def getIdWarehouse(self): 
        """
        Return the warehouse identifier.

        Returns
        -------
        int or None
            Warehouse ID from the model.
        """
        
        return self.idWarehouse


 


