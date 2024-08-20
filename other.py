import threading
import time

class CustomSemaphore:
    def __init__(self, initial):
        self.value = initial  # Initial number of permits
        self.value_lock = 0    # Lock variable (0 means unlocked, 1 means locked)
        self.waiting_threads = 0  # Count of waiting threads

    def atomic_increment(self):
        # Spinlock to simulate an atomic increment
        while True:
            if self.value_lock == 0:
                self.value_lock = 1  # Acquire the lock
                self.value += 1
                self.value_lock = 0  # Release the lock
                break

    def atomic_decrement(self):
        # Spinlock to simulate an atomic decrement
        while True:
            if self.value_lock == 0:
                self.value_lock = 1  # Acquire the lock
                if self.value > 0:
                    self.value -= 1
                    self.value_lock = 0  # Release the lock
                    break
                self.value_lock = 0  # Release the lock

    def acquire(self):
        while True:
            self.atomic_decrement()
            if self.value >= 0:
                break
            else:
                self.atomic_increment()
                time.sleep(0.01)  # Sleep to simulate yielding the processor

    def release(self):
        self.atomic_increment()

def critical_section(thread_id, custom_sem):
    print(f"Thread {thread_id} attempting to enter critical section.")
    
    custom_sem.acquire()
    try:
        print(f"Thread {thread_id} has entered the critical section.")
        time.sleep(1)  # Simulate work in the critical section
    finally:
        print(f"Thread {thread_id} is leaving the critical section.")
        custom_sem.release()

# Create a custom semaphore with 2 permits
custom_sem = CustomSemaphore(2)

# Create and start 4 threads
threads = []
for i in range(4):
    t = threading.Thread(target=critical_section, args=(i, custom_sem))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

print("All threads have finished.")
