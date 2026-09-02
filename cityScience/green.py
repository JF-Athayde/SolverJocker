import os
import html

import google.generativeai as genai


# ============================================================
# CONFIGURAÇÃO
# ============================================================

OUTPUT_HTML = "boletim.html"

API_KEY_GEMINI = "AQ.Ab8RN6JKjy_n8claTOtsDfJt75QFXZ-p5YprLPyZATjzFNJfrg"

if not API_KEY_GEMINI:
    raise RuntimeError(
        "A variável de ambiente GEMINI_API_KEY não foi definida."
    )

genai.configure(api_key=API_KEY_GEMINI)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def limpar_resposta_gemini(texto):
    """
    Remove possíveis blocos Markdown que o Gemini
    eventualmente coloque ao redor do HTML.
    """

    texto = texto.strip()

    if texto.startswith("```html"):
        texto = texto[7:]

    elif texto.startswith("```"):
        texto = texto[3:]

    if texto.endswith("```"):
        texto = texto[:-3]

    return texto.strip()


def gerar_html_base(cidade, pergunta, observacoes, conteudo_ia):
    """
    Monta o HTML final.
    A IA fornece somente o conteúdo da análise.
    """

    cidade = html.escape(cidade)
    pergunta = html.escape(pergunta)
    observacoes = html.escape(observacoes)

    print('IA sendo executado...')

    return f"""<!DOCTYPE html>

<html lang="pt-BR">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        Insight Urbano | Ciência é Top
    </title>


    <style>

        /* ====================================================
           CONFIGURAÇÕES
        ==================================================== */

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}


        :root {{

            --azul: #092d68;
            --azul-claro: #1769a8;

            --dourado: #e5a91a;
            --dourado-claro: #f7cc58;

            --verde: #287b54;

            --fundo: #f4f6f9;
            --branco: #ffffff;

            --texto: #1c2733;
            --cinza: #64707d;

            --borda: #dfe5eb;

            --sombra:
                0 12px 35px
                rgba(9, 45, 104, 0.10);
        }}


        body {{

            font-family:
                Arial,
                Helvetica,
                sans-serif;

            background:
                linear-gradient(
                    180deg,
                    #f4f6f9,
                    #ffffff
                );

            color: var(--texto);

            line-height: 1.65;
        }}


        /* ====================================================
           TOPO
        ==================================================== */

        .top-line {{

            height: 6px;

            background:
                linear-gradient(
                    90deg,
                    var(--azul) 0%,
                    var(--azul) 72%,
                    var(--dourado) 72%,
                    var(--dourado) 100%
                );
        }}


        header {{

            background: white;

            border-bottom:
                3px solid #111;

            padding:
                15px 6%;
        }}


        .header-content {{

            max-width: 1150px;

            margin: auto;

            display: flex;

            justify-content: space-between;

            align-items: center;

            gap: 20px;
        }}


        .brand {{

            display: flex;

            align-items: center;

            gap: 13px;
        }}


        .logo {{

            width: 55px;
            height: 55px;

            background:
                linear-gradient(
                    135deg,
                    var(--azul),
                    var(--azul-claro)
                );

            border-radius: 12px;

            color: white;

            display: flex;

            align-items: center;

            justify-content: center;

            font-size: 17px;

            font-weight: 900;
        }}


        .brand-text strong {{

            display: block;

            color: var(--azul);

            font-size: 15px;
        }}


        .brand-text span {{

            display: block;

            color: var(--cinza);

            font-size: 11px;

            margin-top: 2px;
        }}


        .event-badge {{

            color: white;

            background:
                var(--azul);

            padding:
                11px 24px;

            border-radius:
                30px;

            font-size: 14px;

            font-weight: 900;

            letter-spacing: 0.5px;
        }}


        /* ====================================================
           HERO
        ==================================================== */

        .hero {{

            max-width: 1000px;

            margin:
                35px auto 20px;

            padding:
                0 20px;

            text-align: center;
        }}


        .edition {{

            font-size: 12px;

            color: var(--cinza);

            font-weight: bold;

            text-transform: uppercase;

            letter-spacing: 1.5px;

            margin-bottom: 10px;
        }}


        .hero h1 {{

            color: var(--azul);

            font-size:
                clamp(2rem, 5vw, 3.4rem);

            font-weight: 900;

            margin-bottom: 8px;
        }}


        .hero h1 span {{

            color: var(--dourado);
        }}


        .hero p {{

            max-width: 760px;

            margin: auto;

            color: var(--cinza);

            font-size: 15px;
        }}


        /* ====================================================
           TEMA
        ==================================================== */

        .theme {{

            max-width: 1000px;

            margin:
                25px auto 30px;

            padding:
                24px 30px;

            background:
                linear-gradient(
                    135deg,
                    var(--azul),
                    #124c91
                );

            color: white;

            border-radius: 20px;

            box-shadow: var(--sombra);

            text-align: center;
        }}


        .theme small {{

            display: block;

            font-size: 11px;

            font-weight: 900;

            letter-spacing: 2px;

            opacity: 0.8;

            margin-bottom: 7px;
        }}


        .theme h2 {{

            font-size:
                clamp(1.1rem, 3vw, 1.7rem);

            font-weight: 900;

            text-transform: uppercase;
        }}


        .theme p {{

            margin-top: 8px;

            font-size: 13px;

            opacity: 0.85;
        }}


        /* ====================================================
           CONTEÚDO
        ==================================================== */

        main {{

            max-width: 1000px;

            margin: auto;

            padding:
                0 20px 50px;
        }}


        .info-card {{

            background: white;

            border:
                1px solid var(--borda);

            border-radius: 18px;

            padding: 25px;

            margin-bottom: 20px;

            box-shadow:
                0 7px 25px
                rgba(0,0,0,0.05);
        }}


        .info-card h3 {{

            color: var(--azul);

            font-size: 20px;

            margin-bottom: 15px;
        }}


        .field-title {{

            color: var(--azul);

            font-weight: 900;

            font-size: 12px;

            text-transform: uppercase;

            letter-spacing: 0.8px;
        }}


        .field-value {{

            margin-top: 4px;

            margin-bottom: 15px;

            color: #444;
        }}


        /* ====================================================
           RELATÓRIO DA IA
        ==================================================== */

        .report {{

            background: white;

            border:
                1px solid var(--borda);

            border-radius: 20px;

            padding:
                30px;

            box-shadow: var(--sombra);
        }}


        .report-header {{

            border-bottom:
                3px solid var(--dourado);

            padding-bottom: 18px;

            margin-bottom: 25px;
        }}


        .report-header span {{

            color: var(--dourado);

            font-size: 11px;

            font-weight: 900;

            text-transform: uppercase;

            letter-spacing: 1.5px;
        }}


        .report-header h2 {{

            color: var(--azul);

            margin-top: 5px;

            font-size: 28px;
        }}


        .report-content h2 {{

            color: var(--azul);

            font-size: 21px;

            margin-top: 28px;

            margin-bottom: 10px;

            padding-bottom: 6px;

            border-bottom:
                2px solid #edf0f3;
        }}


        .report-content h3 {{

            color: var(--verde);

            font-size: 17px;

            margin-top: 20px;

            margin-bottom: 7px;
        }}


        .report-content p {{

            margin-bottom: 12px;

            color: #444;
        }}


        .report-content ul {{

            padding-left: 20px;

            margin-bottom: 16px;
        }}


        .report-content li {{

            margin-bottom: 7px;

            color: #444;
        }}


        .report-content strong {{

            color: var(--azul);
        }}


        .highlight {{

            background:
                #f7f9fc;

            border-left:
                5px solid var(--dourado);

            padding:
                15px 18px;

            border-radius:
                8px;

            margin:
                18px 0;
        }}


        .pillar-box {{

            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 12px;

            margin:
                18px 0 25px;
        }}


        .pillar {{

            background:
                #f8fafc;

            border:
                1px solid var(--borda);

            border-radius:
                12px;

            padding:
                15px;
        }}


        .pillar strong {{

            display: block;

            color: var(--azul);

            margin-bottom: 5px;
        }}


        .pillar span {{

            color: var(--cinza);

            font-size: 12px;

            line-height: 1.4;
        }}


        /* ====================================================
           EQUIPE
        ==================================================== */

        .team {{

            margin-top: 30px;

            background:
                var(--azul);

            color: white;

            border-radius: 20px;

            padding: 28px;

            text-align: center;
        }}


        .team h2 {{

            font-size: 23px;

            margin-bottom: 5px;
        }}


        .team p {{

            opacity: 0.8;

            font-size: 12px;

            margin-bottom: 18px;
        }}


        .members {{

            display: flex;

            justify-content: center;

            gap: 10px;

            flex-wrap: wrap;
        }}


        .member {{

            background:
                rgba(255,255,255,0.10);

            border:
                1px solid
                rgba(255,255,255,0.20);

            border-radius: 30px;

            padding:
                9px 16px;

            font-size: 12px;

            font-weight: bold;
        }}


        /* ====================================================
           RODAPÉ
        ==================================================== */

        footer {{

            background:
                #061d43;

            color: white;

            text-align: center;

            padding:
                25px 20px;

            border-top:
                4px solid var(--dourado);
        }}


        footer strong {{

            font-size: 15px;
        }}


        footer p {{

            margin-top: 5px;

            font-size: 11px;

            opacity: 0.65;
        }}


        /* ====================================================
           IMPRESSÃO / PDF
        ==================================================== */

        .print-button {{

            display: block;

            margin:
                0 auto 25px;

            padding:
                12px 22px;

            border: none;

            border-radius: 9px;

            background:
                var(--dourado);

            color:
                #111;

            font-weight: 900;

            cursor: pointer;
        }}


        @media print {{

            .print-button {{

                display: none;

            }}

            body {{

                background: white;

            }}

            .info-card,
            .report,
            .team {{

                box-shadow: none;

            }}

        }}


        /* ====================================================
           RESPONSIVIDADE
        ==================================================== */

        @media (max-width: 700px) {{

            .header-content {{

                flex-direction: column;

                text-align: center;
            }}


            .pillar-box {{

                grid-template-columns:
                    1fr;

            }}


            .report {{

                padding: 20px;

            }}

        }}

    </style>

</head>


<body>


    <div class="top-line"></div>


    <!-- ====================================================
         CABEÇALHO
    ==================================================== -->

    <header>

        <div class="header-content">


            <div class="brand">

                <div class="logo">
                    C7S
                </div>

                <div class="brand-text">

                    <strong>
                        COLÉGIO 7 DE SETEMBRO
                    </strong>

                    <span>
                        42ª Mostra Cultural Professor Antônio Gondim
                    </span>

                </div>

            </div>


            <div class="event-badge">
                MOSTRA CULTURAL — 2026
            </div>

        </div>

    </header>


    <!-- ====================================================
         TÍTULO
    ==================================================== -->

    <section class="hero">

        <div class="edition">
            Equipe Ciência é Top
        </div>

        <h1>
            <span>Insight</span> Urbano
        </h1>

        <p>
            Uma análise sobre problemas cotidianos,
            relações humanas e os princípios necessários
            para a construção de uma sociedade melhor.
        </p>

    </section>


    <!-- ====================================================
         TEMA DA MOSTRA
    ==================================================== -->

    <section class="theme">

        <small>
            TEMA GERADOR
        </small>

        <h2>
            Pilares Setembrinos:
            A Reinvenção da Vida em Sociedade
        </h2>

        <p>
            Mover o conhecimento do campo das ideias
            para a prática cotidiana.
        </p>

    </section>


    <main>


        <!-- =================================================
             CONTEXTO DA ANÁLISE
        ================================================== -->

        <section class="info-card">

            <h3>
                Contexto do Insight
            </h3>


            <div class="field-title">
                Local
            </div>

            <div class="field-value">
                {cidade}
            </div>


            <div class="field-title">
                Situação analisada
            </div>

            <div class="field-value">
                {pergunta}
            </div>


            <div class="field-title">
                Observações
            </div>

            <div class="field-value">
                {observacoes}
            </div>

        </section>


        <!-- =================================================
             RELATÓRIO
        ================================================== -->

        <section class="report">

            <div class="report-header">

                <span>
                    Análise social
                </span>

                <h2>
                    Insight Urbano
                </h2>

            </div>


            <div class="report-content">

                {conteudo_ia}

            </div>

        </section>


        <!-- =================================================
             EQUIPE
        ================================================== -->

        <section class="team">

            <h2>
                Ciência é Top
            </h2>

            <p>
                Projeto desenvolvido para a 42ª Mostra Cultural
                do Colégio 7 de Setembro.
            </p>


            <div class="members">

                <div class="member">
                    Pedra Celso Varela Tote
                </div>

                <div class="member">
                    Cristiano Leão Mendes de Souza
                </div>

            </div>

        </section>

    </main>


    <!-- ====================================================
         RODAPÉ
    ==================================================== -->

    <footer>

        <button
            class="print-button"
            onclick="window.print()"
        >
            Salvar como PDF
        </button>

        <strong>
            CIÊNCIA É TOP
        </strong>

        <p>
            42ª Mostra Cultural Professor Antônio Gondim
            • Colégio 7 de Setembro • 2026
        </p>

    </footer>

</body>

</html>
"""


