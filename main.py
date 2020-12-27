import math
import random
import time
import os
import multiprocessing

multilaunchdepth = 0


# Python program for implementation of MergeSort
def mergeSort(arr, depth):
    if len(arr) > 1:

        # Finding the mid of the array
        mid = len(arr) // 2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        if depth < multilaunchdepth:
            p1 = multiprocessing.Process(target=mergeSort(L, depth+1))
            p1.start()
            mergeSort(R, depth+1)
            p1.join()
        else:
            if depth == 2:
                print("Merge sort depth", depth)
                print(multiprocessing.Process.pid)
            mergeSort(R, depth+1)
            mergeSort(L, depth+1)
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


# Code to print the list


def printList(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()


def createarray(len, bound):
    return [random.randint(0, bound) for x in range(0, len)]


def calculate_depth(array_length, threads):
    global multilaunchdepth
    multilaunchdepth = math.floor(math.log2(threads))
    if array_length < multilaunchdepth:
        multilaunchdepth = 0


# Driver Code
if __name__ == '__main__':
    print(multiprocessing.cpu_count())
    arr = createarray(1000000, 1000)
    calculate_depth(len(arr), 4)
    begin = time.time()
    print(multilaunchdepth)
    mergeSort(arr, 0)
    print(time.time() - begin)

# This code is contributed by Mayank Khanna
