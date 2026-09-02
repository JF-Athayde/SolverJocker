Sim — você quis dizer **`.md`**. Aqui está o conteúdo **cru do `README.md`**, dentro de um bloco para você copiar diretamente para o GitHub:

````md
# 🌎 Insight Urbano

> **Transformando acontecimentos cotidianos em conhecimento sobre a vida em sociedade.**

O **Insight Urbano** é uma aplicação web desenvolvida pela equipe **Ciência é Top** para a **42ª Mostra Cultural Professor Antônio Gondim — Colégio 7 de Setembro (2026)**.

A plataforma permite registrar situações reais observadas no cotidiano e transformá-las em **boletins de análise urbana e social**, utilizando Inteligência Artificial para relacionar os acontecimentos aos chamados **Pilares Setembrinos**.

---

## 🎯 Objetivo

O projeto busca transformar situações comuns da vida urbana em oportunidades de reflexão.

A partir de um acontecimento real, o usuário pode registrar:

- 📍 Cidade
- 🏙️ Local da situação
- 📝 Situação observada
- ⚠️ Problema social ou urbano
- 📊 Consequências
- 🔎 Observações adicionais
- 🧭 Pilares envolvidos

Essas informações são processadas pelo sistema e utilizadas para gerar um **boletim de análise em HTML**.

---

## 🧠 Pilares Setembrinos

A análise utiliza seis princípios como lentes para interpretar cada situação:

| # | Pilar | Ideia principal |
|---|---|---|
| 01 | **Respeito** | Convivência, empatia, diálogo e consideração pelo próximo |
| 02 | **Cidadania** | Participação social, colaboração e construção coletiva |
| 03 | **Responsabilidade** | Consciência sobre as consequências das nossas escolhas |
| 04 | **Zelo** | Cuidado com pessoas, espaços públicos e meio ambiente |
| 05 | **Senso de Justiça** | Equidade, direitos, inclusão e bem coletivo |
| 06 | **Sinceridade** | Honestidade, transparência, diálogo e confiança |

---

## 🤖 Inteligência Artificial

O projeto utiliza uma integração com **Gemini** para auxiliar na interpretação das situações fornecidas pelo usuário.

O fluxo básico da aplicação é:

```text
Situação real
     ↓
Dados fornecidos pelo usuário
     ↓
Seleção dos Pilares Setembrinos
     ↓
Construção do contexto da análise
     ↓
Inteligência Artificial
     ↓
Boletim de análise
     ↓
Arquivo HTML
```

A aplicação organiza os dados do formulário e monta um contexto antes de enviá-lo para o módulo responsável pela geração do boletim.

---

## 🖥️ Tecnologias utilizadas

### Backend

- Python
- Flask
- Integração com Gemini
- Geração dinâmica de arquivos HTML

### Frontend

- HTML5
- CSS3
- JavaScript

### Recursos adicionais

- `uuid` para geração de identificadores únicos
- Sistema de arquivos para armazenamento dos boletins
- Flask `send_file()` para retornar os relatórios ao navegador

---

## 📂 Estrutura do projeto

Uma estrutura aproximada do projeto:

```text
cityScience/
│
├── cityScience/
│   ├── __init__.py
│   │
│   ├── green.py
│   │
│   ├── routes/
│   │   └── ...
│   │
│   └── templates/
│       ├── map.html
│       ├── nerd.html
│       ├── create_bulletin_urban.html
│       │
│       └── examples/
│           └── insight_urbano_*.html
│
├── requirements.txt
├── README.md
└── ...
```

> A estrutura pode variar de acordo com a versão do projeto.

---

## 🚀 Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
```

Entre na pasta:

```bash
cd SEU-REPOSITORIO
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Linux/macOS:

```bash
source .venv/bin/activate
```

No Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração da API

Configure a chave da API do Gemini como variável de ambiente.

Linux/macOS:

```bash
export GEMINI_API_KEY="SUA_CHAVE"
```

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="SUA_CHAVE"
```

> ⚠️ Nunca publique sua chave de API no GitHub.

Recomenda-se utilizar variáveis de ambiente ou um arquivo `.env` durante o desenvolvimento.

---

## ▶️ Executando o projeto

Depois de instalar as dependências e configurar as variáveis:

```bash
python run.py
```

ou:

```bash
flask run
```

A aplicação ficará disponível localmente em:

```text
http://127.0.0.1:5000
```

A página do Insight Urbano:

```text
http://127.0.0.1:5000/create_bulletin_urban
```

---

## 🔄 Funcionamento

O principal fluxo da aplicação acontece na rota:

```text
/create_bulletin_urban
```

A rota aceita:

```text
GET
POST
```

### GET

No acesso normal, o Flask renderiza a página:

```python
return render_template(
    "create_bulletin_urban.html"
)
```

### POST

Ao enviar o formulário, o backend recebe os dados:

```python
city = request.form.get(
    "city",
    ""
).strip()

location = request.form.get(
    "location",
    ""
).strip()

situation = request.form.get(
    "situation",
    ""
).strip()

problem = request.form.get(
    "problem",
    ""
).strip()

consequences = request.form.get(
    "consequences",
    ""
).strip()

observations = request.form.get(
    "observations",
    ""
).strip()

