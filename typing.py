import re
from const import *
class Spliter:
    key_state = [QWERTY, DUBEOLSIK]
    key_state_index = 0

    def __init__(self, text):
        text_s = self.makeSplit(text)

    def makeSplit(self, text):
        result = list()
        array  = list(text)
        for character in array:
            character = self.switch([character])
            if self.key_state_index == HANGUL:
                character = self.get_hangul(character)
                print(character)

            result.append(character)

        print(result)
        return result

    def switch(self, character):
        if re.match('[ㄱ-ㅎㅏ-ㅣ가-힣]', character[-1]):
            key_state_index = HANGUL
        elif re.match('[a-zA-Z]', character[-1]):
            key_state_index = ENGLISH
        else:
            return character

        if self.key_state_index == key_state_index:
            return character

        self.key_state_index += 1
        self.key_state_index %= len(self.key_state)

        character = ['\b'] + character
        return character

    def get_hangul(self, character):
        print("get_hangul:", character)
        char_code = ord(character[-1]) - BASE_CODE
        if char_code < 0:
            return character

        cho_idx = char_code // CHOSUNG
        jung_idx = int((char_code - (CHOSUNG * cho_idx)) / JUNGSUNG)
        jong_idx = int((char_code - (CHOSUNG * cho_idx) - (JUNGSUNG * jung_idx)))
        if jong_idx is 0:
            return character

        character = CHOSUNG_LIST[cho_idx]
        character += JUNGSUNG_LIST[jung_idx]
        character += JONGSUNG_LIST[jong_idx]
        return character

if __name__ == '__main__':
    test = '김동호'
    spliter = Spliter(test)

    '''
    result = list()
    for keyword in split_keyword_list:
        # 한글 여부 check 후 분리
        if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
            if  SWITCH is ENGLISH:
                SWITCH = HANGUL
                result.append('\b')

            char_code = ord(keyword) - BASE_CODE
            char1 = int(char_code / CHOSUNG)
            result.append(CHOSUNG_LIST[char1])
            #print('초성 : {}'.format(CHOSUNG_LIST[char1]))
            char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
            result.append(JUNGSUNG_LIST[char2])
            #print('중성 : {}'.format(JUNGSUNG_LIST[char2]))
            char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
            if char3 is not 0:
                result.append(JONGSUNG_LIST[char3])
            #print('종성 : {}'.format(JONGSUNG_LIST[char3]))
        else:
            if keyword is ' ':
                pass

            elif SWITCH is HANGUL:
                SWITCH = ENGLISH
                result.append('\b')

            result.append(keyword)
    # result
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
    # hold    command (mac) || ctrl (window)
    # push    enter
    # release command (mac) || ctrl (window)
    '''
