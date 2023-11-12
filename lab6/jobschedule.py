import numpy as np
def max_profit_schedule(jobs):
    '''
    Find the schedule to maximize the profit given a list of jobs.
    
    Parameters:
        - jobs: a list of jobs, where each job is a tuple of (processing time, profit, deadline)
    
    Returns:
        - max profit: the maximum profit that can be obtained by scheduling the jobs
        - schedule: a list of job indexes that gives the maximum profit (in chronological order)
    '''
    # Sort jobs according to deadlines
    jobs.sort(key=lambda x: x[2])
    n = len(jobs)
    ddl_latest = jobs[-1][2]    # latest deadline
    dp = np.zeros((n+1, ddl_latest+1), dtype=int)  # dynamic programming table
    
    for i in range(1,n+1):  # i: job index+1
        for j in range(1, ddl_latest+1):  # j: deadline
            ti = jobs[i-1][0]
            pi = jobs[i-1][1]
            di = jobs[i-1][2]
            tmp = min(di, j) - ti  # tmp: the latest time to start job i
            if tmp < 0:  # cannot start job i
                dp[i][j] = dp[i-1][j]
            else:  # can start job i
                dp[i][j] = max(dp[i-1][j], dp[i-1][tmp] + pi)  # max profit of job i
    
    max_profit = dp[n][ddl_latest]
    # Trace back through the dp table to find the jobs that were scheduled
    schedule = []
    j = ddl_latest
    for i in range(n,0,-1):
        if dp[i][j] != dp[i-1][j]:  # job i-1 is scheduled
            schedule.append(i-1)
            j = j - jobs[i-1][0]  # move to the time slot before the start of this job
    schedule.reverse()
    return max_profit, schedule


# test
sample_jobs = [
    [(2, 60, 3), (1, 100, 2), (3, 20, 4), (2, 40, 4)],
    [(3, 100, 4), (1, 80, 1), (2, 70, 2), (1, 10, 3)],
    [(4, 100, 4), (2, 75, 3), (3, 50, 3), (1, 25, 1)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 3), (2, 40, 2), (2, 50, 3)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 4), (2, 40, 4), (2, 50, 3), (1, 80, 2)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 3), (2, 40, 2),
     (2, 50, 3), (1, 80, 2), (4, 90, 4)],
    [(3, 60, 3), (2, 100, 2), (1, 20, 2), (2, 40, 4), (4, 50, 4)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 3), (2, 40, 2),
     (4, 50, 4), (1, 80, 2), (4, 90, 4)],
    [(3, 60, 3), (2, 100, 2), (1, 20, 2), (2, 40, 2), (4, 50, 4), (5, 70, 5)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 3),
     (2, 40, 2), (4, 50, 4), (5, 70, 5), (3, 90, 4)]
]
for jobs in sample_jobs:
    max_profit, schedule = max_profit_schedule(jobs)
    print(max_profit, [jobs[idx] for idx in schedule])
