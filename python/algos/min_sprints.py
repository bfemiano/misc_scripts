# In each sprint, you can *take any number of jobs as long as you have finished all the dependencies before*. Given n jobs and its dependencies, find out minimum number of sprints needed to finish all jobs.

"""
Example:

Input: n = 3, [[0, 2], [1, 2]] // 2 depends on 0; 2 depends on 1
Sprint 1: Take job 0 and 1
Sprint 2: Take job 2
Minimum number of sprints = 2

Sprint 1: Take job 2 -> invalid

Input: n = 4, [[0, 3], [1, 2], [2, 3]]
Sprint 1: Take job 0 and 1
Sprint 2: Take job 2
Sprint 3: Take job 3
Minimum number of sprints = 3

O(n * m)
m = len(dep)
"""

import pytest

def minSprint(n, deps):
    if n == 1:
        return 1
    sprints = 0
    deps_graph = dict()
    for d in deps:
        if d[1] not in deps_graph.keys():
            deps_graph[d[1]] = set()
        if d[0] not in deps_graph.keys():
            deps_graph[d[0]] = set()
        deps_graph[d[1]].add(d[0])

    jobsLeft = n
    jobsRun = set()
    while(jobsLeft > 0):
        jobsRunThisSprint = set()
        for job_id in deps_graph.keys():
            deps = deps_graph[job_id]
            if deps - jobsRun == set() and deps.intersection(jobsRunThisSprint) == set() and job_id not in jobsRun:
                jobsLeft -= 1
                jobsRun.add(job_id)
                jobsRunThisSprint.add(job_id)
        sprints += 1
            
    return sprints


def minSprints2(n, deps):
    if n == 1:
        return 1
    sprints = 1
    deps_graph = dict()
    for d in deps:
        if d[1] not in deps_graph.keys():
            deps_graph[d[1]] = set()
        if d[0] not in deps_graph.keys():
            deps_graph[d[0]] = set()
        deps_graph[d[1]].add(d[0])
    
    
    def _walk(deps, sprints, searched):
        for job_id in deps:
            if len(deps_graph[job_id]) > 0 and job_id not in searched:
                searched.add(job_id)
                sprints = _walk(deps, sprints+1, searched)
        return sprints
    return _walk(deps_graph.keys(), sprints, set())
  
pytest.main()

def test_1sprint():
    assert minSprints2(1, [[0, 0]]) == 1

def test_2sprints():
    assert minSprints2(3, [[0, 2], [1, 2]]) == 2
    
def test_multiIn2Sprint():
    assert minSprints2(4, [[0, 3], [1, 3], [2, 3]]) == 2
    
def test_3sprints():
    assert minSprints2(4, [[0, 3], [1, 2], [2, 3]]) == 3
    
def test_4sprints():
    # 4 sprints because 3 -> {0, 2}, 2 -> 1, 1 -> 0, and there's 0
    assert minSprints2(4, [[0, 3], [1, 2], [2, 3], [0, 1]]) == 4
    
