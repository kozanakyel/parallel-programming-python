import threading

from multithread_context import acquire

lock_state_1 = threading.Lock()
lock_state_2 = threading.Lock()


def thread_1():
    while True:
        with acquire(lock_state_1, lock_state_2):
            print('thread-1')


def thread_2():
    while True:
        with acquire(lock_state_2, lock_state_1):
            print('thread-2')


t1 = threading.Thread(target=thread_1)

t1.daemon = True
t1.start()

t2 = threading.Thread(target=thread_2)
t2.daemon = True
t2.start()