# ============================================================
# GERAÇÃO DO BOLETIM
# ============================================================

def gerar_boletim_html(
    question: str,
    location: str,
    obs: str,
    pilares=None,
    output_filename: str = OUTPUT_HTML
):

    if pilares is None:
        pilares = []

    pilares_texto = ", ".join(pilares)

    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
Você é um especialista em relações humanas, cidadania,
ética, convivência social e análise de problemas urbanos.

Seu trabalho é produzir uma análise para a
42ª Mostra Cultural Professor Antônio Gondim,
do Colégio 7 de Setembro.

Tema gerador:

"Pilares Setembrinos:
A Reinvenção da Vida em Sociedade"

Equipe:
Ciência é Top

Situação apresentada:

Cidade/local:
{location}

Problema ou situação:
{question}

Observações:
{obs}

Pilares selecionados pelo estudante:
{pilares_texto}

Os seis Pilares Setembrinos são:

1. Respeito
Convivência, empatia, diálogo e consideração pelo próximo.

2. Cidadania
Participação social, colaboração e construção coletiva.

3. Responsabilidade
Consciência sobre as consequências das próprias escolhas.

4. Zelo
Cuidado com pessoas, espaços públicos e ambiente.

5. Senso de Justiça
Equidade, direitos, inclusão e busca pelo bem coletivo.

