from collections import deque
class viewAnt :
    """
    Visual representation of an ant in the Tkinter canvas.

    This class stores the screen position of an ant and manages
    its animation state through a movement queue.
    """

    def __init__(self, screenX,screenY):
        """
    Initialize a visual ant instance.

    Sets the initial screen position of the ant and prepares
    the data structures required for animated movement.

    Parameters
    ----------
    screenX : int
        Initial x-coordinate on the canvas.
    screenY : int
        Initial y-coordinate on the canvas.
        """
        self.screenX = screenX
        self.screenY = screenY
        self.is_moving = False
        self.move_queue = deque()

