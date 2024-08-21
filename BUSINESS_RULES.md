### **Regras de Negócio do Código**

Este documento descreve as regras de negócio implementadas no código do jogo de cobras multi-threaded. As regras de negócio determinam como as cobras interagem com o mapa, como a comida é gerada, como as cobras ganham ou perdem, e como as zonas críticas são gerenciadas para evitar condições de corrida.

#### **1. Inicialização do Jogo**
- **Mapa do Jogo:**
  - O jogo ocorre em um mapa definido representado por uma matriz  na variável (`mapa_jogo`) onde cada célula pode conter uma cobra, representado pelo número da cobra ('1','2','3','4'), comida ('F'), ou estar vazia (' ').
  - O mapa é uma zona crítica compartilhada entre as threads, o que significa que o acesso a ele precisa ser controlado para evitar condições de corrida.

- **Estado do Jogo:**
  - O estado do jogo é controlado pela variável `jogo_terminou`, que indica se o jogo chegou ao fim.
  - O jogo termina quando apenas uma cobra permanece viva ou quando uma cobra atinge 3 pontos.

- **Status das Cobras:**
  - O status de cada cobra (viva ou morta) e sua pontuação são armazenados na lista `status_jogo`, onde cada item representa uma cobra com seu ID, status, e pontuação.

#### **2. Gerenciamento do Acesso Crítico**

- **Contagem de Acessos:**
  - A variável `access_counter` é utilizada para contar quantas threads estão tentando acessar a zona crítica ao mesmo tempo.

#### **3. Regras de Movimento das Cobras**
- **Movimentação:**
  - Cada cobra se move de forma aleatória em uma das quatro direções: cima, baixo, esquerda, ou direita. O movimento é restrito pelos limites do mapa.
  - Se a nova posição da cobra já estiver ocupada por parte do corpo da própria cobra, o movimento é ignorado.

- **Colisão e Alimentação:**
  - Se a cobra se mover para uma posição contendo comida ('F'), ela ganha um ponto, a comida é removida do mapa, e a cobra cresce em tamanho.
  - Se a cobra colidir com outra cobra, ela morre, e seu corpo é removido do mapa.

#### **4. Geração de Comida**
- **Posicionamento Aleatório:**
  - A comida é gerada aleatoriamente no mapa em posições vazias. No máximo, duas comidas podem estar presentes no mapa ao mesmo tempo.
  - A geração de comida é uma operação crítica que também requer acesso exclusivo ao mapa, garantindo que as posições de comida sejam corretamente atualizadas e que as threads não entrem em conflito ao gerar comida.

#### **5. Verificação de Status e Término do Jogo**
- **Verificação de Vencedor:**
  - A cada movimento ou ação significativa, o status do jogo é verificado para determinar se o jogo deve terminar. Isso acontece em duas situações:
    1. Apenas uma cobra permanece viva.
    2. Qualquer cobra atinge 3 pontos.
  - Quando o jogo termina, a cobra vencedora é anunciada, e o estado do jogo é atualizado para impedir novas ações..

#### **6. Execução Principal**
- **Execução Paralela:**
  - O jogo é executado em paralelo utilizando um `ThreadPoolExecutor` com um máximo de 5 threads, onde cada thread controla uma cobra ou a geração de comida.
  - O tempo total de execução do jogo é calculado e exibido ao final de cada partida, junto com o status final do mapa e a cobra vencedora.
