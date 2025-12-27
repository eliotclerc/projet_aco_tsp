import tkinter as tk
from tkinter import font
from math import sqrt
from view.viawAnt import viewAnt
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm




class Main_frame(tk.ttk.Frame):

    def __init__(self, container,vme,nb_ants= None,nb_wh= None,warehouses = [], ants = [], edges = [],edges_id=[]):
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
        self.colors = [self.get_hex_color_from_number(i,0,100) for i in range(0,99)]
        self.warehouses = warehouses
        self.nb_ants = nb_ants
        self.nb_wh = nb_wh
        self.model_ants = ants.ants if hasattr(ants, 'ants') else ants
        self.view_ants = [viewAnt(0, 0) for _ in self.model_ants]
        self.edges = edges
        self.play = False
        self.animating = False
        self.paused = False
        self.timeline = []
        self.mode = "live"
        self.pixel_counter = 0
        self.anim_id = 0
        self.edges_id = edges_id


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


        #Adding start & stop button


        self.start_button = tk.ttk.Button(btn_frame, text="▶️ Start",command = self.start).grid(row=0, column=0, padx=2)
        self.stop_button = tk.ttk.Button(btn_frame, text="⏹️ Stop",command = self.stop).grid(row=0, column=1, padx=2)

        #reset button 
        self.reset_button = tk.ttk.Button(left, text="Reset", command=self.reset)
        self.reset_button.grid(row=5, column=0, sticky="EW", pady=5)


        #save button
        self.save_button = tk.ttk.Button(left, text="Save", command=None).grid(row=6, column=0, sticky="EW", pady=5)


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
        self.heatbar.create_text(35, h-10, text="min", anchor="w")
        self.heatbar.create_text(35, 10, text="max", anchor="w")


        #Adding the step slider
    
        self.step_slider = tk.Scale(self,from_=0,to=0,orient="horizontal",command=self.on_slider,state="disabled")
        self.step_slider.grid(row=2, column=2, sticky="EW", padx=110, pady=5)

        
    
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

    def start(self):
        """  Handle start button click event
        """        
        if self.animating:
            self.paused = False

        else : 
            self.play = True
            #self.animating = True
            self.mode = "live"
            self.timeline.clear()
            self.step_slider.config(state="disabled")

    def stop(self):
        if self.animating:
            self.paused = True


    def init_container_on_canva(self) : 
        """
        Creates the containers and the edges between them visually on the canvas
        
        :param self: 
        """
        id = 0
        for i in self.warehouses : 
            i.idWarehouse = id
            self.canvas1.create_oval(i.screenX - i.r, i.screenY - i.r,i.screenX + i.r, i.screenY + i.r,fill="",outline=self.colors[i.idWarehouse],width=3)         
            id +=5
        
        for i in self.edges : 
            i.canvas_id = self.canvas1.create_line(i.warehouse1.screenX, i.warehouse1.screenY, i.warehouse2.screenX, i.warehouse2.screenY, fill=self.get_hex_color_from_number(i.pheromon_coeff,0,1), width=4)
            #print(f"pc spawn ={i.pheromon_coeff}")
    
    
    def spawn_ants(self):
        """
        Creates the ants visually on the canvas

        :param self:
        """
        
        for i, model_ant in enumerate(self.model_ants):
            wh_id = model_ant.current_cycle.cycle_node_ids[-1]          
            warehouse = self.warehouses[wh_id]

            self.view_ants[i].screenX = warehouse.screenX
            self.view_ants[i].screenY = warehouse.screenY

            self.view_ants[i].canvas_id = self.canvas1.create_oval(
                self.view_ants[i].screenX - 5,
                self.view_ants[i].screenY - 5,
                self.view_ants[i].screenX + 5,
                self.view_ants[i].screenY + 5,
                fill="blue"
            )
            
            

    def update_colors(self):
        """
        Docstring for change_edge_color

        :param self: 
        :param edge_to_change: canvas id number associated to every edge from one to n, from the first to the last created in in_container_on_canva
        """
        for i in self.edges : 
            i.update()
            self.canvas1.itemconfig(i.canvas_id,fill=self.get_hex_color_from_number(i.pheromon_coeff,0,1),width=4)
            #print(f"pc udpated ={i.pheromon_coeff}")

    def move_ants(self, view_ant, warehouse_id, speed=2,anim_id = None):

        warehouse = self.warehouses[warehouse_id]

        x_target = warehouse.screenX
        y_target = warehouse.screenY

        view_ant.move_queue.append((x_target, y_target, speed, anim_id))

        if view_ant.is_moving:
            return

        self._start_next_move(view_ant)

    
    def _start_next_move(self, ant):
        
        
        if not ant.move_queue:
            ant.is_moving = False

            if all(not a.is_moving for a in self.view_ants):

                if self.mode == "live":
                    #self.update_colors()
                    self.save_state()
                self.animating = False
                self.paused = False
                self.mode = "replay"
                self.play = True 

                self.step_slider.config(to=len(self.timeline) - 1,state="normal")
                self.step_slider.set(len(self.timeline) - 1)

            return

        ant.is_moving = True
        x_target, y_target, speed, anim_id = ant.move_queue.popleft()

        def step():

            if anim_id != self.anim_id:
                return
            
            if self.paused:
                self.canvas1.after(50, step)
                return
            
            dx = x_target - ant.screenX
            dy = y_target - ant.screenY
            dist = sqrt(dx * dx + dy * dy)

            if dist <= speed:
                self.canvas1.move(ant.canvas_id, dx, dy)
                ant.screenX = x_target
                ant.screenY = y_target
                ant.is_moving = False
                if self.mode == "live":
                    self.update_colors()
                    self.save_state()
                self._start_next_move(ant)
                return

            dxn = dx / dist
            dyn = dy / dist

            self.canvas1.move(ant.canvas_id, dxn * speed, dyn * speed)
            ant.screenX += dxn * speed
            ant.screenY += dyn * speed

            if self.mode == "live":
                self.pixel_counter +=1
                if self.pixel_counter % 5 == 0:
                    self.save_state()
            self.canvas1.after(10, step)

            

        step()

    def save_state(self):
        """
        Function to save the successive positions of the ants and the edges pheromnones
        coefficients
        :param self: 
        """
        self.timeline.append({"ants": [(a.screenX, a.screenY) for a in self.view_ants],"edges": [e.pheromon_coeff for e in self.edges]})


    def render_step(self, idx):
        state = self.timeline[idx]

        for ant, (x, y) in zip(self.view_ants, state["ants"]):
            self.canvas1.coords(ant.canvas_id,x-5, y-5, x+5, y+5)
            ant.screenX = x
            ant.screenY = y

       
        for edge, coeff in zip(self.edges, state["edges"]):
            self.canvas1.itemconfig(edge.canvas_id,fill=self.get_hex_color_from_number(edge.pheromon_coeff,0,1))
        

    def on_slider(self, value):
        if self.mode != "replay":
            return
        self.render_step(int(value))


    def save_initial_state(self):
        self.initial_state = {"ants": [(a.screenX, a.screenY) for a in self.view_ants],"edges": [e.pheromon_coeff for e in self.edges]}

    def reset(self):
       
        self.play = False
        self.animating = False
        self.paused = False
        self.mode = "live"

        for ant in self.view_ants:
            ant.move_queue.clear()
            ant.is_moving = False      
        self.timeline.clear()
        self.pixel_counter = 0


        for ant, (x, y) in zip(self.view_ants, self.initial_state["ants"]):
            self.canvas1.coords(ant.canvas_id, x-5, y-5, x+5, y+5)
            ant.screenX = x
            ant.screenY = y

        for edge in self.edges:
            edge.pheromon_coeff = 0
            self.canvas1.itemconfig(edge.canvas_id, fill=self.get_hex_color_from_number(edge.pheromon_coeff,0,1))

    
        self.step_slider.config(state="disabled", to=0)
        self.step_slider.set(0)
        self.anim_id += 1
        

    def get_color_from_number(self,value, min_val, max_val):
        """
        Maps a number within a specified range to an RGBA color in a blue-to-red gradient.

        Args:
            value (float): The input number.
            min_val (float): The minimum value of the range (maps to blue).
            max_val (float): The maximum value of the range (maps to red).

        Returns:
            tuple: An RGBA color tuple (floats between 0.0 and 1.0).
        """
        # Normalize the value to the range [0, 1]
        norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
        # Use the 'coolwarm_r' colormap which goes from red to blue, then reverse it by specifying cmap='coolwarm' in the return statement
        # The 'coolwarm' colormap goes from blue (low) to red (high)
        cmap = cm.get_cmap('coolwarm')
        # Return the RGBA color
        return cmap(norm(value))
    

    def get_hex_color_from_number(self,value, min_val, max_val):
        """
        Maps a number to a hex color string in a blue-to-red gradient.
        """
        rgba_color = self.get_color_from_number(value, min_val, max_val)
        return mcolors.to_hex(rgba_color)


 



