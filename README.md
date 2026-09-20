# NutriRU 🥗

> **Hackathon SECOMP 2026** — Visão Computacional na Logística Universitária  
> Repositório oficial do projeto NutriRU.

---

## 👥 Equipe

- `[Marcos Vinicius]`
- `[Pedro Horta]`
- `[Icaro Ferreira]`
- `[Pedro Mizukawa]`

---

## 📌 Visão Geral e Contexto

No ambiente universitário, a alimentação no Restaurante Universitário (RU) é parte fundamental da rotina acadêmica. No entanto, os estudantes frequentemente enfrentam dificuldades para acompanhar a qualidade e a composição nutricional das suas refeições, como a ingestão diária de **macronutrientes** (proteínas, carboidratos, gorduras e calorias). 

Do ponto de vista da gestão universitária, há pouca visibilidade em tempo real sobre a **saúde alimentar dos estudantes** e os hábitos de consumo dentro do campus (ex.: quais itens são mais consumidos ou rejeitados).

O **NutriRU** surge como uma solução inteligente baseada em **Visão Computacional** para automatizar o reconhecimento de alimentos prato a prato no RU. A aplicação identifica visualmente os itens presentes na bandeja do estudante, estima a informação nutricional e fornece métricas tanto para o aluno quanto para a gestão de alimentação do campus.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Visão Computacional / Inteligência Artificial:** YOLO (You Only Look Once)
- **Interface / Dashboard:** Streamlit
- **Processamento de Imagens e Dados:** OpenCV, NumPy, Pandas

---

## ⚙️ Arquitetura e Pipeline de Visão Computacional

1. **Captura:** Imagem do prato/bandeja capturada via câmera no RU ou upload pelo usuário.
2. **Detecção e Classificação (YOLO):** O modelo YOLO processa o frame de entrada para localizar (bounding boxes) e classificar os diferentes componentes da refeição (ex.: arroz, feijão, proteína, salada).
3. **Mapeamento Nutricional:** A aplicação associa os objetos detectados às suas respectivas tabelas nutricionais médias por porção.
4. **Apresentação (Streamlit):** Exibição instantânea do total de calorias e macronutrientes do prato, acumulando histórico e estatísticas de consumo.

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python `3.10` ou superior instalado.
- Ambientes com suporte a OpenCV e bibliotecas do ecossistema YOLO (Ultralytics).

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/pedrobevilaqua04/Hackaton---Nucleo-Dev.git
   cd Hackaton---Nucleo-Dev
   ```

2. **Criar e ativar o ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv .venv
   
   # Linux/macOS:
   source .venv/bin/activate
   
   # Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instalar as dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Executar a aplicação Streamlit:**
   ```bash
   streamlit run app.py
   ```
   *Substitua `app.py` pelo nome do arquivo principal da interface, se necessário.*

---

## 📊 Limitações Atuais e Próximos Passos

### Limitações Atuais
- 💡 **Iluminação do RU:** Variações intensas de iluminação no ambiente físico podem afetar a acurácia do modelo de visão.
- 📏 **Estimativa de Volume em 2D:** A inferência a partir de imagens bidimensionais não representa a densidade e o peso real de cada porção com precisão absoluta.

### Próximos Passos / Trabalhos Futuros
- 📅 **Integração com Cardápio Diário:** Conectar a inferência da IA ao cardápio diário publicado pela universidade para restringir e otimizar o escopo de busca do modelo.
- 🧊 **Estimativa 3D de Porções:** Implementar redes de reconstrução/estimativa 3D ou sensores de profundidade para aferir o volume e peso real das porções com maior fidelidade.

> *O caminho é transformar o reconhecimento visual em recomendação nutricional confiável.*

---

## 📜 Licença e Créditos

Projeto desenvolvido durante o **Hackathon da SECOMP 2026 (UNIFEI)**. Recursos e modelos pré-treinados devidamente creditados às bibliotecas open-source utilizadas.
