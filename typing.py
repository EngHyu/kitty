import re

class constRule:
    BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28
    CHOSUNG_LIST  = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    QWERTY = [
    "`1234567890-=",
    "qwertyuiop[]\\",
    "asdfghjkl;\'\n",
    "zxcvbnm,./",
    "~!@#$%^&*()_+",
    "QWERTYUIOP{}|",
    "ASDFGHJKL:\"",
    "ZXCVBNM<>?",
    " ",
    ]

    DVORAK = [
    "`1234567890-=",
    "\',.pyfgcrl/=\\",
    "aoeuidhtns-\n",
    ";qjkxbmwvz",
    "~!@#$%^&*()_+",
    "\"<>PYFGCRL?+|",
    "AOEUIDHTNS_\n",
    ":QJKXBMWVZ",
    " ",
    ]

    DUBEOLSIK = [
    "`1234567890-=",
    "ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔ[]\\",
    "ㅁㄴㅇㄹㅎㅗㅓㅏㅣ;\'\n",
    "ㅋㅌㅊㅍㅠㅜㅡ,./",
    "~!@#$%^&*()_+",
    "ㅃㅉㄸㄲㅆㅛㅕㅑㅒㅖ{}|",
    "ㅁㄴㅇㄹㅎㅗㅓㅏㅣ:\"",
    "ㅋㅌㅊㅍㅠㅜㅡ<>?",
    " ",
    ]

class input:
    key_state = [QWERTY, DUBEOLSIK]
    key_state_index = 0

    SWITCH  = ENGLISH

    def __init__(self, text):
        self.text_o = text
        text_a = self.makeArray(self.text_o)
        text_s = self.makeSplit(text_a)

    def makeArray(self, text):
        return list(text)

    def makeSplit(self, array):
        for character in array:
            if re.match('[ㄱ-ㅎㅏ-ㅣ가-힣]', character):
                pass
        return text

    def switch(self):
        pass

if __name__ == '__main__':
    test_keyword = "몽롱"
    split_keyword_list = list(test_keyword)


    result = list()
    for keyword in split_keyword_list:
        # 한글 여부 check 후 분리
        if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
            if SWITCH is ENGLISH:
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
            print("shift:\tFalse\trows:\t4\tcols:\t0")
            continue

        if key == '\b':
            print("switched!")
            key_state_index = (key_state_index + 1) % len(key_state)

        for index, line in enumerate(key_state[key_state_index]):
            if key in line:
                print("shift:", bool(index // 4), "rows:", index % 4, "cols:", line.index(key), sep="\t")

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
