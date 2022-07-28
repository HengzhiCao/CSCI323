# CSCI 323/700
# Summer 2022
# Assignment 2 - Empircal Analysis of Sorting Algorithms
# Hengzhi CAO


import copy
import math
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate



def random_list(range_max, size):
    numbers = []
    i = 0
    while i < size:
        rnd = random.randint(1, range_max)
        numbers.append(rnd)
        i += 1
    return numbers


def native_sort(arr):
    arr.sort()
    return arr


# From https://www.geeksforgeeks.org/bubble-sort/
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# From https://www.geeksforgeeks.org/selection-sort/
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# From https://www.geeksforgeeks.org/insertion-sort/
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# From https://www.geeksforgeeks.org/cocktail-sort/
def cocktail_sort(a):
    n = len(a)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        start = start + 1
    return a


# From https://www.geeksforgeeks.org/shellsort/
def shell_sort(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        j = gap
        while j < n:
            i = j - gap

            while i >= 0:
                if arr[i + gap] > arr[i]:
                    break
                else:
                    arr[i + gap], arr[i] = arr[i], arr[i + gap]
                i = i - gap

            j += 1
        gap = gap // 2
    return arr


# From https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-search-and-sorting-exercise-8.php
def merge_sort(nlist):
    if len(nlist) > 1:
        mid = len(nlist) // 2
        lefthalf = nlist[:mid]
        righthalf = nlist[mid:]
        merge_sort(lefthalf)
        merge_sort(righthalf)
        i = j = k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                nlist[k] = lefthalf[i]
                i = i + 1
            else:
                nlist[k] = righthalf[j]
                j = j + 1
            k = k + 1

        while i < len(lefthalf):
            nlist[k] = lefthalf[i]
            i = i + 1
            k = k + 1

        while j < len(righthalf):
            nlist[k] = righthalf[j]
            j = j + 1
            k = k + 1

    return nlist


# From https://programmer.ink/think/622220809497d.html
def quick_sort(nums):
    n = len(nums)
    return quick(nums, 0, n - 1)


def quick(nums, left, right):
    if left >= right:
        return nums
    pivot = left
    i = left
    j = right
    while i < j:
        while i < j and nums[j] > nums[pivot]:
            j -= 1
        while i < j and nums[i] <= nums[pivot]:
            i += 1
        nums[i], nums[j] = nums[j], nums[i]
    nums[pivot], nums[j] = nums[j], nums[pivot]
    quick(nums, left, j - 1)
    quick(nums, j + 1, right)
    return nums


# From https://www.geeksforgeeks.org/heap-sort/
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[largest] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        heapify(arr, n, largest)


# The main function to sort an array of given size
def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

    return arr


# From https://codezup.com/implementation-of-counting-sort-algorithm-in-python/
def counting_sort(myList):
    maxValue = 0
    for i in range(len(myList)):
        if myList[i] > maxValue:
            maxValue = myList[i]

    buckets = [0] * (maxValue + 1)

    for i in myList:
        buckets[i] += 1

    i = 0
    for j in range(maxValue + 1):
        for a in range(buckets[j]):
             myList[i] = j
             i += 1

    return myList


# From https://pythonwife.com/sorting-algorithms-in-python/
# From https://www.geeksforgeeks.org/python-program-for-insertion-sort/
def insertionSort(b):
    for i in range(1, len(b)):
        up = b[i]
        j = i - 1
        while j >= 0 and b[j] > up:
            b[j + 1] = b[j]
            j -= 1
        b[j + 1] = up
    return b


def bucket_sort(tempList):
    numberofBuckets = round(math.sqrt(len(tempList)))
    maxVal = max(tempList)
    arr = []

    for i in range(numberofBuckets):
        arr.append([])
    for j in tempList:
        index_b = math.ceil(j*numberofBuckets/maxVal)
        arr[index_b-1].append(j)

    for i in range(numberofBuckets):
        arr[i] = insertionSort(arr[i])

    k = 0
    for i in range(numberofBuckets):
        for j in range(len(arr[i])):
            tempList[k] = arr[i][j]
            k += 1
    return tempList


# From https://www.geeksforgeeks.org/radix-sort/
def countingSort(arr, exp1):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(0, n):
        index = arr[i] // exp1
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]


# Method to do Radix Sort
def radix_sort(arr):
    max1 = max(arr)
    exp = 1
    while max1 / exp > 1:
        countingSort(arr, exp)
        exp *= 10

    return arr

# From https://rosettacode.org/wiki/Sorting_algorithms/Comb_sort#Python
def comb_sort(arr):
    gap = len(arr)
    swaps = True
    while gap > 1 or swaps:
        gap = max(1, int(gap / 1.25))  # minimum gap is 1
        swaps = False
        for i in range(len(arr) - gap):
            j = i+gap
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
                swaps = True

    return arr


def plot_time(dict_searches, sizes, searches):
    search_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for search in searches:
        search_num += 1
        d = dict_searches[search.__name__]
        x_axis = [j + 0.05 * search_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=search.__name__)
    plt.legend()
    plt.title("Run time of Sort Algorithms")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time for ten trials (ms)")
    plt.savefig("Assignment2.png")
    plt.show()


def main():
    sizes = [10, 100, 1000, 10000]
    trials = 10
    sorts = [native_sort,  bubble_sort, selection_sort, insertion_sort, cocktail_sort, shell_sort,
             merge_sort, quick_sort, heap_sort, counting_sort, bucket_sort, radix_sort, comb_sort]
    dict_sorts = {}
    for sort in sorts:
        dict_sorts[sort.__name__] = {}
    for size in sizes:
        for sort in sorts:
            dict_sorts[sort.__name__][size] = 0
        for trial in range(1, trials + 1):
            arr = random_list(100000, size)
            for sort in sorts:
                arr1 = copy.copy(arr)
                arr2 = copy.copy(arr)
                start_time = time.time()
                implement_sort = sort(arr1)
                end_time = time.time()
                build_in_sort = native_sort(arr2)
                if build_in_sort != implement_sort:
                    print("We have found an error in", sort.__name__, "please fix it")
                net_time = end_time - start_time
                dict_sorts[sort.__name__][size] += 1000 * net_time
        dict_sorts[sort.__name__][size] /= trials
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_sorts).T
    # print(df)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    plot_time(dict_sorts, sizes, sorts)


if __name__ == "__main__":
    main()