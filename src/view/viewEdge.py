class viewEdge :
    colors = [
    "#1a237e",  
    "#283593",
    "#1565c0",
    "#0288d1",
    "#26c6da",
    "#4db6ac",
    "#81c784",
    "#aed581",
    "#ffeb3b",
    "#f57f17"
]
    
    def __init__(self,warehouse1,warehouse2,pheromon_coeff = 0) :
        """
        Initializes an edge between two objects of viewWarehouse
        
        :param self: Description
        :param warehouse1: Instance of viewWarehouse
        :param warehouse2: Instance of viewWarehouse
        :param pheromon_coeff: int
        """
        self.warehouse1 = warehouse1
        self.warehouse2 = warehouse2
        self.pheromon_coeff = pheromon_coeff

    def update(self) : 
        """
        getter to go fetch the most recents pheromon_coeff
        
        :param self: Description
        """
        self.pheromon_coeff += 1  



