import re
from collections import Counter

# Sample log output
saida = """
Quantidade de threads tentando escrever na zona crítica do mapa: 1
Quantidade de threads tentando escrever na zona crítica do mapa: 3
Quantidade de threads tentando escrever na zona crítica do mapa: 2
Quantidade de threads tentando escrever na zona crítica do mapa: 3
Quantidade de threads tentando escrever na zona crítica do mapa: 5
Quantidade de threads tentando escrever na zona crítica do mapa: 5
Quantidade de threads tentando escrever na zona crítica do mapa: 5
Quantidade de threads tentando escrever na zona crítica do mapa: 4
Cobra 4 tentou se mover para seu próprio corpo, movimento ignorado.
Quantidade de threads tentando escrever na zona crítica do mapa: 5
Quantidade de threads tentando escrever na zona crítica do mapa: 5
Cobra 4 colidiu com a cobra 2 e morreu!
Quantidade de threads tentando escrever na zona crítica do mapa: 5
Gerando comida em 0, 2
Quantidade de threads tentando escrever na zona crítica do mapa: 3
"""

# Define the regular expression pattern
padrao_threads = re.compile(r'Quantidade de threads tentando escrever na zona crítica do mapa: (\d+)')

# Extract all matches
matches = padrao_threads.findall(saida)

# Convert matches to integers
threads_na_zona_critica = [int(match) for match in matches]

# Count the occurrences of each unique number of threads
threads_count = Counter(threads_na_zona_critica)

# Print the results
print("Threads na zona crítica:", threads_na_zona_critica)
print("Contagem de threads:", threads_count)