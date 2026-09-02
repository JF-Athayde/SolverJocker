from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

from cityScience import app
from cityScience.green import gerar_boletim_html

import os
import uuid


# ============================================================
# CONFIGURAÇÕES
# ============================================================

EXAMPLES_PATH = os.path.join(
    app.root_path,
    "templates",
    "examples"
)

os.makedirs(
    EXAMPLES_PATH,
    exist_ok=True
)


# ============================================================
# MAPA
# ============================================================

@app.route("/map")
def map_page():

    return render_template("map.html")


# ============================================================
# NERD
# ============================================================

@app.route("/nerd")
def nerd():

    return render_template("nerd.html")


# ============================================================
# INSIGHT URBANO
# ============================================================

@app.route(
    "/create_bulletin_urban",
    methods=["GET", "POST"]
)
def create_bulletin_urban():

    # ========================================================
    # GET
    # ========================================================

    if request.method == "GET":

        return render_template(
            "create_bulletin_urban.html"
        )


    # ========================================================
    # DADOS DO FORMULÁRIO
    # ========================================================

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


    # ========================================================
    # PILARES
    # ========================================================

    pillars = request.form.getlist(
        "pillar"
    )


    # ========================================================
    # VALIDAÇÕES
    # ========================================================

    if not city:

        flash(
            "Informe a cidade.",
            "error"
        )

        return redirect(
            url_for("create_bulletin_urban")
        )


    if not situation:

        flash(
            "Descreva a situação observada.",
            "error"
        )

        return redirect(
            url_for("create_bulletin_urban")
        )


    if not pillars:

        flash(
            "Selecione pelo menos um Pilar Setembrino.",
            "error"
        )

        return redirect(
            url_for("create_bulletin_urban")
        )


    # ========================================================
    # MONTA A PERGUNTA PARA O GEMINI
    # ========================================================

    question = situation


    if problem:

        question += (
            "\n\nProblema social ou urbano:\n"
            + problem
        )


    if consequences:

        question += (
            "\n\nConsequências observadas:\n"
            + consequences
        )


    # ========================================================
    # OBSERVAÇÕES
    # ========================================================

    obs = (
        f"Local da situação: {location}\n\n"
        f"{observations}"
    )


    # ========================================================
    # NOME DO ARQUIVO
    # ========================================================

    filename = (
        f"insight_urbano_"
        f"{uuid.uuid4().hex}.html"
    )


    output_path = os.path.join(
        EXAMPLES_PATH,
        filename
    )


    # ========================================================
    # DEBUG
    # ========================================================

    print()
    print("======================================")
    print("       NOVO INSIGHT URBANO")
    print("======================================")
    print(f"Cidade:       {city}")
    print(f"Local:        {location}")
    print(f"Situação:     {situation}")
    print(f"Pilares:      {pillars}")
    print(f"Arquivo:      {output_path}")
    print("======================================")
    print()


    # ========================================================
    # GERAÇÃO COM GEMINI
    # ========================================================

    try:

        gerar_boletim_html(
            question=question,
            location=location,
            obs=obs,
            pilares=pillars,
            output_filename=output_path
        )

    except Exception as error:

        print()
        print("ERRO AO GERAR INSIGHT:")
        print(error)
        print()

        flash(
            "Não foi possível gerar o boletim.",
            "error"
        )

        return redirect(
            url_for("create_bulletin_urban")
        )


    # ========================================================
    # CONFIRMA SE O ARQUIVO FOI CRIADO
    # ========================================================

    if not os.path.exists(output_path):

        print(
            "ERRO: arquivo HTML não foi criado."
        )

        flash(
            "O boletim não foi criado corretamente.",
            "error"
        )

        return redirect(
            url_for("create_bulletin_urban")
        )


    # ========================================================
    # SUCESSO
    # ========================================================

    flash(
        "Insight Urbano gerado com sucesso!",
        "success"
    )


    print(
        f"✅ Arquivo pronto: {output_path}"
    )


    # ========================================================
    # ABRE DIRETAMENTE NO NAVEGADOR
    # ========================================================

    return send_file(
        output_path,
        mimetype="text/html"
    )