import math
import os
import random
import time
from multiprocessing import Process, Array

multi_launch_depth = 0


class Processor(Process):
    def __init__(self, args):
        super(Processor, self).__init__()
        self.args = args

    def run(self):
        mergeSort(self.args[0], self.args[1])


def mergeSort(tbs_arr, depth):
    if len(tbs_arr) > 1:
        mid = len(tbs_arr) // 2
        l_arr = Array('i', tbs_arr[:mid], lock=False)
        r_arr = Array('i', tbs_arr[mid:], lock=False)
        if depth < multi_launch_depth:
            p1 = Processor(args=(l_arr, depth + 1))
            p1.start()
            mergeSort(r_arr, depth + 1)
            p1.join()
        else:
            if depth == multi_launch_depth:
                print("Merge sort depth", depth, os.getpid(), '\n')
            mergeSort(r_arr, depth + 1)
            mergeSort(l_arr, depth + 1)

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
        if depth == 0:
            return tbs_arr


def create_array(array_length, bound):
    v_array = [random.randint(0, bound) for _ in range(0, array_length)]
    return v_array


def calculate_depth(array_length, threads):
    global multi_launch_depth
    if not (threads & (threads - 1) == 0) and threads != 0:
        print("Number of cores must be a power of 2\n")
        raise BaseException()
    multi_launch_depth = math.floor(math.log2(threads))
    if array_length < multi_launch_depth:
        multi_launch_depth = 0


def merge_sort(array, number_of_threads):
    my_array = Array('i', array, lock=False)
    calculate_depth(len(array), number_of_threads)
    return mergeSort(my_array, 0)


def check_array(sorted_list):
    flag = True
    i = 1
    while i < len(sorted_list):
        if sorted_list[i] < sorted_list[i - 1]:
            flag = False
        i += 1
    if flag:
        return True
    else:
        return False


if __name__ == '__main__':
    begin_array = create_array(200000, 10000)
    begin = time.time()
    sorted_array = merge_sort(begin_array, 4)
    print(time.time() - begin)
    # print(list(sorted_array))
    check_array(list(sorted_array))
