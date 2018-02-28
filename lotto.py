#!/usr/bin/env python

import random
import sys

def get_numbers(max):
    nums = set()
    while len(nums) < 7:
        num = random.SystemRandom().randint(1, max)
        strnum = '{:>4}'.format(num)
        nums.add(strnum)
    return nums

if __name__ == '__main__':
    if len(sys.argv) > 1:
        rows = int(sys.argv[1])
    else:
        rows = 1
    print "Lotto, " + str(rows) + " rows"
    for line in range(0, rows):
        for num in sorted(get_numbers(40)):
            sys.stdout.write(num)
        print
