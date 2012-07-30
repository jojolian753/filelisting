#!/usr/bin/env python
# -*- coding: utf-8 -*-

def gen_int():
    i = 0

    while True:
        yield i
        i += 1

test = gen_int()

print test.next()
print test.next()
print test.next()
print test.next()
print test.next()
