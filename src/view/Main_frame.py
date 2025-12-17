import tkinter as tk
from tkinter import font
from math import sqrt

class Main_frame(tk.ttk.Frame):

    def __init__(self, container,nb_ants= None,nb_wh= None,warehouses = [], ants = [], edges = []):
        
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
         
        self.init_container_on_canva()
        self.spawn_ants()

       
        path = ants[0].update()
        path_pairs = [(path[i], path[i+1]) for i in range(0, len(path), 2)]

        for i in self.ants : 
            self.move_ants(i, path_pairs[0][0], path_pairs[0][1], edge=edges[0])

        
        


    def set(self):
        """  Handle button click event
        """        
        try:
            value = int(self.ant.get())
            self.nb_ants = value              
            self.result_label.config(text=f"Ants set to: {value}")
            self.ant_label.config(text=f"Number of ants set to: {self.nb_ants}")
        except ValueError:
            self.result_label.config(text="Invalid number")

    def init_container_on_canva(self) : 
        
        for i in self.warehouses : 
            self.canvas1.create_oval(i.screenX - i.r, i.screenY - i.r,i.screenX + i.r, i.screenY + i.r,fill="",outline="red",width=3)
        
        for i in self.edges : 
            i.canvas_id = self.canvas1.create_line(i.warehouse1.screenX, i.warehouse1.screenY, i.warehouse2.screenX, i.warehouse2.screenY, fill=i.colors[i.pheromon_coeff], width=4)
        

    def spawn_ants(self):

        for ant in self.ants:
            ant.canvas_id = self.canvas1.create_oval(ant.screenX - 5, ant.screenY - 5,ant.screenX + 5, ant.screenY + 5,fill="blue")

    def change_edge_color(self,edge_to_change):

        edge_to_change.update()
        self.canvas1.itemconfig(edge_to_change.canvas_id, fill=edge_to_change.colors[edge_to_change.pheromon_coeff], width=5)

    def move_ants(self, ant, x_target, y_target, speed=2, edge=None):

        dx = x_target - ant.screenX
        dy = y_target - ant.screenY
        dist = sqrt(dx*dx + dy*dy)

        if dist <= speed:
            self.canvas1.move(ant.canvas_id, dx, dy)
            ant.screenX = x_target
            ant.screenY = y_target

            if edge is not None:
                self.change_edge_color(edge) 

            return

        dx /= dist
        dy /= dist

    
        self.canvas1.move(ant.canvas_id, dx * speed, dy * speed)
        ant.screenX += dx * speed
        ant.screenY += dy * speed

        self.canvas1.after(10, self.move_ants, ant, x_target, y_target, speed, edge)


    

    


