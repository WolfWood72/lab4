import matplotlib.pyplot as plt
from Gost_28147_89 import Gost_28147_89
import itertools
num_rounds = 16
block_size = 64
messege = "Ставни стон глотали. В час рассветный, тишиной облиты,Солнцу принесли дары"
key = "123456789"
bit_index = 6
def collect_data( type_key, type_func, change_bit_mode, bit_index):
    coder = Feistel( block_size=block_size, type_key=type_key,
                     type_func= type_func, num_rounds=num_rounds,change_bit_mode=change_bit_mode, change_bit_index=bit_index)

    coder.encoding(messege, key)
    graph_info = coder.graph_info
    plt.plot(range(len(graph_info)), graph_info)
    plt.xlabel("round")  # Метка по оси x в формате TeX
    plt.ylabel("bit")  # Метка по оси y в формате TeX
    plt.savefig("{}_{}_{}.png".format(type_func,type_key,  change_bit_mode ))

    plt.close()
    #lt.show()  # Показать график
type_key_list = ["cycle", "scrembler"]
type_func_list = ["single", "scrembler"]
change_bit_mode = ["messege", "key"]

combinations = list(itertools.product(type_key_list, type_func_list, change_bit_mode))
for type_key,func,mode in  combinations:
    print(type_key,func,mode)
    collect_data( type_key=type_key, type_func=func, change_bit_mode=mode, bit_index=bit_index)
#collect_data( type_key="cycle", type_func="single", change_bit_mode="messege", bit_index=bit_index)
