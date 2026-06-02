import requests
import pandas as pd
from datetime import datetime
from time import perf_counter
from colorama import Fore, init
import re

init(autoreset=True)

# =====================================================
# CONFIGURAÇÕES
# =====================================================

BASE_URL = "https://webservice.codevasf.gov.br"

session = requests.Session()
session.headers.update({
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://legado-site.codevasf.gov.br",
    "Referer": "https://legado-site.codevasf.gov.br/",
    "User-Agent": "Mozilla/5.0"
})

# =====================================================
# FUNÇÕES
# =====================================================

ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

def limpar_texto(valor):
    if isinstance(valor, str):
        return ILLEGAL_CHARACTERS_RE.sub("", valor)
    return valor

def solicitar_ano():
    ano_atual = datetime.now().year

    while True:
        try:
            ano = int(input(
                f"\nInforme o exercício {Fore.LIGHTBLUE_EX}(2010 até {ano_atual}){Fore.GREEN}: "
            ))

            if 2010 <= ano <= ano_atual:
                print(f"\n{Fore.YELLOW}Ano selecionado: {Fore.WHITE}{ano}")
                return str(ano)

            print(f"{Fore.RED}Ano inválido!")

        except ValueError:
            print(f"{Fore.RED}Digite apenas números.")


def get_json(url, tentativas=3):
    ultimo_erro = None
    for tentativa in range(tentativas):
        try:
            response = session.get(url, timeout=60)
            response.raise_for_status()
            return response.json()

        except Exception as erro:
            ultimo_erro = erro
            print(f"{Fore.YELLOW}Tentativa {tentativa+1}/{tentativas} falhou")
    raise ultimo_erro

def buscar_contratos(ano):
    dados = get_json(
        f"{BASE_URL}/sigec/portal-plone/contratos-lista/exercicio/{ano}"
    )
    return dados.get("data", [])


def buscar_detalhes(token):
    data = get_json(
        f"{BASE_URL}/sigec/portal-plone/contrato-get/info/C/id/{token}"
    ).get("data")

    return data if isinstance(data, dict) else None


def buscar_anexos(token):
    data = get_json(
        f"{BASE_URL}/sigec/portal-plone/contrato-get/info/A/id/{token}"
    ).get("data")

    return data.get("anexos", []) if isinstance(data, dict) else []


# =====================================================
# EXECUÇÃO
# =====================================================

inicio = perf_counter()

ano = solicitar_ano()

print(f"\n{Fore.CYAN}Buscando contratos...")
contratos = buscar_contratos(ano)

total = len(contratos)

print(f"{Fore.GREEN}{total:,} contratos encontrados.")

# =====================================================
# ARMAZENAMENTO
# =====================================================

contratos_lista = []
entidades_lista = []
empenhos_lista = []
anexos_lista = []
erros_lista = []

# =====================================================
# PROCESSAMENTO
# =====================================================

