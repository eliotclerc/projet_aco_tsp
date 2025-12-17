import tkinter as tk
from tkinter import ttk
from Frame_app import Frame_app
from Main_frame import Main_frame
from viewWarehouse import viewWarehouse
from viawAnt import viewAnt
from viewEdge import viewEdge

warehouses_positions = [(100, 100),(700, 100),(100, 500),(700, 500)]
edge_screen = []



vA1 = viewAnt(100,100)
vA2 = viewAnt(700,100)
ants_list = [vA1,vA2]
whs = [viewWarehouse(screenX=x, screenY=y) for (x, y) in warehouses_positions]


for i in whs : 
    for j in range(0, len(whs)):
        if (j <= whs.index(i)) : 
            continue 
        else : 
            edge_screen.append(viewEdge(i,whs[j]))



if __name__ == "__main__":

    app = Frame_app()
    
    #Test ici, je créer un fenetre avec l'interface complète, je place des entrpôts arbitrairement, 
    #Je créer une fourmis, je la fais bouger d'un entrepots à une autre puis à un denier, enfin 
    
    frame = Main_frame(app,warehouses=whs,ants = ants_list,edges=edge_screen)
    frame.init_container_on_canva()
    frame.spawn_ants()

    path_pairs = frame.ants[0].update()
    print(path_pairs)
    frame.move_ants(frame.ants[0],path_pairs[0][0],path_pairs[0][1])
    frame.move_ants(frame.ants[0],path_pairs[1][0],path_pairs[1][1])

    frame.move_ants(frame.ants[1],path_pairs[1][0],path_pairs[1][1])
    frame.move_ants(frame.ants[1],path_pairs[2][0],path_pairs[2][1])

    app.mainloop()



