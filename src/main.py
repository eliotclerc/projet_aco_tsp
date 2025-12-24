import tkinter as tk
from tkinter import ttk
from view.Frame_app import Frame_app
from view.Main_frame import Main_frame
from view.viewWarehouse import viewWarehouse
from view.viawAnt import viewAnt
from view.viewEdge import viewEdge
from view.view_main import lists_from_view_model_to_view



def main():
    
    whs,ants_list,edge_screen = lists_from_view_model_to_view()
    app = Frame_app()
    frame = Main_frame(app,warehouses=whs,ants = ants_list,edges=edge_screen)
    frame.init_container_on_canva()
    frame.spawn_ants()
    frame.save_initial_state()
    


    app.mainloop()

main()