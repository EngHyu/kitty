import json
from const import *
class Arduino:
    def __init__(self):
        #"""
        with open('./layout.json') as data_file:
            self.layout = json.load(data_file)

        self.shift, self.ctrl, self.cmd, self.space, self.enter \
        = self.find_special_keys(SHIFT, CTRL, CMD, SPACE, ENTER)



    def find_special_keys(self, *SPECIAL_KEYs):
        result = list()
        for key in SPECIAL_KEYs:
            if key == SHIFT:
                result.append(self.layout[-2][0])
                continue

            if key == CTRL:
                result.append(self.layout[-1][1])
                continue

            if key == CMD:
                result.append(self.layout[-1][3])
                continue

            if key == SPACE:
                result.append(self.layout[-1][4])
                continue

            if key == ENTER:
                result.append(self.layout[-3][-1])
                continue

            result.append(None)

        return result

    def hold(self, key):
        print("hold", key[:2])

    def release(self, key):
        print("release", key[:2])

    def type(self, *keys):
        if (len(keys) > 1):
            for key in keys[:-1]:
                self.hold(key)

        self.hold(keys[-1])
        self.release(keys[-1])

        if (len(keys) > 1):
            for key in keys[:-1]:
                self.release(key)

    def switch(self):
        self.type(self.cmd, self.space)

    def upload(self):
        self.type(self.cmd, self.enter)

    def type_space_bar(self):
        self.type(self.space)



if __name__ == "__main__":
    arduino = Arduino()
    arduino.upload()
