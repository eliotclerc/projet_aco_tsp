import tkinter as tk


class Frame_app(tk.Tk):

    def __init__(self):
        """
        Initializes instances of Frame_app to define, frame size and the main frames root
        
        :param self: 
        """
        super().__init__()

        root = tk.Tk()
        
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()

        self.title('ACO algorithm')
        self.geometry(str(self.screen_width) + "x" + str(self.screen_height))
        self.resizable(True, True)

        for i in range(3):
            self.columnconfigure(i, weight=1)
            
        for i in range(6): 
            self.rowconfigure(i, weight=1)

    def get_geom(self):
        return [self.screen_width,self.screen_height]





        
