import os
import requests
import sys

# Recolha rigorosa e secreta de todas as variáveis de ambiente
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

def atualizar_credenciais_em_seguranca():
    # Alvo na tabela de utilizadores apontando especificamente para o admin2
    url = f"{SUPABASE_URL}/rest/v1/tb_usuarios?username=eq.admin2"
    
    # A password viaja encriptada no corpo da requisição HTTPS, sem nunca tocar no código
    payload = {
        "password_plana": ADMIN2_NEW_PASS
    }
    
    try:
        response = requests.patch(url, headers=HEADERS, json=payload)
        if response.status_code in [200, 204]:
            print("Segurança: Password do admin2 atualizada com sucesso via Secret Pipeline.")
        else:
            print(f"Erro ao atualizar credenciais: {response.text}")
    except Exception as e:
        print(f"Erro crítico no pipeline de segurança: {str(e)}")

if __name__ == "__main__":
    atualizar_credenciais_em_seguranca()
