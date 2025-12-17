class viewEdge :
    colors = [
        "navy", "blue", "deep sky blue", "sky blue", "light blue",
        "turquoise", "cyan", "light sea green", "sea green", "green"
        ]
    
    def __init__(self,warehouse1,warehouse2,pheromon_coeff = 0) :

        self.warehouse1 = warehouse1
        self.warehouse2 = warehouse2
        self.pheromon_coeff = pheromon_coeff

    def update(self) : 
        
        self.pheromon_coeff += 1  



