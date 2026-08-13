"""Configuração central do projeto.

Concentra caminhos de pastas e o *registro de fontes* usado por todas as etapas.
Ao adicionar uma nova fonte (Etapa 1), registre-a em ``FONTES`` seguindo o mesmo
formato — as demais etapas leem daqui, mantendo a integração.
"""
from __future__ import annotations

from pathlib import Path

# --- Caminhos base -----------------------------------------------------------
# src/config.py  ->  raiz do projeto = parent de src/
RAIZ = Path(__file__).resolve().parent.parent

DIR_DADOS = RAIZ / "dados"
DIR_BRUTOS = DIR_DADOS / "brutos"            # Etapa 2 (respostas cruas da API)
DIR_PROCESSADOS = DIR_DADOS / "processados"  # Etapa 3 (CSV tidy)
DIR_PUBLICADOS = RAIZ / "docs" / "dados"     # Etapa 5 (JSON consumido pelo front)


def garantir_pastas() -> None:
    """Cria as pastas de dados caso ainda não existam."""
    for pasta in (DIR_BRUTOS, DIR_PROCESSADOS, DIR_PUBLICADOS):
        pasta.mkdir(parents=True, exist_ok=True)


# --- Registro de fontes ------------------------------------------------------
# Cada fonte é identificada por um "slug" (chave) reutilizado em todas as etapas.
BCB_OLINDA_BASE = "https://olinda.bcb.gov.br/olinda/servico"
# API do SGS (Sistema Gerenciador de Séries Temporais): uma chamada por código de série.
BCB_SGS_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json"
RFB_SERIE_HISTORICA = (
    "https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos"
    "/receitadata/arrecadacao/serie-historica"
)

