# CSCI 323/700
# Summer 2022
# Assignment 3 - Empirical Performance of Matrix Multiplication
# Hengzhi Cao

import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from pandas.io.formats import string
from tabulate import tabulate
import re
import texttable

assn_num = 3


def lpsst(s):
    n = len(s)
    table = [[0 for x in range(n)] for y in range(n)]
    max_Length = 1
    i = 0
    while (i < n):
        table[i][i] = True
        i = i + 1
    start = 0
    i = 0
    while i < n - 1:
        if (s[i] == s[i + 1]):
            table[i][i + 1] = True
            start = i
            max_Length = 2
        i = i + 1
    k = 3
    while k <= n:
        i = 0
        while i < (n - k + 1):
            j = i + k - 1
            if (table[i + 1][j - 1] and
                    s[i] == s[j]):
                table[i][j] = True

                if (k > max_Length):
                    start = i
                    max_Length = k
            i = i + 1
        k = k + 1
    return s[start: start + max_Length - 1]

    return max_Length


def lpssq(s):
    m = len(s)
    rev = s[:: -1]
    n = len(rev)
    L = [[None] * (n + 1) for i in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif s[i - 1] == rev[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    index = L[m][n]
    lcs = [""] * (index + 1)
    i, j = m, n
    while i > 0 and j > 0:
        if s[i - 1] == rev[j - 1]:
            lcs[index - 1] = s[i - 1]
            i -= 1
            j -= 1
            index -= 1
        elif L[i - 1][j] > L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    ans = ""
    for x in range(len(lcs)):
        ans += lcs[x]
    return ans


def test_lpsst_and_lpssq(s):
    st = lpsst(s)
    sq = lpssq(s)
    print("The test string is ", s, "with length", len(s))
    print("Its Longest Palindromic Substring is", st, "with length", len(st))
    print("Its Longest Palindromic Subsequence is", sq, "with length", len(sq))


def process_file(file_name):
    results = []
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            line = line.upper()  # convert to upper case
            line = re.sub(r'[^A-Z]', '', line)  # remove all non-alphabet chars
            start_time = time.time()
            st = lpsst(line)
            end_time = time.time()
            time_st = end_time - start_time
            start_time = time.time()
            sq = lpssq(line)
            end_time = time.time()
            time_sq = end_time - start_time
            results.append([line, len(line), st, len(st), time_st, sq, len(sq), time_sq])
    headers = ["String", "Length", "LPSST", "Length", "Time", "LPSSQ", "Length", "Time"]
    tt = texttable.Texttable(500)
    tt.set_cols_align(["l", "r", "l", "r", "r", "l", "r", "r"])
    tt.set_cols_dtype(["t", "i", "t", "i", "f", "t", "i", "f"])
    tt.add_rows(results)
    tt.header(headers)
    print(tt.draw())
    return results


def main():
    process_file('sentences.txt')
    process_file('palindromes.txt')





if __name__ == "__main__":
    main()
