"""Orquestrador do pipeline — executa as Etapas 2 → 5 para uma fonte.

Uso:
    python run_pipeline.py                      # roda a fonte padrão
    python run_pipeline.py meios_pagamento_mensal
    python run_pipeline.py --sem-coleta         # reusa o bruto já baixado

Cada nova fonte deve registrar aqui seus módulos de coleta/tratamento/publicação
em ``PIPELINES``, mantendo o mesmo contrato entre etapas (ver CONTEXTO.md, seção 7).
"""
from __future__ import annotations

import argparse
import importlib

from src import config

# Mapeia slug -> módulos de cada etapa (todos expõem funções coletar/tratar/publicar).
PIPELINES = {
    "meios_pagamento_mensal": {
        "coleta": "src.coleta.meios_pagamento",
        "tratamento": "src.tratamento.meios_pagamento",
        "publicacao": "src.publicacao.meios_pagamento",
    },
}


def rodar(slug: str, sem_coleta: bool = False) -> None:
    if slug not in PIPELINES:
        raise SystemExit(f"Sem pipeline para '{slug}'. Disponíveis: {', '.join(PIPELINES)}")
    etapas = PIPELINES[slug]
    print(f"=== Pipeline: {config.fonte(slug)['nome']} ===")

    if sem_coleta:
        print("[pipeline] Etapa 2 (coleta) pulada — reusando bruto existente.")
    else:
        importlib.import_module(etapas["coleta"]).coletar(slug)

    importlib.import_module(etapas["tratamento"]).tratar(slug)
    importlib.import_module(etapas["publicacao"]).publicar(slug)
    print("=== Pipeline concluído com sucesso ===")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline de dados financeiros abertos.")
    parser.add_argument("slug", nargs="?", default="meios_pagamento_mensal",
                        help="Slug da fonte (ver src/config.py).")
    parser.add_argument("--sem-coleta", action="store_true",
                        help="Não consulta a API; reusa o bruto já salvo.")
    args = parser.parse_args()
    rodar(args.slug, sem_coleta=args.sem_coleta)


if __name__ == "__main__":
    main()
