import tkinter as tk
from tkinter import simpledialog
from sympy import pretty, sympify

class Block:
    def __init__(self, canvas, x, y, name="new Block", formel="k"):
        self.x = x
        self.y = y
        self.blockwidth = 50
        self.name = name
        self.formel = formel
        self.canvas = canvas
        
        # creation of the block
        self.box = canvas.create_rectangle(x, y,
                                    x+self.blockwidth, y+50,
                                    fill="lightgray",
                                    outline="black")
        # creation of the name label
        self.name_label = canvas.create_text(x+2, y-5,
                                        text=self.name,
                                        anchor=tk.W,
                                        fill="black",
                                        font=("Cascadia Code", 10))
        
        # creation of the formal label
        self.formel_label = canvas.create_text(x+10, y+25,
                                        text=self.formel,
                                        anchor=tk.W,
                                        fill="black",
                                        font=("Cascadia Code", 10))  
        self.__binding_init__()

    def __binding_init__(self):
        self.canvas.tag_bind(self.box, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.formel_label, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.box, "<Button-2>", self.on_right_click)
        self.canvas.tag_bind(self.formel_label, "<Button-2>", self.on_right_click)

    def __str__(self) -> str:
        return self.name

    def on_click(self, event):
        print("Block clicked (left click)")
        
    def on_right_click(self, event):
        print("Block clicked (rigth click)")
        context_menu = tk.Menu(self.canvas, tearoff=0)
        context_menu.add_command(label="Edit Name",
                                 command=self.edit_name)
        context_menu.add_command(label="Edit Formel",
                                 command=self.edit_formel)
        context_menu.add_command(label="Delete Block",
                                 command=self.delete_block)
        context_menu.tk_popup(event.x_root, event.y_root)

    def edit_name(self):
        new_text = simpledialog.askstring("Edit Name", "Enter the new name of the Block:")
        if new_text:
            self.canvas.itemconfig(self.name_label, text=new_text)
            self.name = new_text
            
    def edit_formel(self):
        new_text = simpledialog.askstring("Edit Formel", "Enter the new formal of the Block:")
        if new_text:
            expr = sympify(new_text, evaluate=False)
            human_readable_expression = pretty(expr,  use_unicode=True)
            self.canvas.itemconfig(self.formel_label, text=human_readable_expression)
            self.resize_block()

    def delete_block(self):
        if tk.messagebox.askokcancel("Delete Block", "Are you sure you want to delete this block?"):
            self.canvas.delete(self.box)
            self.canvas.delete(self.formel_label)
           
    def resize_block(self):
        text_width = self.canvas.bbox(self.formel_label)[2] - self.canvas.bbox(self.formel_label)[0]
        self.blockwidth = text_width + 20
        self.canvas.coords(self.box,
                           self.x, self.y,
                           self.x+self.blockwidth, self.y+50)
        self.canvas.coords(self.formel_label, self.x+10, self.y+25)
        
    def get_output_coordinates(self):
        return self.x+self.blockwidth, self.y+25
    
    def get_input_coordinates(self):
        return self.x, self.y+25
    
    def move(self, event):
        self.x = round(event.x / 10) * 10
        self.y = round(event.y / 10) * 10
        
        self.canvas.coords(self.box,
                           self.x, self.y,
                           self.x+self.blockwidth, self.y+50)
        self.canvas.coords(self.formel_label, self.x+10, self.y+25)
        self.canvas.coords(self.name_label, self.x+2, self.y-5)
       
    def is_clicked(self, x, y):
        x0, y0, x1, y1 = self.canvas.bbox(self.box)
        return x0 <= x <= x1 and y0 <= y <= y1
    