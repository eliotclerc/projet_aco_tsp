import tkinter as tk
from tkinter import ttk
from .Frame_app import Frame_app
from .Main_frame import Main_frame
from .viewWarehouse import viewWarehouse
from .viawAnt import viewAnt
from .viewEdge import viewEdge



def lists_from_view_model_to_view(whs_vm ,ants_vm = [],screen_geom = []) : 
   
    
    lmx = [x for x, y in whs_vm]
    lmy = [y for x, y in whs_vm]

    min_x, max_x = min(lmx), max(lmx)
    min_y, max_y = min(lmy), max(lmy)
    canvas_w = int(0.6 * screen_geom[0])
    canvas_h = int(0.8 * screen_geom[1])
    margin = 50

    mapped_whs_pos = [(margin + ((x - min_x) / (max_x - min_x)) * (canvas_w - 2 * margin),margin + ((y - min_y) / (max_y - min_y)) * (canvas_h - 2 * margin)) for (x,y) in whs_vm]
    whs = [viewWarehouse(a,b) for (a,b) in mapped_whs_pos]

    """
    lax = [x for x, y in ants_vm]
    lay = [y for x, y in ants_vm]

    min_x, max_x = min(lax), max(lax)
    min_y, max_y = min(lay), max(lay)
    canvas_w = int(0.6 * screen_geom[0])
    canvas_h = int(0.8 * screen_geom[1])

    mapped_ant_start_pos = [(margin + ((x - min_x) / (max_x - min_x)) * (canvas_w - 2 * margin),margin + ((y - min_y) / (max_y - min_y)) * (canvas_h - 2 * margin)) for (x,y) in ants_vm]
    ants = [viewAnt(a,b) for (a,b) in mapped_ant_start_pos]
    """

    edge_screen = []
    #edge_id = []

    for i in whs : 
        for j in range(0, len(whs)):
            if (j <= whs.index(i)) : 
                continue 
            else : 
                edge_screen.append(viewEdge(i,whs[j]))
                #edge_id.append((whs.index(i),j))


    
    """
    for i, wh in enumerate(whs):
        for j in range(0, i + 1):
            edge_screen.append(viewEdge(wh, whs[j]))

    print(len(edge_screen))

    #A corriger si on veut utiliser celui-la, il crée des edges en trop
    """

    return whs,edge_screen
  

#a,b,c = lists_from_view_model_to_view()

if __name__ == "__main__":
    """
    app = Frame_app()       
    frame = Main_frame(app,warehouses=a,ants = b,edges=c)
    frame.init_container_on_canva()
    frame.spawn_ants()
    frame.save_initial_state()
    

  
    path = [(700,100),(100,500),(700,500)]

   
    def check_start():
        if frame.play and not frame.animating:
            frame.play = False
            frame.animating = True
            frame.anim_id += 1
            current_anim = frame.anim_id

            frame.move_ants(frame.ants[0], path[0][0], path[0][1],anim_id=current_anim)
            frame.move_ants(frame.ants[0], path[1][0], path[1][1],anim_id=current_anim)

            frame.move_ants(frame.ants[1], path[1][0], path[1][1],anim_id=current_anim)
            frame.move_ants(frame.ants[1], path[2][0], path[2][1],anim_id=current_anim)

        app.after(50, check_start)


    check_start()

   

    app.mainloop()

"""


