__author__ = 'ganghan-yong'

from random import randint

def gen_number():
    num = randint(0, 999999)
    num_str = str(num)

    while len(num_str) != 6 :
        num_str = '0' + num_str

    return num_str