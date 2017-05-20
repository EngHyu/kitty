import re
from const import *
from arduino_wifi_shield import *
class Spliter:
    key_state_array = [QWERTY, DUBEOLSIK]
    key_state_index = 0
    key_state = key_state_array[key_state_index]

    def __init__(self, text):
        self.arduino = Arduino()
        with open('./layout.json') as keyboard_layout:
            self.layout = json.load(keyboard_layout)

        text = self.text_process(text)
        self.type_process(text)

    def text_process(self, text):
        result = list()
        array  = list(text)
        for character in array:
            character = self.add_switch([character])

            if self.key_state_index == HANGUL:
                character = self.get_hangul(character)

            result += character

        result = self.to_default_key_state(result)
        return result

    def add_switch(self, character):
        if re.match('[ㄱ-ㅎㅏ-ㅣ가-힣]', character[-1]):
            key_state_index = HANGUL
        elif re.match('[a-zA-Z]', character[-1]):
            key_state_index = ENGLISH
        else:
            return character

        if self.key_state_index == key_state_index:
            return character

        self.set_switch()
        character = ['\0'] + character
        return character

    def set_switch(self):
        self.key_state_index += 1
        self.key_state_index %= len(self.key_state_array)
        self.key_state = self.key_state_array[self.key_state_index]

    def get_hangul(self, character):
        char_code = ord(character[-1]) - BASE_CODE
        if char_code < 0:
            return character

        cho_idx = char_code // CHOSUNG
        jung_idx = int((char_code - (CHOSUNG * cho_idx)) / JUNGSUNG)
        jong_idx = int((char_code - (CHOSUNG * cho_idx) - (JUNGSUNG * jung_idx)))

        if character[0] == '\0':
            character = ['\0']
        else:
            character = []

        character += CHOSUNG_LIST[cho_idx]
        character += JUNGSUNG_LIST[jung_idx]
        if jong_idx is not 0:
            character += JONGSUNG_LIST[jong_idx]

        return character

    def to_default_key_state(self, result):
        if self.key_state_index == HANGUL:
            self.key_state_index = ENGLISH
            result += '\x00'

        return result

    def type_process(self, text):
        for key in text:
            if key == '\x00':
                self.set_switch()
                self.arduino.switch()
                continue

            if key == ' ':
                self.arduino.type_space_bar()
                continue

            for idx_line, line in enumerate(self.key_state):
                idx_key = line.find(key)
                if idx_key == -1:
                    continue

                print(key)
                if idx_line >= 6:
                    self.arduino.type(self.arduino.shift, self.layout[idx_line % 6][idx_key])
                else:
                    self.arduino.type(self.layout[idx_line % 6][idx_key])
                break

        self.arduino.upload()

if __name__ == '__main__':
    test = '''this is called test 큐ㅋㅠ'''
    spliter = Spliter(test)
