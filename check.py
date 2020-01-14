#!/usr/bin/python
# -*- coding: utf-8 -*-
# test.py

from progress.bar import Bar, IncrementalBar
from progress.spinner import Spinner
import time
import os
import subprocess
import settings as set

global repeat
repeat = False

def check():
    #set.readNodes()
    global repeat
    repeat = False
    overallCheck = True
    sumB = 0
    babeld = []
    sumT = 0
    tracker = []
    for node in set.name:
        tmp = subprocess.check_output(['docker exec mn.%s docker ps' % node],shell=True)
        doc = open('./tmp.txt', 'w+')
        doc.write(tmp)
        doc.close()
        checkB = False #Check for babeld container
        checkT = False #Check for opentracker container

        with open('./tmp.txt') as info:
            lines = info.readlines()
            for line in lines:
                tmp = line.split()
                #print tmp[-1]
                if tmp[-1] == 'babeld':
                    checkB = True
                if node in set.servers:
                    if tmp[-1] == 'opentracker':
                        checkT = True
                else:
                    checkT = True
        if checkB == False:
            overallCheck = False
            babeld.append(node)
            sumB = sumB + 1
        if checkT == False:
            overallCheck = False
            tracker.append(node)
            sumT = sumT + 1

    print ('%s container(s) not running babeld: %s' % (str(sumB),babeld))
    print ('%s container(s) not running opentracker: %s' % (str(sumT),tracker))

    #print ('%s babeld container not running correctly\n%s opentracker container not running correctly' % (str(sumB), str(sumT)))

    for node in babeld:
        if node in set.servers:
            subprocess.call(["docker exec mn.%s sh -c 'export IP=%s && docker-compose -f stack_server.yml up -d'" % (node, set.ip[set.name.index(node)])],shell=True)
        else:
            subprocess.call(["docker exec mn.%s sh -c 'export IP=%s && docker-compose -f stack_client.yml up -d'" % (node, set.ip[set.name.index(node)])],shell=True)
    for node in tracker:
        if not node in babeld:
            subprocess.call(["docker exec mn.%s sh -c 'export IP=%s && docker-compose -f stack_server.yml up -d'" % (node, set.ip[set.name.index(node)])],shell=True)

    if overallCheck == True:
        repeat = False
    else:
        repeat = True
#check()
