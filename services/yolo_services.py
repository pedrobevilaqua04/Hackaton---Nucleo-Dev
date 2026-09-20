import numpy as np
from PIL import Image
from ultralytics import YOLO

INFO_ALIMENTOS = {
    "apple":          {"categoria": "carboidrato", "kcal_por_grama": 0.52},
    "avocado":        {"categoria": "carboidrato", "kcal_por_grama": 1.60},
    "bacon":          {"categoria": "proteina",    "kcal_por_grama": 5.41},
    "bagel":          {"categoria": "carboidrato", "kcal_por_grama": 2.50},
    "banana":         {"categoria": "carboidrato", "kcal_por_grama": 0.89},
    "beef":           {"categoria": "proteina",    "kcal_por_grama": 2.50},
    "bell pepper":    {"categoria": "verdura",     "kcal_por_grama": 0.31},
    "blueberry":      {"categoria": "carboidrato", "kcal_por_grama": 0.57},
    "bread":          {"categoria": "carboidrato", "kcal_por_grama": 2.65},
    "broccoli":       {"categoria": "verdura",     "kcal_por_grama": 0.34},
    "burger":         {"categoria": "proteina",    "kcal_por_grama": 2.95},
    "cabbage":        {"categoria": "verdura",     "kcal_por_grama": 0.25},
    "carrot":         {"categoria": "verdura",     "kcal_por_grama": 0.41},
    "champignons":    {"categoria": "verdura",     "kcal_por_grama": 0.22},
    "cheese":         {"categoria": "proteina",    "kcal_por_grama": 4.02},
    "chicken":        {"categoria": "proteina",    "kcal_por_grama": 1.65},
    "corn":           {"categoria": "carboidrato", "kcal_por_grama": 0.86},
    "cucumber":       {"categoria": "verdura",     "kcal_por_grama": 0.15},
    "cutlet":         {"categoria": "proteina",    "kcal_por_grama": 2.90},
    "dill":           {"categoria": "verdura",     "kcal_por_grama": 0.43},
    "egg":            {"categoria": "proteina",    "kcal_por_grama": 1.55},
    "french fries":   {"categoria": "carboidrato", "kcal_por_grama": 3.12},
    "garlic":         {"categoria": "verdura",     "kcal_por_grama": 1.49},
    "grape":          {"categoria": "carboidrato", "kcal_por_grama": 0.69},
    "green beans":    {"categoria": "verdura",     "kcal_por_grama": 0.31},
    "green peas":     {"categoria": "verdura",     "kcal_por_grama": 0.81},
    "hot dog":        {"categoria": "proteina",    "kcal_por_grama": 2.90},
    "kiwi":           {"categoria": "carboidrato", "kcal_por_grama": 0.61},
    "lemon":          {"categoria": "carboidrato", "kcal_por_grama": 0.29},
    "lettuce":        {"categoria": "verdura",     "kcal_por_grama": 0.15},
    "lime":           {"categoria": "carboidrato", "kcal_por_grama": 0.30},
    "mashed potato":  {"categoria": "carboidrato", "kcal_por_grama": 0.88},
    "noodles":        {"categoria": "carboidrato", "kcal_por_grama": 1.38},
    "oatmeal":        {"categoria": "carboidrato", "kcal_por_grama": 0.71},
    "omelette":       {"categoria": "proteina",    "kcal_por_grama": 1.54},
    "onion":          {"categoria": "verdura",     "kcal_por_grama": 0.40},
    "orange":         {"categoria": "carboidrato", "kcal_por_grama": 0.47},
    "pancakes":       {"categoria": "carboidrato", "kcal_por_grama": 2.27},
    "parsley":        {"categoria": "verdura",     "kcal_por_grama": 0.36},
    "pasta":          {"categoria": "carboidrato", "kcal_por_grama": 1.31},
    "pineapple":      {"categoria": "carboidrato", "kcal_por_grama": 0.50},
    "pizza":          {"categoria": "carboidrato", "kcal_por_grama": 2.66},
    "pork":           {"categoria": "proteina",    "kcal_por_grama": 2.42},
    "potato":         {"categoria": "carboidrato", "kcal_por_grama": 0.87},
    "rice":           {"categoria": "carboidrato", "kcal_por_grama": 1.30},
    "salmon":         {"categoria": "proteina",    "kcal_por_grama": 2.08},
    "sausages":       {"categoria": "proteina",    "kcal_por_grama": 3.01},
    "shrimp":         {"categoria": "proteina",    "kcal_por_grama": 0.99},
    "spinach":        {"categoria": "verdura",     "kcal_por_grama": 0.23},
    "strawberry":     {"categoria": "carboidrato", "kcal_por_grama": 0.32},
    "toast":          {"categoria": "carboidrato", "kcal_por_grama": 2.80},
    "tomato":         {"categoria": "verdura",     "kcal_por_grama": 0.18},
    "tuna":           {"categoria": "proteina",    "kcal_por_grama": 1.16},
}

