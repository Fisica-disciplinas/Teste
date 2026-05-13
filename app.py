import streamlit as st
from fpdf import FPDF
from datetime import datetime
import random

# Configuração da página com a identidade visual do IFPI
st.set_page_config(page_title="Teste Diagnóstico - Física IFPI", page_icon="🔬")

# Cabeçalho Institucional
st.markdown("""
    <div style='background-color: #2f9e41; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;'>
        <h1 style='margin:0;'>INSTITUTO FEDERAL DO PIAUÍ</h1>
        <p style='margin:0;'>Campus Parnaíba | Licenciatura em Física</p>
        <p style='margin:0;'><b>Professor: Lucas Izidio</b></p>
    </div>
""", unsafe_allow_html=True)

# Banco de dados atualizado conforme o arquivo anexado
BANCO_QUESTOES = [
    {
        "q": "Qual é a ordem de grandeza e o valor aproximado da velocidade média de crescimento da planta Hesperoyucca whipplei em micrômetros por segundo (µm/s), sabendo que cresceu 3,7 m em 14 dias?",
        "o": ["3,06 × 10⁰ µm/s", "3,06 × 10² µm/s", "3,06 × 10⁻² µm/s", "3,06 × 10⁶ µm/s"],
        "c": "3,06 × 10⁰ µm/s",
        "r": "14 dias = 1.209.600 s. Velocidade = 3,7 m / 1.209.600 s ≈ 3,058 × 10⁻⁶ m/s. Convertendo para µm (10⁻⁶ m), temos ≈ 3,06 × 10⁰ µm/s. Ordem de grandeza: 10⁰."
    },
    {
        "q": "Quantos algarismos significativos há nas medidas 0,0056 g e 1,2300 g/cm³, respectivamente?",
        "o": ["4 e 5", "2 e 5", "2 e 4", "4 e 4"],
        "c": "2 e 5",
        "r": "Zeros à esquerda não são significativos (0,0056 tem 2 AS). Em decimais, zeros à direita são significativos (1,2300 tem 5 AS)."
    },
    {
        "q": "Aplicando a regra do menor número de algarismos significativos para multiplicação, qual o resultado da área de uma lâmina de 4,32 cm por 2,1 cm?",
        "o": ["9,072 cm²", "9,07 cm²", "9,1 cm²", "9,0 cm²"],
        "c": "9,1 cm²",
        "r": "O fator 2,1 possui apenas dois AS. O resultado 9,072 deve ser arredondado para dois AS, resultando em 9,1 cm²."
    },
    {
        "q": "Qual é a ordem de grandeza do comprimento de 1000 km se expresso no Sistema Internacional de Unidades (metros)?",
        "o": ["10³", "10⁵", "10⁶", "10⁹"],
        "c": "10⁶",
        "r": "1000 km = 1.000.000 m = 10⁶ m."
    },
    {
        "q": "Ao medir um osso com uma régua cuja menor divisão é 1 mm e anotar 9,65 cm, o que podemos afirmar fisicamente sobre os algarismos dessa medida?",
        "o": ["Todos os algarismos são exatos", "9 e 6 são corretos, enquanto o 5 é estimado (duvidoso)", "O algarismo 9 é o único correto", "A medida possui 4 algarismos significativos"],
        "c": "9 e 6 são corretos, enquanto o 5 é estimado (duvidoso)",
        "r": "Em instrumentos analógicos, o último algarismo da medida é sempre estimado pelo observador (duvidoso)."
    },
    {
        "q": "Qual foi a velocidade escalar média de uma viagem onde o carro percorre 8,4 km a 70 km/h e o motorista caminha mais 2,0 km por 30 minutos?",
        "o": ["16,8 km/h", "35,0 km/h", "70,0 km/h", "12,4 km/h"],
        "c": "16,8 km/h",
        "r": "Tempo dirigindo = 0,12 h. Tempo total = 0,12 + 0,50 = 0,62 h. Distância total = 10,4 km. Vm = 10,4 / 0,62 ≈ 16,8 km/h."
    },
    {
        "q": "Em uma viagem de retorno, um pesquisador viaja metade da distância a 55 km/h e a outra metade a 90 km/h. Qual a velocidade escalar média da viagem inteira?",
        "o": ["72,5 km/h", "68,3 km/h", "35,0 km/h", "0 km/h"],
        "c": "68,3 km/h",
        "r": "Para metades iguais de distância, usa-se a média harmônica: (2 * 55 * 90) / (55 + 90) ≈ 68,3 km/h."
    },
    {
        "q": "Qual o resultado correto da expressão (0,58 dm³ - 0,050 dm³) × 0,112 mol/dm³, considerando as regras de algarismos significativos?",
        "o": ["0,05936 mol", "0,0594 mol", "0,059 mol", "0,06 mol"],
        "c": "0,059 mol",
        "r": "A subtração resulta em 0,53 (2 AS). O produto 0,53 * 0,112 = 0,05936 deve ser arredondado para dois AS: 0,059."
    },
    {
        "q": "Qual a distância aproximada percorrida por um caça a 3400 km/h durante um piscar de olhos de 100 ms?",
        "o": ["94,4 m", "340 m", "34 m", "9,4 m"],
        "c": "94,4 m",
        "r": "3400 km/h ≈ 944,4 m/s. Distância = 944,4 * 0,1 s = 94,44 m."
    },
    {
        "q": "Expressando a distância de 483 km em notação científica no Sistema Internacional (metros), qual o valor obtido?",
        "o": ["483 × 10³ m", "4,83 × 10⁵ m", "4,83 × 10⁴ m", "4,83 × 10⁻⁵ m"],
        "c": "4,83 × 10⁵ m",
        "r": "483 km = 483.000 m. Em notação científica: 4,83 × 10⁵ m."
    }
]

# Inicializa as questões aleatórias na sessão
if 'questoes_random' not in st.session_state:
    lista_temp = []
    for item in BANCO_QUESTOES:
        opcoes = list(item["o"])
        random.shuffle(opcoes)
        lista_temp.append({
            "q": item["q"],
