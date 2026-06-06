import streamlit as str
import requests
import json
import pandas as pd

# CONFIGURAÇÃO DA INTERFACE - PADRÃO CRU DE PRIMEIRA LIGA
str.set_page_config(page_title="Operação Chapa Quente | OCQ", page_icon="📈", layout="wide")

# =====================================================================
# GOVERNANÇA DE CREDENCIAIS: LEITURA SEGURA VIA STREAMLIT SECRETS
# =====================================================================
try:
    SUPABASE_URL = str.secrets["SUPABASE_URL"]
    SUPABASE_KEY = str.secrets["SUPABASE_KEY"]
    GROQ_API_KEY = str.secrets["GROQ_API_KEY"]
except KeyError as e:
    str.error(f"Erro de Infraestrutura: A variável obrigatória {e} não foi configurada nos Secrets do Streamlit.")
    str.stop()

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# FUNÇÕES AUXILIARES DE CONEXÃO ESTRUTURADA
def supabase_request(endpoint, method="GET", data=None):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=HEADERS, json=data)
        return response.json()
    except Exception as e:
        return []

def chamar_lasaro_ia(prompt_sistema, prompt_usuario):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.2
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.json()['choices'][0]['message']['content']
    except:
        return "Erro ao contactar o cérebro estratégico do Lásaro IA. Verifica a tua chave da API Groq nos Secrets."

# CONTROLO DE SESSÃO E AUTENTICAÇÃO
if 'autenticado' not in str.session_state:
    str.session_state['autenticado'] = False

if not str.session_state['autenticado']:
    str.title("🔒 Operação Chapa Quente - Controlo de Acesso")
    str.subheader("Digital Solutions & Consulting IT")
    
    campo_user = str.text_input("Utilizador Comercial")
    campo_pass = str.text_input("Chave de Segurança (Password)", type="password")
    
    if str.button("Autenticar Operação"):
        # Consulta direta à tabela de segurança implementada no Supabase
        usuarios = supabase_request(f"tb_usuarios?username=eq.{campo_user}", "GET")
        if usuarios and usuarios[0]['password_plana'] == campo_pass:
            str.session_state['autenticado'] = True
            str.session_state['user'] = campo_user
            str.rerun()
        else:
            str.error("Credenciais inválidas. O caixa não perdoa erros de digitação.")
    str.stop()

# --- LEITURA GLOBAL DE VARIÁVEIS FINANCEIRAS DO SUPABASE ---
config_data = supabase_request("tb_config_empresa?select=*", "GET")
custo_fixo = float(config_data[0]['custo_fixo_mensal']) if config_data else 2000.0
margem_alvo = float(config_data[0]['margem_alvo_minima']) if config_data else 40.0

caixa_data = supabase_request("tb_fluxo_caixa_semanal?order=data_registo.desc&limit=1", "GET")
saldo_caixa = float(caixa_data[0]['saldo_consolidado']) if caixa_data else 0.0

# PROCESSAMENTO MATEMÁTICO DO RUNWAY REAL
dias_runway = int((saldo_caixa / custo_fixo) * 30) if custo_fixo > 0 and saldo_caixa > 0 else 0

# --- INTERFACE PRINCIPAL DO OPERADOR ---
str.title("📈 OPERAÇÃO CHAPA QUENTE (OCQ)")
str.caption(f"Painel Estratégico da **Digital Solutions & Consulting IT** | Operador Ativo: {str.session_state['user']}")

# LINHA PRINCIPAL: CARTÕES CRUS DE DESEMPENHO FINANCEIRO
c1, c2, c3, c4 = str.columns(4)
c1.metric(label="SALDO CONSOLIDADO EM CAIXA", value=f"{saldo_caixa:,.2f} €")
c2.metric(label="CUSTO FIXO OPERACIONAL MENSAL", value=f"{custo_fixo:,.2f} €")

if dias_runway < 45:
    c3.metric(label="RUNWAY (DIAS DE VIDA)", value=f"{dias_runway} DIAS", delta="- CRÍTICO", delta_color="inverse")
else:
    c3.metric(label="RUNWAY (DIAS DE VIDA)", value=f"{dias_runway} DIAS", delta="ESTÁVEL")

c4.metric(label="MARGEM ALVO MÍNIMA", value=f"{margem_alvo}%")

str.markdown("---")

