import streamlit as st
from PIL import Image

# Tenta importar o serviço do YOLO.
# Enquanto a equipe ainda estiver implementando, a interface continua abrindo.
try:
    from services.yolo_service import detectar_imagem
    YOLO_DISPONIVEL = True
except Exception:
    YOLO_DISPONIVEL = False


# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="NutriVision RU",
    page_icon="🍽️",
    layout="centered"
)


# =========================
# CABEÇALHO
# =========================

st.title("🍽️ NutriVision RU")

st.write(
    "Envie uma imagem ou vídeo da sua refeição para identificar "
    "os alimentos presentes no prato."
)

st.divider()


# =========================
# TIPO DE ENTRADA
# =========================

tipo_entrada = st.radio(
    "Escolha o tipo de arquivo:",
    ["Imagem", "Vídeo"],
    horizontal=True
)


# =========================
# IMAGEM
# =========================

if tipo_entrada == "Imagem":

    arquivo = st.file_uploader(
        "Selecione uma imagem",
        type=["jpg", "jpeg", "png"]
    )

    if arquivo is not None:

        imagem = Image.open(arquivo).convert("RGB")

        st.image(
            imagem,
            caption="Imagem selecionada",
            use_container_width=True
        )

        if st.button(
            "Analisar imagem",
            type="primary",
            use_container_width=True
        ):

            if not YOLO_DISPONIVEL:

                st.warning(
                    "O serviço do YOLO ainda não está conectado."
                )

            else:

                with st.spinner("Identificando alimentos..."):

                    try:
                        resultado = detectar_imagem(imagem)

                        st.subheader("Alimentos identificados")

                        if not resultado:

                            st.warning(
                                "Nenhum alimento foi identificado."
                            )

                        else:

                            for item in resultado:

                                classe = item.get(
                                    "class",
                                    "Desconhecido"
                                )

                                confianca = item.get(
                                    "confidence",
                                    0
                                )

                                st.write(
                                    f"**{classe}** "
                                    f"— {confianca * 100:.1f}%"
                                )

                    except Exception as erro:

                        st.error(
                            f"Erro ao processar a imagem: {erro}"
                        )


# =========================
# VÍDEO
# =========================

else:

    arquivo = st.file_uploader(
        "Selecione um vídeo",
        type=["mp4", "avi", "mov"]
    )

    if arquivo is not None:

        st.video(arquivo)

        if st.button(
            "Analisar vídeo",
            type="primary",
            use_container_width=True
        ):

            st.info(
                "A análise de vídeo será integrada "
                "ao serviço do YOLO na próxima etapa."
            )


# =========================
# INFORMAÇÕES
# =========================

st.divider()

with st.expander("Como o sistema funciona?"):

    st.write(
        """
        1. O usuário envia uma imagem ou vídeo da refeição.
        2. O YOLO identifica os alimentos presentes.
        3. O sistema retorna as classes detectadas e suas confianças.
        4. Futuramente, os alimentos serão associados a dados nutricionais.
        """
    )


st.caption(
    "Protótipo desenvolvido para o Hackathon SECOMP 2026."
)