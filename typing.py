import re
from const import *
class Spliter:
    key_state_array = [QWERTY, DUBEOLSIK]
    key_state_index = 0
    key_state = QWERTY

    def __init__(self, text):
        text_s = self.text_process(text)
        self.type_process(text_s)

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
            result += '\0'

        return result

    def type_process(self, text):
        print(text, self.key_state)
        print(end='\n\"\"\"\n')
        for key in text:
            if key == '\0':
                self.set_switch()
                # self.arduino.switch()
                print(end="~")
                continue

            if key == ' ':
                # self.arduino.push_space_bar()
                print(end="!")
                continue

            for index, line in enumerate(self.key_state):
                if key in line:
                    # self.arduino.push_key(self.key_state_index, index)
                    print(key, end="")
                    break
        print(end='\n\"\"\"\n\n')


if __name__ == '__main__':
    test = '''
김동ㅎgㅎ
dfsdf
sdfsdfsdf'''
    spliter = Spliter(test)

    '''
    for key in result:
        if key == ' ':
            # push space bar
            print('shift:\tFalse\trows:\t4\tcols:\t0')
            continue

        if key == '\b':
            print('switched!')
            key_state_index = (key_state_index + 1) % len(key_state)

        for index, line in enumerate(key_state[key_state_index]):
            if key in line:
                print('shift:', bool(index // 4), 'rows:', index % 4, 'cols:', line.index(key), sep='\t')

                if index >= 4:
                    pass
                    # hold shift
                # push row and col

                if index >= 4:
                    pass
                    # release shift
                break
    '''
