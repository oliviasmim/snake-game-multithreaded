import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

random.seed(5)

# Define o mapa 
tamanho_mapa = 7
mapa_jogo = [[' ' for _ in range(tamanho_mapa)] for _ in range(tamanho_mapa)]

jogo_terminou = False
comida_posicoes = []
posicoes_validas = [' ', 'F']
# Placar do jogo, variável compartilhada
status_jogo =  [{'id': 1, 'status': 'viva', 'pontos': 0},
                {'id': 2, 'status': 'viva', 'pontos': 0}, 
                {'id': 3, 'status': 'viva', 'pontos': 0}, 
                {'id': 4, 'status': 'viva', 'pontos': 0}]

cobra_vencedora = None
mapa_lock = threading.Lock()
status_jogo_lock = threading.Lock()

access_counter = 0
counter_lock = threading.Lock()

def escrever_mapa_zona_critica():
    global access_counter
    with counter_lock:
        access_counter += 1
        print(f"Quantidade de threads tentando escrever na zona crítica do mapa: {access_counter}")


def verificar_status_jogo():
    global jogo_terminou
    global cobra_vencedora
    global status_jogo

    cobras_vivas = [cobra for cobra in status_jogo if cobra['status'] == 'viva']
    if len(cobras_vivas) == 1:
        cobra_vencedora = cobras_vivas[0]['id']
        print(f"A Cobra {cobra_vencedora} é a última sobrevivente e venceu o jogo! Status do jogo: {status_jogo}")
        jogo_terminou = True
        return
    elif any(cobra['pontos'] >= 3 for cobra in status_jogo):
        cobra_vencedora = next(cobra['id'] for cobra in status_jogo if cobra['pontos'] >= 3)
        print(f"A Cobra {cobra_vencedora} atingiu 3 pontos e venceu o jogo! Status do jogo: {status_jogo}")
        jogo_terminou = True
        return

def escrever_status_jogo(cobra_id, status="viva", pontos=0, retries=5, delay=0.1):
    global jogo_terminou
    global status_jogo
    global status_jogo_lock

    for _ in range(retries):
        
        if status_jogo_lock.acquire(timeout=0.1):
            try:
                if jogo_terminou:
                    return False
                status_jogo[cobra_id - 1]['status'] = status
                status_jogo[cobra_id - 1]['pontos'] += pontos
                verificar_status_jogo()
                return True
            finally:
                status_jogo_lock.release()
        else:
            time.sleep(delay)
    
    print(f"escrever_status_jogo: Thread {cobra_id} falhou ao adquirir o lock após {retries} tentativas.")
    return False

def escrever_mapa(thread_id, x, y, string, retries=5, delay=0.1):
    global jogo_terminou
    global mapa_jogo
    global mapa_lock
    
    for _ in range(retries):
        escrever_mapa_zona_critica()
        if mapa_lock.acquire(timeout=0.1):
            try:
                if jogo_terminou:
                    return False
                if mapa_jogo[x][y] in posicoes_validas or mapa_jogo[x][y] == str(thread_id):
                    mapa_jogo[x][y] = string
                    return True
            finally:
                mapa_lock.release()
                with counter_lock:
                    global access_counter
                    access_counter -= 1
        else:
            print("retry")
            time.sleep(delay)

    print(f"escrever_mapa: Thread {thread_id} falhou ao adquirir o lock após {retries} tentativas.")
    return False

def gerar_comida():
    global jogo_terminou
    global comida_posicoes
    # Gera duas posições de comida
    # O mapa é uma zona crítica já que é compartilhado entre as threads, portanto a geração de comida precisa verificar se a posição está vazia
    while not jogo_terminou:
            if jogo_terminou:
                break

            while len(comida_posicoes) < 2:
                if jogo_terminou:
                    break
                x, y = random.randint(0, tamanho_mapa-1), random.randint(0, tamanho_mapa-1)
                # Verifica se a posição gerada está vazia
                if escrever_mapa('thread_comida', x, y, 'F'):
                    # Adiciona a posição da comida
                    print(f"Gerando comida em {x}, {y}")
                    comida_posicoes.append([x, y])
                    

