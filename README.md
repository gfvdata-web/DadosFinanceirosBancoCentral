# Dados Financeiros Abertos — Brasil

Exploração de **dados financeiros públicos brasileiros** (Banco Central e demais fontes
oficiais abertas), com consumo via **API**, análise estatística em **Python** e
**dashboards** em HTML + CSS + Chart.js publicados via **GitHub Pages**.

> 📄 A organização completa do projeto e suas etapas está em **[CONTEXTO.md](CONTEXTO.md)**.
> Cite a *Etapa* correspondente ao pedir mudanças (ex.: "melhorar a Etapa 4").

## Estudo inicial

**BCB — Estatísticas de Meios de Pagamento (mensal):** quantidade e valor de movimentação
por `AnoMes` e forma de pagamento (Pix, TED, TEC, Cheque, Boleto, DOC) no Brasil.

## Como rodar

```bash
# 1. Ambiente (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Pipeline completo (coleta -> tratamento -> publicação)
python run_pipeline.py

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
