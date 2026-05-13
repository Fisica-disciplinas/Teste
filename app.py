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

# Banco de dados fiel ao arquivo anexado
BANCO_QUESTOES = [
    {
        "q": "A planta de crescimento mais rápido de que se tem notícia, a Hesperoyucca whipplei, cresceu 3,7 m em 14 dias. Qual é a ordem de grandeza e o valor aproximado da velocidade média de crescimento dessa planta em micrômetros por segundo (µm/s)?",
        "o": ["3,06 × 10⁰ µm/s", "3,06 × 10² µm/s", "3,06 × 10⁻² µm/s", "3,06 × 10⁶ µm/s"],
        "c": "3,06 × 10⁰ µm/s"
    },
    {
        "q": "Durante um experimento no laboratório para determinar a massa específica de diferentes substâncias, um aluno anota as seguintes medições: 0,0056 g e 1,2300 g/cm³. Quantos algarismos significativos há em cada uma dessas medidas, respectivamente?",
        "o": ["4 e 5", "2 e 5", "2 e 4", "4 e 4"],
        "c": "2 e 5"
    },
    {
        "q": "Um biólogo está calculando a área de uma lâmina de vidro para microscópio e multiplica as medidas de seus lados: 4,32 cm por 2,1 cm. Aplicando rigorosamente a regra do menor número de algarismos significativos para multiplicação, qual deve ser o resultado final registrado no relatório?",
        "o": ["9,072 cm²", "9,07 cm²", "9,1 cm²", "9,0 cm²"],
        "c": "9,1 cm²"
    },
    {
        "q": "Imagine que estamos modelando um problema biológico ou geológico através de um novelo gigante que possui cerca de 2 m de raio. Se desenrolarmos todo o fio e obtivermos um comprimento total de 1000 km, qual é a ordem de grandeza desse comprimento se expresso no Sistema Internacional de Unidades (metros)?",
        "o": ["10³", "10⁵", "10⁶", "10⁹"],
        "c": "10⁶"
    },
    {
        "q": "Ao medir o comprimento de um osso em laboratório com uma régua de excelente qualidade (cuja menor divisão é de 1 mm), um estudante anota o valor de 9,65 cm. Fisicamente, o que podemos afirmar sobre os algarismos dessa medida?",
        "o": ["Todos os algarismos são exatos, pois a régua é precisa.", "Os algarismos 9 e 6 são lidos na régua (corretos), enquanto o 5 é um algarismo estimado (duvidoso).", "O algarismo 9 é o único correto, os demais são duvidosos.", "A medida possui 4 algarismos significativos."],
        "c": "Os algarismos 9 e 6 são lidos na régua (corretos), enquanto o 5 é um algarismo estimado (duvidoso)."
    },
    {
        "q": "Você está dirigindo rumo a uma base de pesquisa ambiental em uma estrada retilínea. O carro percorre 8,4 km a 70 km/h, mas repentinamente para por falta de gasolina. Nos 30 minutos seguintes, você caminha mais 2,0 km ao longo da estrada até chegar a um posto. Qual foi a sua velocidade escalar média desde o início da viagem até a chegada ao posto?",
        "o": ["16,8 km/h", "35,0 km/h", "70,0 km/h", "12,4 km/h"],
        "c": "16,8 km/h"
    },
    {
        "q": "Após abastecer, o pesquisador faz o caminho de volta. Ele viaja metade da distância total a 55 km/h e a outra metade da distância a 90 km/h. Qual é a velocidade escalar média durante essa viagem inteira de retorno? (Dica: Pense na relação entre a distância e o tempo total).",
        "o": ["72,5 km/h", "68,3 km/h", "35,0 km/h", "0 km/h"],
        "c": "68,3 km/h"
    },
    {
        "q": "Ao fazer diferentes operações com valores de medidas na mesma expressão, como calcular a quantidade de matéria, um aluno obtém a seguinte expressão: (0,58 dm³ - 0,050 dm³) × 0,112 mol/dm³. Realizando primeiro a subtração e considerando o fator que tem o menor número de algarismos significativos (que é 2), a resposta final correta é:",
        "o": ["0,05936 mol", "0,0594 mol", "0,059 mol", "0,06 mol"],
        "c": "0,059 mol"
    },
    {
        "q": "Um piscar de olhos humano dura, em média, cerca de 100 ms. Um caça a jato de alta performance se move a uma velocidade de 3400 km/h. Qual é, aproximadamente, a distância percorrida por esse caça apenas durante o piscar de olhos do piloto?",
        "o": ["94,4 m", "340 m", "34 m", "9,4 m"],
        "c": "94,4 m"
    },
    {
        "q": "Um piloto de avião agrícola voa 483 km para o leste em 45,0 minutos para espalhar sementes. Expressando a distância de 483 km em notação científica no Sistema Internacional (metros), obtemos:",
        "o": ["483 × 10³ m", "4,83 × 10⁵ m", "4,83 × 10⁴ m", "4,83 × 10⁻⁵ m"],
        "c": "4,83 × 10⁵ m"
    }
]

if 'shuffled_questions' not in st.session_state:
    data_copy = []
    for item in BANCO_QUESTOES:
        opts = list(item["o"])
        random.shuffle(opts)
        data_copy.append({"q": item["q"], "o": opts, "c": item["c"]})
    random.shuffle(data_copy)
    st.session_state.shuffled_questions = data_copy

def gerar_pdf_professor(nome, nota, porcentagem):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(47, 158, 65)
    pdf.cell(190, 10, txt="IFPI - COMPROVANTE DE ATIVIDADE", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("helvetica", '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(190, 8, txt=f"Estudante: {nome}", ln=True)
    pdf.cell(190, 8, txt=f"Disciplina: Introdução às Ciências da Natureza", ln=True)
    pdf.cell(190, 8, txt=f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(10)
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(190, 15, txt=f"NOTA FINAL: {nota} / 10.0", ln=True, align='C', border=1)
    pdf.set_font("helvetica", '', 12)
    pdf.cell(190, 10, txt=f"Aproveitamento: {porcentagem}%", ln=True, align='C')
    return bytes(pdf.output())

with st.form("quiz_ifpi"):
    nome_aluno = st.text_input("Nome Completo (para registro no SUAP):")
    respostas_usuario = []
    for i, item in enumerate(st.session_state.shuffled_questions):
        st.write(f"**Questão {i+1}**")
        respostas_usuario.append(st.radio(item["q"], item["o"], index=None, key=f"quest_{i}"))
        st.write("")
    
    enviar = st.form_submit_button("FINALIZAR TESTE")

if enviar:
    if not nome_aluno or None in respostas_usuario:
        st.warning("⚠️ Preencha seu nome e responda todas as questões.")
    else:
        acertos = sum(1 for i, r in enumerate(respostas_usuario) if r == st.session_state.shuffled_questions[i]["c"])
        nota_final = float(acertos)
        porcentagem = int((acertos/10)*100)
        
        st.success(f"Teste finalizado! Sua nota foi {nota_final}")
        
        pdf_bytes = gerar_pdf_professor(nome_aluno, nota_final, porcentagem)
        st.download_button(
            label="📄 BAIXAR COMPROVANTE (Enviar ao Professor)",
            data=pdf_bytes,
            file_name=f"SUAP_{nome_aluno.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