# NAVEGAÇÃO ENTRE OS MÓDULOS CORE VALIDADOS
opcao_modulo = str.sidebar.radio("Navegação Estratégica", [
    "Módulo I: O Termómetro do Lásaro",
    "Módulo II: Auditoria & Central de Conceitos",
    "Módulo III: Engenharia de Projetos (Precificação)",
    "Módulo IV: Sala de Mentoria (Lásaro IA)"
])

# ================= MÓDULO I: INPUTS FINANCEIROS =================
if opcao_modulo == "Módulo I: O Termómetro do Lásaro":
    str.header("📊 O Termómetro do Lásaro: Injeção de Variáveis Financeiras")
    
    with str.form("form_financeiro"):
        col_f1, col_f2, col_f3 = str.columns(3)
        novo_saldo = col_f1.number_input("Saldo Bancário Total Consolidado (€)", value=saldo_caixa)
        novas_entradas = col_f2.number_input("Entradas Reais da Semana (€)", value=0.0)
        novas_saidas = col_f3.number_input("Saídas Reais da Semana (€)", value=0.0)
        
        if str.form_submit_state("Registar Fecho de Caixa"):
            payload_caixa = {
                "saldo_consolidado": novo_saldo,
                "entradas_reais": novas_entradas,
                "saidas_reais": novas_saidas
            }
            supabase_request("tb_fluxo_caixa_semanal", "POST", payload_caixa)
            str.success("Métricas de caixa integradas na base de dados com sucesso.")
            str.rerun()

    str.subheader("📂 Histórico de Contratos Ativos e Margem Residual")
    projetos = supabase_request("tb_projetos_contratos?select=*", "GET")
    if projetos:
        df_proj = pd.DataFrame(projetos)
        df_proj['Margem Bruta %'] = ((df_proj['valor_total'] - df_proj['custo_variavel_alocado']) / df_proj['valor_total']) * 100
        str.dataframe(df_proj[['nome_cliente', 'valor_total', 'setup_fee_pago', 'custo_variavel_alocado', 'Margem Bruta %', 'status_milestone']], use_container_width=True)
    else:
        str.info("Nenhum contrato ativo registado no Supabase.")

# ================= MÓDULO II: AUDITORIA E CONCEITOS =================
elif opcao_modulo == "Módulo II: Auditoria & Central de Conceitos":
    str.header("🧠 Auditoria Estratégica Textual & Glossário Dinâmico")
    
    col_perguntas, col_glossario = str.columns([3, 2])
    
    with col_perguntas:
        str.subheader("📋 Responde às Perguntas que o Diabo Nem Lembra")
        perguntas_bd = supabase_request("tb_auditoria_perguntas?select=*", "GET")
        
        if perguntas_bd:
            for p in perguntas_bd:
                str.markdown(f"**Bloco: {p['bloco']}**")
                nova_resposta = str.text_area(label=p['pergunta_texto'], value=p['resposta_texto_fundador'], key=f"p_{p['chave_pergunta']}")
                
                if str.button(f"Atualizar Diagnóstico: {p['chave_pergunta']}", key=f"btn_{p['chave_pergunta']}"):
                    supabase_request(f"tb_auditoria_perguntas?id=eq.{p['id']}", "PATCH", {"resposta_texto_fundador": nova_resposta})
                    str.success("Resposta guardada no histórico auditável.")
                    str.rerun()
                str.markdown("---")

    with col_glossario:
        str.subheader("📖 Central de Conceitos em Tempo Real")
        termo_selecionado = str.selectbox("Selecione um indicador para auditar o conceito técnico:", 
                                         ["Margem de Contribuição", "Runway (Tempo de Sobrevivência)", "Ciclo Financeiro", "Valuation"])
        
        # PROMPT DE CONTEXTO REAL DA EMPRESA ENVIADO PARA A IA
        prompt_sistema_glossario = (
            "Tu és o Lásaro do Carmo Jr. Explica o conceito macroeconómico solicitado de forma assertiva, "
            "crua, sem rodeios e usando estritamente os dados reais da empresa fornecidos pelo utilizador. "
            "Mostra as consequências reais daqueles números no negócio."
        )
        
        dados_contexto = f"Custo Fixo: {custo_fixo}€, Saldo de Caixa Atual: {saldo_caixa}€, Dias de Runway Disponíveis: {dias_runway} dias."
        
        if str.button("Explicar Conceito Aplicado à Minha Realidade"):
            resposta_ia = chamar_lasaro_ia(prompt_sistema_glossario, f"Explique o termo: '{termo_selecionado}' com base nestes dados reais da empresa: {dados_contexto}")
            str.info(resposta_ia)

