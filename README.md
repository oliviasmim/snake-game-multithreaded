## **Projeto: Snake Game Multithreaded com Diferentes Mecanismos de Sincronização**

### **Objetivo do Projeto**

O objetivo deste projeto é explorar e comparar diferentes mecanismos de sincronização em um ambiente multithreaded, utilizando um jogo da cobra como base. Três métodos de sincronização foram implementados: Mutex, Semáforo e Exclusão Mútua. O projeto busca analisar como cada um desses mecanismos influencia o desempenho, a integridade dos dados e o comportamento geral do jogo.

### **Visão Geral do Projeto**

O projeto consiste em três implementações distintas do jogo da cobra, cada uma utilizando um método de sincronização diferente para gerenciar o acesso a recursos compartilhados (como o mapa do jogo e o placar). As threads representam cobras que se movem pelo mapa, comem comida e competem para sobreviver. A sincronização é essencial para evitar condições de corrida e garantir que o jogo funcione corretamente em um ambiente multithreaded.

As regras do jogo e uma descrição aprofundada delas você encontra no arquivo `BUSINESS_RULES.md`

### **Referências**

Este projeto foi inspirado pelos conceitos apresentados em aula, tendo como referência o livro "Sistemas Operacionais Modernos" de Andrew S. Tanenbaum, que aborda a importância da sincronização em sistemas operacionais e a necessidade de mecanismos eficazes para evitar condições de corrida em ambientes multithreaded.

## **Guia de Instalação**

### **Pré-requisitos**

- Python 3.x instalado na máquina.
- Ou um ambiente virtual Python.

