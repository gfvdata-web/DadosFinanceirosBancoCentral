# Catálogo de Fontes (Etapa 1)

Dicionário de dados das fontes usadas no projeto. Cada fonte registrada aqui
também precisa estar em [`src/config.py`](../src/config.py) (dicionário `FONTES`).

---

## meios_pagamento_mensal — BCB · Estatísticas de Meios de Pagamento (mensal)

- **Órgão:** Banco Central do Brasil (BCB)
- **API:** Olinda / OData — serviço `MPV_DadosAbertos`
- **Recurso:** `MeiosdePagamentosMensalDA` (FunctionImport, parâmetro `AnoMes`)
- **Endpoint (série completa):**
  ```
  https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata/MeiosdePagamentosMensalDA(AnoMes=@AnoMes)?@AnoMes=''&$format=json
  ```
  > Passar `@AnoMes=''` (vazio) retorna todos os meses. Para um mês específico, use `@AnoMes='202605'`.
- **Periodicidade:** mensal
- **Formatos disponíveis:** `json` (padrão), `xml`, `text/csv`, `text/html`
- **Licença:** Dados abertos — Banco Central do Brasil
- **Portal:** https://dadosabertos.bcb.gov.br/dataset/estatisticas-meios-pagamentos

### Dicionário de dados (formato original "wide")

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `AnoMes` | string `YYYYMM` | Ano e mês de referência |
| `quantidade{Forma}` | decimal | Quantidade de transações da forma (**milhares**) |
| `valor{Forma}` | decimal | Valor movimentado da forma (**R$ milhões**) |

Formas (`{Forma}`): `Pix`, `TED`, `TEC`, `Cheque`, `Boleto`, `DOC`.

> **Unidades:** quantidade em **milhares de transações**; valor em **R$ milhões**.
> **Observação:** `DOC` e `TEC` aparecem zerados nos meses recentes (instrumentos descontinuados).

### Formato tidy após a Etapa 3

| Coluna | Descrição |
|--------|-----------|
| `ano_mes` | `YYYY-MM` |
| `forma_pagamento` | Pix / TED / TEC / Cheque / Boleto / DOC |
| `quantidade` | milhares de transações |
| `valor` | R$ milhões |

---

## Fontes candidatas (a documentar)

- BCB — SGS (Sistema Gerenciador de Séries Temporais): juros, câmbio, inflação.
- BCB — Meios de Pagamento **trimestral** (`MeiosdePagamentosTrimestralDA`): inclui cartões.
- Tesouro Transparente / Tesouro Direto.
- IBGE / Portal Brasileiro de Dados Abertos (indicadores financeiros).