for indice, contrato in enumerate(contratos[:100], start=1):

    token = contrato["id"]
    numero = contrato["numero"]

    try:

        detalhe = buscar_detalhes(token)

        if not detalhe:
            erros_lista.append({
                "numero_contrato": numero,
                "token_contrato": token,
                "erro": "Detalhe vazio"
            })
            continue

        anexos = buscar_anexos(token)

        entidades = detalhe.get("entidades", [])
        empenhos = detalhe.get("empenhos", [])

        contratos_lista.append({
            "token_contrato": token,
            "id_interno": detalhe.get("id"),
            "numero": detalhe.get("numero"),
            "tipo": detalhe.get("tipo"),
            "situacao": detalhe.get("situacao"),
            "data_inicio": detalhe.get("dtInicio"),
            "data_termino": detalhe.get("dtTermino"),
            "data_publicacao": detalhe.get("dtPublicacao"),
            "data_celebracao": detalhe.get("dtCelebracao"),
            "valor_total": detalhe.get("vrTotal"),
            "objeto": detalhe.get("objeto"),
            "qtd_entidades": len(entidades),
            "qtd_empenhos": len(empenhos),
            "qtd_anexos": len(anexos)
        })

        for entidade in entidades:
            entidades_lista.append({
                "numero_contrato": numero,
                "contratado_id": entidade.get("contratadoId"),
                "cnpj": entidade.get("contratadoCodigo"),
                "nome": entidade.get("contratadoNome"),
                "vinculo": entidade.get("vinculo")
            })

        for empenho in empenhos:
            empenhos_lista.append({
                "numero_contrato": numero,
                "gestora": empenho.get("empenhoGestora"),
                "gestao": empenho.get("empenhoGestao"),
                "exercicio": empenho.get("empenhoExercicio"),
                "numero_empenho": empenho.get("empenhoNumero"),
                "valor_empenhado": empenho.get("empenhoValorEmpenhado"),
                "descricao": empenho.get("empenhoObservacao"),
                "link_transparencia": empenho.get("empenhoLinkTransparencia")
            })

        for anexo in anexos:
            anexos_lista.append({
                "numero_contrato": numero,
                "token_anexo": anexo.get("id"),
                "tipo": anexo.get("tipo"),
                "tipo_descricao": anexo.get("tipoDescricao"),
                "termo": anexo.get("termo"),
                "termo_descricao": anexo.get("termoDescricao"),
                "titulo": anexo.get("titulo"),
                "descricao": anexo.get("descricao"),
                "nome_arquivo": anexo.get("nome")
            })

        if indice % 50 == 0:
            print(
                f"{Fore.CYAN}[{indice:,}/{total:,}] "
                f"Contratos:{len(contratos_lista):,} | "
                f"Entidades:{len(entidades_lista):,} | "
                f"Empenhos:{len(empenhos_lista):,} | "
                f"Anexos:{len(anexos_lista):,}"
            )

    except Exception as erro:

        erros_lista.append({
            "numero_contrato": numero,
            "token_contrato": token,
            "erro": str(erro)
        })

        print(
            f"{Fore.RED}[ERRO] {numero} -> {erro}"
        )

# =====================================================
# DATAFRAMES
# =====================================================

df_contratos = pd.DataFrame(contratos_lista).map(limpar_texto)
df_entidades = pd.DataFrame(entidades_lista).map(limpar_texto)
df_empenhos = pd.DataFrame(empenhos_lista).map(limpar_texto)
df_anexos = pd.DataFrame(anexos_lista).map(limpar_texto)
df_erros = pd.DataFrame(erros_lista).map(limpar_texto)

# =====================================================
# EXPORTAÇÃO
# =====================================================

arquivo_saida = f"Contratos_CODEVASF_{ano}.xlsx"

print(f"\n{Fore.CYAN}Gerando Excel...")

with pd.ExcelWriter(arquivo_saida, engine="openpyxl") as writer:
    df_contratos.to_excel(writer, "Contratos", index=False)
    df_entidades.to_excel(writer, "Entidades", index=False)
    df_empenhos.to_excel(writer, "Empenhos", index=False)
    df_anexos.to_excel(writer, "Anexos", index=False)
    df_erros.to_excel(writer, "Erros", index=False)

# =====================================================
# RESUMO
# =====================================================

fim = perf_counter()

print(f"\n{Fore.GREEN}Coleta concluída!")
print(f"{Fore.YELLOW}Contratos: {len(df_contratos):,}")
print(f"{Fore.YELLOW}Entidades: {len(df_entidades):,}")
print(f"{Fore.YELLOW}Empenhos: {len(df_empenhos):,}")
print(f"{Fore.YELLOW}Anexos: {len(df_anexos):,}")
print(f"{Fore.RED}Erros: {len(df_erros):,}")
print(f"{Fore.CYAN}Tempo total: {round(fim - inicio, 2)} segundos")
print(f"{Fore.GREEN}Arquivo salvo: {arquivo_saida}")
