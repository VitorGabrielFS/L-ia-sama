# 🤠 Léia – Assistente Virtual com Personalidade

A **Léia** é uma assistente virtual sarcástica, irônica e com um toque de humor ácido.  
Ela interage por **voz**, aprende os hábitos do usuário com **machine learning** e aparece na tela como uma **bonequinha interativa** que pode ser movida com o mouse.  

---

## 🎯 Objetivo
Criar uma IA que:
- **Ouve** e transcreve a fala do usuário (ASR).  
- **Identifica quem está falando**, mesmo com variações na voz.  
- **Entende a intenção** do que foi dito (NLP).  
- **Responde com uma voz sintetizada** (TTS).  
- **Aprende os costumes do usuário** com **Reinforcement Learning**.  
- **Mostra um avatar interativo na tela**, que reage e pode ser movido pelo mouse.  

---

## 🧩 Estrutura do Projeto

leia_ai/
│
├── main/ # ponto de entrada do sistema
├── audio/ # captura e pré-processamento de áudio
├── asr/ # reconhecimento de fala (voz → texto)
├── speaker/ # identificação do locutor
├── nlu/ # interpretação de intenção (NLP)
├── tts/ # síntese de voz (texto → fala)
├── rl/ # aprendizado de hábitos (reinforcement learning)
├── actions/ # integração com o sistema (apps, mouse, web)
├── avatar/ # bonequinha na tela (sprites, animações)
├── data/ # datasets e logs
├── utils/ # ferramentas auxiliares
├── tests/ # testes unitários
└── requirements.txt # dependências

yaml
Copiar
Editar

---

## 👥 Divisão de Tarefas

### Amigo (Parte 1 – Áudio + Reconhecimento)
- **Captura e tratamento de áudio** (`audio/`)  
- **Reconhecimento de fala (ASR)** (`asr/`)  
- **Identificação de quem está falando** (`speaker/`)  

### Eu (Parte 2 – Interpretação + Resposta + Avatar)
- **Processamento de linguagem natural (NLU)**  
- **Síntese de fala (voz da Léia)**  
- **Aprendizado por reforço (hábitos do usuário)**  
- **Avatar interativo na tela**  
- **Integração com PC e web**  

---

## ⚙️ Fluxo de Funcionamento

1. Usuário fala → microfone capta.  
2. Áudio é processado e convertido em texto + identificação do locutor.  
3. Texto vai para o módulo de NLP + RL → Léia entende e decide resposta.  
4. Resposta é convertida em áudio pela voz da Léia.  
5. Avatar reage e interage com o usuário na tela.  

---

## 🚀 Tecnologias Previstas
- **Python** como linguagem principal.  
- **PyTorch / TensorFlow** para machine learning.  
- **Torchaudio / Librosa** para processamento de áudio.  
- **Custom ASR (ex: Wav2Vec2, DeepSpeech)** para voz → texto.  
- **TTS neural (Tacotron, VITS, etc.)** para fala da Léia.  
- **PyGame / PyQt / Tkinter** para o avatar interativo.  
- **Reinforcement Learning (Gym, RLlib)** para hábitos.  

---

## 📅 Status
🚧 **Em desenvolvimento** – primeiras versões ainda em construção.  

---

## 💡 Ideia
Mais do que um simples assistente, a **Léia** é quase um "pet virtual" que vive no seu PC, ajudando você, tirando sarro e se adaptando à sua rotina.

---