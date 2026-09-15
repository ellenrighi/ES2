# Engenharia de Software II — Xadrez

Interface em Python com PPlay e Pygame. Requer Python 3.8 ou superior.

## Executar

Na pasta do projeto, crie um ambiente virtual:

```bash
python3 -m venv .venv
```

Ative no macOS/Linux:

```bash
source .venv/bin/activate
```

No Windows, use `python -m venv .venv` para criar e, no PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale a dependência e abra a interface:

```bash
python -m pip install -r requirements.txt
python main.py
```

O PPlay já está incluído no repositório.

## Telas e controles

- **Jogar** abre a seleção de modo.
- **Regras** abre um pop-up com um resumo e fundo semitransparente. Feche pelo **×** ou por **Esc**.
- **Multiplayer** e **Vs IA** estão desativados.
- A **seta no canto superior esquerdo** ou **Esc** retorna da seleção para a tela inicial.
- Use o mouse ou **Tab / Shift+Tab** e **Enter / Espaço** para navegar pelos botões ativos.
- Feche a janela para sair. A interface se adapta ao tamanho da janela mantendo as proporções.

Esta etapa contém duas telas e um pop-up de regras. A tela inicial tem um pequeno tabuleiro com um rei decorativo. Não há motor de xadrez, partidas, rede ou inteligência artificial.

## Organização dos arquivos

```text
main.py                 # Ponto de entrada
interface/
  actions/              # Execução, eventos e navegação da interface
  components/           # Botões, tabuleiro com a peça e pop-up de regras
  drawing/              # Utilitários de fonte, texto e carregamento de ícones
  screens/
    home.py             # Desenho e botões da tela inicial
    modes.py            # Desenho e botões da seleção de modo
  theme.py              # Cores da interface
  paths.py              # Caminhos dos recursos
assets/
  icons/                # Rei e seta em PNG
  images/               # Outras imagens
  licenses/             # Licenças dos recursos
PPlay/                  # Biblioteca incluída no projeto
```

Cada arquivo de comportamento em `interface/` contém uma única função. Cada tela declara seus botões no próprio arquivo. A função `run` guarda a tela atual e o foco do teclado; `handle_event` retorna os novos valores quando o usuário interage. A biblioteca PPlay mantém sua organização original.

## Créditos

Resumo baseado nas [regras de xadrez da FIDE](https://handbook.fide.com/chapter/E012023).

Ícones [chess-king (filled)](https://github.com/tabler/tabler-icons/blob/main/icons/filled/chess-king.svg) e [arrow-left](https://github.com/tabler/tabler-icons/blob/main/icons/outline/arrow-left.svg) de Tabler Icons, de Paweł Kuna, sob [licença MIT](assets/licenses/LICENSE-tabler.txt).
Os ícones foram adaptados às cores da interface e exportados em PNG para exibição com Pygame.
