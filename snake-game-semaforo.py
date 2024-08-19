import threading
import random
import time

# Define o mapa compartilhado
tamanho_mapa = 15
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
semaphore = threading.Semaphore(1)

def gerar_comida():
    global jogo_terminou
    global comida_posicoes
    # Gera duas posições de comida
    # O mapa é uma zona crítica já que é compartilhado entre as threads, portanto a geração de comida precisa verificar se a posição está vazia
    while not jogo_terminou:
        with semaphore:
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
        time.sleep(0.01)

# Lógica de movimento da cobra
def mover_cobra(id_cobra):
    global jogo_terminou
    global status_jogo
    direcoes = ['up', 'down', 'left', 'right']

    # Inicializa a posição da cobra de forma aleatória em uma posição vazia, sendo posicao = [y, x]
    # o ponto de origem (0,0) está localizado no canto superior esquerdo da tela ou do mapa
    with semaphore:
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
        with semaphore:        
            
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
                    status_jogo[id_cobra - 1]['pontos'] += 1
                    # Remove a comida da posição
                    comida_posicoes.remove(nova_posicao)
                    # Aumenta o tamanho da cobra
                    corpo_cobra.append(nova_posicao.copy())
                    mapa_jogo[nova_posicao[0]][nova_posicao[1]] = str(id_cobra)
                    # Verifica o placar
                    # if status_jogo[id_cobra - 1]['pontos'] >= 3:
                    #     print(f"Cobra {id_cobra} ganhou o jogo!")
                    #     jogo_terminou = True

            # Verifica se a nova posição está ocupada por outra cobra
            elif mapa_jogo[nova_posicao[0]][nova_posicao[1]] not in posicoes_validas:
                status_jogo[id_cobra - 1]['status'] = 'morta'
                print(f"Cobra {id_cobra} colidiu com a cobra {mapa_jogo[nova_posicao[0]][nova_posicao[1]]} e morreu!")
                for segment in corpo_cobra:
                    mapa_jogo[segment[0]][segment[1]] = ' '
                return
            
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

        time.sleep(0.01)

def verificar_status_jogo():
    global jogo_terminou
    global cobra_vencedora
    global status_jogo

    while not jogo_terminou:
        with semaphore:
            cobras_vivas = [cobra for cobra in status_jogo if cobra['status'] == 'viva']
            if len(cobras_vivas) == 1:
                cobra_vencedora = cobras_vivas[0]['id']
                print(f"A Cobra {cobra_vencedora} é a última sobrevivente e venceu o jogo!")
                jogo_terminou = True
                return
            elif any(cobra['pontos'] >= 3 for cobra in status_jogo):
                cobra_vencedora = next(cobra['id'] for cobra in status_jogo if cobra['pontos'] >= 3)
                print(f"A Cobra {cobra_vencedora} atingiu 3 pontos e venceu o jogo!")
                jogo_terminou = True
                return
        time.sleep(0.01)

# Cria e inicia as threads
cobra1 = threading.Thread(target=mover_cobra, args=(1,))
cobra2 = threading.Thread(target=mover_cobra, args=(2,))
cobra3 = threading.Thread(target=mover_cobra, args=(3,))
cobra4 = threading.Thread(target=mover_cobra, args=(4,))

# Inicializa a comida como uma thread separada
thread_comida = threading.Thread(target=gerar_comida)
thread_comida.start()

thread_status = threading.Thread(target=verificar_status_jogo)
thread_status.start()

cobra1.start()
cobra2.start()
cobra3.start()
cobra4.start()

cobra1.join()
cobra2.join()
cobra3.join()
cobra4.join()

# Finaliza a thread de comida
jogo_terminou = True
thread_comida.join()
thread_status.join()

# Imprime o estado final do mapa
for linha in mapa_jogo:
    print(' '.join(linha))