6. Sinceridade
Honestidade, transparência, diálogo e confiança.

OBJETIVO:

Transformar a situação apresentada em um
"Insight Urbano", mostrando que problemas cotidianos
podem ser analisados a partir dos valores necessários
para uma vida melhor em sociedade.

O texto será apresentado diretamente aos jurados.

Portanto:

- escreva em português;
- use linguagem clara;
- seja inteligente e reflexivo;
- evite linguagem excessivamente acadêmica;
- não invente estatísticas;
- não invente acontecimentos;
- utilize somente as informações fornecidas;
- conecte claramente o problema aos pilares;
- mostre consequências sociais;
- proponha ações práticas;
- destaque que a transformação começa no cotidiano;
- mantenha foco na sociedade, nas relações humanas
  e na convivência.

ESTRUTURA OBRIGATÓRIA:

1. "O que está acontecendo?"
Explique claramente a situação apresentada.

2. "Por que isso importa?"
Mostre por que esse problema afeta a vida em sociedade.

3. "Relação com os Pilares Setembrinos"
Crie cartões HTML para os pilares envolvidos.
O designe dos cartões deve estar em grid não ocupuando uma linha todo cada, 2 por linha ou mais

Formato:

<div class="pillar-box">

    <div class="pillar">
        <strong>Nome do Pilar</strong>
        <span>
            Explique de forma objetiva como o pilar
            está relacionado ao problema.
        </span>
    </div>