### **Passos de Instalação**

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/oliviasmim/snake-game-multithreaded.git
   cd snake-game-multithreaded
   ```

   Não há dependências externas para este projeto além do Python padrão.

2. **Execute as implementações do jogo:**

   Para rodar cada implementação, execute um dos seguintes comandos:

   ```bash
   python3 snake-game-mutex.py
   python3 snake-game-semaforo.py
   python3 snake-game-exclusao-mutua.py
   ```

## **Como Executar o Relatório**

O script `gerar-relatorio.py` foi criado para executar cada implementação do jogo, coletar dados e gerar um relatório comparativo dos resultados.

### **Passos para Executar o Relatório**

1. **Execute o script de relatório:**

   ```bash
   python3 gerar-relatorio.py
   ```

2. **Saída Esperada do Relatório:**

   O script de relatório irá gerar um arquivo `snake_game_report_<data>.txt` dentro da pasta `reports/`. O conteúdo típico do relatório será algo como:

   ```
   Relatório para snake-game-mutex.py:
     - Número de vezes que mais de 1 thread estava na zona crítica: 18
     - Cobras vencedoras:
         Cobra 1: 6 vitória(s)
         Cobra 2: 3 vitória(s)
         Cobra 3: 5 vitória(s)
         Cobra 4: 6 vitória(s)
     - Mediana das condições de corrida prevenidas: 2
     - Tempo médio de execução: 0.27 segundos

   Relatório para snake-game-semaforo.py:
     - Número de vezes que mais de 1 thread estava na zona crítica: 17
     - Cobras vencedoras:
         Cobra 1: 6 vitória(s)
         Cobra 2: 2 vitória(s)
         Cobra 3: 3 vitória(s)
         Cobra 4: 9 vitória(s)
     - Mediana das condições de corrida prevenidas: 2
     - Tempo médio de execução: 0.12 segundos

   Relatório para snake-game-exclusao-mutua.py:
     - Número de vezes que mais de 1 thread estava na zona crítica: 18
     - Cobras vencedoras:
         Cobra 1: 8 vitória(s)
         Cobra 2: 5 vitória(s)
         Cobra 3: 5 vitória(s)
         Cobra 4: 2 vitória(s)
     - Mediana das condições de corrida prevenidas: 2
     - Tempo médio de execução: 0.33 segundos
   ```

## **Implementações**

### **1. Jogo da Cobra com Semáforo**

Nesta implementação, o semáforo é utilizado para controlar o acesso ao mapa do jogo, permitindo que até duas threads acessem a zona crítica simultaneamente. Isso reduz a chance de condições de corrida, permitindo uma execução mais rápida e eficiente do jogo.

A implementação do semáforo sem o uso de bibliotecas internas do Python, utilizando lógica de incremento e decremento com controle manual de acesso. Você pode encontrar o código da classe semaforo.py

**Sincronização com Semáforo:**

- O semáforo foi configurado para permitir que até duas threads acessem a zona crítica ao mesmo tempo. Isso evita condições de corrida, onde múltiplas cobras poderiam tentar escrever no mapa ao mesmo tempo, resultando em comportamento imprevisível.
- Cada thread (cobra) tenta adquirir o semáforo antes de acessar o mapa. Se o semáforo permitir, a cobra entra na zona crítica; caso contrário, a thread deve aguardar até que o semáforo seja liberado.

**Como Funciona:**

- O semáforo limita o número de threads que podem acessar o mapa ao mesmo tempo.
- A contagem de acessos é monitorada para garantir que o semáforo esteja funcionando corretamente.
- O semáforo oferece um bom equilíbrio entre desempenho e controle de concorrência.

**Como Executar:**

```bash
python3 snake-game-semaforo.py
```

### **2. Jogo da Cobra com Mutex**

Nesta implementação, o mutex é utilizado para garantir que apenas uma thread por vez possa acessar as zonas críticas do código. Isso assegura que as operações sejam realizadas de forma segura e sequencial, prevenindo qualquer tipo de conflito entre as threads.

**Sincronização com Mutex:**

- O mutex (mutual exclusion) é usado para garantir que apenas uma thread por vez possacessar a zona crítica, que neste caso é o mapa do jogo ou a atualização do status do jogoIsso previne condições de corrida, onde múltiplas cobras poderiam tentar escrever no mapa amesmo tempo, resultando em comportamento imprevisível.
- Três mutexes distintos são utilizados para controlar diferentes zonas críticas:
  - `mutex_zona_critica`: Controla o acesso ao contador que monitora quantas threads estão tentando acessar a zona crítica do mapa.
  - `mutex_escrever_status_jogo`: Controla a escrita no placar do jogo, assegurando que status de cada cobra seja atualizado de forma correta e consistente.
  - `mutex_escrever_mapa`: Controla as operações de leitura e escrita no mapa do jogo.

**Como Funciona:**

- O mutex controla rigorosamente o acesso às zonas críticas, como o mapa do jogo e o placar.
- Três mutexes são utilizados para diferentes partes críticas do código, garantindo que os dados sejam manipulados de forma segura.
- A contagem de acessos é usada para monitorar o comportamento do mutex.

**Como Executar:**

```bash
python3 snake-game-mutex.py
```

### **3. Jogo da Cobra com Exclusão Mútua**

A exclusão mútua é implementada utilizando locks (travas) para garantir que apenas uma thread por vez possa acessar as zonas críticas, como o mapa do jogo ou o placar do status das cobras. Isso previne condições de corrida, onde múltiplas cobras poderiam tentar acessar ou modificar os mesmos recursos ao mesmo tempo, resultando em comportamento imprevisível.

**Como Funciona:**

- Locks são utilizados para implementar a exclusão mútua, assegurando que apenas uma thread acesse as zonas críticas por vez.
- A exclusão mútua é aplicada tanto no mapa do jogo quanto no placar, garantindo operações seguras.
- A contagem de acessos é usada para garantir que o comportamento esperado esteja sendo respeitado.

**Locks Utilizados:**

- `mapa_lock`: Controla o acesso ao mapa do jogo, assegurando que apenas uma thread po
  ler ou escrever no mapa de cada vez.
- `status_jogo_lock`: Garante que apenas uma thread por vez possa atualizar o placar
  jogo, mantendo a integridade das informações de status das cobras.
- `counter_lock`: Controla o acesso ao contador de threads tentando entrar na zona críti
  garantindo que esse contador seja atualizado corretamente.

**Características Principais:**

- **Exclusão Mútua com Locks:** Utilização de locks para implementar exclusão mútuaassegurando que apenas uma thread acesse as zonas críticas por vez.
- **Contador de Acessos:** O código monitora o número de threads tentando acessar a zoncrítica do mapa, garantindo que o comportamento esperado da exclusão mútua esteja em vigor.
- **Segurança e Consistência:** A implementação de exclusão mútua garante que todas aoperações críticas no jogo sejam realizadas de maneira segura e consistente, prevenindconflitos entre as threads.

**Como Executar:**

```bash
python3 snake-game-exclusao-mutua.py
```