# Carrega o seu modelo treinado da pasta models/
model = YOLO("models/best.pt")


def detectar_imagem(imagem: Image.Image):
    """
    Executa o YOLO e retorna:
    - detecções
    - imagem anotada com boxes/máscaras
    """

    img_np = np.array(imagem)

    results = model(img_np, conf=0.25)
    result = results[0]

    # Imagem com boxes/máscaras desenhados pelo YOLO
    imagem_anotada = result.plot()

    # YOLO/OpenCV usa BGR; Streamlit espera RGB
    imagem_anotada = imagem_anotada[:, :, ::-1]

    if result.boxes is None or len(result.boxes) == 0:
        return {
            "deteccoes": [],
            "imagem_anotada": imagem_anotada,
        }

    classes_ids = result.boxes.cls.cpu().numpy()
    confiancas = result.boxes.conf.cpu().numpy()
    nomes_classes = result.names

    resultado_final = []

    # Se houver segmentação
    if result.masks is not None:
        mascaras = result.masks.data.cpu().numpy()

        areas = [
            np.sum(mask > 0)
            for mask in mascaras
        ]

    # Se houver apenas bounding boxes
    else:
        caixas = result.boxes.xyxy.cpu().numpy()

        areas = [
            max(0, x2 - x1) * max(0, y2 - y1)
            for x1, y1, x2, y2 in caixas
        ]

    area_total = sum(areas) or 1

    for cls_id, conf, area in zip(
        classes_ids,
        confiancas,
        areas,
    ):
        nome = nomes_classes[int(cls_id)]

        porcentagem = round(
            (area / area_total) * 100,
            1,
        )

        resultado_final.append({
            "class": nome,
            "confidence": float(conf),
            "porcentagem": porcentagem,
        })

    return {
        "deteccoes": resultado_final,
        "imagem_anotada": imagem_anotada,
    }

def calcular_calorias(deteccoes, peso_total: float = 500.0):
    if not deteccoes:
        return {
            "calorias_totais": 0.0,
            "itens": [],
            "percentual_area_categoria": {},
            "percentual_calorias_categoria": {},
        }

    itens = []
    calorias_totais = 0.0
    area_por_categoria = {}
    kcal_por_categoria = {}

    for det in deteccoes:
       nome = det["class"]
nome_chave = nome.strip().lower()

porcentagem_area = det["porcentagem"]

info = INFO_ALIMENTOS.get(nome_chave)
        if info is None:
            # Alimento não catalogado: ignora no cálculo calórico,
            # mas ainda soma na área "desconhecida" se quiser tratar depois
            continue

        categoria = info["categoria"]
        kcal_g = info["kcal_por_grama"]

        peso_estimado_g = peso_total * (porcentagem_area / 100.0)
        kcal_item = peso_estimado_g * kcal_g

        calorias_totais += kcal_item
        area_por_categoria[categoria] = area_por_categoria.get(categoria, 0.0) + porcentagem_area
        kcal_por_categoria[categoria] = kcal_por_categoria.get(categoria, 0.0) + kcal_item

        itens.append({
            "class": nome,
            "categoria": categoria,
            "porcentagem_area": porcentagem_area,
            "peso_estimado_g": round(peso_estimado_g, 1),
            "kcal_estimado": round(kcal_item, 1),
        })

    # Normaliza percentuais de calorias (0-100)
    percentual_calorias_categoria = {
        cat: round((kcal / calorias_totais) * 100, 1) if calorias_totais > 0 else 0.0
        for cat, kcal in kcal_por_categoria.items()
    }

    percentual_area_categoria = {
        cat: round(area, 1) for cat, area in area_por_categoria.items()
    }

    return {
        "calorias_totais": round(calorias_totais, 1),
        "itens": itens,
        "percentual_area_categoria": percentual_area_categoria,
        "percentual_calorias_categoria": percentual_calorias_categoria,
    }