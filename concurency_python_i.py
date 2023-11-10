import threading
import multiprocessing
import os


def hello_from_process():
    print(f'Hello from child process {os.getpid()}!')

def hello_from_thread():
    print(f"Hello from thread {threading.current_thread()}!")


# hello_thread = threading.Thread(target=hello_from_thread)
# hello_thread.start()

# total_threads = threading.active_count()
# thread_name = threading.current_thread().name

# print(f"Python is currently running {total_threads} thread(s)")
# print(f"The current thread is {thread_name}")

# hello_thread.join()

if __name__ == '__main__':
    hello_process = multiprocessing.Process(target=hello_from_process)
    hello_process.start()
    print(f'Hello from parent process {os.getpid()}')
    hello_process.join()
