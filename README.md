<div align="center">

<img src="https://i.imgur.com/eweiiNd.png" alt="Alerta Mosquito Logo" width="480"/>

# Alerta Mosquito 🦟

**Um jogo de tabuleiro educativo que ensina crianças a combater a dengue de forma lúdica e interativa.**

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6%2B-00B140?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Projeto%20Acadêmico-F5A623?style=for-the-badge)

</div>

---

## 📖 Sobre o Projeto

**Alerta Mosquito** é um jogo educativo desenvolvido em Python com Pygame como projeto acadêmico universitário. Ele combina um **jogo de tabuleiro** com **quatro minigames de ação** para ensinar crianças sobre a dengue, seus sintomas, formas de transmissão, tratamento e, principalmente, como prevenir a proliferação do mosquito *Aedes aegypti*.

A proposta é simples: aprender brincando. Em vez de cartilhas ou vídeos, o jogador vive as situações de prevenção na prática, tomando decisões e enfrentando desafios que reforçam o conhecimento de forma natural.

<div align="center">
<img src="https://i.imgur.com/OiGmg2a.png" alt="Tela inicial do jogo" width="720"/>
<p><sub>Tela inicial do Alerta Mosquito</sub></p>
</div>

---

## 🎓 Objetivos Educacionais

O jogo trabalha conteúdos reais sobre dengue por meio de 34 perguntas de múltipla escolha e mecânicas de minigames que simulam situações de combate ao mosquito. Os temas abordados incluem:

| Tema | O que o jogo ensina |
|---|---|
| 🦟 Transmissão | Quem transmite a dengue e como funciona o ciclo do mosquito |
| 🌊 Criadouros | Quais locais acumulam água parada e como eliminá-los |
| 🤒 Sintomas | Sinais da doença e quando buscar atendimento médico |
| 💊 Tratamento | O que fazer (e o que evitar) ao contrair dengue |
| 🛡️ Prevenção | Repelentes, roupas adequadas, descarte correto de lixo |
| 🔬 Ciclo biológico | Fases do mosquito: ovo, larva, pupa e adulto |

> A gamificação torna o aprendizado mais envolvente ao colocar o jogador como agente ativo na luta contra a dengue, em vez de receptor passivo de informações.

---

## 🎮 Conheça o Jogo

O jogo funciona como um **jogo de tabuleiro para 2 a 4 jogadores**. Cada participante escolhe um personagem, rola o dado e avança pelo mapa em formato de circuito. As casas do tabuleiro determinam o que acontece a cada rodada.

### Seleção de Personagens

Antes de começar, cada jogador escolhe um dos quatro personagens disponíveis clicando no retrato correspondente. O jogo suporta de 2 a 4 jogadores na mesma sessão.

<div align="center">
<img src="https://i.imgur.com/GwfIa3D.png" alt="Tela de seleção de personagens" width="720"/>
<img src="https://i.imgur.com/ENK7wog.png" alt="Tela de seleção de personagens" width="720"/>
<p><sub>Tela de seleção de personagens, cada jogador escolhe o seu antes de iniciar</sub></p>
</div>

### O Tabuleiro

O mapa é um circuito fechado em formato de grade. Os jogadores se movem em turnos, rolando o dado e avançando casa por casa. A câmera do tabuleiro pode ser explorada livremente entre as jogadas utilizando as setas do teclado.

<div align="center">

<table>
  <tr>
    <td align="center">
      <img src="https://i.imgur.com/y3lsl5j.png" alt="Visão geral do tabuleiro" width="360"/>
      <br/><sub>Visão geral do tabuleiro com os jogadores posicionados</sub>
    </td>
    <td align="center">
      <img src="https://i.imgur.com/SCF3cLM.png" alt="Dado e HUD dos jogadores" width="360"/>
      <br/><sub>HUD com dados coloridos por jogador e barra de medalhas</sub>
    </td>
  </tr>
</table>

</div>

### Tipos de Casas 🧩

Ao cair em uma casa, o jogador enfrenta um evento diferente:

