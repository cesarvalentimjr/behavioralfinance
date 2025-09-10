import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# Configuração da página
st.set_page_config(
    page_title="Estudos de Contabilidade Comportamental",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #4F46E5;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #6B7280;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    .professor-name {
        text-align: center;
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .block-header {
        color: #374151;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .context-box {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #4F46E5;
    }
    .activity-box {
        background-color: #EEF2FF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #C7D2FE;
    }
    .reflection-box {
        background-color: #F9FAFB;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1.5rem;
        border: 1px solid #E5E7EB;
    }
    .simulation-result {
        background-color: #DCFCE7;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border: 1px solid #BBF7D0;
    }
    .price-display {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #4F46E5;
        text-align: center;
        margin: 1rem 0;
    }
    .info-message {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Função para inicializar o estado da sessão
def init_session_state():
    if 'current_block' not in st.session_state:
        st.session_state.current_block = 1
    
    # Estados do Bloco 1
    if 'block1_round' not in st.session_state:
        st.session_state.block1_round = 0
    if 'block1_current_price' not in st.session_state:
        st.session_state.block1_current_price = 100.0
    if 'block1_prices_log' not in st.session_state:
        st.session_state.block1_prices_log = []
    if 'block1_selected_group' not in st.session_state:
        st.session_state.block1_selected_group = None
    if 'block1_info_message' not in st.session_state:
        st.session_state.block1_info_message = 'Selecione um grupo para começar.'
    if 'block1_simulation_started' not in st.session_state:
        st.session_state.block1_simulation_started = False
    if 'block1_revealed_group' not in st.session_state:
        st.session_state.block1_revealed_group = None
    
    # Estados do Bloco 2
    if 'block2_show_result' not in st.session_state:
        st.session_state.block2_show_result = False
    if 'block2_gains_choice' not in st.session_state:
        st.session_state.block2_gains_choice = None
    if 'block2_losses_choice' not in st.session_state:
        st.session_state.block2_losses_choice = None

# Dados para os grupos do Bloco 1
RATIONAL_INFO = [
    'Análise de mercado indica que o valor patrimonial da empresa está em R$100.',
    'Novo relatório financeiro mostra crescimento de 5% no lucro líquido no último trimestre.',
    'A empresa anunciou um novo produto, mas as projeções de receita se mantiveram conservadoras.',
    'A concorrência enfrenta problemas de liquidez, o que pode fortalecer a posição da empresa no longo prazo.',
    'Uma auditoria interna confirma que a empresa está com a saúde financeira estável.',
]

NOISE_INFO = [
    'Rumor: A empresa vai anunciar uma nova parceria que pode dobrar o lucro!',
    'Boato: Um grande fundo de investimento está se desfazendo da posição na empresa.',
    'Notícia: Concorrência lança produto inovador que pode afetar as vendas.',
    'Análise: O setor está em baixa, sinal de que a ação deve cair nos próximos dias.',
    'Especialista em TV: O mercado está eufórico, é hora de comprar!',
]

# Dados para o Bloco 3
PETRO_DATA = [
    {'name': 'Jan/19', 'valor': 25.5}, {'name': 'Fev/19', 'valor': 27.1}, {'name': 'Mar/19', 'valor': 26.8},
    {'name': 'Abr/19', 'valor': 28.5}, {'name': 'Mai/19', 'valor': 27.9}, {'name': 'Jun/19', 'valor': 29.3},
    {'name': 'Jul/19', 'valor': 31.0}, {'name': 'Ago/19', 'valor': 29.5}, {'name': 'Set/19', 'valor': 30.2},
    {'name': 'Out/19', 'valor': 31.8}, {'name': 'Nov/19', 'valor': 28.7}, {'name': 'Dez/19', 'valor': 30.1},
    {'name': 'Jan/20', 'valor': 28.9}, {'name': 'Fev/20', 'valor': 26.4}, {'name': 'Mar/20', 'valor': 14.2},
    {'name': 'Abr/20', 'valor': 12.8}, {'name': 'Mai/20', 'valor': 15.6}, {'name': 'Jun/20', 'valor': 18.3},
    {'name': 'Jul/20', 'valor': 20.1}, {'name': 'Ago/20', 'valor': 22.4}, {'name': 'Set/20', 'valor': 19.8},
    {'name': 'Out/20', 'valor': 21.5}, {'name': 'Nov/20', 'valor': 24.2}, {'name': 'Dez/20', 'valor': 26.8},
    {'name': 'Jan/21', 'valor': 29.3}, {'name': 'Fev/21', 'valor': 31.7}, {'name': 'Mar/21', 'valor': 28.9},
    {'name': 'Abr/21', 'valor': 26.4}, {'name': 'Mai/21', 'valor': 24.8}, {'name': 'Jun/21', 'valor': 27.2},
    {'name': 'Jul/21', 'valor': 29.6}, {'name': 'Ago/21', 'valor': 25.3}, {'name': 'Set/21', 'valor': 23.1},
    {'name': 'Out/21', 'valor': 28.7}, {'name': 'Nov/21', 'valor': 32.4}, {'name': 'Dez/21', 'valor': 30.8}
]

def render_header():
    """Renderiza o cabeçalho da aplicação"""
    st.markdown('<h1 class="main-header">Estudos de Contabilidade Comportamental</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Aplicação para execução de exercícios e estudos de caso.</p>', unsafe_allow_html=True)
    st.markdown('<p class="professor-name">Prof. Dr. César Valentim</p>', unsafe_allow_html=True)

def render_navigation():
    """Renderiza a navegação entre blocos"""
    st.sidebar.title("📚 Navegação")
    
    blocks = {
        1: "🏠 Bloco 1 - Fundamentos e Ruído",
        2: "🧠 Bloco 2 - Prospect Theory",
        3: "📈 Bloco 3 - Análise de Mercado",
        4: "🧩 Bloco 4 - Síntese e Reflexão"
    }
    
    selected_block = st.sidebar.radio(
        "Selecione um bloco:",
        options=list(blocks.keys()),
        format_func=lambda x: blocks[x],
        index=st.session_state.current_block - 1
    )
    
    if selected_block != st.session_state.current_block:
        st.session_state.current_block = selected_block
        st.rerun()

def render_block1():
    """Renderiza o Bloco 1 - Fundamentos e Ruído"""
    st.markdown('<h2 class="block-header">📌 Bloco 1 – Fundamentos e Ruído</h2>', unsafe_allow_html=True)
    
    # Contexto
    st.markdown("""
    <div class="context-box">
        <strong style="color: #4F46E5;">Contexto:</strong> A bolha imobiliária nos EUA foi alimentada por crédito fácil, 
        securitização de hipotecas e confiança excessiva nos modelos de risco. Quando as inadimplências cresceram, 
        ativos lastreados em hipotecas perderam valor rapidamente, gerando crise global.
    </div>
    """, unsafe_allow_html=True)
    
    # Estudo de Caso
    st.markdown("""
    <div class="activity-box">
        <h3 style="color: #374151; margin-bottom: 0.5rem;">Estudo de Caso: Crise de 2008</h3>
        <p style="font-weight: bold; margin-bottom: 0.5rem;">Atividade: Discussão em Grupo</p>
        <ul>
            <li>Como noise traders e efeito manada alimentaram a bolha?</li>
            <li>Quais sinais de irracionalidade poderiam ter sido percebidos antes?</li>
            <li>Que lições a contabilidade deveria ter aprendido com essa crise?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Exercício Prático
    st.markdown("### Exercício Prático: Simulação de Mercado")
    
    if not st.session_state.block1_simulation_started:
        st.markdown("**Selecione seu grupo para começar a simulação:**")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("🏢 Grupo 1", key="group1", use_container_width=True):
                handle_group_selection('rational')
            
            if st.button("📊 Grupo 2", key="group2", use_container_width=True):
                handle_group_selection('noise')
    
    else:
        # Mostrar grupo selecionado
        if st.session_state.block1_revealed_group:
            st.info(st.session_state.block1_revealed_group)
        
        # Mostrar preço atual
        st.markdown(f"""
        <div class="price-display">
            <h3 style="margin: 0; color: #374151;">Preço Atual da Ação</h3>
            <h1 style="margin: 0; color: #4F46E5;">R$ {st.session_state.block1_current_price:.2f}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar informação da rodada
        st.markdown(f"""
        <div class="info-message">
            <strong>Rodada {st.session_state.block1_round}:</strong><br>
            <em>"{st.session_state.block1_info_message}"</em>
        </div>
        """, unsafe_allow_html=True)
        
        # Input para próximo preço (se simulação não terminou)
        if st.session_state.block1_round <= 10:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                next_price = st.number_input(
                    "Insira o novo preço:",
                    min_value=0.0,
                    value=st.session_state.block1_current_price,
                    step=0.01,
                    key="next_price_input"
                )
            
            with col2:
                if st.button("🔄 Próxima Rodada", use_container_width=True):
                    handle_next_round(next_price)
        
        else:
            st.markdown("""
            <div class="simulation-result">
                <h3 style="color: #059669; margin: 0;">Simulação Concluída! Hora da discussão.</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de preços
        if len(st.session_state.block1_prices_log) > 1:
            st.markdown("### Registro de Preços")
            
            df_prices = pd.DataFrame(st.session_state.block1_prices_log)
            
            fig = px.line(
                df_prices, 
                x='name', 
                y='valor',
                title='Evolução dos Preços da Ação',
                markers=True
            )
            fig.update_layout(
                xaxis_title="Rodada",
                yaxis_title="Preço (R$)",
                yaxis=dict(range=[90, 110])
            )
            fig.update_traces(line_color='#4F46E5', line_width=3)
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Reflexão
    st.markdown("""
    <div class="reflection-box">
        <h3 style="color: #374151; margin-bottom: 0.5rem;">Reflexão em Grupo</h3>
        <ul>
            <li>Como o ruído observado na simulação se conecta com decisões contábeis reais?</li>
            <li>Se você fosse auditor, como lidaria com relatórios baseados em premissas influenciadas pelo "efeito manada"?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def handle_group_selection(group):
    """Manipula a seleção de grupo no Bloco 1"""
    st.session_state.block1_selected_group = group
    st.session_state.block1_simulation_started = True
    st.session_state.block1_round = 1
    st.session_state.block1_current_price = 100.0
    st.session_state.block1_prices_log = [{'name': 'Rodada 0', 'valor': 100.0}]
    
    group_name = "1" if group == 'rational' else "2"
    st.session_state.block1_revealed_group = f"Você selecionou o Grupo {group_name}."
    
    info_array = RATIONAL_INFO if group == 'rational' else NOISE_INFO
    st.session_state.block1_info_message = info_array[0]
    
    st.rerun()

def handle_next_round(next_price):
    """Manipula a próxima rodada no Bloco 1"""
    if next_price <= 0:
        st.error('Por favor, insira um preço válido.')
        return
    
    # Atualizar log de preços
    st.session_state.block1_prices_log.append({
        'name': f'Rodada {st.session_state.block1_round}',
        'valor': float(next_price)
    })
    
    st.session_state.block1_current_price = float(next_price)
    st.session_state.block1_round += 1
    
    if st.session_state.block1_round <= 10:
        # Próxima mensagem
        info_array = RATIONAL_INFO if st.session_state.block1_selected_group == 'rational' else NOISE_INFO
        next_message = random.choice(info_array)
        st.session_state.block1_info_message = next_message
    else:
        # Simulação finalizada
        group_name = 'Investidores Racionais' if st.session_state.block1_selected_group == 'rational' else 'Noise Traders'
        st.session_state.block1_revealed_group = f'Simulação finalizada. Você era do grupo de {group_name}.'
        st.session_state.block1_info_message = 'Discuta os resultados com a sua turma.'
    
    st.rerun()

def render_block2():
    """Renderiza o Bloco 2 - Prospect Theory"""
    st.markdown('<h2 class="block-header">📌 Bloco 2 – Prospect Theory, Heurísticas e Vieses</h2>', unsafe_allow_html=True)
    
    # Contexto
    st.markdown("""
    <div class="context-box">
        <strong style="color: #4F46E5;">Contexto:</strong> A Enron manipulou demonstrações contábeis para ocultar dívidas, 
        usando veículos de propósito específico. Analistas ignoraram sinais de alerta, reforçando o viés de confirmação.
    </div>
    """, unsafe_allow_html=True)
    
    # Atividade
    st.markdown("""
    <div class="activity-box">
        <h3 style="color: #374151; margin-bottom: 0.5rem;">Atividade: Perguntas aos Grupos</h3>
        <ul>
            <li>Como heurísticas (representatividade, disponibilidade) influenciaram investidores e auditores?</li>
            <li>Que vieses específicos permitiram que o problema crescesse tanto?</li>
            <li>Como auditores poderiam ter mitigado esses vieses?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Exercício Prático
    st.markdown("### Exercício Prático: Questionário de Prospect Theory")
    
    with st.form("prospect_theory_form"):
        st.markdown("**Cenário 1: Ganhos**")
        st.markdown("Escolha entre as opções:")
        
        gains_choice = st.radio(
            "Cenário de Ganhos:",
            options=['A', 'B'],
            format_func=lambda x: {
                'A': 'Opção A: ganhar R$900 com certeza.',
                'B': 'Opção B: 90% de chance de ganhar R$1000, 10% de não ganhar nada.'
            }[x],
            key="gains_radio"
        )
        
        st.markdown("**Cenário 2: Perdas**")
        st.markdown("Escolha entre as opções:")
        
        losses_choice = st.radio(
            "Cenário de Perdas:",
            options=['C', 'D'],
            format_func=lambda x: {
                'C': 'Opção C: perder R$900 com certeza.',
                'D': 'Opção D: 90% de chance de perder R$1000, 10% de não perder nada.'
            }[x],
            key="losses_radio"
        )
        
        submitted = st.form_submit_button("Ver Resultados", use_container_width=True)
        
        if submitted:
            st.session_state.block2_gains_choice = gains_choice
            st.session_state.block2_losses_choice = losses_choice
            st.session_state.block2_show_result = True
    
    # Mostrar resultados
    if st.session_state.block2_show_result:
        st.markdown("""
        <div class="simulation-result">
            <h4 style="color: #059669; margin-bottom: 0.5rem;">Discussão dos Resultados:</h4>
            <p>A maioria das pessoas tende a escolher a Opção A (aversão ao risco em ganhos) e a Opção D 
            (propensão ao risco em perdas). Este resultado demonstra a <strong>Aversão à Perda</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Análise das escolhas do usuário
        user_pattern = ""
        if st.session_state.block2_gains_choice == 'A' and st.session_state.block2_losses_choice == 'D':
            user_pattern = "Suas escolhas seguem o padrão típico da Prospect Theory!"
        elif st.session_state.block2_gains_choice == 'B' and st.session_state.block2_losses_choice == 'C':
            user_pattern = "Suas escolhas são consistentes com a teoria da utilidade esperada."
        else:
            user_pattern = "Suas escolhas mostram um padrão misto interessante para discussão."
        
        st.info(f"**Suas escolhas:** Ganhos: {st.session_state.block2_gains_choice}, Perdas: {st.session_state.block2_losses_choice}. {user_pattern}")
    
    # Reflexão
    st.markdown("""
    <div class="reflection-box">
        <h3 style="color: #374151; margin-bottom: 0.5rem;">Reflexão em Grupo</h3>
        <ul>
            <li>Como a aversão à perda afeta decisões contábeis como impairment ou provisões?</li>
            <li>Vocês já observaram casos reais em que gestores evitaram reconhecer perdas óbvias?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def render_block3():
    """Renderiza o Bloco 3 - Análise de Mercado"""
    st.markdown('<h2 class="block-header">📌 Bloco 3 – Análise de Mercado e Vieses Cognitivos</h2>', unsafe_allow_html=True)
    
    # Contexto
    st.markdown("""
    <div class="context-box">
        <strong style="color: #4F46E5;">Contexto:</strong> Análise do comportamento de preços de ações da Petrobras 
        durante o período de 2019-2021, incluindo os impactos da pandemia de COVID-19 e volatilidade do mercado de petróleo.
    </div>
    """, unsafe_allow_html=True)
    
    # Gráfico da Petrobras
    st.markdown("### Cotações da Petrobras (2019-2021)")
    
    df_petro = pd.DataFrame(PETRO_DATA)
    
    fig = px.line(
        df_petro,
        x='name',
        y='valor',
        title='Evolução das Cotações da Petrobras',
        markers=True
    )
    fig.update_layout(
        xaxis_title="Período",
        yaxis_title="Preço (R$)",
        xaxis_tickangle=-45
    )
    fig.update_traces(line_color='#059669', line_width=3)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise interativa
    st.markdown("### Análise Interativa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Identifique os períodos:**")
        
        period_analysis = st.selectbox(
            "Selecione um período para análise:",
            options=[
                "Jan/19 - Dez/19: Período pré-pandemia",
                "Jan/20 - Jun/20: Início da pandemia",
                "Jul/20 - Dez/21: Recuperação e volatilidade"
            ]
        )
        
        if "pré-pandemia" in period_analysis:
            st.info("**Análise:** Período de relativa estabilidade com tendência de alta moderada.")
        elif "Início da pandemia" in period_analysis:
            st.warning("**Análise:** Queda abrupta devido ao pânico do mercado e colapso do preço do petróleo.")
        else:
            st.success("**Análise:** Recuperação gradual com alta volatilidade devido a incertezas macroeconômicas.")
    
    with col2:
        st.markdown("**Vieses Observados:**")
        
        bias_type = st.radio(
            "Que vieses podem ser identificados?",
            options=[
                "Efeito Manada",
                "Ancoragem",
                "Disponibilidade",
                "Excesso de Confiança"
            ]
        )
        
        bias_explanations = {
            "Efeito Manada": "Investidores seguindo movimentos de massa durante a queda de março/2020.",
            "Ancoragem": "Fixação em preços históricos altos, dificultando aceitação da nova realidade.",
            "Disponibilidade": "Supervalorização de notícias recentes sobre petróleo e pandemia.",
            "Excesso de Confiança": "Subestimação dos riscos durante períodos de alta."
        }
        
        st.info(f"**{bias_type}:** {bias_explanations[bias_type]}")
    
    # Atividade prática
    st.markdown("""
    <div class="activity-box">
        <h3 style="color: #374151; margin-bottom: 0.5rem;">Atividade Prática</h3>
        <p><strong>Cenário:</strong> Você é um analista em março de 2020. O preço da Petrobras caiu de R$28,9 para R$14,2.</p>
        <p><strong>Questão:</strong> Qual seria sua recomendação e que vieses você tentaria evitar?</p>
    </div>
    """, unsafe_allow_html=True)
    
    recommendation = st.text_area(
        "Sua análise e recomendação:",
        placeholder="Descreva sua análise considerando os vieses comportamentais...",
        height=100
    )
    
    if recommendation:
        st.success("Análise registrada! Discuta com o grupo as diferentes perspectivas.")
    
    # Reflexão
    st.markdown("""
    <div class="reflection-box">
        <h3 style="color: #374151; margin-bottom: 0.5rem;">Reflexão em Grupo</h3>
        <ul>
            <li>Como os vieses identificados afetam as decisões de investimento?</li>
            <li>Que ferramentas contábeis poderiam ajudar a mitigar esses vieses?</li>
            <li>Como a volatilidade extrema impacta a avaliação de ativos?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def render_block4():
    """Renderiza o Bloco 4 - Síntese e Reflexão"""
    st.markdown('<h2 class="block-header">📌 Bloco 4 – Síntese e Reflexão Final</h2>', unsafe_allow_html=True)
    
    # Resumo dos conceitos
    st.markdown("### Resumo dos Conceitos Abordados")
    
    concepts = {
        "Bloco 1": {
            "title": "Fundamentos e Ruído",
            "concepts": ["Noise Traders", "Efeito Manada", "Bolhas Especulativas", "Crise de 2008"]
        },
        "Bloco 2": {
            "title": "Prospect Theory",
            "concepts": ["Aversão à Perda", "Heurísticas", "Viés de Confirmação", "Caso Enron"]
        },
        "Bloco 3": {
            "title": "Análise de Mercado",
            "concepts": ["Ancoragem", "Disponibilidade", "Excesso de Confiança", "Volatilidade"]
        }
    }
    
    for block, data in concepts.items():
        with st.expander(f"{block}: {data['title']}"):
            for concept in data['concepts']:
                st.write(f"• {concept}")
    
    # Autoavaliação
    st.markdown("### Autoavaliação")
    
    st.markdown("**Avalie seu entendimento dos conceitos (1-5):**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        noise_traders = st.slider("Noise Traders e Efeito Manada", 1, 5, 3)
        prospect_theory = st.slider("Prospect Theory", 1, 5, 3)
    
    with col2:
        heuristics = st.slider("Heurísticas e Vieses", 1, 5, 3)
        practical_application = st.slider("Aplicação Prática", 1, 5, 3)
    
    # Gráfico de autoavaliação
    if st.button("Gerar Gráfico de Autoavaliação"):
        assessment_data = {
            'Conceito': ['Noise Traders', 'Prospect Theory', 'Heurísticas', 'Aplicação Prática'],
            'Nota': [noise_traders, prospect_theory, heuristics, practical_application]
        }
        
        fig = px.bar(
            assessment_data,
            x='Conceito',
            y='Nota',
            title='Sua Autoavaliação',
            color='Nota',
            color_continuous_scale='viridis'
        )
        fig.update_layout(yaxis=dict(range=[0, 5]))
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Plano de ação
    st.markdown("### Plano de Ação Pessoal")
    
    action_plan = st.text_area(
        "Como você aplicará esses conhecimentos na sua prática profissional?",
        placeholder="Descreva ações específicas que você pretende implementar...",
        height=150
    )
    
    if action_plan:
        st.success("Plano de ação registrado!")
    
    # Reflexão final
    st.markdown("""
    <div class="reflection-box">
        <h3 style="color: #374151; margin-bottom: 0.5rem;">Reflexão Final em Grupo</h3>
        <ul>
            <li>Que vieses foram mais evidentes ao longo do curso?</li>
            <li>Como vocês aplicarão esse conhecimento na prática contábil e de auditoria?</li>
            <li>Se pudessem criar um checklist anti-vieses, quais itens incluiriam?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Recursos adicionais
    st.markdown("### Recursos Adicionais")
    
    with st.expander("📚 Leituras Recomendadas"):
        st.markdown("""
        - **Kahneman, D.** - "Thinking, Fast and Slow"
        - **Thaler, R.** - "Nudge: Improving Decisions About Health, Wealth, and Happiness"
        - **Ariely, D.** - "Predictably Irrational"
        - **Shefrin, H.** - "Behavioral Corporate Finance"
        """)
    
    with st.expander("🔗 Links Úteis"):
        st.markdown("""
        - [Behavioral Economics Guide](https://www.behavioraleconomics.com/)
        - [CVM - Comissão de Valores Mobiliários](http://www.cvm.gov.br/)
        - [IASB - International Accounting Standards Board](https://www.ifrs.org/)
        """)

def main():
    """Função principal da aplicação"""
    init_session_state()
    render_header()
    render_navigation()
    
    # Renderizar o bloco atual
    if st.session_state.current_block == 1:
        render_block1()
    elif st.session_state.current_block == 2:
        render_block2()
    elif st.session_state.current_block == 3:
        render_block3()
    elif st.session_state.current_block == 4:
        render_block4()

if __name__ == "__main__":
    main()

