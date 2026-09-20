import numpy as np
from PIL import Image
from ultralytics import YOLO

# ==========================================
# CONFIGURAÇÃO DE MODELOS E DICIONÁRIOS
# ==========================================

# Carrega os dois modelos personalizados e o modelo YOLO base de suporte
try:
    model1 = YOLO("models/best.pt")
except Exception:
    model1 = None

try:
    model2 = YOLO("models/best2.pt")
except Exception:
    model2 = None

try:
    model_base = YOLO("yolov8n-seg.pt")
except Exception:
    model_base = None

# Base de dados de informações nutricionais por alimento
INFO_ALIMENTOS = {
    "apple":         {"categoria": "carboidrato", "kcal_por_grama": 0.52},
    "avocado":       {"categoria": "carboidrato", "kcal_por_grama": 1.60},
    "bacon":         {"categoria": "proteina",    "kcal_por_grama": 5.41},
    "bagel":         {"categoria": "carboidrato", "kcal_por_grama": 2.50},
    "banana":        {"categoria": "carboidrato", "kcal_por_grama": 0.89},
    "beef":          {"categoria": "proteina",    "kcal_por_grama": 2.50},
    "bell pepper":   {"categoria": "verdura",     "kcal_por_grama": 0.31},
    "blueberry":     {"categoria": "carboidrato", "kcal_por_grama": 0.57},
    "bread":         {"categoria": "carboidrato", "kcal_por_grama": 2.65},
    "broccoli":      {"categoria": "verdura",     "kcal_por_grama": 0.34},
    "burger":        {"categoria": "proteina",    "kcal_por_grama": 2.95},
    "cabbage":       {"categoria": "verdura",     "kcal_por_grama": 0.25},
    "carrot":        {"categoria": "verdura",     "kcal_por_grama": 0.41},
    "champignons":   {"categoria": "verdura",     "kcal_por_grama": 0.22},
    "cheese":        {"categoria": "proteina",    "kcal_por_grama": 4.02},
    "chicken":       {"categoria": "proteina",    "kcal_por_grama": 1.65},
    "corn":          {"categoria": "carboidrato", "kcal_por_grama": 0.86},
    "cucumber":      {"categoria": "verdura",     "kcal_por_grama": 0.15},
    "cutlet":        {"categoria": "proteina",    "kcal_por_grama": 2.90},
    "dill":          {"categoria": "verdura",     "kcal_por_grama": 0.43},
    "egg":           {"categoria": "proteina",    "kcal_por_grama": 1.55},
    "french fries":  {"categoria": "carboidrato", "kcal_por_grama": 3.12},
    "garlic":        {"categoria": "verdura",     "kcal_por_grama": 1.49},
    "grape":         {"categoria": "carboidrato", "kcal_por_grama": 0.69},
    "green beans":   {"categoria": "verdura",     "kcal_por_grama": 0.31},
    "green peas":    {"categoria": "verdura",     "kcal_por_grama": 0.81},
    "hot dog":       {"categoria": "proteina",    "kcal_por_grama": 2.90},
    "kiwi":          {"categoria": "carboidrato", "kcal_por_grama": 0.61},
    "lemon":         {"categoria": "carboidrato", "kcal_por_grama": 0.29},
    "lettuce":       {"categoria": "verdura",     "kcal_por_grama": 0.15},
    "lime":          {"categoria": "carboidrato", "kcal_por_grama": 0.30},
    "mashed potato": {"categoria": "carboidrato", "kcal_por_grama": 0.88},
    "noodles":       {"categoria": "carboidrato", "kcal_por_grama": 1.38},
    "oatmeal":       {"categoria": "carboidrato", "kcal_por_grama": 0.71},
    "omelette":      {"categoria": "proteina",    "kcal_por_grama": 1.54},
    "onion":         {"categoria": "verdura",     "kcal_por_grama": 0.40},
    "orange":        {"categoria": "carboidrato", "kcal_por_grama": 0.47},
    "pancakes":      {"categoria": "carboidrato", "kcal_por_grama": 2.27},
    "parsley":       {"categoria": "verdura",     "kcal_por_grama": 0.36},
    "pasta":         {"categoria": "carboidrato", "kcal_por_grama": 1.31},
    "pineapple":     {"categoria": "carboidrato", "kcal_por_grama": 0.50},
    "pizza":         {"categoria": "carboidrato", "kcal_por_grama": 2.66},
    "pork":          {"categoria": "proteina",    "kcal_por_grama": 2.42},
    "potato":        {"categoria": "carboidrato", "kcal_por_grama": 0.87},
    "rice":          {"categoria": "carboidrato", "kcal_por_grama": 1.30},
    "salmon":        {"categoria": "proteina",    "kcal_por_grama": 2.08},
    "sausages":      {"categoria": "proteina",    "kcal_por_grama": 3.01},
    "shrimp":        {"categoria": "proteina",    "kcal_por_grama": 0.99},
    "spinach":       {"categoria": "verdura",     "kcal_por_grama": 0.23},
    "strawberry":    {"categoria": "carboidrato", "kcal_por_grama": 0.32},
    "toast":         {"categoria": "carboidrato", "kcal_por_grama": 2.80},
    "tomato":        {"categoria": "verdura",     "kcal_por_grama": 0.18},
    "tuna":          {"categoria": "proteina",    "kcal_por_grama": 1.16},
    # Adicionais comuns do RU
    "arroz":         {"categoria": "carboidrato", "kcal_por_grama": 1.30},
    "feijao":        {"categoria": "proteina",    "kcal_por_grama": 1.20},
    "frango":        {"categoria": "proteina",    "kcal_por_grama": 1.65},
    "carne":         {"categoria": "proteina",    "kcal_por_grama": 2.50},
    "ovo":           {"categoria": "proteina",    "kcal_por_grama": 1.55},
    "salada":        {"categoria": "verdura",     "kcal_por_grama": 0.15},
}


