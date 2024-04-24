import tkinter as tk
from Block import Block
from Connect import ConnectModel

def open():
    root = tk.Tk()
    app = SysConSim(root)
    root.mainloop()

class SysConSim:
    def __init__(self, master):
        self.master = master
        self.master.title("System Control Simulator")
        self.selected_ui_element = None
        self.canvas = tk.Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.connectModel = ConnectModel()
        
        self.ui_elements = []
        self.connectors = []
        
        self.add_block_button = tk.Button(master,
                                          text="Add Block",
                                          command=self.add_block)
        self.connect_block_button = tk.Button(master,
                                              text="Connect two Blocks", 
                                              command=self.connect_blocks)
        
        self.add_block_button.pack(side=tk.TOP)
        self.connect_block_button.pack(side=tk.TOP)

        self.__binding_init__()

    def __binding_init__(self):
        self.canvas.bind("<Button-1>", self.left_clicked)
        self.canvas.bind("<B1-Motion>", self.move_block)

    def add_block(self):
        x, y = 100, 100  # You can choose the initial position of the block
        block = Block(self.canvas, x, y, "Block")
        self.ui_elements.append(block)

    def left_clicked(self, event):
        self.select_element(event)

    def select_element(self, event):
        self.selected_ui_element = None
        for ui_element in self.ui_elements:
            if ui_element.is_clicked(event.x, event.y):
                print("Clicked on block:", ui_element.name)
                ui_element.canvas.itemconfig(ui_element.box, outline="blue")
                self.selected_ui_element = ui_element
                self.connectModel.register_element(ui_element)
            else:
                ui_element.canvas.itemconfig(ui_element.box, outline="black")

    def connect_blocks(self):
        if self.connectModel.is_connectable():
            print("Connectable")
            (x_src, y_src) = (self.connectModel.element_src
                                        .get_output_coordinates())
            (x_dst, y_dst) = (self.connectModel.element_dst
                                        .get_input_coordinates())
            line = self.canvas.create_line(x_src, y_src, x_dst, y_dst, fill="black")
            self.connectors.append((self.connectModel.element_src,
                                    self.connectModel.element_dst,
                                    line))
        
    def redraw_line(self):
        for connector in self.connectors:
            if self.selected_ui_element in connector:
                element_src, element_dst, line = connector
                x_src, y_src = element_src.get_output_coordinates()
                x_dst, y_dst = element_dst.get_input_coordinates()
                self.canvas.coords(line, x_src, y_src, x_dst, y_dst)
    
    def move_block(self, event):
        if self.selected_ui_element:
            self.selected_ui_element.move(event)
            self.redraw_line()
