import math
import random
import time
from multiprocessing import Process, Queue


class Processor(Process):
    def __init__(self, args):
        super(Processor, self).__init__()
        self.args = args

    def run(self):
        self.args[3].put(mergemator(self.args[0], self.args[1], self.args[2]))


def mergemator(tbs_arr, depth, sync_depth):
    if len(tbs_arr) > 1:
        mid = len(tbs_arr) // 2
        if depth < sync_depth:
            q = Queue()
            p1 = Processor(args=(tbs_arr[:mid], depth + 1, sync_depth, q))
            p1.start()
            l_arr = mergemator(tbs_arr[mid:], depth + 1, sync_depth)
            r_arr = q.get()
            p1.join()
        else:
            l_arr = mergemator(tbs_arr[:mid], depth + 1, sync_depth)
            r_arr = mergemator(tbs_arr[mid:], depth + 1, sync_depth)
        i = j = k = 0
        while i < len(l_arr) and j < len(r_arr):
            if l_arr[i] < r_arr[j]:
                tbs_arr[k] = l_arr[i]
                i += 1
            else:
                tbs_arr[k] = r_arr[j]
                j += 1
            k += 1
        while i < len(l_arr):
            tbs_arr[k] = l_arr[i]
            i += 1
            k += 1
        while j < len(r_arr):
            tbs_arr[k] = r_arr[j]
            j += 1
            k += 1
    return tbs_arr


def create_array(array_length, bound):
    return [random.randint(0, bound) for _ in range(0, array_length)]


def calculate_depth(array_length, threads):
    if not (threads & (threads - 1) == 0) and threads != 0:
        print("Number of cores must be a power of 2\n")
        raise BaseException()
    sync_depth = math.floor(math.log2(threads))
    if array_length < sync_depth:
        return 0
    else:
        return sync_depth


def merge_sort(array, number_of_threads):
    return mergemator(array, 0, calculate_depth(len(array), number_of_threads))


def check_array(sorted_list):
    flag = True
    i = 1
    while i < len(sorted_list):
        if sorted_list[i] < sorted_list[i - 1]:
            flag = False
        i += 1
    return flag


if __name__ == '__main__':
    begin_array = create_array(1000000, 1000000)
    begin = time.time()
    sorted_array = merge_sort(begin_array, 4)
    print(time.time() - begin)
    print(check_array(sorted_array))
