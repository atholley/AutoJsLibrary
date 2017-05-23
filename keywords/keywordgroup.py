"""
Copyright 15/06/2017 UNSW Testing - Abu Tholley

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import inspect

try:
    from decorator import decorator
except SyntaxError:  # decorator module requires Python/Jython 2.4+
    decorator = None
if sys.platform == 'cli':
    decorator = None  # decorator module doesn't work with IronPython 2.6


def _run_on_failure_decorator(method, *args, **kwargs):
    """
    A decorator to run when the tests fail
    :param method: the method to run
    :param args: the tuple arguments to pass to the method
    :param kwargs: the dict arguments to pass to the method
    :return: runs the method on failure, raises exception if the method itself fails
    """
    try:
        return method(*args, **kwargs)
    except Exception, err:
        self = args[0]
        if hasattr(self, '_run_on_failure'):
            self._run_on_failure()
        raise


class KeywordGroupMetaClass(type):
    def __new__(mcs, clsname, bases, dict):
        if decorator:
            for name, method in dict.items():
                if not name.startswith('_') and inspect.isroutine(method):
                    dict[name] = decorator(_run_on_failure_decorator, method)
        return type.__new__(mcs, clsname, bases, dict)


class KeywordGroup(object):
    __metaclass__ = KeywordGroupMetaClass