| Casa | Efeito |
|---|---|
| 💰 **+R$5** | Ganha moedas |
| 🗑️ **−R$3** | Perde moedas |
| 🎲 **Dado extra** | Rola o dado novamente e avança mais casas |
| 🃏 **Carta** | Responde uma pergunta educativa sobre dengue |
| 🎮 **Minigame** | Entra em um dos quatro minigames de ação |
| 🏅 **Medalha** | Recebe uma medalha |
| 🌀 **Teleporte** | É teletransportado para uma casa aleatória do tabuleiro |

### Cartas de Perguntas

Ao cair em uma casa de carta, o jogador vê uma pergunta de múltipla escolha sobre dengue e prevenção. São 34 perguntas no banco de dados, sorteadas aleatoriamente a cada rodada, caso a resposta seja correta, o jogador ganha **+10 moedas**, perder não rende nada.

<div align="center">

<table>
  <tr>
    <td align="center">
      <img src="https://i.imgur.com/LtjBw5g.png" alt="Carta de pergunta sobre dengue" width="360"/>
      <br/><sub>Carta com pergunta educativa de múltipla escolha</sub>
    </td>
    <td align="center">
      <img src="https://i.imgur.com/58X0QxC.png" alt="Resposta da carta sendo exibida" width="360"/>
      <br/><sub>Feedback visual após o jogador escolher uma alternativa</sub>
    </td>
  </tr>
</table>

</div>

---

## 🕹️ Os Quatro Minigames

Quando um jogador cai em uma casa de minigame, um dos quatro minigames é sorteado aleatoriamente. Ganhar rende **+10 moedas**, perder não rende nada.

---

### 🔫 Acerte o Mosquito

**Acerte os mosquitos voando antes que o tempo acabe.**

Dez mosquitos voam em diferentes direções pela tela. O jogador deve clicar neles para abatê-los. Ao ser acertado, o mosquito cai. O jogo termina quando todos são eliminados (vitória) ou o timer de 8 segundos esgota (derrota).

<div align="center">
<img src="https://i.imgur.com/mOM3mz9.png" alt="Minigame Acerte o Mosquito" width="640"/>
<p><sub>Minigame Acerte o Mosquito - clique nos mosquitos antes que o tempo acabe</sub></p>
</div>

---

### 💧 Pingo D'Água

**Deslize pelo labirinto e tampe os baldes antes que transbordem.**

O jogador controla um personagem que se move pela tela usando as teclas direcionais. Quatro baldes estão enchendo progressivamente com água de estalactites. Encostar em um balde o fecha (tampa). Se algum transbordar, um mosquito pula na tela' e o jogador perde.

<div align="center">
<img src="https://i.imgur.com/sKnO56Q.png" alt="Minigame Pingo D'Água" width="640"/>
<p><sub>Minigame Pingo D'Água — navegue pela tela e tampe os baldes a tempo</sub></p>
</div>

---

### 🚀 Space Dengue

**Defenda-se de mosquitos alienígenas no espaço ao estilo Space Invaders.**

Uma horda de mosquitos avança em formação. O jogador controla um agente de saúde e atira para eliminá-los antes que atravessem a rua.

<div align="center">
<img src="https://i.imgur.com/XjNkGzD.png" alt="Minigame Space Dengue" width="640"/>
<p><sub>Minigame Space Dengue - elimine os mosquitos antes que atravessem a rua</sub></p>
</div>

---

### 🏃 Corrida Contra a Dengue

**Corra pela cidade e elimine criadouros de dengue no ritmo certo.**

Um personagem corre automaticamente por um cenário. Obstáculos (balde, lixo, pneu) aparecem exigindo a tecla direcional correta: ↑ para lixo, → para pneu, ↓ para balde. Pressionar errado causa stun temporário. O objetivo é eliminar 20 criadouros.

<div align="center">
<img src="https://i.imgur.com/9HzZzNx.png" alt="Minigame Corrida Contra a Dengue" width="640"/>
<p><sub>Minigame Corrida   Contra a Dengue - pressione a tecla correta para eliminar cada criadouro</sub></p>
</div>

---

## 🏆 Tela de Vitória

