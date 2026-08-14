# Dados Financeiros Abertos — Brasil (repositório arquivado)

> ⚠️ **Este repositório foi dividido e está arquivado.** Ele reunia três fontes de dados no
> mesmo lugar; desde ago/2026 cada fonte tem seu **próprio repositório**, autocontido, com
> pipeline e painel independentes. Nada aqui se perdeu — tudo foi migrado.
>
> Este repositório permanece somente como **registro histórico** (histórico de commits
> anterior à divisão). Não receba mudanças novas aqui.

## Para onde foi cada coisa

| O que era | Onde está agora | Painel |
|-----------|-----------------|--------|
| Visão global, catálogos, convenções | [`controle-global`](https://github.com/gfvdata-web/controle-global) | — |
| BCB — Meios de Pagamento (mensal) | [`fonte-meios-pagamento`](https://github.com/gfvdata-web/fonte-meios-pagamento) | [painel](https://gfvdata-web.github.io/fonte-meios-pagamento/) |
| RFB — Arrecadação das Receitas Federais | [`fonte-arrecadacao-federal`](https://github.com/gfvdata-web/fonte-arrecadacao-federal) | [painel](https://gfvdata-web.github.io/fonte-arrecadacao-federal/) |
| BCB — Crédito por modalidade (SGS) | [`fonte-credito-modalidade`](https://github.com/gfvdata-web/fonte-credito-modalidade) | [painel](https://gfvdata-web.github.io/fonte-credito-modalidade/) |

O mapa detalhado de migração (arquivo a arquivo) está em
[`controle-global/GUIA-REPOSITORIOS.md`](https://github.com/gfvdata-web/controle-global/blob/main/GUIA-REPOSITORIOS.md).

---

## Conteúdo original (histórico)

Exploração de **dados financeiros públicos brasileiros** (Banco Central e demais fontes
oficiais abertas), com consumo via **API**, análise estatística em **Python** e
**dashboards** em HTML + CSS + Chart.js publicados via **GitHub Pages**.

## Como rodar

```bash
# 1. Ambiente (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Pipeline completo (coleta -> tratamento -> publicação), uma fonte por vez
python run_pipeline.py                          # fonte padrão (meios de pagamento)
python run_pipeline.py arrecadacao_federal
python run_pipeline.py credito_modalidade

# 3. Dashboard (abrir o site local)
#    servir a pasta docs/ e acessar no navegador
python -m http.server 8000 --directory docs
#    -> http://localhost:8000
```

`run_pipeline.py --sem-coleta` reaproveita o dado bruto já baixado (não chama a API).

## Estrutura

| Pasta | Etapa | Papel |
|-------|-------|-------|
| `src/coleta/` | 2 | Coleta via API → `dados/brutos/` |
| `src/tratamento/` | 3 | Tidy → `dados/processados/` |
| `src/analise/` | 4 | Estatística e métricas |
| `src/publicacao/` | 5 | JSON → `docs/dados/` |
| `docs/` | 6 | Dashboards (site publicado) |
| `catalogo/` | 1 | Catálogo e dicionário de fontes |

## Licença dos dados

Dados abertos do Banco Central do Brasil e demais fontes públicas citadas em
[`catalogo/fontes.md`](catalogo/fontes.md).
