import pandas as pd
import numpy as np
import random as rd
import math

def toss(val):
    n = rd.random() * 100
    if n < val:
        return -1
    else:
        return 1

def cal_height(max_stack_height):
    n = rd.random() * max_stack_height
    n = int(n)
    flag = rd.random() * 100
    if flag >= 80:
        return n
    else:
        return max_stack_height

def create_stack(max_stack_height):
    stack = list()
    # n = 94
    h = cal_height(max_stack_height)
    r = cal_height(int(h * .3))
    for i in range(r):
        stack.append(-1)
    for i in range(h - r):
        stack.append(1)
        # n = math.sqrt(n)
    return stack

def create_row(no_of_stacks, max_stack_height):
    stacks = list()
    for i in range(no_of_stacks):
        stacks.append(create_stack(max_stack_height))
    return stacks

def create_final_stack_in_alph(stacks):
    alp = list()
    for letter in range(ord('A'), ord('Z') + 1):
        alp.append(chr(letter))

    final_stack = list()
    row = 1
    for stack in stacks:
        s = list()
        col = 0
        for c in stack:
            if c == -1:
                s.append('F')
            elif c == 1:
                val = str(row) + alp[col]
                s.append(val)
                col += 1
        final_stack.append(s)
        row += 1
    return final_stack

def make_liner_array_of_loading_cont(loading_plan, row_height):
    liner_array = list()
    for i in range(len(loading_plan)):
        cnt = 0
        for j in range(row_height):
            value = loading_plan.iloc[i, j]
            if pd.isna(value) == False:
                cnt += 1
                liner_array.append(value)
    return liner_array

def create_df_to_2d_array(df, row_height):
    arr = []
    for i in range(len(df)):
        row = []
        for j in range(row_height):
            val = df.iloc[i, j]
            if pd.isna(val) == False:
                row.append(val)
        arr.append(row)
    return arr

def create_dock_stacks_plan(liner_array_of_loading_plan, no_of_dock_stacks, max_stack_height):
    dock_stacks = [[] for _ in range(no_of_dock_stacks)]
    for cont in liner_array_of_loading_plan:
        key = np.random.randint(0, no_of_dock_stacks)
        if len(dock_stacks[key]) == max_stack_height:
            while len(dock_stacks[key]) == max_stack_height:
                key = np.random.randint(0, no_of_dock_stacks)
        dock_stacks[key].append(cont)
    return dock_stacks