from Block import Block

class ConnectModel:
    def __init__(self):
        self.element_dst = None
        self.element_src = None

    def register_element(self, element):
        if(element == self.element_dst):
            return
        
        self.element_src = self.element_dst
        self.element_dst = element
        print(f"reigstered as src: {self.element_src} and dst: {self.element_dst}")

    def is_connectable(self):
        if(type(self.element_dst) is not Block):
            return False
        if(type(self.element_src) is not Block):
            return False
        return True