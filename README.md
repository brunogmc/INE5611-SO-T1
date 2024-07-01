
# Jogo: Antiaéreas contra os aliens

## Descrição

O objetivo deste trabalho é aplicar os conceitos de threads, exclusão mútua e coordenação de processos por meio do projeto e implementação de um jogo

"Antiaéreas contra os aliens" é um jogo desenvolvido em Python usando a biblioteca Pygame. O objetivo do jogo é defender a Terra de naves alienígenas usando uma bateria antiaérea. O jogador pode escolher entre três níveis de dificuldade: Fácil, Médio e Difícil. 

O jogador deve mirar e atirar nas naves enquanto gerencia a munição limitada. Se o número de naves destruídas for maior que o número de naves que alcançarem o solo, o jogador vence.

## Requisitos

Para rodar o jogo, você precisará do Python 3.x e das seguintes bibliotecas:

- [Pygame](https://www.pygame.org/)
- [Threading](https://docs.python.org/3/library/threading.html)
- [Time](https://docs.python.org/3/library/time.html)
- [Math](https://docs.python.org/3/library/math.html)
- [Random](https://docs.python.org/3/library/random.html)

## Instalação

1. **Clone o repositório ou baixe os arquivos**

   ```bash
   git clone https://github.com/brunogmc/INE5611-SO-T1.git
   cd INE5611-SO-T1
   ```

2. **Instale as dependências**

   Certifique-se de ter o Python 3.x instalado. Você pode instalar o Pygame usando `pip`:

   ```bash
   pip install pygame
   ```

## Como Jogar

1. **Execute o jogo**

   No terminal, navegue até a pasta do projeto e execute:

   ```bash
   python game.py
   ```

   Isso iniciará o jogo e abrirá a janela do Pygame.

2. **Escolha a dificuldade**

   Use as teclas `1`, `2`, ou `3` para selecionar o nível de dificuldade:
   - `1`: Fácil
   - `2`: Médio
   - `3`: Difícil

3. **Controles do jogo**

   - `a, q, w, e, r`: Ajustam a mira da bateria antiaérea.
   - `Espaço`: Atira uma bala, se houver balas disponíveis.
   - `s`: Recarrega a munição.

4. **Objetivo do jogo**

   - Destrua o maior número possível de naves alienígenas antes que elas alcancem o solo.
   - Se metade das naves for destruída, você ganha.
   - Se metade das naves alcançar o solo, você perde.

## Recursos

- **Movimento e tiro controlados pelo jogador**
- **Níveis de dificuldade ajustáveis**
- **Gerenciamento de munição com recarga automática**

## Contribuição

Se você quiser contribuir para o projeto, sinta-se à vontade para abrir uma pull request ou enviar sugestões na seção de Issues.

