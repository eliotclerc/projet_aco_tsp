import tkinter as tk
from tkinter import font
from math import sqrt

class Main_frame(tk.ttk.Frame):

    def __init__(self, container,nb_ants= None,nb_wh= None,warehouses = [], ants = [], edges = []):
        """
        Initializes the tkinter window, creates all of the buttons and the canva, defines the methods to 
        make the animations
        
        :param self: Description
        :param container: instance of Frame_app
        :param nb_ants: int
        :param nb_wh: int
        :param warehouses: instance of viewWarehouse
        :param ants: instance of viewAnt
        :param edges: instance of viewEdge
        """
        self.colors = ["#0d133d","#141c5a","#1a237e","#1f2e8a","#283593","#2f3fa0","#1565c0","#1976d2","#1e88e5","#2196f3","#0288d1","#039be5","#26c6da","#4dd0e1","#4db6ac","#66bb6a","#81c784","#9ccc65","#aed581","#cddc39","#d4e157","#ffeb3b","#fbc02d","#f9a825","#f57f17","#ef6c00","#e65100"]


        self.warehouses = warehouses
        self.nb_ants = nb_ants
        self.nb_wh = nb_wh
        self.ants= ants
        self.edges = edges

        custom_font = tk.font.Font(family="Arial", size=8,weight = "bold")
        super().__init__(container)
        options = {'padx': 5, 'pady': 5}
        self.grid(sticky=tk.NSEW)

        #Two columns : one for configuration (left), one for the canvas (right)
        self.columnconfigure(0, weight=0)  #Left column
        self.columnconfigure(1, weight=0) #Canvas Column
        self.columnconfigure(2,weight=0) # Heatbar column
        
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)

        
        #Configuration frame: 
        left = tk.ttk.Frame(self)
        left.grid(row=0, column=0, sticky="N", padx=20, pady=20)

        # ant label
        self.ant_label = tk.ttk.Label(left, text='Number of ants :')
        self.ant_label.grid(column=0, row=0, sticky="W", pady=10)

        # ant entry
        self.ant = tk.StringVar()
        self.ant_entry = tk.ttk.Entry(left, textvariable=self.ant)
        self.ant_entry.grid(column=0, row=1, sticky="EW", pady=5)
        self.ant_entry.focus()

        #set button
        self.set_button = tk.ttk.Button(left, text='Set', command=self.set)
        self.set_button.grid(column=0, row=2, sticky="EW", pady=5)

        # result label
        self.result_label = tk.ttk.Label(left, text="")
        self.result_label.grid(column=0, row=3, sticky="W", pady=5)

        #Creating a frame to place two buttons in one column : start and stop

        btn_frame = tk.ttk.Frame(left)
        btn_frame.grid(row=4, column=0, sticky="W", pady=10)


        tk.ttk.Button(btn_frame, text="▶️ Start").grid(row=0, column=0, padx=2)
        tk.ttk.Button(btn_frame, text="⏹️ Stop").grid(row=0, column=1, padx=2)

        #reset button 
        tk.ttk.Button(left, text="Reset", command=self.set).grid(row=5, column=0, sticky="EW", pady=5)

        #save button
        tk.ttk.Button(left, text="Save", command=self.set).grid(row=6, column=0, sticky="EW", pady=5)


        #Adding the canva : 
        self.canvas1 = tk.Canvas(self, width=container.get_geom()[0]*0.6, height=container.get_geom()[1]*0.8, background='white')
        self.canvas1.grid(row=0, column=2, sticky="NSEW", padx=110, pady=10)

        #Adding processing info label:
        self.ant_label = tk.ttk.Label(self, text=f"Number of ants set to: {self.nb_ants}",font = custom_font,foreground="darkblue",borderwidth=2,relief="solid")
        self.ant_label.grid(column=2, row=1, sticky="NSEW", padx=110)
         
        #Adding the heatbar
        self.heatbar = tk.Canvas(self, width=70, height = container.get_geom()[1]*0.8, highlightthickness=1, highlightbackground="black")
        self.heatbar.grid(row=0, column=2, sticky="E", pady=10)
        self.heatbar.delete("all")
        h = int(self.heatbar["height"])
        step = h / len(self.colors)

        for i, color in enumerate(self.colors):
            y0 = h - (i + 1) * step
            y1 = h - i * step
            self.heatbar.create_rectangle(0, y0, 30, y1,fill=color,outline="")

        #Create labels min / max
        self.heatbar.create_text(35, h-10, text="max", anchor="w")
        self.heatbar.create_text(35, 10, text="min", anchor="w")

        
    def set(self):
        """  Handle set button click event
        """        
        try:
            value = int(self.ant.get())
            self.nb_ants = value              
            self.result_label.config(text=f"Ants set to: {value}")
            self.ant_label.config(text=f"Number of ants set to: {self.nb_ants}")
        except ValueError:
            self.result_label.config(text="Invalid number")

    def init_container_on_canva(self) : 
        """
        Creates the containers and the edges between them visually on the canvas
        
        :param self: 
        """
        
        for i in self.warehouses : 
            self.canvas1.create_oval(i.screenX - i.r, i.screenY - i.r,i.screenX + i.r, i.screenY + i.r,fill="",outline="red",width=3)
        
        for i in self.edges : 
            i.canvas_id = self.canvas1.create_line(i.warehouse1.screenX, i.warehouse1.screenY, i.warehouse2.screenX, i.warehouse2.screenY, fill=self.colors[i.pheromon_coeff], width=4)
        

    def spawn_ants(self):
        """
        Creates the ants visually on the canvas

        :param self:
        """
        for ant in self.ants:
            ant.canvas_id = self.canvas1.create_oval(ant.screenX - 5, ant.screenY - 5,ant.screenX + 5, ant.screenY + 5,fill="blue")

    def change_edge_color(self,edge_to_change):
        """
        Docstring for change_edge_color
        
        :param self: 
        :param edge_to_change: canvas id number associated to every edge from one to n, from the first to the last created in in_container_on_canva
        """
        edge_to_change.update()
        self.canvas1.itemconfig(edge_to_change.canvas_id, fill=self.colors[edge_to_change.pheromon_coeff], width=5)

    def move_ants(self, ant, x_target, y_target, speed=2,callback=None):
        """
        Makes an ant visually move from its position screenX & screenY to x_target & y_target.
        
        :param self: Description
        :param ant: instance of viewAnt
        :param x_target: int
        :param y_target: int
        :param speed: int
        """
        dx = x_target - ant.screenX
        dy = y_target - ant.screenY
        dist = sqrt(dx*dx + dy*dy)
       

        if dist <= speed:
            self.canvas1.move(ant.canvas_id, dx, dy)
            ant.screenX = x_target
            ant.screenY = y_target

            if callback:
                callback()
        

            return

        dx /= dist
        dy /= dist

    
        self.canvas1.move(ant.canvas_id, dx * speed, dy * speed)
        ant.screenX += dx * speed
        ant.screenY += dy * speed

        self.canvas1.after(10, self.move_ants, ant, x_target, y_target, speed,callback)


    

    


