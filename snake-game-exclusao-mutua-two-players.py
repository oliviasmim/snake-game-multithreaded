import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

# Define o mapa compartilhado
tamanho_mapa = 10
mapa_jogo = [[' ' for _ in range(tamanho_mapa)] for _ in range(tamanho_mapa)]
jogo_terminou = False
comida_posicoes = []
posicoes_validas = [' ', 'F']
# Placar do jogo, variável compartilhada
placar = [0, 0]
lock = threading.Lock()

def gerar_comida():
    global jogo_terminou
    global comida_posicoes
    # Gera duas posições de comida
    # O mapa é uma zona crítica já que é compartilhado entre as threads, portanto a geração de comida precisa verificar se a posição está vazia
    while not jogo_terminou:
        with lock:
            if jogo_terminou:
                return
            while len(comida_posicoes) < 2:
                # Gera uma posição aleatória para x e y
                x, y = random.randint(0, tamanho_mapa-1), random.randint(0, tamanho_mapa-1)
                # Verifica se a posição gerada está vazia
                if mapa_jogo[x][y] == ' ':
                    # Adiciona a posição da comida
                    print(f"Gerando comida em {x}, {y}")
                    comida_posicoes.append([x, y])
                    # Atualiza o mapa com o símbolo da comida
                    mapa_jogo[x][y] = 'F'
        # time.sleep(0.1)

# Lógica de movimento da cobra
def mover_cobra(id_cobra):
    global jogo_terminou
    direcoes = ['up', 'down', 'left', 'right']

    # Inicializa a posição da cobra de forma aleatória em uma posição vazia, sendo posicao = [y, x]
    # o ponto de origem (0,0) está localizado no canto superior esquerdo da tela ou do mapa
    with lock:
        while True:
            posicao = [random.randint(0, tamanho_mapa-1), random.randint(0, tamanho_mapa-1)]
            if mapa_jogo[posicao[0]][posicao[1]] == ' ':
                mapa_jogo[posicao[0]][posicao[1]] = str(id_cobra)
                break

    corpo_cobra = [posicao.copy()]

    while not jogo_terminou:
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
        # with lock:
        print(f"Cobra {id_cobra} tentando adquirir o Lock...")
        if lock.locked():
            print(f"Lock adquirido por outra cobra")
        if lock.acquire(timeout=0.1):        
            try:
                print(f"Cobra {id_cobra} conseguiu adquirir o Lock.")
                if jogo_terminou:
                    return
                #print(f"Cobra {id_cobra} se moveu para {nova_posicao}, no mapa: {mapa_jogo[nova_posicao[0]][nova_posicao[1]]}")
                if nova_posicao in corpo_cobra:
                    print(f"Cobra {id_cobra} tentou se mover para seu próprio corpo, movimento ignorado.")
                    continue

                # Verifica se tem comida na nova posição
                if mapa_jogo[nova_posicao[0]][nova_posicao[1]] == 'F':
                    if nova_posicao in comida_posicoes:
                        # A cobra come a comida
                        placar[id_cobra-1] += 1
                        # Remove a comida da posição
                        comida_posicoes.remove(nova_posicao)
                        # Aumenta o tamanho da cobra
                        corpo_cobra.append(nova_posicao.copy())
                        mapa_jogo[nova_posicao[0]][nova_posicao[1]] = str(id_cobra)
                        # Verifica o placar
                        if placar[id_cobra-1] >= 3:
                            print(f"Cobra {id_cobra} ganhou o jogo!")
                            jogo_terminou = True

                # Verifica se a nova posição está ocupada por outra cobra
                elif mapa_jogo[nova_posicao[0]][nova_posicao[1]] not in posicoes_validas:
                    jogo_terminou = True
                    print(f"Cobra {id_cobra} colidiu com outra cobra!, Placar: {placar}. Jogo encerrado!")
                
                # Atualiza o corpo da cobra
                else:
                    # Atualiza o mapa com o corpo da cobra
                    mapa_jogo[nova_posicao[0]][nova_posicao[1]] = str(id_cobra)
                    corpo_cobra.append(nova_posicao.copy())
                    # Remove a cauda da cobra
                    cauda = corpo_cobra.pop(0)
                    mapa_jogo[cauda[0]][cauda[1]] = ' '
                    # Atualiza a posição da cobra
                posicao = nova_posicao
            finally:
                lock.release()
                print(f"Cobra {id_cobra} acaba de liberar o Lock.")
        else:
            print(f"Cobra {id_cobra} precisou aguardar para adquirir o Lock.")
        # time.sleep(0.1)

# # Cria e inicia as threads
# cobra1 = threading.Thread(target=mover_cobra, args=(1,))
# cobra2 = threading.Thread(target=mover_cobra, args=(2,))


# # Inicializa a comida como uma thread separada
# thread_comida = threading.Thread(target=gerar_comida)
# thread_comida.start()

# cobra1.start()
# cobra2.start()


# cobra1.join()
# cobra2.join()

# # Finaliza a thread de comida
# jogo_terminou = True
# thread_comida.join()

# # Imprime o estado final do mapa
# for linha in mapa_jogo:
#     print(' '.join(linha))

def main():
    global jogo_terminou
    jogo_terminou = False

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(mover_cobra, 1)
        executor.submit(mover_cobra, 2)
        executor.submit(gerar_comida)

    # Mostrar o vetor "mapa" após a execução das threads
    print("Vetor 'mapa' após execução das threads:")
    for linha in mapa_jogo:
        print(' '.join(linha))

if __name__ == "__main__":
    main()