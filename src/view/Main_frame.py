import tkinter as tk
import tkinter.font as tkfont
from math import sqrt
from view.viawAnt import viewAnt
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from PIL import Image, ImageDraw
from pathlib import Path
from model.aco import AcoModel


class Main_frame(tk.ttk.Frame):

    def __init__(self, container,vme,nb_ants= None,nb_wh= None,warehouses = [], ants = [], edges = [],edges_id=[],max_steps = 0, graph=None, alpha=1.0, beta=2.0, evaporation=0.5):
        """
    Initialize the main Tkinter frame of the application.

    This constructor builds the full graphical interface, initializes
    all UI components (controls, canvas, status panels), and sets up
    the internal state required to animate and visualize the Ant Colony
    Optimization (ACO) algorithm.

    It also initializes:
    - visual representations of ants and edges
    - animation control flags
    - timeline storage for replay mode
    - UI layout and widgets

    Parameters
    ----------
    container : tk.Tk or tk.Frame
        Parent container of the Main_frame.
    vme : object
        External model or controller reference (unused here but kept for integration).
    nb_ants : int, optional
        Initial number of ants.
    nb_wh : int, optional
        Number of warehouses (nodes).
    warehouses : list
        List of warehouse view objects (nodes positions and radius).
    ants : list or object
        Ant model instances or a container holding them.
    edges : list
        List of edge view objects connecting warehouses.
    edges_id : list
        List of canvas IDs associated with edges.
    max_steps : int
        Maximum number of algorithm iterations.
        """
        
        self.colors = [self.get_hex_color_from_number(i,0,100) for i in range(0,100)]
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
        self.automated = False
        self.current_step = 0   
        self.max_steps = max_steps
        self.info_font = tkfont.Font(size=10)
        
        # Store graph and ACO parameters for later ACO creation
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.aco = None  # Will be created when start is pressed

  
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
        left.grid_columnconfigure(0, weight=0,minsize =300)

        config_frame = tk.ttk.LabelFrame(left, text="Configuration")
        config_frame.grid(row=0, column=0, sticky="EW", pady=(0, 15))
        config_frame.columnconfigure(0, weight=1)

        #Action frame: 

        action_frame = tk.ttk.LabelFrame(left, text="Actions")
        action_frame.grid(row=1, column=0, sticky="EW", pady=(0, 15))
        action_frame.columnconfigure(0, weight=1)
    
        #Status frame :
        status_frame = tk.ttk.LabelFrame(left, text="Status")
        status_frame.grid(row=2, column=0, sticky="EW")
        status_frame.columnconfigure(0, weight=1)


        # ant label
        self.ant_label = tk.ttk.Label(left, text='Input number of ants :')
        self.ant_label.grid(column=0, row=0, sticky="W", pady=10)

        # ant entry - using IntVar for integer validation
        self.ant = tk.IntVar()
        self.ant_entry = tk.Spinbox(left, from_=1, to=1000, textvariable=self.ant, width=20)
        self.ant_entry.grid(in_=config_frame, row=1, column=0, sticky="EW")
        self.ant_entry.focus()

        #set button
        self.set_button = tk.ttk.Button(left, text='Set', command=self.set)
        self.set_button.grid(in_=config_frame, row=2, column=0, sticky="EW")
  

        #Creating a frame to place two buttons in one column : start and stop
        btn_frame = tk.ttk.Frame(left)
        btn_frame.grid(in_=action_frame, row=0, column=0, sticky="EW")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)


        #Adding start & stop button
        self.start_button = tk.ttk.Button(btn_frame, text="▶️ Start", command=self.start)
        self.start_button.grid(row=0, column=0, sticky="EW", padx=2)

        self.stop_button = tk.ttk.Button(btn_frame, text="⏹️ Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1, sticky="EW", padx=2)


        #reset button 
        self.reset_button = tk.ttk.Button(left, text="Reset", command=self.reset)
        self.reset_button.grid(in_=action_frame, row=1, column=0, sticky="EW", pady=5)


        #Adding the canva : 
        self.canvas1 = tk.Canvas(self, width=container.get_geom()[0]*0.6, height=container.get_geom()[1]*0.8, background='white')
        self.canvas1.grid(row=0, column=2, sticky="NSEW", padx=110, pady=10)


        #save button
        self.save_button = tk.ttk.Button(left, text="Save", command = lambda: self.save(self.canvas1, filename="output.png"))
        self.save_button.grid(in_=action_frame, row=2, column=0, sticky="EW")
        self.save_button.config(state=tk.DISABLED)

        #Adding processing ant info label:
        initial_text = f"Number of ants set to: {self.nb_ants}" if self.nb_ants is not None else "Number of ants set to: Not set"
        self.ants_info_label = tk.ttk.Label(left,text=initial_text,font=self.info_font)
        self.ants_info_label.grid(in_=status_frame, row=0, column=0, sticky="W")


        #Adding processing step info label:
        self.step_info_label = tk.ttk.Label(left,text=f"Step counter: {self.current_step} / {self.max_steps}",font=self.info_font)
        self.step_info_label.grid(in_=status_frame, row=1, column=0, sticky="W")


        #Adding ACO status label: 
        self.step_aco_label = tk.ttk.Label(left,text=f"ACO status: settings",font=self.info_font)
        self.step_aco_label.grid(in_=status_frame, row=2, column=0, sticky="W")
         
        #Adding save status label
        self.save_feedback_label = tk.ttk.Label(left,text="",font=self.info_font)
        self.save_feedback_label.grid(in_=status_frame, row=3, column=0, sticky="W")


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
        """
    Read and validate the number of ants entered by the user.

    This method parses the value from the input field, updates the
    internal ant count, and refreshes the corresponding status label.
    If the input is invalid, an error message is displayed instead.
    If ACO already exists, shows the actual number of ants in ACO.
        """      
        try:
            value = self.ant.get() 
            self.nb_ants = value

            if self.aco is not None:
                actual_nb_ants = len(self.aco.ants)
                self.ants_info_label.config(text=f"Number of ants set to: {value} (ACO has {actual_nb_ants} ants)",font=self.info_font)
            else:
                self.ants_info_label.config(text=f"Number of ants set to: {self.nb_ants}",font=self.info_font)
            self.step_info_label.config(text=f"Step counter: {self.current_step} / {self.max_steps}")
        except (ValueError, tk.TclError):
            self.ants_info_label.config(text=f"Number of ants set to: Invalid number")

    def start(self):
        """
    Start or resume the ACO animation.

    If an animation is paused, it resumes execution.
    Otherwise, this method initializes a new live run by:
    - creating ACO model with the number of ants from UI
    - switching to live mode
    - clearing the timeline
    - disabling configuration inputs
    - enabling the animation loop
        """     
        
        self.step_aco_label.config(text=f"ACO: running")
        if self.animating:
            self.paused = False
            self.play = True

        else: 
            # Get number of ants from UI and create ACO
            try:
                self.nb_ants = self.ant.get()  
            except (ValueError, tk.TclError):
                return
            
            # Create ACO model
            
            try:
                self.nb_ants = self.ant.get()
            except (ValueError, tk.TclError):
                return

            # Toujours créer une nouvelle ACO
            self.aco = AcoModel(self.graph, self.nb_ants, self.alpha, self.beta, self.evaporation)
            self.model_ants = self.aco.ants

            # Reset visuel des fourmis
            for view_ant in self.view_ants:
                if hasattr(view_ant, 'canvas_id') and view_ant.canvas_id:
                    self.canvas1.delete(view_ant.canvas_id)

            self.view_ants = [viewAnt(0, 0) for _ in self.model_ants]

            self.spawn_ants()
            self.save_initial_state()

            actual_nb_ants = len(self.aco.ants)
            self.nb_ants = actual_nb_ants
            self.ants_info_label.config(text=f"Number of ants set to: {actual_nb_ants}", font=self.info_font)


            self.play = True
            self.mode = "live"
            self.timeline.clear()
            self.step_slider.config(state="disabled")
            self.set_button.config(state=tk.DISABLED)
            self.ant_entry.config(state=tk.DISABLED)
           

    def stop(self):
        """
    Pause the ongoing animation.

    This method temporarily freezes all ant movements without
    resetting the simulation state.
        """
        if self.animating:
            self.paused = True
            self.play = False

            self.step_aco_label.config(text=f"Paused")


    def init_container_on_canva(self) : 
        """
    Draw all warehouses and edges on the canvas.

    Warehouses are drawn as circles and edges as colored lines
    whose color represents the current pheromone intensity.
    Each edge canvas ID is stored for later updates.
        """
      
        for i in self.warehouses : 
            self.canvas1.create_oval(i.screenX - i.r, i.screenY - i.r,i.screenX + i.r, i.screenY + i.r,fill="",outline=self.colors[0],width=3)         
           
        
        for i in self.edges : 
            i.canvas_id = self.canvas1.create_line(i.warehouse1.screenX, i.warehouse1.screenY, i.warehouse2.screenX, i.warehouse2.screenY, fill=self.get_hex_color_from_number(i.pheromon_coeff,0,1), width=4)
           
    
    
    def spawn_ants(self):
        """
    Create and display all ants on the canvas.

    Each ant is positioned at its starting warehouse and
    represented as a small filled circle.
        """
        
        for i, model_ant in enumerate(self.model_ants):
            wh_id = model_ant.current_cycle.cycle_node_ids[-1]          
            warehouse = self.warehouses[wh_id]

            self.view_ants[i].screenX = warehouse.screenX
            self.view_ants[i].screenY = warehouse.screenY
            self.view_ants[i].canvas_id = self.canvas1.create_oval(self.view_ants[i].screenX - 5,self.view_ants[i].screenY - 5,self.view_ants[i].screenX + 5,self.view_ants[i].screenY + 5,fill="blue")
            
    def update_colors(self):
        """
    Update pheromone values and edge colors for one algorithm step.

    This method:
    - increments the step counter
    - updates pheromone coefficients on all edges
    - refreshes edge colors accordingly
    - switches to replay mode when the maximum number of steps is reached
        """
        self.current_step += 1
        for i in self.edges : 
            i.update()
            self.canvas1.itemconfig(i.canvas_id,fill=self.get_hex_color_from_number(i.pheromon_coeff,0,1),width=4)
            if(self.current_step < self.max_steps) :
                self.step_info_label.config(text=f"Step counter: {self.current_step} / {self.max_steps}")
            else :
                self.step_info_label.config(text=f"Step counter: {self.max_steps} / {self.max_steps}")
                self.save_button.config(state=tk.NORMAL)
                self.step_aco_label.config(text=f"ACO status: done")
                self.mode = "replay"
                self.animating = True
                self.play = False 
                   

                self.step_slider.config(to=len(self.timeline) - 1,state="normal")
                self.step_slider.set(len(self.timeline) - 1)


    def move_ants(self, view_ant, warehouse_id, speed=2,anim_id = None):
        """
    Schedule the movement of an ant toward a target warehouse.

    The movement is added to the ant's movement queue and executed
    progressively with animation frames.

    Parameters
    ----------
    view_ant : viewAnt
        Visual ant instance to move.
    warehouse_id : int
        Index of the target warehouse.
    speed : int, optional
        Movement speed in pixels per frame.
    anim_id : int, optional
        Animation identifier used to cancel outdated animations.
        """
        warehouse = self.warehouses[warehouse_id]

        x_target = warehouse.screenX
        y_target = warehouse.screenY

        view_ant.move_queue.append((x_target, y_target, speed, anim_id))

        if view_ant.is_moving:
            return

        self._start_next_move(view_ant)

    
    def _start_next_move(self, ant):
        """
    Execute the next movement in an ant's movement queue.

    This internal method animates the ant step-by-step toward
    its target and triggers pheromone updates once all ants
    have completed their movements.
        """
        
        if not ant.move_queue:
            ant.is_moving = False
            
         
            if all(not a.is_moving for a in self.view_ants):

                if self.mode == "live":
                    self.update_colors()
                    self.save_state()
                self.animating = False
                self.paused = False
                
            
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
    Save the current visual state of the simulation.

    Stores the positions of all ants and pheromone values of
    all edges into the timeline for replay purposes.
        """
        self.timeline.append({"ants": [(a.screenX, a.screenY) for a in self.view_ants],"edges": [e.pheromon_coeff for e in self.edges]})


    def render_step(self, idx):
        """
    Render a previously saved simulation step.

    This method restores ant positions and edge pheromone
    values from the timeline for replay visualization.

    Parameters
    ----------
    idx : int
        Index of the step to render.
        """

        state = self.timeline[idx]

        for ant, (x, y) in zip(self.view_ants, state["ants"]):
            self.canvas1.coords(ant.canvas_id,x-5, y-5, x+5, y+5)
            ant.screenX = x
            ant.screenY = y

       
        for edge, coeff in zip(self.edges, state["edges"]):
            edge.pheromon_coeff = coeff
            self.canvas1.itemconfig(edge.canvas_id,fill=self.get_hex_color_from_number(coeff,0,1))
        

    def on_slider(self, value):
        """
    Handle slider movement during replay mode.

    Updates the visualization to match the selected
    timeline step.

    Parameters
    ----------
    value : str
        Slider value representing the step index.
        """
        if self.mode != "replay":
            return
        self.render_step(int(value))


    def save_initial_state(self):
        """
    Store the initial state of the simulation.

    Saves initial ant positions and edge pheromone values
    to allow a clean reset of the visualization.
        """
        self.initial_state = {"ants": [(a.screenX, a.screenY) for a in self.view_ants],"edges": [e.pheromon_coeff for e in self.edges]}

    def reset(self):
        """
    Reset the simulation to its initial state.

    This method:
    - stops all animations
    - clears the timeline
    - resets ant positions and pheromone values
    - re-enables configuration controls
    - prepares the application for a new run
        """
        self.aco = None
        self.play = False
        self.animating = False
        self.paused = False
        self.mode = "live"
        self.current_step = 0 
        self.step_info_label.config(text=f"Step counter: {self.current_step} / {self.max_steps}")
        self.step_aco_label.config(text=f"ACO status: settings")
        self.set_button.config(state=tk.NORMAL)
        self.ant_entry.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)


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
        self.mode = "live"
        self.current_step = 0
        self.timeline.clear()

        self.step_slider.set(0)
        self.anim_id += 1
        self.set_button.config(state=tk.NORMAL)
        self.ant_entry.config(state=tk.NORMAL)
        

    def get_color_from_number(self,value, min_val, max_val):
        """
    Convert a numeric value to an RGBA color using a colormap.

    The value is normalized within the given range and mapped
    to a blue-to-red gradient.

    Parameters
    ----------
    value : float
        Input value to map.
    min_val : float
        Minimum normalization value.
    max_val : float
        Maximum normalization value.

    Returns
    -------
    tuple
        RGBA color tuple.
        """
        norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
        cmap = cm.get_cmap('coolwarm')
        return cmap(norm(value))
    

    def get_hex_color_from_number(self,value, min_val, max_val):
        """
    Convert a numeric value to a hexadecimal color string.

    Uses a blue-to-red gradient to represent the magnitude
    of the value.

    Parameters
    ----------
    value : float
        Input value to map.
    min_val : float
        Minimum normalization value.
    max_val : float
        Maximum normalization value.

    Returns
    -------
    str
        Hexadecimal color string.
        """
        rgba_color = self.get_color_from_number(value, min_val, max_val)
        return mcolors.to_hex(rgba_color)

    def save(self, canva, filename="canvas.png"):

        """
    Export the current canvas visualization as a PNG image.

    This method redraws warehouses and edges into a PIL image
    and saves it to the input_output directory.

    Parameters
    ----------
    canva : tk.Canvas
        Canvas to export.
    filename : str, optional
        Output image filename.
        """
        self.canvas1.update_idletasks()

        base_dir = Path(__file__).resolve().parent       
        output_dir = base_dir.parent / "input_output"     
        output_dir.mkdir(exist_ok=True)                   
        output_path = output_dir / filename
        width = canva.winfo_width()
        height = canva.winfo_height()
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        for i in self.edges:
            draw.line((i.warehouse1.screenX, i.warehouse1.screenY,i.warehouse2.screenX, i.warehouse2.screenY),fill=self.get_hex_color_from_number(i.pheromon_coeff, 0, 1),width=4)
        
        r = 25
        for i in self.warehouses:draw.ellipse((i.screenX - r, i.screenY - r, i.screenX + r, i.screenY + r),fill = None,outline=self.colors[0],width=3)

        img.save(output_path)
        self.save_feedback_label.config(text="Image saved ✓",foreground="green",font=tkfont.Font(size=9, slant="italic"))
        self.after(2000, lambda: self.save_feedback_label.config(text=""))