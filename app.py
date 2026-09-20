import streamlit as st
from PIL import Image


# =========================================================
# YOLO
# =========================================================

try:
    from services.yolo_service import detectar_imagem
    YOLO_DISPONIVEL = True
except ImportError:
    YOLO_DISPONIVEL = False


# =========================================================
# PÁGINA
# =========================================================

st.set_page_config(
    page_title="NutriVision RU",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "mascote" not in st.session_state:
    st.session_state.mascote = "default"


# =========================================================
# ESTILO
# =========================================================

st.markdown("""
<style>

/* ---------- Página ---------- */

.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(143,108,183,.13) 0 2px, transparent 3px),
        radial-gradient(circle at 82% 22%, rgba(255,255,255,.10) 0 1px, transparent 2px),
        radial-gradient(circle at 65% 70%, rgba(173,142,211,.09) 0 2px, transparent 3px),
        radial-gradient(circle at 50% -15%, #51406d 0%, #29233f 38%, #17131f 100%);
    background-size: 180px 180px, 130px 130px, 220px 220px, auto;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
#MainMenu,
footer {
    display: none !important;
}

.block-container {
    max-width: 960px;
    padding: 2.7rem 1.2rem 3rem;
}


/* ---------- Cabeçalho ---------- */

.hero {
    text-align: center;
    margin-bottom: 4rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    color: #fff8ef;
    text-shadow: 0 4px 18px rgba(164,125,206,.22);
}

.hero-subtitle {
    color: #d0c6dc;
    font-size: 1.05rem;
    margin-top: .7rem;
}


/* ---------- Card ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    position: relative;
    overflow: visible;

    background: rgba(39,32,57,.88);
    backdrop-filter: blur(8px);

    border: 1px solid #725e8c !important;

    box-shadow:
        0 8px 0 #100d18,
        0 22px 45px rgba(0,0,0,.24);

    transition: transform .2s ease, box-shadow .2s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);

    box-shadow:
        0 10px 0 #100d18,
        0 27px 50px rgba(0,0,0,.30);
}


/* ---------- Upload / botões ---------- */

[data-testid="stFileUploaderDropzone"] {
    transition: transform .15s ease, border-color .15s ease;
}

[data-testid="stFileUploaderDropzone"]:hover {
    transform: translateY(-2px);
    border-color: #b39bcb !important;
}

.stButton > button {
    transition: transform .15s ease, filter .15s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.08);
}


/* ---------- Resultados ---------- */

.food-result {
    display: flex;
    justify-content: space-between;
    gap: 1rem;

    padding: .8rem 1rem;
    margin: .5rem 0;

    background: #272032;
    border: 1px solid #665179;
    border-radius: 12px;

    transition: .15s ease;
}

.food-result:hover {
    transform: translateX(5px);
    background: #332940;
}

.food-name {
    color: #fff8ef;
    font-weight: 600;
}

.food-confidence {
    color: #91d29d;
    font-weight: 700;
}


/* =========================================================
   MASCOTE
========================================================= */

.mascot {
    height: 48px;
    position: relative;

    margin-top: -66px;
    margin-bottom: 25px;

    z-index: 20;
    pointer-events: none;
}

.monster {
    position: absolute;
    left: 50%;
    bottom: 0;

    width: 88px;
    height: 64px;

    transform: translateX(-50%);

    background: linear-gradient(145deg, #b99cdd, #8063aa);

    border: 3px solid #d8c5ef;
    border-radius: 45% 45% 38% 38%;

    box-shadow:
        0 7px 0 #513b70,
        0 12px 18px rgba(0,0,0,.25);

    animation: monsterFloat 3s ease-in-out infinite;
}


/* Chifres */

.horn {
    position: absolute;
    top: -13px;

    width: 16px;
    height: 20px;

    background: #9b7ac3;

    border: 3px solid #d8c5ef;
    border-bottom: 0;
    border-radius: 50% 50% 0 0;
}

.horn.left {
    left: 12px;
    transform: rotate(-18deg);
}

.horn.right {
    right: 12px;
    transform: rotate(18deg);
}


/* Olhos */

.eye {
    position: absolute;
    top: 22px;

    width: 10px;
    height: 12px;

    background: #20172d;
    border-radius: 50%;
}

.eye.left {
    left: 23px;
}

.eye.right {
    right: 23px;
}


/* Boca */

.mouth {
    position: absolute;
    left: 50%;
    bottom: 14px;

    width: 20px;
    height: 3px;

    transform: translateX(-50%);

    background: #3a2749;
    border-radius: 10px;
}


/* Braços */

.arm {
    position: absolute;
    bottom: -10px;

    width: 25px;
    height: 12px;

    background: #8d6bb5;

    border: 3px solid #d8c5ef;
    border-radius: 12px;
}

.arm.left {
    left: -10px;
    transform: rotate(12deg);
}

.arm.right {
    right: -10px;
    transform: rotate(-12deg);
}


/* Feliz */

.mascot-happy .mouth {
    width: 22px;
    height: 11px;
    bottom: 10px;

    background: transparent;

    border-bottom: 4px solid #3a2749;
    border-radius: 50%;
}

.mascot-happy .monster {
    animation: monsterHappy .55s ease-in-out infinite alternate;
}


/* Triste */

.mascot-sad .mouth {
    width: 22px;
    height: 10px;
    bottom: 7px;

    background: transparent;

    border-top: 4px solid #3a2749;
    border-radius: 50%;
}

.mascot-sad .monster {
    animation: none;
    transform: translateX(-50%) translateY(5px);
}

.mascot-sad .eye {
    height: 9px;
}


/* Animações */

@keyframes monsterFloat {
    0%, 100% {
        transform: translateX(-50%) translateY(0);
    }

    50% {
        transform: translateX(-50%) translateY(-4px);
    }
}

@keyframes monsterHappy {
    from {
        transform: translateX(-50%) translateY(0) rotate(-2deg);
    }

    to {
        transform: translateX(-50%) translateY(-7px) rotate(2deg);
    }
}


/* ---------- Mobile ---------- */

@media (max-width: 700px) {

    .block-container {
        padding: 1.3rem .8rem 2rem;
    }

    .hero-title {
        font-size: 2.1rem;
    }

    .mascot {
        margin-top: -55px;
    }

    .monster {
        width: 72px;
        height: 54px;
    }

    .food-result {
        flex-direction: column;
        gap: .2rem;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# MASCOTE
# =========================================================

def estado_mascote(resultado):
    """
    Regra provisória.

    Depois substituímos apenas esta função pela análise
    dos dados nutricionais/macros.
    """

    classes = {
        str(item.get("class", "")).strip().lower()
        for item in (resultado or [])
        if isinstance(item, dict)
    }

    vegetais = {
        "salad",
        "salada",
        "lettuce",
        "alface",
        "tomato",
        "tomate",
        "carrot",
        "cenoura",
        "cabbage",
        "vegetable",
        "vegetables",
    }

    return "happy" if classes & vegetais else "sad"


def html_mascote(estado):
    return (
        f'<div class="mascot mascot-{estado}">'
        '<div class="monster">'
        '<span class="horn left"></span>'
        '<span class="horn right"></span>'
        '<span class="eye left"></span>'
        '<span class="eye right"></span>'
        '<span class="mouth"></span>'
        '<span class="arm left"></span>'
        '<span class="arm right"></span>'
        '</div>'
        '</div>'
    )


# =========================================================
# RESULTADOS
# =========================================================

def mostrar_resultado(resultado):

    if not resultado:
        st.warning("Nenhum alimento foi identificado.")
        return

    st.subheader("Alimentos identificados")

    for item in resultado:

        if not isinstance(item, dict):
            continue

        nome = item.get("class", "Desconhecido")
        confianca = float(
            item.get("confidence", 0)
        ) * 100

        st.markdown(
            f'<div class="food-result">'
            f'<span class="food-name">{nome}</span>'
            f'<span class="food-confidence">{confianca:.1f}%</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


# =========================================================
# CABEÇALHO
# =========================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-title">🍽️ NutriVision RU</div>'
    '<div class="hero-subtitle">'
    'Descubra o que há no seu prato e entenda melhor sua refeição no RU.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# CARD PRINCIPAL
# =========================================================

with st.container(border=True):

    # Lugar fixo do mascote
    mascot_slot = st.empty()

    mascot_slot.markdown(
        html_mascote(st.session_state.mascote),
        unsafe_allow_html=True,
    )

    st.subheader("Analise sua refeição")

    st.write(
        "Envie uma imagem ou vídeo do seu prato. "
        "O sistema identificará os alimentos usando visão computacional."
    )

    tipo = st.radio(
        "Tipo de entrada:",
        ["Imagem", "Vídeo"],
        horizontal=True,
    )


    # =====================================================
    # IMAGEM
    # =====================================================

    if tipo == "Imagem":

        arquivo = st.file_uploader(
            "Envie uma foto do seu prato",
            type=["jpg", "jpeg", "png"],
            key="imagem",
        )

        # Sem imagem -> estado neutro
        if not arquivo:

            if st.session_state.mascote != "default":

                st.session_state.mascote = "default"

                mascot_slot.markdown(
                    html_mascote("default"),
                    unsafe_allow_html=True,
                )

        else:

            try:

                imagem = Image.open(
                    arquivo
                ).convert("RGB")

                st.image(
                    imagem,
                    caption="Pré-visualização",
                    use_container_width=True,
                )

                if st.button(
                    "Analisar refeição",
                    type="primary",
                    use_container_width=True,
                ):

                    if not YOLO_DISPONIVEL:

                        st.info(
                            "O modelo YOLO ainda não está conectado."
                        )

                    else:

                        with st.spinner(
                            "Identificando alimentos..."
                        ):

                            resultado = detectar_imagem(
                                imagem
                            )

                        # Atualiza reação
                        estado = estado_mascote(
                            resultado
                        )

                        st.session_state.mascote = estado

                        mascot_slot.markdown(
                            html_mascote(estado),
                            unsafe_allow_html=True,
                        )

                        mostrar_resultado(
                            resultado
                        )

            except Exception as erro:

                st.error(
                    f"Erro ao abrir ou processar a imagem: {erro}"
                )


    # =====================================================
    # VÍDEO
    # =====================================================

    else:

        # Vídeo ainda não é analisado -> mascote neutro
        if st.session_state.mascote != "default":

            st.session_state.mascote = "default"

            mascot_slot.markdown(
                html_mascote("default"),
                unsafe_allow_html=True,
            )

        arquivo = st.file_uploader(
            "Envie um vídeo da sua refeição",
            type=["mp4", "avi", "mov"],
            key="video",
        )

        if arquivo:

            st.video(
                arquivo
            )

            if st.button(
                "Analisar vídeo",
                type="primary",
                use_container_width=True,
            ):

                st.info(
                    "A integração de vídeo com o YOLO "
                    "será adicionada em seguida."
                )


# =========================================================
# INFORMAÇÕES
# =========================================================

st.write("")

with st.expander("Como funciona?"):

    st.markdown("""
1. Envie uma foto ou vídeo da refeição.
2. O YOLO identifica os alimentos.
3. O sistema apresenta cada alimento e a confiança da detecção.
4. Os alimentos serão associados aos dados nutricionais para calcular os macros.
""")


st.caption(
    "Hackathon SECOMP 2026 • NutriVision RU"
)