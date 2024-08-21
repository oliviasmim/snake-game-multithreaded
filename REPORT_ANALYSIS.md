### Análise dos dados do log snake_game_report_2024-08-20.txt:

#### **Visão Geral do Código**

1. **Implementação com Mutex (`snake-game-mutex.py`):**
   - **Mutex (Mutual Exclusion):** Garante que apenas uma thread acesse a seção crítica (o mapa do jogo) por vez. Isso é realizado através de chamadas aos métodos `acquire()` e `release()` no objeto Mutex, que bloqueia e libera o acesso, respectivamente.
   - **Objetivo:** Reduzir as condições de corrida permitindo que apenas uma thread acesse o recurso compartilhado em qualquer momento.

2. **Implementação com Semáforo (`snake-game-semaforo.py`):**
   - **Semáforo:** Permite que um número limitado de threads acesse a seção crítica simultaneamente. Neste caso, o Semáforo foi configurado para permitir até duas threads simultâneas.
   - **Objetivo:** Aumentar a eficiência permitindo algum nível de concorrência controlada, ao mesmo tempo em que previne condições de corrida.

3. **Implementação com Exclusão Mútua (`snake-game-exclusao-mutua.py`):**
   - **Exclusão Mútua:** Semelhante ao Mutex, mas implementado de maneira mais rígida para garantir que apenas uma thread possa acessar a seção crítica por vez, potencialmente usando técnicas personalizadas para reforçar o acesso exclusivo.
   - **Objetivo:** Prevenir as condições de corrida de maneira mais agressiva, limitando ainda mais a concorrência entre threads.

---

#### **Relatório dos Resultados**

Os resultados foram obtidos após executar cada implementação 100 vezes, e são apresentados abaixo:

1. **Frequência de Acesso à Zona Crítica**
   - **Mutex:** 27.127 vezes
   - **Semáforo:** 27.950 vezes
   - **Exclusão Mútua:** 10.689 vezes

   **Análise:**
   - **Mutex:** A alta frequência de acesso à zona crítica sugere que, embora o Mutex controle o acesso, ainda há muita contenção entre as threads.
   - **Semáforo:** A frequência ainda maior no Semáforo pode ser atribuída à permissão de múltiplas threads na seção crítica, aumentando a contenção e a probabilidade de tentativas simultâneas de acesso.
   - **Exclusão Mútua:** A menor frequência indica um controle mais rígido sobre o acesso, resultando em menos tentativas simultâneas de entrada na seção crítica.

2. **Análise das Cobras Vencedoras**
   - **Mutex:** Cobra 1 (31 vitórias), Cobra 2 (14 vitórias), Cobra 3 (28 vitórias), Cobra 4 (27 vitórias)
   - **Semáforo:** Cobra 1 (41 vitórias), Cobra 2 (16 vitórias), Cobra 3 (27 vitórias), Cobra 4 (16 vitórias)
   - **Exclusão Mútua:** Cobra 1 (35 vitórias), Cobra 2 (19 vitórias), Cobra 3 (24 vitórias), Cobra 4 (22 vitórias)

   **Análise:**
   - **Mutex:** A distribuição mais equilibrada das vitórias sugere que o Mutex oferece uma competição mais justa entre as threads.
   - **Semáforo:** A predominância da Cobra 1 pode indicar que o Semáforo, ao permitir mais concorrência, introduz uma leve inclinação na alocação de recursos.
   - **Exclusão Mútua:** Embora a Cobra 1 também tenha a maioria das vitórias, a distribuição é menos desequilibrada em comparação com o Semáforo, indicando um controle mais consistente.

3. **Mediana das Condições de Corrida Prevenidas**
   - **Mutex:** 234,5
   - **Semáforo:** 247,0
   - **Exclusão Mútua:** 40,0

   **Análise:**
   - **Mutex:**  eficaz em prevenir condições de corrida, mas ainda há uma quantidade considerável de contenção.
   - **Semáforo:** previne condições de corrida com mais frequência, mas isso também reflete a maior contenção entre threads.
   - **Exclusão Mútua:** essa mediana significativamente menor indica que a Exclusão Mútua é extremamente eficaz em prevenir condições de corrida, restringindo o acesso concorrente.

4. **Tempo Médio de Execução**
   - **Mutex:** 0,10 segundos
   - **Semáforo:** 0,14 segundos
   - **Exclusão Mútua:** 0,13 segundos

   **Análise:**
   - **Mutex:** O tempo médio de execução mais rápido sugere que o Mutex é eficiente em gerenciar a sincronização das threads, sem muita sobrecarga.
   - **Semáforo:** O tempo ligeiramente maior pode ser devido ao gerenciamento de múltiplas threads dentro da seção crítica, o que aumenta a complexidade.
   - **Exclusão Mútua:** O tempo moderado reflete um equilíbrio entre o controle rigoroso da concorrência e a necessidade de garantir a exclusividade no acesso à seção crítica.

---

#### **Conclusão**

- O Mutex oferece um bom equilíbrio entre desempenho e "justiça" entre as threads.
- O Semáforo, enquanto eficiente na prevenção de condições de corrida, pode introduzir alguma desigualdade na execução das threads.
- A Exclusão Mútua é a mais eficaz na prevenção de condições de corrida, mas com um custo ligeiramente maior em termos de tempo de execução.