FONTES: dict[str, dict] = {
    "meios_pagamento_mensal": {
        "nome": "BCB — Estatísticas de Meios de Pagamento (mensal)",
        "descricao": (
            "Quantidade e valor de movimentação por AnoMes e forma de pagamento no Brasil."
        ),
        "url": (
            f"{BCB_OLINDA_BASE}/MPV_DadosAbertos/versao/v1/odata/"
            "MeiosdePagamentosMensalDA(AnoMes=@AnoMes)?@AnoMes=''&$format=json"
        ),
        # Formas de pagamento e o sufixo das colunas quantidade{X}/valor{X}.
        "formas": {
            "Pix": "Pix",
            "TED": "TED",
            "TEC": "TEC",
            "Cheque": "Cheque",
            "Boleto": "Boleto",
            "DOC": "DOC",
        },
        "unidades": {
            "quantidade": "milhares de transações",
            "valor": "R$ milhões",
        },
        "periodicidade": "mensal",
        "licenca": "Dados abertos — Banco Central do Brasil",
    },
    "arrecadacao_federal": {
        "nome": "RFB — Arrecadação das Receitas Federais (série histórica)",
        "descricao": (
            "Valor arrecadado mensal por tributo no Brasil, a preços correntes, "
            "publicado pela Receita Federal no portal ReceitaData."
        ),
        # Página de listagem: usada como fallback para descobrir os XLSX quando os
        # nomes de arquivo mudam de ano a ano (ex.: "1994 a 2025" -> "1994 a 2026").
        "url": f"{RFB_SERIE_HISTORICA}/",
        "arquivos": [
            {
                "nome": "arrecadacao-das-receitas-federais-1970-a-1993.xlsx",
                "url": f"{RFB_SERIE_HISTORICA}/arrecadacao-das-receitas-federais-1970-a-1993.xlsx",
                # Moedas diferentes por ano (Cr$, Cz$, NCz$, CR$) e a aba 1970-1985 é
                # anual: coletado para rastreabilidade, mas fora da série tratada.
                "tratar": False,
            },
            {
                "nome": "arrecadacao-das-receitas-federais-1994-a-2025.xlsx",
                "url": f"{RFB_SERIE_HISTORICA}/arrecadacao-das-receitas-federais-1994-a-2025.xlsx",
                "tratar": True,
            },
        ],
        # Etapa 2 também baixa o IPCA (SGS 433) para deflacionar na Etapa 3.
        "url_ipca": (
            "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
            "?formato=json&dataInicial=01/12/1993"
        ),
        # Rótulos amigáveis para as linhas do XLSX (chave = rótulo original, sem recuo).
        "rotulos": {
            "IMPOSTO SOBRE IMPORTAÇÃO": "Imposto de Importação",
            "IMPOSTO SOBRE EXPORTAÇÃO": "Imposto de Exportação",
            "I.P.I-TOTAL": "IPI",
            "IMPOSTO SOBRE A RENDA-TOTAL": "Imposto de Renda",
            "IOF - I. S/ OPERAÇÕES FINANCEIRAS": "IOF",
            "ITR - I. TERRITORIAL RURAL": "ITR",
            "COFINS - CONTRIB. P/ A SEGURIDADE SOCIAL": "COFINS",
            "CONTRIBUIÇÃO PARA O PIS/PASEP": "PIS/PASEP",
            "CSLL - CONTRIB. SOCIAL S/ LUCRO LÍQUIDO": "CSLL",
            "CIDE-COMBUSTÍVEIS": "CIDE-Combustíveis",
            "CONTRIBUIÇÃO PARA O FUNDAF": "FUNDAF",
            "PSS - CONTRIB. DO PLANO DE SEGURIDADE DO SERVIDOR": "PSS",
            "OUTRAS RECEITAS ADMINISTRADAS": "Outras receitas administradas",
            "RECEITA PREVIDENCIÁRIA [B]": "Receita previdenciária",
            "ADMINISTRADAS POR OUTROS ÓRGÃOS [D]": "Administradas por outros órgãos",
            "SUBTOTAL [A]": "Subtotal administradas (exceto previdenciária)",
            "ADMINISTRADAS PELA RFB [C]=[A]+[B]": "Administradas pela RFB",
            "TOTAL GERAL [E]=[C]+[D]": "Total geral",
        },
        # Linhas de nível 1 que somam exatamente o "TOTAL GERAL" (base das participações).
        "componentes_total": [
            "IMPOSTO SOBRE IMPORTAÇÃO",
            "IMPOSTO SOBRE EXPORTAÇÃO",
            "I.P.I-TOTAL",
            "IMPOSTO SOBRE A RENDA-TOTAL",
            "IOF - I. S/ OPERAÇÕES FINANCEIRAS",
            "ITR - I. TERRITORIAL RURAL",
            "COFINS - CONTRIB. P/ A SEGURIDADE SOCIAL",
            "CONTRIBUIÇÃO PARA O PIS/PASEP",
            "CSLL - CONTRIB. SOCIAL S/ LUCRO LÍQUIDO",
            "CIDE-COMBUSTÍVEIS",
            "CONTRIBUIÇÃO PARA O FUNDAF",
            "PSS - CONTRIB. DO PLANO DE SEGURIDADE DO SERVIDOR",
            "OUTRAS RECEITAS ADMINISTRADAS",
            "RECEITA PREVIDENCIÁRIA [B]",
            "ADMINISTRADAS POR OUTROS ÓRGÃOS [D]",
        ],
        # Linhas somatórias do próprio XLSX (não entram em participação/ranking).
        "agregados": [
            "SUBTOTAL [A]",
            "ADMINISTRADAS PELA RFB [C]=[A]+[B]",
            "TOTAL GERAL [E]=[C]+[D]",
        ],
        "linha_total": "TOTAL GERAL [E]=[C]+[D]",
        "unidades": {
            "valor": "R$ milhões (correntes)",
            "valor_constante": "R$ milhões (constantes, IPCA do último mês)",
        },
        "periodicidade": "mensal",
        "licenca": "CC-BY-ND 3.0 — Receita Federal do Brasil",
    },
    "credito_modalidade": {
        "nome": "BCB — Crédito por modalidade (SGS)",
        "descricao": (
            "Saldo da carteira, taxa média de juros e spread das operações de crédito "
            "do Sistema Financeiro Nacional, por modalidade e por segmento (PF/PJ)."
        ),
        # Uma chamada por código de série (o SGS não tem consulta multi-série).
        "url": BCB_SGS_URL,
        # Dados nacionais: o SGS só publica recorte por UF para crédito PJ por *porte*
        # (MEI/microempresa/pequeno porte), não por modalidade — por isso não há coluna `uf`.
        "url_portal": "https://dadosabertos.bcb.gov.br/dataset/20539-saldo-da-carteira-de-credito---total",
        # Séries de juros/spread por modalidade começam em mar/2011; o saldo vem de 2007,
        # mas cortamos em 2011-03 para que todas as medidas cubram o mesmo período.
        "data_inicial": "01/03/2011",
        "segmentos": {
            "Total": "Total (PF + PJ)",
            "PF": "Pessoas físicas",
            "PJ": "Pessoas jurídicas",
        },
        # segmento -> modalidade -> medida -> código da série no SGS.
        # "Total" é a linha agregada do segmento (única com spread publicado).
        "series": {
            "Total": {
                "Total": {"saldo": 20539, "taxa": 20714, "spread": 20783},
            },
            "PF": {
                "Total": {"saldo": 20541, "taxa": 20716, "spread": 20785},
                "Cheque especial": {"saldo": 20573, "taxa": 20741},
                "Crédito pessoal não consignado": {"saldo": 20574, "taxa": 20742},
                "Crédito pessoal consignado": {"saldo": 20579, "taxa": 20747},
                "Aquisição de veículos": {"saldo": 20581, "taxa": 20749},
                "Cartão de crédito rotativo": {"saldo": 20587, "taxa": 22022},
                "Cartão de crédito parcelado": {"saldo": 20588, "taxa": 22023},
                "Desconto de cheques": {"saldo": 20591, "taxa": 20755},
                "Crédito rural": {"saldo": 20609, "taxa": 20771},
                "Financiamento imobiliário": {"saldo": 20612, "taxa": 20774},
                "Microcrédito": {"saldo": 20620, "taxa": 20782},
            },
            "PJ": {
                "Total": {"saldo": 20540, "taxa": 20715, "spread": 20784},
                "Desconto de duplicatas e recebíveis": {"saldo": 20544, "taxa": 20719},
                "Capital de giro": {"saldo": 20550, "taxa": 20725},
                "Conta garantida": {"saldo": 20551, "taxa": 20726},
                "Cheque especial": {"saldo": 20552, "taxa": 20727},
                "Aquisição de veículos": {"saldo": 20553, "taxa": 20728},
                "Vendor": {"saldo": 20559, "taxa": 20734},
                "Compror": {"saldo": 20560, "taxa": 20735},
                "Cartão de crédito rotativo": {"saldo": 20561, "taxa": 22019},
                "Cartão de crédito parcelado": {"saldo": 20562, "taxa": 22020},
                "Adiantamento sobre contratos de câmbio (ACC)": {"saldo": 20565, "taxa": 20736},
                "Financiamento a importações": {"saldo": 20566, "taxa": 20737},
                "Financiamento a exportações": {"saldo": 20567, "taxa": 20738},
                "Repasse externo": {"saldo": 20568, "taxa": 20739},
                "Crédito rural": {"saldo": 20597, "taxa": 20760},
                "Financiamento imobiliário": {"saldo": 20600, "taxa": 20763},
                "Financiamento com recursos do BNDES": {"saldo": 20604, "taxa": 20767},
            },
        },
        "unidades": {
            "saldo": "R$ milhões",
            "taxa_juros_aa": "% ao ano",
            "spread_pp": "p.p. ao ano",
        },
        "periodicidade": "mensal",
        "licenca": "Open Database License (ODbL) — Banco Central do Brasil",
    },
}


def series_sgs(cfg: dict) -> list[tuple[str, str, str, int]]:
    """Achata ``cfg['series']`` em ``(segmento, modalidade, medida, codigo)``.

    Usado pela coleta (uma requisição por tupla) e pela análise (para saber quais
    combinações existem sem reabrir o dicionário aninhado).
    """
    return [
        (segmento, modalidade, medida, codigo)
        for segmento, modalidades in cfg["series"].items()
        for modalidade, medidas in modalidades.items()
        for medida, codigo in medidas.items()
    ]


def fonte(slug: str) -> dict:
    """Retorna a configuração de uma fonte pelo slug, com erro claro se ausente."""
    if slug not in FONTES:
        disponiveis = ", ".join(FONTES) or "(nenhuma)"
        raise KeyError(f"Fonte '{slug}' não registrada. Disponíveis: {disponiveis}")
    return FONTES[slug]
