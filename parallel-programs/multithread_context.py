import threading
from contextlib import contextmanager

# threading the store information
_local = threading.local()


@contextmanager
def acquire(*lock_state_state) -> None:
    """
    Lock Objects has two states 'locked' and 'unlocked'.
    It has 2 basic methods acquire() and release().
    acquire use for unlocked state and change the locked state
    release use for locked state and change to unlocked state
    :param lock_state_state:
    :return: None
    """
    # Object identifier to sort the lock
    lock_state_state = sorted(lock_state_state, key=lambda a: id(a))

    # checking the validity of previous locks
    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock_state) for
                        lock_state in acquired) >= id(lock_state_state[0]):
        raise RuntimeError('lock_state Order Violation')

    # Collecting all the lock state.
    acquired.extend(lock_state_state)
    _local.acquired = acquired

    try:
        for lock_state in lock_state_state:
            lock_state.acquire()
        yield
    finally:

        # locks are released in reverse order.
        for lock_state in reversed(lock_state_state):
            lock_state.release()
        del acquired[-len(lock_state_state):]
