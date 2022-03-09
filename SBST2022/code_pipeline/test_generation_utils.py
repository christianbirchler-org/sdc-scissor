"""
Function / decorator which tries very hard to register a function to be executed at importerer exit.

Author:     Giampaolo Rodola'
License:    MIT
Link:       https://grodola.blogspot.com/2016/02/how-to-always-execute-exit-functions-in-py.html


"""

from __future__ import print_function
import atexit
import os
import functools
import signal
import sys


_registered_exit_funs = set()
_executed_exit_funs = set()


def register_exit_fun(fun=None, signals=[signal.SIGTERM],
                      logfun=lambda s: print(s, file=sys.stderr)):
    """Register a function which will be executed on "normal"
    interpreter exit or in case one of the `signals` is received
    by this process (differently from atexit.register()).
    Also, it makes sure to execute any other function which was
    previously registered via signal.signal(). If any, it will be
    executed after our own `fun`.

    Functions which were already registered or executed via this
    function will be ignored.

    Note: there's no way to escape SIGKILL, SIGSTOP or os._exit(0)
    so don't bother trying.

    You can use this either as a function or as a decorator:

        @register_exit_fun
        def cleanup():
            pass

        # ...or

        register_exit_fun(cleanup)

    Note about Windows: I tested this some time ago and didn't work
    exactly the same as on UNIX, then I didn't care about it
    anymore and didn't test since then so may not work on Windows.

    Parameters:

    - fun: a callable
    - signals: a list of signals for which this function will be
      executed (default SIGTERM)
    - logfun: a logging function which is called when a signal is
      received. Default: print to standard error. May be set to
      None if no logging is desired.
    """
    def stringify_sig(signum):
        if sys.version_info < (3, 5):
            smap = dict([(getattr(signal, x), x) for x in dir(signal)
                         if x.startswith('SIG')])
            return smap.get(signum, signum)
        else:
            return signum

    def fun_wrapper():
        if fun not in _executed_exit_funs:
            try:
                fun()
            finally:
                _executed_exit_funs.add(fun)

    def signal_wrapper(signum=None, frame=None):
        if signum is not None:
            if logfun is not None:
                logfun("signal {} received by process with PID {}".format(
                    stringify_sig(signum), os.getpid()))
        fun_wrapper()
        # Only return the original signal this process was hit with
        # in case fun returns with no errors, otherwise process will
        # return with sig 1.
        if signum is not None:
            if signum == signal.SIGINT:
                raise KeyboardInterrupt
            # XXX - should we do the same for SIGTERM / SystemExit?
            print("DEBUG calling sys.exit with ", signum)
            sys.exit(signum)

    def register_fun(fun, signals):
        if not callable(fun):
            raise TypeError("{!r} is not callable".format(fun))
        set([fun])  # raise exc if obj is not hash-able

        signals = set(signals)
        for sig in signals:
            # Register function for this signal and pop() the previously
            # registered one (if any). This can either be a callable,
            # SIG_IGN (ignore signal) or SIG_DFL (perform default action
            # for signal).
            old_handler = signal.signal(sig, signal_wrapper)
            if old_handler not in (signal.SIG_DFL, signal.SIG_IGN):
                # ...just for extra safety.
                if not callable(old_handler):
                    continue
                # This is needed otherwise we'll get a KeyboardInterrupt
                # strace on interpreter exit, even if the process exited
                # with sig 0.
                if (sig == signal.SIGINT and
                        old_handler is signal.default_int_handler):
                    continue
                # There was a function which was already registered for this
                # signal. Register it again so it will get executed (after our
                # new fun).
                if old_handler not in _registered_exit_funs:
                    atexit.register(old_handler)
                    _registered_exit_funs.add(old_handler)

        # This further registration will be executed in case of clean
        # interpreter exit (no signals received).
        if fun not in _registered_exit_funs or not signals:
            atexit.register(fun_wrapper)
            _registered_exit_funs.add(fun)

    # This piece of machinery handles 3 usage cases. register_exit_fun()
    # used as:
    # - a function
    # - a decorator without parentheses
    # - a decorator with parentheses
    if fun is None:
        @functools.wraps
        def outer(fun):
            return register_fun(fun, signals)
        return outer
    else:
        register_fun(fun, signals)
        return fun