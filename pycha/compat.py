import sys

# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3


if PY3:  # pragma: no cover
    from inspect import getfullargspec  # noqa
else:  # pragma: no cover
    from inspect import getargspec as getfullargspec  # noqa
