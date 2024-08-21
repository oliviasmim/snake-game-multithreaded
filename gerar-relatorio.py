import subprocess
import re
from datetime import datetime
from statistics import median

# Configuração
scripts = ['snake-game-mutex.py', 'snake-game-semaforo.py', 'snake-game-exclusao-mutua.py']
vezes_por_script = 50  # Número de vezes que cada script será executado

# REGEX para pegar os dados do log
padrao_threads = re.compile(r'Quantidade de threads tentando escrever na zona crítica do mapa: (\d+)')
padrao_vencedor = re.compile(r'Cobra vencedora:\s+(\d+)')
padrao_tempo = re.compile(r'Tempo de execução:\s+([\d\.]+)\s+segundos')

# Armazenando para os resultados
resultados = {script: {'mais_de_2_threads': 0, 'cobras_vencedoras': {}, 'tempos_execucao': [], 'race_conditions': []} for script in scripts}

# Executa cada script pela quantidade de vezes que for setado em vezes_por_script
for script in scripts:
    print(f"Executando {script} {vezes_por_script} vez(es)...")
    for _ in range(vezes_por_script):
        # Executa o script e pega a saída
        resultado = subprocess.run(['python3', script], capture_output=True, text=True, errors='ignore')
        saida = resultado.stdout
        
        # Conta momentos onde mais de 2 threads estavam na zona crítica
        threads_na_zona_critica = [int(match) for match in padrao_threads.findall(saida)]
        count_mais_de_2_threads = sum(1 for t in threads_na_zona_critica if t > 1)
        resultados[script]['mais_de_2_threads'] += count_mais_de_2_threads
        resultados[script]['race_conditions'].append(count_mais_de_2_threads)
        
        # Pega a cobra vencedora
        vencedor_encontrado = padrao_vencedor.search(saida)
        if vencedor_encontrado:
            cobra_vencedora = vencedor_encontrado.group(1)
            if cobra_vencedora in resultados[script]['cobras_vencedoras']:
                resultados[script]['cobras_vencedoras'][cobra_vencedora] += 1
            else:
                resultados[script]['cobras_vencedoras'][cobra_vencedora] = 1
        
        # Pega o tempo de execução
        tempo_encontrado = padrao_tempo.search(saida)
        if tempo_encontrado:
            tempo_execucao = float(tempo_encontrado.group(1))
            resultados[script]['tempos_execucao'].append(tempo_execucao)

# Gera relatório
relatorio = []
for script, dados in resultados.items():
    relatorio.append(f"Relatório para {script}:")
    relatorio.append(f"  - Número de vezes que mais de 1 thread estava na zona crítica: {dados['mais_de_2_threads']}")
    
    # Resumo das cobras vencedoras
    relatorio.append("  - Cobras vencedoras:")
    for cobra, contagem in dados['cobras_vencedoras'].items():
        relatorio.append(f"      Cobra {cobra}: {contagem} vitória(s)")
    
    # Calcula a mediana das condições de corrida prevenidas
    if dados['race_conditions']:
        mediana_race_conditions = median(dados['race_conditions'])
        relatorio.append(f"  - Mediana das condições de corrida prevenidas: {mediana_race_conditions}")
       
    # Resumo dos tempos de execução
    if dados['tempos_execucao']:
        # Média dos tempos de execução
        tempo_medio = sum(dados['tempos_execucao']) / len(dados['tempos_execucao'])
        relatorio.append(f"  - Tempo médio de execução: {tempo_medio:.2f} segundos")
    else:
        relatorio.append("  - Nenhum tempo de execução registrado")
    
    relatorio.append("")

# Print em console
conteudo_relatorio = "\n".join(relatorio)
print(conteudo_relatorio)

# Define o nome do arquivo do relatório com a data atual
data_atual = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
nome_arquivo = f"./reports/snake_game_report_{data_atual}.txt"

# Cria um arquivo de relatório
with open(nome_arquivo, "w") as arquivo_relatorio:
    arquivo_relatorio.write(conteudo_relatorio)
