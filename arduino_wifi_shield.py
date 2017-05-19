class Arduino:
    def __init__(self):
        #with open('./layout.txt', 'r') as f:
        #    self.layout = f.readlines()
        #self.shift, self.ctrl, self.cmd, self.space = self.layout[0]
        self.shift = "shift"
        self.ctrl  = "ctrl"
        self.cmd   = "cmd"
        self.space = "space"
        self.enter = "enter"
        
    def hold(self, key):
        print("hold", key)

    def release(self, key):
        print("release", key)

    def type(self, *keys):
        if (len(keys) > 1):
            for key in keys[:-1]:
                self.hold("!" + key)

        self.hold(keys[-1])
        self.release(keys[-1])

        if (len(keys) > 1):
            for key in keys[:-1]:
                self.release("~" + key)

    def switch(self):
        self.type(self.cmd, self.ctrl, self.space)

    def upload(self):
        self.type(self.cmd, self.enter)

    def type_space_bar(self):
        self.type(self.space)

if __name__ == "__main__":
    arduino = Arduino()
    arduino.type_space_bar()