pillars = request.form.getlist(
    "pillar"
)
```

Depois disso, os dados são validados e preparados para a análise.

---

## 📝 Geração do Insight

O sistema combina as informações fornecidas pelo usuário para formar o contexto da análise.

Exemplo:

```text
Cidade:
Fortaleza

Local:
Praça pública

Situação:
Acúmulo de lixo em uma praça.

Problema social ou urbano:
Descarte irregular de resíduos.

Consequências:
Prejuízo à limpeza, ao meio ambiente e às pessoas que utilizam o espaço.
```

Os dados são encaminhados para o módulo:

```python
gerar_boletim_html(...)
```

O módulo é responsável por gerar o boletim final.

---

## 📄 Boletins gerados

Cada análise recebe um nome único:

```text
insight_urbano_<uuid>.html
```

Exemplo:

```text
insight_urbano_8f91c8d8bde64b42b7a5d8e2f1a6c321.html
```

Os arquivos são armazenados em:

```text
cityScience/templates/examples/
```

Depois da criação, o arquivo pode ser enviado diretamente ao navegador:

```python
return send_file(
    output_path,
    mimetype="text/html"
)
```

---

## 🎨 Interface

A interface do Insight Urbano possui uma identidade visual inspirada na Mostra Cultural.

A página utiliza:

- Design responsivo
- Cards
- Formulários
- Seleção visual dos pilares
- Tela de carregamento
- Identidade institucional
- Layout adaptado para dispositivos móveis

### Interface

```text
┌──────────────────────────────────────────────┐
│                INSIGHT URBANO                │
├──────────────────────┬───────────────────────┤
│ Cidade               │ Local                 │
├──────────────────────┴───────────────────────┤
│ Situação observada                           │
├──────────────────────────────────────────────┤
│ Problema social ou urbano                    │
├──────────────────────────────────────────────┤
│ Consequências                                │
├──────────────────────────────────────────────┤
│             PILARES SETEMBRINOS              │
├──────────────────────────────────────────────┤
│              [ GERAR BOLETIM ]               │
└──────────────────────────────────────────────┘
```

---

## 🧪 Validações

O backend verifica se as informações essenciais foram preenchidas.

### Cidade

```python
if not city:
    flash(
        "Informe a cidade.",
        "error"
    )
```

### Situação

```python
if not situation:
    flash(
        "Descreva a situação observada.",
        "error"
    )
```

### Pilares

```python
if not pillars:
    flash(
        "Selecione pelo menos um Pilar Setembrino.",
        "error"
    )
```

---

## 🐛 Debug

Durante o desenvolvimento, o backend mostra no terminal informações sobre cada análise.

Exemplo:

```text
======================================
       NOVO INSIGHT URBANO
======================================
Cidade:       Fortaleza
Local:        Praça
Situação:     Acúmulo de lixo
Pilares:      ['Zelo', 'Cidadania']
Arquivo:      cityScience/templates/examples/insight_urbano_xxxxx.html
======================================
```

Depois da geração:

```text
✅ Arquivo pronto:
cityScience/templates/examples/insight_urbano_xxxxx.html
```

Esse sistema facilita a identificação de erros no envio do formulário e na criação dos boletins.

---

## 💡 Exemplos de análise

### 🗑️ Lixo em uma praça

Pilares possíveis:

```text
Zelo
Cidadania
Responsabilidade
```

### 🚗 Acidente de trânsito

Pilares possíveis:

```text
Responsabilidade
Respeito
Senso de Justiça
```

### 🗣️ Conflito entre pessoas

Pilares possíveis:

```text
Respeito
Sinceridade
Senso de Justiça
```

### ♿ Problemas de acessibilidade

Pilares possíveis:

```text
Senso de Justiça
Cidadania
Zelo
```

O objetivo é ir além da identificação do problema, analisando como comportamentos, decisões e relações sociais influenciam a vida coletiva.

---

## 🔬 Conceito

O Insight Urbano parte de uma ideia simples:

> **A cidade também é um espaço de aprendizagem.**

Situações cotidianas podem revelar problemas e comportamentos relacionados à:

- cidadania;
- responsabilidade;
- convivência;
- justiça;
- cuidado;
- confiança;
- participação social.

Assim, o projeto conecta:

```text
Tecnologia
     +
Inteligência Artificial
     +
Observação do cotidiano
     +
Educação
     +
Vida em sociedade
```

---

## 🏫 Mostra Cultural

Projeto desenvolvido para a:

**42ª Mostra Cultural Professor Antônio Gondim**

**Colégio 7 de Setembro — 2026**

### Equipe Ciência é Top

- Pedra Celso Varela Tote
- Cristiano Leão Mendes de Souza

---

## 📌 Status

🚧 **Projeto em desenvolvimento**

O projeto pode receber novas funcionalidades, melhorias na análise das situações e novas formas de visualização dos boletins.

---

## 📜 Licença

Este projeto foi desenvolvido para fins educacionais e de apresentação na Mostra Cultural.

Consulte os responsáveis pelo projeto antes de reutilizar partes do código em outros trabalhos.

---

## ⭐ Ciência é Top

**Insight Urbano**

> *Do conhecimento no campo das ideias para a prática cotidiana.*
````

