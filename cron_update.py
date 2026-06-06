import os
import requests
import sys

# Recolha invisível e rigorosa das chaves guardadas no cofre do GitHub
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ADMIN2_NEW_PASS = os.getenv("ADMIN2_PASSWORD")

if not all([SUPABASE_URL, SUPABASE_KEY, ADMIN2_NEW_PASS]):
    print("Erro de Infraestrutura: Chaves de segurança ausentes no ambiente do GitHub.")
    sys.exit(1)

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def executar_automacao_diaria():
    print("A iniciar pipeline de sincronização diária...")
    
    # --- ETAPA 1: ATUALIZAÇÃO SEGURA DA PALAVRA-PASSE VIA REST API ---
    # Alvo exato no registo do utilizador 'admin2'
    url_usuario = f"{SUPABASE_URL}/rest/v1/tb_usuarios?username=eq.admin2"
    payload_usuario = {"password_plana": ADMIN2_NEW_PASS}
    
    try:
        res_user = requests.patch(url_usuario, headers=HEADERS, json=payload_usuario)
        if res_user.status_code in [200, 204]:
            print("Segurança: Credenciais do utilizador admin2 sincronizadas em segundo plano.")
        else:
            print(f"Aviso de Autenticação: Falha ao mapear utilizador: {res_user.text}")
    except Exception as e:
        print(f"Falha na comunicação de segurança: {str(e)}")

    # --- ETAPA 2: MANUTENÇÃO DIÁRIA DE ROTINA DO FLUXO DE CAIXA ---
    url_caixa = f"{SUPABASE_URL}/rest/v1/tb_fluxo_caixa_semanal"
    payload_caixa = {
        "entradas_reais": 0.0,
        "saidas_reais": 0.0
    }
    
    try:
        res_caixa = requests.post(url_caixa, headers=HEADERS, json=payload_caixa)
        if res_caixa.status_code in [200, 201]:
            print("Sucesso: Ping de integridade diária registado no fluxo de caixa.")
        else:
            print(f"Falha ao registar rotina de caixa: {res_caixa.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Erro crítico no processamento de dados: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    executar_automacao_diaria()
