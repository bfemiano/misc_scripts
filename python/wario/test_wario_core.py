from unittest2 import TestCase

from lib.bdm.wario.task import wario_run, WarioTask, WarioTaskNotComplete, WarioWrapperTask


class NotWarioTask(object):
    pass

class WarioTaskNoDependenciesThatRuns(WarioTask):

    def __init__(self, *args, **kwargs):
        super(WarioTaskNoDependenciesThatRuns, self).__init__(*args, **kwargs)
        self.finished = False

    def run(self):
        self.finished = True

    def complete(self):
        return self.finished

class WarioTaskNoDependenciesThatFails(WarioTask):

    def __init__(self, *args, **kwargs):
        super(WarioTaskNoDependenciesThatFails, self).__init__(*args, **kwargs)
        self.finished = False

    def complete(self):
        return self.finished



class WarioTaskWithDependencies(WarioTaskNoDependenciesThatRuns):

    def __init__(self, *args, **kwargs):
        super(WarioTaskWithDependencies, self).__init__(*args, **kwargs)
        self.dep = WarioTaskNoDependenciesThatRuns() #requires() will otherwise build a new instance each call.

    def requires(self):
        return self.dep

class WarioTaskWhereDependenciesFail(WarioTaskNoDependenciesThatRuns):

    def __init__(self, *args, **kwargs):
        super(WarioTaskWhereDependenciesFail, self).__init__(*args, **kwargs)
        self.dep = WarioTaskNoDependenciesThatFails()

    def requires(self):
        return self.dep


class FakeWarioWrapperClass(WarioWrapperTask):

    def __init__(self, *args, **kwargs):
        super(FakeWarioWrapperClass, self).__init__(*args, **kwargs)
        self.first_dep = WarioTaskNoDependenciesThatRuns()
        self.second_dep = WarioTaskWithDependencies()

    def requires(self):
        return [
            self.first_dep,
            self.second_dep,
        ]

class MockOutputTargetExists(object):

    def exists(self):
        return True

class MockOutputTargetDoesNotExist(object):

    def exists(self):
        return False

class WarioTaskWithDefaultCompleteSuccess(WarioTask):

    def output(self):
        return MockOutputTargetExists()

class WarioTaskWithDefaultCompleteFail(WarioTask):

    def output(self):
        return [
            MockOutputTargetDoesNotExist()
        ]

class TestWario(TestCase):

    def test_not_wario_task(self):
        #throw exception if not wario task.
        task = NotWarioTask()
        try:
            wario_run(task)
            self.fail("Should not run task")
        except ValueError as e:
            self.assertEqual(e.message, "Task is not an instance of WarioTask, instead found NotWarioTask")

    def test_no_reqs_just_runs_and_completes(self):
        task = WarioTaskNoDependenciesThatRuns()
        wario_run(task)
        self.assertTrue(task.complete())

    def test_no_reqs_runs_but_does_not_complete(self):
        task = WarioTaskNoDependenciesThatFails()
        try:
            wario_run(task)
            self.fail("Should throw exception")
        except WarioTaskNotComplete:
            pass
        finally:
            self.assertFalse(task.complete())

    def test_with_reqs_recurses_and_completes_all_tasks(self):
        task = WarioTaskWithDependencies()
        wario_run(task)
        self.assertTrue(task.complete())
        self.assertTrue(all([t.complete() for t in [task.requires()]]))


    def test_with_reqs_recurses_but_dependency_fails(self):
        task = WarioTaskWhereDependenciesFail()
        try:
            wario_run(task)
            self.fail("It should throw an exception")
        except WarioTaskNotComplete:
            pass
        finally:
            self.assertFalse(task.complete())

    def test_with_mock_output_succeeds(self):
        task = WarioTaskWithDefaultCompleteSuccess()
        wario_run(task)
        self.assertTrue(task.complete())

    def test_with_mock_output_fails(self):
        task = WarioTaskWithDefaultCompleteFail()
        try:
            wario_run(task)
            self.fail("Should throw no complete exception")
        except WarioTaskNotComplete:
            pass
        finally:
            self.assertFalse(task.complete())

    def test_wrapper_task(self):
        task = FakeWarioWrapperClass()
        wario_run(task)
        self.assertTrue(task.complete())