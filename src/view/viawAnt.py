from collections import deque
class viewAnt :

    def __init__(self, screenX,screenY):
        """
        initializes position of object ant

        :param self: Description
        :param screenX: int
        :param screenY: int
        :param ismoving: bool
        """
        self.screenX = screenX
        self.screenY = screenY
        self.is_moving = False
        self.move_queue = deque()

    def update(self):
        """
        Getter to go fetch the ants next position
        
        :param self: Description
        """

        return [(700,100),(100,500),(700,500)]
        