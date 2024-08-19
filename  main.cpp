#include <iostream>
#include <vector>
#include <thread> 
#include <chrono> 

using namespace std;

const int largura = 20;
const int altura = 20;

// Estrutura para representar uma coordenada
struct Coordenada {
    int x;
    int y;
};

// Classe para representar a Cobra
class Cobra {
public:
    Cobra(Coordenada inicio) : direcao('D') {
        corpo.push_back(inicio);
    }

    void mover() {
        // Implemente a lógica de movimento da cobra aqui
        Coordenada novaCabeca = corpo.front(); // Cabeça da cobra, o .front() pega o primeiro elemento do vetor

        switch (direcao) {
        	case 'C': novaCabeca.y--; break;
			case 'B': novaCabeca.y++; break;
			case 'D': novaCabeca.x++; break;
			case 'E': novaCabeca.x--; break;
     	}

		// Verifica se a cobra comeu a comida
		if (comeu) {
			corpo.insert(corpo.begin(), novaCabeca); 
			comeu = false;
		}
		

    }

    vector<Coordenada> corpo; // Vetor de coordenadas que representam o corpo da cobra
    char direcao; // 'C', 'B', 'D', 'E'
	bool comeu = false;
};

// Classe para representar a Comida
class Comida {
public:
    Comida() {
        gerarNovaPosicao();
    }

    void gerarNovaPosicao() {
        // Implemente a lógica de geração de posição aleatória aqui
    }

    Coordenada posicao;
};

// Classe principal do Jogo
class Jogo {
public:
    Jogo() : cobra({largura / 2, altura / 2}), comida() {}

    void iniciar() {
        while (jogoEmAndamento) {
            processarEntrada();
            atualizarJogo();
            renderizar();

            this_thread::sleep_for(chrono::milliseconds(100)); // Controla a velocidade do jogo
        }
    }

private:
    void processarEntrada() {
        // Implemente a lógica de leitura de teclado aqui
    }

    void atualizarJogo() {
        cobra.mover();

        // Implemente a lógica de colisão e atualização do jogo aqui
    }

    void renderizar() {
        system("cls"); // Limpa a tela do console (Windows)

        // Implemente a lógica de desenho do jogo aqui
    }

    bool jogoEmAndamento = true;
    Cobra cobra;
    Comida comida;
};

int main() {
    Jogo jogo;
    jogo.iniciar();

    return 0;
}