import threading
import time

class CustomSemaphore:
    def __init__(self, initial):
        self.value = initial  # Initial number of permits
        self.condition = threading.Condition()

    def acquire(self):
        with self.condition:
            while self.value <= 0:
                self.condition.wait()  # Wait until a permit is available
            self.value -= 1  # Decrement the number of available permits

    def release(self):
        with self.condition:
            self.value += 1  # Increment the number of available permits
            self.condition.notify()  # Notify waiting threads that a permit is available

# Create a custom semaphore with 2 permits
custom_sem = CustomSemaphore(2)

def critical_section(thread_id):
    print(f"Thread {thread_id} attempting to enter critical section.")
    
    custom_sem.acquire()  # Custom semaphore acquire (wait)
    try:
        print(f"Thread {thread_id} has entered the critical section.")
        time.sleep(1)  # Simulate work in the critical section
    finally:
        print(f"Thread {thread_id} is leaving the critical section.")
        custom_sem.release()  # Custom semaphore release (signal)

# Create and start 4 threads
threads = []
for i in range(4):
    t = threading.Thread(target=critical_section, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

print("All threads have finished.")
