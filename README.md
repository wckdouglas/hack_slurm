# hack_slurm #

This repository hosted scripts that I created to make use of multicores on high-performance cmputing environment and parallelly run several lines of codes simultaneously. 

Requirement:
[GNU parallel](http://www.gnu.org/software/parallel/)

My work flow is:

```
$ slurmJob.py -c ${COMMAND_LIST} -j ${JOB_NAME} -N 1 -n ${NUMBER_OF_JOBS} -A ${ALLOCATION} \
			-t ${TIME} -p ${HOW_MANY_JOBS_TO_RUN_AT_SAME_TIME}    # This creates several slurm scripts
$ batch_submit # This submits all the slurm scripts
$ batch_del ${JOB_NAME} # This grep everything from the slurm queue 
						# that has the jobname and do $(scancel)
```

Usage:
```
usage: slurmJob.py [-h] -c CMDLST [-j JOBNAME] [-N NUMBEROFNODE]
                   [-n NUMBEROFJOB]
                   [-A {Exosome-RNA-seq,tRNA-profiling-and-b,2013lambowitz}]
                   [-t TIME] [-q QUEUE] [-p PROCESSES]

A script to create slurm scripts from list of commands

optional arguments:
  -h, --help            show this help message and exit
  -c CMDLST, --cmdlst CMDLST
                        A list of command, each line is a command
  -j JOBNAME, --jobname JOBNAME
                        Jobname (default: job)
  -N NUMBEROFNODE, --numberOfNode NUMBEROFNODE
                        Number of node for each command (default: 1)
  -n NUMBEROFJOB, --numberOfJob NUMBEROFJOB
                        Number of job per node (default: 1)
  -A {Exosome-RNA-seq,tRNA-profiling-and-b,2013lambowitz}, --allocation {Exosome-RNA-seq,tRNA-profiling-and-b,2013lambowitz}
                        Account (default: 2013lambowitz)
  -t TIME, --time TIME  Run time (hh:mm:ss) default: 1:00:00
  -q QUEUE, --queue QUEUE
                        Queue (default: normal)
  -p PROCESSES, --processes PROCESSES
                        How many process to run in the same time (default: 24)
```