</div>

Use somente os pilares realmente relacionados.

4. "Impactos na sociedade"
Explique os principais impactos sociais.

5. "Do problema à ação"
Apresente de 3 a 5 ações práticas que poderiam
contribuir para melhorar a situação.

6. "Reflexão final"
Finalize com uma reflexão forte e apropriada
para apresentação aos jurados.

Inclua pelo menos uma caixa de destaque usando:

<div class="highlight">
    ...
</div>

IMPORTANTE:

Retorne SOMENTE um fragmento HTML.

NÃO retorne:

- <!DOCTYPE html>
- <html>
- <head>
- <body>
- CSS
- JavaScript
- Markdown
- ```html

O HTML será inserido automaticamente
dentro de uma página já pronta.

Use somente:

<h2>
<h3>
<p>
<ul>
<li>
<strong>
<em>
<div class="highlight">
<div class="pillar-box">
<div class="pillar">
<span>

Não use scripts.
Não use imagens externas.
Não use gráficos.
Não use fontes externas.
"""


    # ========================================================
    # UMA ÚNICA CHAMADA À API DO GEMINI
    # ========================================================

    model = genai.GenerativeModel("gemini-3.5-flash-lite")

    response = model.generate_content(prompt)

    conteudo_ia = limpar_resposta_gemini(
        response.text
    )


    # ========================================================
    # MONTA O HTML
    # ========================================================

    html_final = gerar_html_base(
        cidade=location,
        pergunta=question,
        observacoes=obs,
        conteudo_ia=conteudo_ia
    )


    # ========================================================
    # SALVA
    # ========================================================

    with open(
        output_filename,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(html_final)


    caminho = os.path.abspath(
        output_filename
    )

    print(
        f"✅ Boletim gerado com sucesso:"
        f"\n{caminho}"
    )


# ============================================================
# EXEMPLO
# ============================================================

if __name__ == "__main__":

    gerar_boletim_html(

        question=(
            "Foi observado o descarte de lixo "
            "em uma praça utilizada pela comunidade."
        ),

        location="Fortaleza - CE",

        obs=(
            "A praça é utilizada por moradores, "
            "crianças e comerciantes. O descarte "
            "inadequado prejudica o uso do espaço."
        ),

        pilares=[
            "Zelo",
            "Responsabilidade",
            "Cidadania"
        ],

        output_filename="boletim.html"
    )