import tkinter as tk
from tkinter import ttk
from .Frame_app import Frame_app
from .Main_frame import Main_frame
from .viewWarehouse import viewWarehouse
from .viawAnt import viewAnt
from .viewEdge import viewEdge
"""
Utility functions to convert view-model data into Tkinter view objects.

This module handles the mapping of model coordinates to screen coordinates
and the creation of visual warehouses and edges.
"""



def lists_from_view_model_to_view(whs_vm ,vme,screen_geom = []) : 
   
    """
    Convert warehouse coordinates from the view-model to screen-space view objects.

    This function:
    - Normalizes warehouse coordinates from the model space
    - Maps them into canvas coordinates with margins
    - Creates visual warehouse objects
    - Creates visual edges between all warehouse pairs (upper triangle only)

    Parameters
    ----------
    whs_vm : list[tuple[float, float]]
        List of warehouse coordinates from the model (x, y).
    vme : object
        Edge-related model data passed to each viewEdge.
    screen_geom : list[int]
        Screen dimensions as [width, height].

    Returns
    -------
    tuple[list[viewWarehouse], list[viewEdge]]
        - List of visual warehouse objects
        - List of visual edge objects
    """
    
    lmx = [x for x, y in whs_vm]
    lmy = [y for x, y in whs_vm]

    min_x, max_x = min(lmx), max(lmx)
    min_y, max_y = min(lmy), max(lmy)
    canvas_w = int(0.6 * screen_geom[0])
    canvas_h = int(0.8 * screen_geom[1])
    margin = 50

    mapped_whs_pos = [(margin + ((x - min_x) / (max_x - min_x)) * (canvas_w - 2 * margin),margin + ((y - min_y) / (max_y - min_y)) * (canvas_h - 2 * margin)) for (x,y) in whs_vm]
    whs = [viewWarehouse(a,b) for (a,b) in mapped_whs_pos]


    edge_screen = []
 

    for i in whs : 
        for j in range(0, len(whs)):
            if (j <= whs.index(i)) : 
                continue 
            else : 
                edge_screen.append(viewEdge(warehouse1=i,warehouse2=whs[j],wh_id1=whs.index(i),wh_id2=j,vme =vme))
              
    return whs,edge_screen
  

