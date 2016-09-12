#!/usr/bin/env python

import fileinput
import argparse
import os
import subprocess

def writeJob(commandlist, jobname, commandRank, numberOfJob, numberOfNode, allocation, queue, time, concurrent_job):
    commandFiles = 'command_%i.bash' %commandRank
    options = \
	"#!/bin/bash \n" +\
	"#SBATCH -J %s # Job name \n"                       %(jobname) +\
	"#SBATCH -N %i   # Total number of nodes \n"        %(numberOfNode)+\
	"#SBATCH -n %i   # Total number of tasks\n"         %(numberOfJob)+\
	"#SBATCH -p %s    # Queue name \n"                  %(queue)+\
	"#SBATCH -o %s.o%s # Name of stdout output file \n" %(jobname,'%j')+ \
	"#SBATCH -t %s # Run time (hh:mm:ss) \n"            %time +\
	"#SBATCH -A %s \nmodule load gcc\n"                           %(allocation)  +\
        "export PATH=%s:$PATH\n"  %('/'.join(subprocess.check_output(['which' ,'python']).split('/')[:-1]))
    with open('launcher_%i.slurm' %(commandRank), 'w') as slurmFile:
	slurmFile.write(options)
        if concurrent_job == 1:
            slurmFile.write('bash %s \n' %(concurrent_job,commandFiles)) 
        else:
            slurmFile.write('parallel -j%i :::: %s \n' %(concurrent_job,commandFiles)) 
    with open(commandFiles,'w') as commandFile:
        commandFile.write('\n'.join(commandlist) + '\n')
    return 0

def main(args):
    commandFile = args.cmdlst
    jobname = args.jobname
    numberOfJob = args.numberOfJob
    numberOfNode = args.numberOfNode
    allocation = args.allocation
    queue = args.queue	
    time = args.time
    concurrent_job = args.processes
    with open(commandFile,'ru') as f:
        commands = f.readlines()
        commandlist = []
        i = 0
        commandRank = 0
        for command in commands: 
            commandlist.append(command.strip())
            i += 1
            if i % numberOfJob == 0: 
    	        writeJob(commandlist, jobname, commandRank, numberOfJob, numberOfNode, allocation, queue, time, concurrent_job)
                commandRank += 1
		i = 0
                commandlist=[]
    if commandlist:
    	writeJob(commandlist, jobname, commandRank, i, numberOfNode, allocation, queue, time, concurrent_job)
        commandRank += 1
    print 'Written %i scripts' %commandRank

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='A script to create slurm scripts from list of commands')
	parser.add_argument('-c', '--cmdlst', help='A list of command, each line is a command', required=True)
	parser.add_argument('-j', '--jobname', default='job',help='Jobname (default: job)')
	parser.add_argument('-N', '--numberOfNode', default=1, type=int, help='Number of node for each command (default: 1)')
	parser.add_argument('-n', '--numberOfJob', default=1, type=int, help='Number of job per node (default: 1)')
	parser.add_argument('-A', '--allocation', default = '2013lambowitz', help= 'Account (default: 2013lambowitz)', choices = {'tRNA-profiling-and-b', '2013lambowitz', 'Exosome-RNA-seq'})
	parser.add_argument('-t', '--time', default='01:00:00', help='Run time (hh:mm:ss) default: 1:00:00')
	parser.add_argument('-q','--queue', default='normal',help='Queue (default: normal)')
        parser.add_argument('-p','--processes', default=24,help='How many process to run in the same time (default: 24)', type=int)
	args = parser.parse_args()
	main(args)
