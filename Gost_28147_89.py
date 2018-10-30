from Scrembler import Scrembler
import numpy as np
import matplotlib.pyplot as plt


def benchmark(func):
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print("Время шифрования: ", time.clock() - t)
        return res
    return wrapper

class Gost_28147_89:
    def __init__(self, type_key="gost_key", num_rounds=32, block_size=64, change_bit_mode=None, change_bit_index=None):
        self.__block_size = block_size
        self.__type_key = type_key
        self.__num_rounds = num_rounds

        self.__key_dict = {"gost_key": self.__gost_key
                           }
        self.get_key = self.__key_dict[type_key]
        self.change_bit_mode = change_bit_mode
        self.change_bit_index = change_bit_index
        self.graph_info = None
        self.KEY_LENGTH = 256
        self.SUBKEY_LENGTH = 32
        self.SUBKEY_ORDER = [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,8,7,6,5,4,3,2,1]
        self.S = [
            [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
            [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
            [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
            [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
            [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
            [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
            [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
            [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]

        ]




    def __gost_key(self, key, i , mode= 'encode'):
        return key[(self.SUBKEY_ORDER[i]-1)*32: self.SUBKEY_ORDER[i]*32]


    def __make_format(self, value, n_bit=15):
        _format = '0' + str(n_bit) + 'b'
        value.encode('utf-8')
        return [int(j) for j in ''.join(format(ord(i), _format) for i in value)]

    def __change_bit(self, text, ind):
        if text[ind] == 1:
            text[ind] = 0

        else:
            text[ind] = 1
        return text

    def change_info(self, text, key):
        if self.change_bit_mode == 'messege':
            return self.__change_bit(text, self.change_bit_index), key
        elif self.change_bit_mode == 'key':
            return text, self.__change_bit(key, self.change_bit_index)
        else:
            return text, key

    def __CycleArrayShift(self,arr, N):
        return list(np.roll(arr,N))

    def __BitListToInt(self, BitList):
        out = 0
        for bit in BitList:
            out = (out << 1) | bit
        return out

    def __IntToBitList(self, n, need_length=None):
        arr = [int(digit) for digit in bin(n)[2:]]
        if need_length:
            while len(arr) != need_length:
                arr = [0] + arr
        return arr

    def __XorBitList(self, a, b):
        return [i ^ j for i, j in zip(a, b)]


    def __make_round(self, left, right, key):
        temp = self.__XorBitList(right, key)
        tt = []
        for i in range(8):
            s_index = self.__BitListToInt(temp[i * 4: (i + 1) * 4])
            tt.append(self.__IntToBitList(self.S[i][s_index], 4))
        tt = list(np.array(tt).ravel())

        tt = self.__CycleArrayShift(tt,11)

        swap = right.copy()
        right = self.__XorBitList(tt, left)
        left = swap.copy()
        return left, right

    def encoding(self, message, key):
        @benchmark
        def make_code(b_messege, key):
            history_round = []
            code = b_messege
            length_mess = len(b_messege)
            for i in range(self.__num_rounds):
                temp = []
                for n in range(0, length_mess, self.__block_size):
                    block = code[n: n + self.__block_size]
                    N = len(block) // 2
                    Right = block[N:]
                    Left = block[:N]
                    # print("round {}".format(i))
                    Right, Left = self.__make_round(Left.copy(), Right.copy(), self.get_key(key, i))
                    if not i != 31:
                        temp += Left + Right
                    else:
                        temp +=  Right + Left
                history_round.append(temp)
                code = temp
            return code, history_round

        key = self.__make_format(key)
        if len(key) < self.KEY_LENGTH:
            raise ValueError("Key must be equal or greater than 256")
        if len(key) > self.KEY_LENGTH:
            key = key[:self.KEY_LENGTH]
        bit_message = self.__make_format(message)
        #print(len(bit_message))
        #print(bit_message)

        code, hist1 = make_code(bit_message, key)

        if self.change_bit_mode:
            changed_mess, changed_key = self.change_info(bit_message, key)
            changed_code, hist2 = make_code(changed_mess, changed_key)
            self.graph_info = []
            for i in range(self.__num_rounds):
                self.graph_info.append(sum(map(lambda x: abs(x[0] - x[1]), list(zip(hist1[i], hist2[i])))))
            self.make_plot(range(len(self.graph_info)),self.graph_info)
        #print(code)
        res = ""
        for i in range(0, len(code), 15):
            tmp = ''.join(str(j) for j in code[i: i + 15])
            res += chr(int(tmp, 2))

        return res

    def decoding(self, code, key):
        key = self.__make_format(key)
        bit_code = self.__make_format(code)

        if len(key) < self.KEY_LENGTH:
            raise ValueError("Key must be equal or greater than 256")
        if len(key) > self.KEY_LENGTH:
            key = key[:self.KEY_LENGTH]

        length_code = len(bit_code)
        mess = []

        for n in range(0, length_code, self.__block_size):
            block = bit_code[n: n + self.__block_size]
            N = len(block) // 2

            Right = block[:N]
            Left = block[N:]


            for i in range(self.__num_rounds - 1, -1, -1):
                Right, Left = self.__make_round(Right, Left, self.get_key(key, i))
            mess += Left + Right


        res = ""
        for i in range(0, len(mess), 15):
            tmp = ''.join(str(j) for j in mess[i: i + 15])
            res += chr(int(tmp, 2))


        # code.append(Right)
        return res

    def make_plot(self, X, Y):
        plt.plot(X, Y)
        plt.xlabel("round")  # Метка по оси x в формате TeX
        plt.ylabel("bit")  # Метка по оси y в формате TeX
        plt.savefig("plot_{}.png".format(self.change_bit_mode))