# ================= MÓDULO III: ENGENHARIA DE PROJETOS =================
elif opcao_modulo == "Módulo III: Engenharia de Projetos (Precificação)":
    str.header("📐 Simulador de Engenharia Financeira e Propostas B2B")
    
    col_p1, col_p2 = str.columns(2)
    
    with col_p1:
        str.subheader("📥 Inputs Operacionais do Contrato")
        nome_cli = str.text_input("Nome do Cliente Prospetado")
        poupanca_cliente = str.number_input("Poupança Mensal que a tua Automação gera para o Cliente (€)", value=1000.0)
        custo_desenv = str.number_input("Custo Total Estimado de Engenharia (Horas freelancers + Infraestrutura) (€)", value=500.0)
        
    with col_p2:
        str.subheader("⚖️ Precificação Inteligente Baseada em Valor (ROI)")
        # Lógica matemática: preço mínimo garante 50% de margem, preço sugerido captura 3 meses de ROI gerado
        preco_minimo = custo_desenv / (1 - (margem_alvo/100))
        preco_sugerido = max(preco_minimo, poupanca_cliente * 3)
        setup_obrigatorio = preco_sugerido * 0.40
        
        str.warning(f"**PREÇO MÍNIMO PARA MANTER A MARGEM ALVO:** {preco_minimo:,.2f} €")
        str.success(f"**PREÇO SUGERIDO (VALOR ENTREGUE/ROI):** {preco_sugerido:,.2f} €")
        str.info(f"**SETUP FEE OBRIGATÓRIO (40% ENTRADA):** {setup_obrigatorio:,.2f} €")
        
        if str.button("Gravar Proposta Ganha no Supabase"):
            payload_projeto = {
                "nome_cliente": nome_cli,
                "valor_total": preco_sugerido,
                "setup_fee_pago": setup_obrigatorio,
                "custo_variavel_alocado": custo_desenv,
                "status_milestone": "Contrato Assinado"
            }
            supabase_request("tb_projetos_contratos", "POST", payload_projeto)
            str.success("Contrato integrado no portfólio de alta performance.")

# ================= MÓDULO IV: MENTORIA VIRTUAL =================
elif opcao_modulo == "Módulo IV: Sala de Mentoria (Lásaro IA)":
    str.header("🤖 Sala de Mentoria Virtual com o Cérebro do Lásaro do Carmo Jr.")
    str.caption("A IA tem visibilidade completa sobre o teu caixa, custos e o teu nível de respostas escritas.")
    
    perguntas_resumo = supabase_request("tb_auditoria_perguntas?select=pergunta_texto,resposta_texto_fundador", "GET")
    projetos_resumo = supabase_request("tb_projetos_contratos?select=nome_cliente,valor_total,custo_variavel_alocado", "GET")
    
    PROMPT_SISTEMA_LASARO = (
        "Tu és o Lásaro do Carmo Jr., mentor de negócios veterano, ex-CEO da Jequiti e Hinode. "
        "O teu estilo de comunicação é direto ao ponto, realista, firme, focado no lucro, caixa e "
        "geração de resultado real na última linha. Tu detestas métricas de vaidade e desculpas corporativas. "
        "Analisa os dados financeiros e as respostas textuais fornecidas pelo utilizador e responde sempre como o Lásaro real faria "
        "numa sessão de mentoria à porta fechada. Cobra eficiência operacional, processes e corte de custos."
    )
    
    CONTEXTO_EMPRESA_COMPLETO = {
        "financeiro_atual": {
            "saldo_caixa": saldo_caixa,
            "custo_fixo_mensal": custo_fixo,
            "dias_runway": dias_runway
        },
        "auditoria_respostas_dono": perguntas_resumo,
        "contratos_atuais": projetos_resumo
    }
    
    pergunta_usuario = str.text_input("O que queres discutir hoje sobre a saúde financeira do teu negócio?")
    
    if str.button("Enfrentar a Realidade (Chamar Lásaro)"):
        if pergunta_usuario:
            prompt_final = f"CONTEXTO REAL DA EMPRESA: {json.dumps(CONTEXTO_EMPRESA_COMPLETO)} \n\n PERGUNTA DO EMPRESÁRIO: {pergunta_usuario}"
            with str.spinner("O Lásaro está a analisar os teus números..."):
                resposta_lasaro = chamar_lasaro_ia(PROMPT_SISTEMA_LASARO, prompt_final)
                str.chat_message("assistant").write(resposta_lasaro)
