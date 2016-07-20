# hack_slurm #

This repository hosted scripts that I created to make use of multicores on high-performance cmputing environment and parallelly run several lines of codes simultaneously. 

My work flow is:

```
$ slurmJob.py -c ${COMMAND_LIST} -j ${JOB_NAME} -N 1 -n ${NUMBER_OF_JOBS} -A ${ALLOCATION} \
			-t ${TIME} -p ${HOW_MANY_JOBS_TO_RUN_AT_SAME_TIME}    # This creates several slurm scripts
$ batch_submit # This submits all the slurm scripts
# batch_del ${JOB_NAME} # This grep everything from the slurm queue that has the jobname and do $(scancel)
```
