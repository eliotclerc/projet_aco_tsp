import tkinter as tk
from tkinter import ttk
from Frame_app import Frame_app
from Main_frame import Main_frame
from viewWarehouse import viewWarehouse
from viawAnt import viewAnt
from viewEdge import viewEdge


#------------------Déclaration des listes nécessaires pour initialiser la windows-----------------------
########################################################################################################
whs = [viewWarehouse(100, 100),viewWarehouse(700, 100),viewWarehouse(100, 500),viewWarehouse(700, 500)]
edge_screen = []
vA1 = viewAnt(100,100)
vA2 = viewAnt(700,100)
ants_list = [vA1,vA2]
for i in whs : 
    for j in range(0, len(whs)):
        if (j <= whs.index(i)) : 
            continue 
        else : 
            edge_screen.append(viewEdge(i,whs[j]))
########################################################################################################


if __name__ == "__main__":
    app = Frame_app()       
    frame = Main_frame(app,warehouses=whs,ants = ants_list,edges=edge_screen)
    frame.init_container_on_canva()
    frame.spawn_ants()
    frame.save_initial_state()
    

    """
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

    """
    app.mainloop()




