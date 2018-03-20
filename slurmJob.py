#!/usr/bin/env python

from __future__ import print_function
import fileinput
import argparse
import os
import sys
import subprocess

def writeJob(commandlist, jobname, commandRank, numberOfJob, numberOfNode, allocation, queue, time, concurrent_job):
    commandFiles = 'command_%i.bash' %commandRank
    options = \
        "#!/bin/bash \n" +\
        "#SBATCH -J %s # Job name \n"                       %(jobname) +\
        "#SBATCH -N %i   # Total number of nodes \n"        %(numberOfNode)+\
        "#SBATCH -n 24   # Total number of tasks %i\n"         %(numberOfJob)+\
        "#SBATCH -p %s    # Queue name \n"                  %(queue)+\
        "#SBATCH -o %s.o%s # Name of stdout output file \n" %(jobname,'%j')+ \
        "#SBATCH -t %s # Run time (hh:mm:ss) \n"            %time +\
        "#SBATCH -A %s \nmodule load gcc\nmodule load java\n" %(allocation)  +\
        'ulimit -c unlimited\n' +\
        "export PATH=%s:$PATH"  %('/'.join(str(subprocess.check_output(['which' ,'python'])).split('/')[:-1]))
    with open('launcher_%i.slurm' %(commandRank), 'w') as slurmFile:
        print(options, file = slurmFile)
        if concurrent_job == 1:
            print('bash %s' %(commandFiles), file = slurmFile) 
        else:
            print('parallel -j%i :::: %s \n' %(concurrent_job,commandFiles), file = slurmFile) 
    with open(commandFiles,'w') as commandFile:
        print('\n'.join(commandlist) + '\n', file = commandFile)
    return 0

def main(args):
    commandFile = args.cmdlst
    jobname = args.jobname
    numberOfJob = args.numberOfCmd
    numberOfNode = args.numberOfNode
    allocation = args.allocation
    queue = args.queue  
    time = args.time
    concurrent_job = args.processes
    with open(commandFile,'r') as f:
        commands = f.readlines()
        commandlist = []
        i = 0
        commandRank = 0
        for command in commands: 
            commandlist.append(str(command).strip())
            i += 1
            if i % numberOfJob == 0: 
                writeJob(commandlist, jobname, commandRank, numberOfJob, numberOfNode, allocation, queue, time, concurrent_job)
                commandRank += 1
                i = 0
                commandlist=[]
    if commandlist:
        writeJob(commandlist, jobname, commandRank, i, numberOfNode, allocation, queue, time, concurrent_job)
        commandRank += 1
    print('Written %i scripts' %commandRank, file = sys.stdout)
    return 0

if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='A script to create slurm scripts from list of commands')
        parser.add_argument('-c', '--cmdlst', help='A list of command, each line is a command', required=True)
        parser.add_argument('-j', '--jobname', default='job',help='Jobname (default: job)')
        parser.add_argument('-N', '--numberOfNode', default=1, type=int, help='Number of node for each job (default: 1)')
        parser.add_argument('-n', '--numberOfCmd', default=1, type=int, help='Number of command per node (default: 1)')
        parser.add_argument('-A', '--allocation', default = '2013lambowitz', 
                help= 'Account (default: 2013lambowitz)', 
                choices = {'tRNA-profiling-and-b', '2013lambowitz', 'Exosome-RNA-seq'})
        parser.add_argument('-t', '--time', default='01:00:00', help='Run time (hh:mm:ss) default: 1:00:00')
        parser.add_argument('-q','--queue', default='normal',help='Queue (default: normal)')
        parser.add_argument('-p','--processes', default=24,help='How many process to run in the same time (default: 24)', type=int)
        args = parser.parse_args()
        main(args)
