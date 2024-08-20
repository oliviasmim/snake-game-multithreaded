import time

class Semaforo:
    def __init__(self, quantidadeThreads):
        self.quantidade = quantidadeThreads  
        self.quantidade_lock = 0    # Lock 

    def increment(self):
        while True:
            if self.quantidade_lock == 0:
                self.quantidade_lock = 1  
                self.quantidade += 1
                self.quantidade_lock = 0  
                break

    def decrement(self):
        while True:
            if self.quantidade_lock == 0:
                self.quantidade_lock = 1  
                if self.quantidade > 0:
                    self.quantidade -= 1
                    self.quantidade_lock = 0 
                    return True  # Returna True if acquire
                self.quantidade_lock = 0  

    def acquire(self):
        while True:
            if self.decrement():
                return True
            else:
                time.sleep(0.01) 

    def release(self):
        self.increment()
