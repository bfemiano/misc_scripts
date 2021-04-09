import os

class WarioLocalTarget(object):

    def __init__(self, path):
        self.path = path

    def exists(self):
        return os.path.isfile(self.path)

class WarioTask(object):

    def __init__(self, *args, **kwargs):
        self.task_id = '%s (%s)' % (self.__class__.__name__ , ','.join(args))

    def run(self):
        pass #By default, do nothing. Some tasks will only have requirements.

    def output(self):
        raise NotImplementedError

    def complete(self):
        output = self.output()
        if not output:
            return False
        if not isinstance(output, list):
            output = [output]
        return all(o.exists() for o in output)

    def requires(self):
        return None

class WarioWrapperTask(WarioTask):

    def complete(self):
        reqs = self.requires()
        if not reqs:
            return True
        if not isinstance(reqs, list):
            reqs = [reqs]
        return all(r.complete() for r in reqs)

class WarioTaskNotComplete(ValueError):
    pass


def wario_run(task):
    if not isinstance(task, WarioTask):
        raise ValueError("Task is not an instance of WarioTask, instead found %s" % task.__class__.__name__)

    if not task.complete():
        reqs = task.requires()
        if reqs and not isinstance(reqs, list):
            reqs = [reqs]
        if reqs and not all(r.complete() for r in reqs):
            for r in reqs:
                wario_run(r)
        print 'Requirements met for task %s, RUNNING.' % task.task_id
        task.run()
        if not task.complete():
            raise WarioTaskNotComplete("Ran task %s but it still is not complete. " % task.task_id)
    print 'Done task %s ' % task.task_id
