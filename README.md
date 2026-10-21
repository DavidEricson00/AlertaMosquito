# Alerta Mosquito 🦟

Jogo educativo desenvolvido em Python com Pygame focado no combate e prevenção à Dengue, combinando um jogo de tabuleiro com perguntas informativas e quatro minigames dinâmicos.

---

## 📋 Requisitos e Instalação

### Pré-requisitos
- Python 3.10 ou superior
- Pip gerenciador de pacotes

### Instalação das dependências
Instale os pacotes necessários através do arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Executar o Jogo

Na raiz do diretório `AlertaMosquito`, execute o ponto de entrada principal:

```bash
python main.py
```

### Controles Principais
- **Tela de Título:**
  - `Espaço` / `Enter` / `Clique`: Iniciar seleção de personagens.
  - `1`, `2`, `3`, `4`: Atalhos rápidos para testar minigames específicos (0: Pingo d'Água, 1: Corrida/Runner, 2: Space Dengue, 3: Pistola Mosquito).
  - `M`: Atalho para minigame aleatório.
  - `Esc`: Sair do jogo.
- **Seleção de Personagens:**
  - `Clique do Mouse`: Selecione de 2 a 4 jogadores e seus personagens, depois clique em "Iniciar".
- **Tabuleiro:**
  - `Espaço` / `Enter`: Rolar o dado e avançar casas.
  - `W, A, S, D` ou `Setas`: Mover a câmera livre pelo tabuleiro no modo de visualização.
  - `Esc` / `Clique`: Retornar da visualização da câmera para o dado.
  - `Clique do Mouse` na Carta: Escolher a alternativa na pergunta sobre a Dengue.

---

## 📁 Estrutura do Projeto

O projeto foi reorganizado em uma arquitetura modular com separação clara entre código (`src/`) e recursos (`assets/`):

```text
AlertaMosquito/
├── assets/                          # Todos os recursos visuais e fontes
│   ├── fonts/                       # Fontes tipográficas (Press Start 2P, TT Milks)
│   ├── characters/                  # Spritesheets de andamento, ícones e retratos
│   ├── ui/                          # Dados, números, moedas, medalhas e barra de tempo
│   ├── screens/                     # Recursos visuais por tela (title, character_select, board)
│   ├── minigames/                   # Recursos visuais exclusivos de cada minigame
│   │   ├── pistol_mosquito/         # Cenário, mira, mosquito e veia
│   │   ├── water_drop/              # Cenário de caverna, água, areia, baldes e estalactites
│   │   ├── space_dengue/            # Fundo espacial, mosquito alien, lasers e barreiras
│   │   └── runner/                  # Menino correndo, obstáculos (balde, lixo, pneu) e nuvens
│   └── raw/                         # Protótipos originais, artes conceituais e arquivos .aseprite
├── src/                             # Código-fonte modular
│   ├── core/                        # Núcleo do jogo, configurações, caminhos e utilitários
│   │   ├── paths.py                 # Resolução dinâmica e multiplataforma de caminhos
│   │   ├── config.py                # Dimensões da tela, cores e taxas de atualização
│   │   ├── player.py                # Modelos de Jogador e sessão de Jogo
│   │   └── utils.py                 # Funções auxiliares (escala, texto, colisões, interpolação)
│   ├── screens/                     # Telas e interfaces principais do jogo
│   │   ├── title.py                 # Tela inicial / de título
│   │   ├── character_select.py      # Tela de seleção de 2 a 4 personagens
│   │   ├── board.py                 # Sistema de tabuleiro, casas e movimentação
│   │   ├── trivia.py                # Banco de 34 perguntas educativas sobre a dengue
│   │   └── victory.py               # Tela de vitória com confetes e animações
│   ├── minigames/                   # Módulos dos quatro minigames
│   │   ├── pistol_mosquito/         # Minigame de acertar os mosquitos voando
│   │   ├── water_drop/              # Minigame da caverna tampando os baldes de água
│   │   ├── space_dengue/            # Minigame estilo space invaders eliminando mosquitos
│   │   └── runner/                  # Minigame de corrida pulando e desviando de criadouros
│   └── legacy/                      # Arquivos preservados para histórico (telaresultado.py)
├── main.py                          # Ponto de entrada e máquina de estados principal
├── requirements.txt                 # Dependências do projeto (Pygame)
├── .gitignore                       # Filtros de arquivos ignorados no controle de versão
└── README.md                        # Documentação do projeto
```

---

## 🎨 Localização de Recursos Compartilhados

- **Fontes do jogo:** Localizadas em `assets/fonts/`.
- **Personagens (Ícones, Sprites de andamento, Retratos):** Localizados em `assets/characters/`.
- **Elementos de Interface Compartilhados:** Localizados em `assets/ui/` (dados coloridos em `ui/dice/`, números em `ui/numbers/`, moedas e medalhas em `ui/hud/`).
- **Resolução de Caminhos no Código:** A função `get_asset_path()` em `src/core/paths.py` resolve dinamicamente os caminhos a partir da raiz do projeto, garantindo compatibilidade multiplataforma independente do diretório de execução.
