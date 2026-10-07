# Documentacao do Jogo de Xadrez (V1)

## 1. Visao geral
Este documento define a base do jogo de xadrez a ser construido com a biblioteca **PPlay**.  
A V1 e **sem IA** e cobre: **tabuleiro, pecas, movimentos, turno e movimentos especiais**.

Base de referencia utilizada:
- `pplay.md` (loop, input e renderizacao com PPlay)
- `classes.md` (modelo de classes do dominio)
- `wiki.md` (requisitos funcionais e backlog por historias)

## 2. Objetivo da V1
Entregar uma partida local de xadrez entre dois lados humanos no mesmo computador, com:
- Tabuleiro 8x8
- Posicionamento inicial completo
- Movimentacao legal basica de todas as pecas
- Movimentos especiais: roque, en passant e promocao
- Captura
- Alternancia de turno

## 3. Escopo funcional (incluido)
### 3.1 Regras de movimentacao basica (RF01 / US-01..US-06)
- **Peao**: avanco de 1, avanco de 2 na primeira jogada, captura diagonal.
- **Torre**: movimento ortogonal sem saltar pecas.
- **Bispo**: movimento diagonal sem saltar pecas.
- **Cavalo**: movimento em L, pode saltar pecas.
- **Dama**: combinacao de torre + bispo.
- **Rei**: movimento de 1 casa em qualquer direcao.

### 3.2 Dinamica da partida
- O jogador seleciona uma peca por clique.
- O jogador clica na casa de destino para tentar o movimento.
- Movimento invalido e rejeitado.
- Movimento valido atualiza o tabuleiro e alterna o turno.

### 3.3 Movimentos especiais (RF02-RF04 / US-07..US-12)
- **Roque menor e maior**: permitido apenas se rei/torre ainda nao moveram, caminho livre e sem casas de passagem sob ataque.
- **En passant**: permitido somente no lance imediatamente seguinte ao avanco duplo do peao adversario.
- **Promocao**: ao chegar na ultima fileira, o peao deve ser promovido (Dama, Torre, Bispo ou Cavalo).

### 3.4 Interface minima (RF29 parcial)
- Destaque simples da peca selecionada.
- Exibicao textual do turno atual (Brancas/Pretas).

## 4. Fora do escopo inicial
- IA (RF11-RF15)
- Xeque/xeque-mate/afogamento (RF05-RF07)
- Persistencia, PGN/FEN e historico (RF21-RF28)
- Relogio, undo, resign, efeitos e temas avancados

## 5. Arquitetura proposta
Inspirada em `classes.md`, com simplificacao da V1:

1. **Dominio**
   - `Color`: WHITE, BLACK
   - `Move`: origem, destino, peca_movida, peca_capturada
   - `Piece` (abstrata) e subclasses (`Pawn`, `Knight`, `Bishop`, `Rook`, `Queen`, `King`)
   - `Board`: matriz 8x8 e operacoes de leitura/escrita/aplicacao de lance

2. **Aplicacao**
   - `Game`: estado da partida, turno atual e execucao de jogadas validas

3. **Apresentacao**
   - `ChessGUI`: renderizacao, clique do mouse e loop principal

> `RuleValidator` e `AIPlayer` ficam reservados para fases futuras.

## 6. Integracao com PPlay
Conforme `pplay.md` e modulos reais da pasta `PPlay`:
- `Window`: criacao da janela, loop e `update()`
- `Mouse`: leitura de clique e coordenadas virtuais (`get_position`, `button_down`)
- `Keyboard` (opcional para atalhos de debug/restart)
- `GameImage`/`Sprite`: desenhar tabuleiro e pecas
- `Window.draw_text`: mostrar turno e mensagens simples

Fluxo de frame:
1. Ler input (mouse)
2. Traduzir clique para casa do tabuleiro
3. Processar selecao/lance
4. Desenhar tabuleiro, pecas e HUD
5. Chamar `window.update()`

## 7. Estrutura de pastas recomendada
```text
xadrez-prototipo2/
  assets/
    board.png
    pieces/
      white_pawn.png
      ...
  src/
    domain/
      color.py
      move.py
      piece.py
      pieces/
        pawn.py
        rook.py
        knight.py
        bishop.py
        queen.py
        king.py
      board.py
      move_generator.py
    application/
      game.py
    presentation/
      chess_gui.py
  main.py
  chess.md
```

## 8. Backlog de implementacao da V1
1. Modelar entidades de dominio e tipos base.
2. Implementar tabuleiro e setup inicial das pecas.
3. Implementar geracao de movimentos basicos por peca.
4. Implementar roque menor/maior com validacoes de legalidade.
5. Implementar estado e execucao de en passant.
6. Implementar promocao de peao com escolha de peca.
7. Implementar validacao de destino (livre, captura, bloqueio por peca amiga).
8. Implementar controle de turno.
9. Implementar interface PPlay com clique para jogar.
10. Adicionar feedback visual minimo (selecao + turno).

## 9. Criterios de aceite da V1
- E possivel iniciar uma partida com todas as pecas na posicao correta.
- Apenas o jogador do turno consegue mover pecas.
- Movimentos ilegais sao bloqueados.
- Capturas validas removem a peca adversaria.
- Turno alterna corretamente a cada jogada valida.
- Roque e executado apenas quando todos os pre-requisitos sao satisfeitos.
- En passant so ocorre no timing correto e remove o peao capturado.
- Promocao ocorre obrigatoriamente ao atingir a ultima fileira.
- A interface permanece responsiva durante toda a partida.
