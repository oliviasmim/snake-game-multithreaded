#!/bin/python
import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

"""
Considere um conjunto de threads TP_1, TP_2, ..., TP_N TP2 compartilhando um vetor chamado "mapa" com X posições iniciadas com valores (0, None).

O código em cada thread tem duas funções. 
    A primeira é produzir Y números aleatórios entre 0 e N-1 (as posições possíveis em "mapa"). 
    A segunda é acessar o vetor mapa, executar uma função "estimativa_montecarlo_pi()" e escrever o resultado desta função em cada posição definida pelos Y números.

Considere também que o vetor é uma região crítica. Como seria a solução deste cenário usando exclusão mútua?
"""
# Número de posicoes no vetor mapa
tamanho_vetor = 10

# Número de tentativas para cada thread
n_tentativas = 30

# vetor "mapa" com N posições iniciadas com 0
mapa = [(0, None) for _ in range(tamanho_vetor)]

# Usando o método Lock para garantir que apenas uma thread tenha acesso a uma região crítica 
# Note que ainda é necessário organizar a "regra de negócio do código".
# Leia mais em: https://docs.python.org/3/glossary.html#term-global-interpreter-lock
mapa_lock = threading.Lock()
# para facilitar o Log, inclui uma variável que vai ajudar a informar qual a thread que está usando o "mapa_lock" 
# no momento em que outra thread estiver aguardando.
lock_holder = None  # Variável para armazenar o ID da thread que possui o lock

# Estimando o valor de pi usando o método de Monte Carlo
# Quanto maior o número 'n', mais precisa será a estimativa. 
# Quanto mais precisa, mais complexa é a execução. 
def estimativa_montecarlo_pi():
    n = random.choice([1000, 5000, 10000, 50000, 100000, 500000, 1000000, 5000000])
    dentro_circulo = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            dentro_circulo += 1
    return 4 * dentro_circulo / n

# Definindo a 'regra de negócio'. Cada thread deve executar a mesma função. 
def thread_function(thread_id):
    # Produzir Y números aleatórios entre 0 e X-1
    posicoes = [random.randint(0, tamanho_vetor-1) for _ in range(n_tentativas)]

    # Varrer todas as posições produzidas aleatoriamente. 
    # Atente para incluir apenas posicoes que existem no vetor.
    for pos in posicoes:
        print(f"Thread {thread_id} tentando adquirir o mapa_lock...")
        
        # Inclui, em três momentos, linhas que garantem execução assíncrona e concorrente
        #   1) incluindo a diretiva "mapa_lock.acquire(timeout=1)". Veja detalhes em https://docs.python.org/3/library/threading.html#threading.Lock.acquire
        #   2) estimação de pi com diferente numero de pontos, e, portanto, diferentes tempos de execução. 
        #   3) incluindo um tempo 'aleatório' para cada thread dormir depois de conseguir acesso ao mapa_lock em 'time.sleep(random.uniform(0.01, 0.1))'
        if mapa_lock.acquire(timeout=1):  # Tentar adquirir o lock com timeout de 1 segundo
            try:
                print(f"Thread {thread_id} conseguiu adquirir o mapa_lock.")
                # Simular carga de trabalho
                time.sleep(random.uniform(0.01, 0.1))
                # Testar se alguma outra Thread já escreveu nesta posiçãos
                if mapa[pos] == (0, None):
                    # Executar a função estimativa e escrever o resultado na posição do vetor
                    mapa[pos] = (estimativa_montecarlo_pi(), thread_id)
                    print(f"Thread {thread_id} escreveu no mapa na posição {pos}.")
                else: 
                    print(f"A posição {pos} do mapa já foi usada: {mapa[pos]}.")
            finally:
                mapa_lock.release()
                print(f"Thread {thread_id} acaba de liberar o Lock.")
        else:
            print(f"Thread {thread_id} precisou aguardar para adquirir o mapa_lock.")

# Função principal que usa ThreadPoolExecutor
def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(thread_function, 1)
        executor.submit(thread_function, 2)
        executor.submit(thread_function, 3)

    # Mostrar o vetor "mapa" após a execução das threads
    print("Vetor 'mapa' após execução das threads:")
    for i, valor in enumerate(mapa):
        print(f"Posição {i}: {valor}")

if __name__ == "__main__":
    main()
