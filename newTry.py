import math
import multiprocessing
import os
import random
import time
from multiprocessing import Process, Queue


class Processor(Process):

    def __init__(self, args):
        super(Processor, self).__init__()
        self.args = args

    def run(self):
        mergeSort(self.args[0], self.args[1])

def mergeSort(arr, depth):
    if len(arr) > 1:

        # Finding the mid of the array
        mid = len(arr) // 2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        if depth < multilaunchdepth:
            p1 = Processor(args=(L, depth+1))
            p1.start()
            mergeSort(R, depth + 1)
            p1.join()
        else:
            if depth == multilaunchdepth:
                print("Merge sort depth", depth, os.getpid())
            mergeSort(R, depth + 1)
            mergeSort(L, depth + 1)
        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def createarray(len, bound):
    return [random.randint(0, bound) for x in range(0, len)]


def calculate_depth(array_length, threads):
    global multilaunchdepth
    multilaunchdepth = math.floor(math.log2(threads))
    if array_length < multilaunchdepth:
        multilaunchdepth = 0


# Driver Code
if __name__ == '__main__':
    arr = createarray(1000000, 1000)
    P = Processor(args=(arr, 0))
    calculate_depth(len(arr), 4)
    begin = time.time()
    mergeSort(arr, 0)
    print(time.time() - begin)

