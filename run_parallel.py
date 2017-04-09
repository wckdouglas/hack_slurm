#!/usr/bin/env python

from multiprocessing import Pool
import sys
import os


def run_command(command):
    print 'Running: %s' %command
    os.system(command)
    return 0

def main():
    if len(sys.argv) != 3:
        sys.exit('[usage] python %s <threads> <command list>' %(sys.argv[0]))
    threads = int(sys.argv[1].split('j')[1])
    print 'Using threads %i' %threads
    commands = [line.strip() for line in open(sys.argv[2])]
    pool = Pool()
    pool.map(run_command, commands)

if __name__ == '__main__':
    main()

