


class viewEdge :
    
    """
    Visual edge connecting two warehouses.

    This class represents an edge in the Tkinter view and mirrors
    pheromone values from the model via a view-model interface.
    """

    def __init__(self,warehouse1,warehouse2,wh_id1,wh_id2,vme,pheromon_coeff=0) :
        """
        Initialize a visual edge between two warehouses.

        Parameters
        ----------
        warehouse1 : viewWarehouse
            First warehouse endpoint.
        warehouse2 : viewWarehouse
            Second warehouse endpoint.
        wh_id1 : int
            Index of the first warehouse in the model matrix.
        wh_id2 : int
            Index of the second warehouse in the model matrix.
        vme : object
            View-model edge interface providing normalized pheromone values.
        pheromon_coeff : float, optional
            Initial pheromone coefficient (default is 0).
        """

        self.warehouse1 = warehouse1
        self.warehouse2 = warehouse2
        self.pheromon_coeff = pheromon_coeff
        self.vme = vme
        self.wh_id1=wh_id1
        self.wh_id2=wh_id2

    def update(self) : 
        """
        Update the pheromone coefficient from the view-model.

        Fetches the latest normalized pheromone value from the model
        and stores it locally for rendering.
        """
        self.pheromon_coeff = float(self.vme.get_normalized()[self.wh_id1][self.wh_id2])