# ==========================================
# FUNÇÕES DE PROCESSAMENTO E INFERÊNCIA
# ==========================================

def processar_resultados_modelo(result, nomes_classes):
    """Extrai caixas, máscaras e classes de um modelo YOLO, aplicando o filtro anti-soda."""
    itens = []
    if result.boxes is None or len(result.boxes) == 0:
        return itens

    classes_ids = result.boxes.cls.cpu().numpy()
    confiancas = result.boxes.conf.cpu().numpy()

    # Verifica se há máscaras para calcular a área proporcional
    if result.masks is not None:
        mascaras = result.masks.data.cpu().numpy()
        areas = [np.sum(mask > 0) for mask in mascaras]
        area_total = sum(areas) if sum(areas) > 0 else 1

        for cls_id, conf, area in zip(classes_ids, confiancas, areas):
            nome_alimento = nomes_classes[int(cls_id)]
            
            # Substitui 'soda' ou 'refrigerante' por 'carne' automaticamente
            nome_lower = nome_alimento.lower()
            if "soda" in nome_lower or "refrigerante" in nome_lower:
                nome_alimento = "carne"

            porcentagem = round((area / area_total) * 100, 1)
            
            itens.append({
                "class": nome_alimento,
                "confidence": float(conf),
                "porcentagem": porcentagem,
            })
    else:
        caixas = result.boxes.xyxy.cpu().numpy()
        areas = [
            max(0, x2 - x1) * max(0, y2 - y1)
            for x1, y1, x2, y2 in caixas
        ]
        area_total = sum(areas) if sum(areas) > 0 else 1

        for cls_id, conf, area in zip(classes_ids, confiancas, areas):
            nome_alimento = nomes_classes[int(cls_id)]
            
            # Substitui 'soda' ou 'refrigerante' por 'carne' automaticamente
            nome_lower = nome_alimento.lower()
            if "soda" in nome_lower or "refrigerante" in nome_lower:
                nome_alimento = "carne"

            porcentagem = round((area / area_total) * 100, 1)
            
            itens.append({
                "class": nome_alimento, 
                "confidence": float(conf), 
                "porcentagem": porcentagem,
            })
            
    return itens


def detectar_imagem(imagem: Image.Image):
    """Executa em conjunto os modelos (best.pt, best2.pt e yolov8n-seg.pt),

    unifica as deteções e gera a imagem anotada para o Streamlit.
    """
    img_np = np.array(imagem)
    resultado_final = []
    
    # Guarda o resultado principal para desenhar a imagem anotada (prioriza o model1)
    imagem_anotada = None

    # 1. Executa o primeiro modelo personalizado (best.pt)
    if model1 is not None:
        res1 = model1(img_np, conf=0.25)[0]
        resultado_final.extend(processar_resultados_modelo(res1, res1.names))
        imagem_anotada = res1.plot()

    # 2. Executa o segundo modelo personalizado (best2.pt)
    if model2 is not None:
        res2 = model2(img_np, conf=0.25)[0]
        resultado_final.extend(processar_resultados_modelo(res2, res2.names))
        if imagem_anotada is None:
            imagem_anotada = res2.plot()

    # 3. Executa o modelo YOLO base para complementar
    if model_base is not None:
        res_base = model_base(img_np, conf=0.30)[0]
        resultado_final.extend(processar_resultados_modelo(res_base, res_base.names))
        if imagem_anotada is None:
            imagem_anotada = res_base.plot()

    # Fallback caso nenhum modelo tenha gerado plot
    if imagem_anotada is None:
        imagem_anotada = img_np

    # YOLO/OpenCV usa BGR; Streamlit espera RGB
    if len(imagem_anotada.shape) == 3 and imagem_anotada.shape[2] == 3:
        imagem_anotada = imagem_anotada[:, :, ::-1]

    return {
        "deteccoes": resultado_final,
        "imagem_anotada": imagem_anotada,
    }


# ==========================================
# CÁLCULO NUTRICIONAL E CALÓRICO
# ==========================================

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
            # Tenta busca parcial caso o nome venha composto
            encontrou = False
            for chave_cat, dados_cat in INFO_ALIMENTOS.items():
                if chave_cat in nome_chave:
                    info = dados_cat
                    encontrou = True
                    break
            if not encontrou:
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