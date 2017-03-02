# -*- coding: utf8 -*-
import binascii
import codecs


# матрица начальной перестановки
PI = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Перестановка сжатия для удаления битов проверки –из 64-битового  ключа удаляют  биты 8,16,24,  32,...,64
#и  переставляет остальные биты согласно таблице(в  ходе  перестановки сохраняется нумерация битов расширенного ключа)
CP_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# перестановка сжатия преобразует 56 бит в 48 битов, которые образуют раундовый ключ Ki+1
CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

# Матрица расширения до 48 бит
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# SBOX
S_BOX = [

    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
     ],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
     ],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
     ],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
     ],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
     ],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
     ],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
     ],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
     ]
]

# Перестановка после каждого замещения Sbox для каждого раунда
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# финальная матрица перестановки
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

# Матрица, которая определяет сдвиг для каждого раунда ключей В раундах 1,2,9 и 16 смещение на 1 бит, в других раундах на 2 бита
SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def string_to_bit_array(text):  # Преобразовать строку в список битов
    array = list()
    for char in text:
        binval = binvalue(char, 8)  # Получить символьное значение на один байт
        array.extend([int(x) for x in list(binval)])  # Добавляем биты в окончательный список
    return array


def bit_array_to_string(array):  # Воссоздать строку из битового массива
    res = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in bytes]) for bytes in nsplit(array, 8)]])
    return res


def binvalue(val, bitsize):  # Возвращает двоичное значение в виде строки из заданного размера
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise "binary value larger than the expected size"
    while len(binval) < bitsize:
        binval = "0" + binval  # Добавляем столько 0, чтобы получить желаемый размер
    return binval


def nsplit(s, n):  # Split a list into sublists of size "n"
    return [s[k:k + n] for k in range(0, len(s), n)]


ENCRYPT = 1
DECRYPT = 0


class des():
    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()

    def run(self, key, text, action=ENCRYPT, padding=False):
        if len(key) < 8:
            raise "Key Should be 8 bytes long"
        elif len(key) > 8:
            key = key[:8]  # Если размер ключа больше 8 байтов,то обрезаем его, чтобы получить ключ длинной  8 байтов

        self.password = key
        self.text = text

        if padding and action == ENCRYPT:
            self.addPadding()
        elif len(self.text) % 8 != 0:  # размер данных должен быть мкратным 8 байтам
            raise "Data size should be multiple of 8"

        self.generatekeys()  # Сформировать все ключи
        text_blocks = nsplit(self.text, 8)  # Разделить текст в блоки по 8 байтов 64 бита
        result = list()
        for block in text_blocks:  # Цикл по всем блокам данных
            block = string_to_bit_array(block)  # преобразуем блок в массив битов
            block = self.permut(block, PI)  # Применить начальную перестановку
            g, d = nsplit(block, 32)  # g(LEFT), d(RIGHT)
            tmp = None
            for i in range(16):  # 16 раундов
                d_e = self.expand(d, E)  # Расширяем d(right), чтобы соответствовать размеру Ki (48bits)
                if action == ENCRYPT:
                    tmp = self.xor(self.keys[i], d_e)  # если в зашифровании используется Ki
                else:
                    tmp = self.xor(self.keys[15 - i], d_e)  # Если расшифрование начинается со следующего ключа
                tmp = self.substitute(tmp)  # Метод, который будет применять SBOXes
                tmp = self.permut(tmp, P)
                tmp = self.xor(g, tmp)
                g = d
                d = tmp
            result += self.permut(d + g, PI_1)  # конечная перестановка и добавляем результат в result
        final_res = bit_array_to_string(result)
        if padding and action == DECRYPT:
            return self.removePadding(final_res)  # Удалите дополнение, если расшифровывают, и дополнение верно
        else:
            return final_res  # Возвращаем заключительный ряд данных зашифрованных/расшифрованных

    def substitute(self, d_e):  # Байты замены, используя SBOX
        subblocks = nsplit(d_e, 6)  # Разделение битового массива по 6 бит
        result = list()
        for i in range(len(subblocks)):  # Для всех подсписков
            block = subblocks[i]
            row = int(str(block[0]) + str(block[5]), 2)  # Получить строку с первым и последним битом
            column = int(''.join([str(x) for x in block[1:][:-1]]), 2)  # Колонкой является 2,3,4,5th биты
            val = S_BOX[i][row][column]  # берем значение в SBOX, для раунда (i)
            bin = binvalue(val, 4)  # Преобразование значения в двоичный
            result += [int(x) for x in bin]  # и добавляем это в результирующий список
        return result

    def permut(self, block, table):  # переставляем данный блок, используя данную таблицу
        return [block[x - 1] for x in table]

    def expand(self, block, table):
        return [block[x - 1] for x in table]

    def xor(self, t1, t2):  # применяем xor и возвращаем  результирующий список
        return [x ^ y for x, y in zip(t1, t2)]

    def generatekeys(self):  # создаем все ключи
        self.keys = []
        key = string_to_bit_array(self.password)
        key = self.permut(key, CP_1)  # применяем начальную перестановку на ключе
        g, d = nsplit(key, 28)  # разделяем на (g->LEFT),(d->RIGHT)
        for i in range(16):  # 16 раундов
            g, d = self.shift(g, d, SHIFT[i])  # применить сдвиг раунда
            tmp = g + d  # слияние
            self.keys.append(self.permut(tmp, CP_2))  # Применяем перестановку, чтобы получить Ki

    def shift(self, g, d, n):  # Сдвиг списка заданного значения
        return g[n:] + g[:n], d[n:] + d[:n]

    def addPadding(self):  # Добавляем отступы к DATAS с использованием PKCS5 спецификации.
        pad_len = 8 - (len(self.text) % 8)
        self.text += pad_len * chr(pad_len)

    def removePadding(self, data):  # Удаляем дополнения открытого текста
        pad_len = ord(data[-1])
        return data[:-pad_len]

    def encrypt(self, key, text, padding=False):
        return self.run(key, text, ENCRYPT, padding)

    def decrypt(self, key, text, padding=False):
        return self.run(key, text, DECRYPT, padding)


if __name__ == '__main__':
    key=input ('Key: ')
    text=input('Text: ')
    #key = "secret_k"
    #text = "Hello wo"
    d = des()
    r = d.encrypt(key, text)
    r2 = d.decrypt(key, r)
    #binascii.b2a_hex(r)
    #r='lalala'
    output = ''.join(hex(ord(c)) for c in r)

    print("Ciphered: ",output)
    #codecs.encode(r, 'hex')
    print(r)
    print("Deciphered: ", r2)