# Lógica de movimento da cobra
def mover_cobra(id_cobra):
    global jogo_terminou
    global status_jogo
    direcoes = ['up', 'down', 'left', 'right']

    # Inicializa a posição da cobra de forma aleatória em uma posição vazia, sendo posicao = [y, x]
    # o ponto de origem (0,0) está localizado no canto superior esquerdo da tela ou do mapa
    while True:
        posicao = [random.randint(0, tamanho_mapa-1), random.randint(0, tamanho_mapa-1)]
        if escrever_mapa(str(id_cobra), posicao[0], posicao[1], str(id_cobra)):
            break

    corpo_cobra = [posicao.copy()]

    while not jogo_terminou and status_jogo[id_cobra - 1]['status'] == 'viva':
        # Gera uma direção aleatória para a cobra se mover
        direcao = random.choice(direcoes)
        # Calcula a nova posição da cobra
        nova_posicao = posicao.copy()
        # Atualiza a nova posição com base na direção
        if direcao == 'up':
            nova_posicao[0] -= 1
        elif direcao == 'down':
            nova_posicao[0] += 1
        elif direcao == 'left':
            nova_posicao[1] -= 1
        elif direcao == 'right':
            nova_posicao[1] += 1
        
        # Garante que a cobra permaneça dentro dos limites do mapa
        nova_posicao[0] = max(0, min(nova_posicao[0], tamanho_mapa-1))
        nova_posicao[1] = max(0, min(nova_posicao[1], tamanho_mapa-1))
        # Atualiza o mapa e verifica o estado do jogo (zona crítica propensa a condições de corrida)
        if nova_posicao in corpo_cobra:
            print(f"Cobra {id_cobra} tentou se mover para seu próprio corpo, movimento ignorado.")

        # Verifica se tem comida na nova posição
        elif mapa_jogo[nova_posicao[0]][nova_posicao[1]] == 'F':

            if nova_posicao in comida_posicoes:
                # A cobra come a comida
                # Remove a comida da posição
                comida_posicoes.remove(nova_posicao)
                # Atualiza o placar
                escrever_status_jogo(id_cobra, 'viva', 1)
                # Aumenta o tamanho da cobra
                corpo_cobra.append(nova_posicao.copy())
                escrever_mapa(str(id_cobra), nova_posicao[0], nova_posicao[1], str(id_cobra))
                
        # Verifica se a nova posição está ocupada por outra cobra
        elif mapa_jogo[nova_posicao[0]][nova_posicao[1]] not in posicoes_validas:
            escrever_status_jogo(id_cobra, 'morta', 0)

            print(f"Cobra {id_cobra} colidiu com a cobra {mapa_jogo[nova_posicao[0]][nova_posicao[1]]} e morreu!")
            if mapa_lock.acquire(timeout=0.3):
                try:
                    for segment in corpo_cobra:
                        x, y = segment
                        mapa_jogo[x][y] = ' '
                finally:
                    mapa_lock.release()
            break

        # Atualiza o corpo da cobra
        else:
            # Atualiza o mapa com o corpo da cobra
            escrever_mapa(str(id_cobra), nova_posicao[0], nova_posicao[1], str(id_cobra))
            corpo_cobra.append(nova_posicao.copy())
            # Remove a cauda da cobra
            cauda = corpo_cobra.pop(0)
            escrever_mapa(str(id_cobra), cauda[0], cauda[1], ' ')
            # Atualiza a posição da cobra
        posicao = nova_posicao



def main():
    global jogo_terminou
    global cobra_vencedora
    jogo_terminou = False

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(mover_cobra, 1)
        executor.submit(mover_cobra, 2)
        executor.submit(mover_cobra, 3)
        executor.submit(mover_cobra, 4)
        executor.submit(gerar_comida)

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    print(f"Tempo de execução: {elapsed_time:.2f} segundos.")
    print("Cobra vencedora: ", cobra_vencedora)
    print("Vetor 'mapa' após execução das threads:")
    for linha in mapa_jogo:
        print(' '.join(linha))

if __name__ == "__main__":
    main()