Após um jogador acumular cinco medalhas, a tela de vitória é exibida com confetes animados, o personagem vencedor no pódio e uma mensagem de parabéns. O jogo retorna automaticamente ao menu após 5 segundos.

---

## 🖥️ Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| **Python 3.10+** | Linguagem principal do projeto |
| **Pygame 2.6+** | Motor gráfico, eventos, sprites e renderização |
| **Pathlib** | Resolução multiplataforma de caminhos de assets |

---

## ⚙️ Pré-requisitos e Instalação

### Requisitos

- **Python 3.10** ou superior
- **pip** (gerenciador de pacotes do Python)

### Passo a passo

**1. Clone o repositório**

```bash
git clone https://github.com/DavidEricson00/AlertaMosquito.git
cd AlertaMosquito
```

**2. (Opcional) Crie e ative um ambiente virtual**

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Execute o jogo**

```bash
python main.py
```

---

## 🎯 Como Jogar

### Controles

| Tela | Ação | Controle |
|---|---|---|
| **Título** | Iniciar | `Espaço`, `Enter` ou clique |
| **Título** | Sair | `Esc` |
| **Seleção** | Escolher personagem | Clique no retrato |
| **Tabuleiro** | Rolar o dado / avançar | `Espaço` ou `Enter` |
| **Tabuleiro** | Mover câmera | `W A S D` ou Setas |
| **Tabuleiro** | Voltar ao dado | `Esc` ou clique |
| **Carta** | Escolher alternativa | Clique do mouse |
| **Minigame: Pistola** | Atirar | Clique do mouse |
| **Minigame: Pingo** | Mover personagem | Setas ou `W A S D` |
| **Minigame: Space** | Mover nave / atirar | Setas (mover), `Espaço` (atirar) |
| **Minigame: Corrida** | Eliminar obstáculo | ↑ lixo · ↓ balde · → pneu |

### Atalhos de desenvolvimento (Tela de Título)

| Tecla | Ação |
|---|---|
| `1` | Iniciar Pingo D'Água diretamente |
| `2` | Iniciar Corrida diretamente |
| `3` | Iniciar Space Dengue diretamente |
| `4` | Iniciar Pistola Mosquito diretamente |
| `M` | Iniciar minigame aleatório |

### Objetivo

Acumule **medalhas** passando pelas casas especiais nos cantos do tabuleiro. O primeiro jogador a coletar cinco medalhas vence e é celebrado na tela de vitória.

---

## 📁 Estrutura do Projeto

```
AlertaMosquito/
├── main.py                          # Ponto de entrada e máquina de estados principal
├── requirements.txt                 # Dependências (Pygame >= 2.6.0)
│
├── assets/                          # Recursos visuais e fontes
│   ├── fonts/                       # Press Start 2P e TT Milks
│   ├── characters/                  # Spritesheets, ícones e retratos dos personagens
│   ├── ui/                          # Dados, moedas, medalhas e barra de timer
│   ├── screens/                     # Backgrounds e elementos de cada tela
│   └── minigames/                   # Assets exclusivos de cada minigame
│       ├── pistol_mosquito/
│       ├── water_drop/
│       ├── space_dengue/
│       └── runner/
│
└── src/                             # Código-fonte modular
    ├── core/
    │   ├── config.py                # Dimensões da janela e cores dos jogadores
    │   ├── paths.py                 # Resolução de caminhos multiplataforma
    │   ├── player.py                # Modelos Jogador e Jogo (estado da sessão)
    │   └── utils.py                 # Funções auxiliares de escala, tint e colisão
    ├── screens/
    │   ├── title.py                 # Tela inicial com animação de logo
    │   ├── character_select.py      # Seleção de 2 a 4 personagens
    │   ├── board.py                 # Tabuleiro, dados, cartas, câmera e HUD
    │   ├── trivia.py                # Banco de 34 perguntas educativas
    │   └── victory.py              # Tela de vitória com confetes animados
    └── minigames/
        ├── pistol_mosquito/         # Clique nos mosquitos voadores
        ├── water_drop/              # Tampe baldes na caverna
        ├── space_dengue/            # Space Invaders com mosquitos alienígenas
        └── runner/                  # Corrida com obstáculos direcionais
```

