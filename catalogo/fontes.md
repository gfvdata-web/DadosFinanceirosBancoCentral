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

## arrecadacao_federal — RFB · Arrecadação das Receitas Federais (série histórica)

- **Órgão:** Receita Federal do Brasil (RFB) — portal ReceitaData
- **Acesso:** download de arquivo (**XLSX**), não há API
- **Página da série:**
  https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos/receitadata/arrecadacao/serie-historica
- **Arquivos (conferidos em jul/2026):**
  ```
  .../serie-historica/arrecadacao-das-receitas-federais-1970-a-1993.xlsx
  .../serie-historica/arrecadacao-das-receitas-federais-1994-a-2025.xlsx
  ```
  > O portal (Plone) linka os arquivos com o sufixo `/view`; o download direto é a URL
  > sem esse sufixo. O nome muda quando a RFB estende a série (`1994 a 2026`, etc.) —
  > por isso a Etapa 2 relê a página de listagem e descobre o arquivo vigente quando a
  > URL registrada em `src/config.py` falha.
- **Periodicidade:** mensal · **Geo:** ⚪ nacional (sem recorte por UF/município)
- **Licença:** CC-BY-ND 3.0 — Receita Federal do Brasil

### Layout do XLSX (formato original "wide" e hierárquico)

- **Uma aba por ano** (`1994`, `1995`, …, `2025`).
- Linhas 2–5: título, período, base de preços e **unidade monetária**.
- Linha 6: cabeçalho `RECEITAS | JAN | … | DEZ | TOTAL`.
- Linhas 7+: um tributo por linha; o **recuo do rótulo indica o nível** na hierarquia
  (0 espaços = tributo; 2–3 = abertura; 4 = sub-abertura).
- Valores a **preços correntes**, em **R$ milhões** (o arquivo não traz preços constantes).
- Os 38 rótulos são **idênticos** nos 32 anos — não há variação de grafia a conciliar.

### Recorte adotado e por quê

Só o arquivo **1994→2025** entra no pipeline. O de 1970–1993 é coletado (rastreabilidade)
mas **não é tratado**: mistura quatro padrões monetários (Cr$, Cz$, NCz$, CR$) entre as
abas e traz 1970–1985 em base **anual**, o que não forma série comparável nem mensal.

### Deflação

A Etapa 2 também baixa o **IPCA mensal** do BCB/SGS (série **433**) e a Etapa 3 gera um
número-índice para converter os valores correntes em **constantes do último mês da série**
(hoje dez/2025). É a convenção de deflação adotada no projeto.

```
https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/12/1993
```

### Formato tidy após a Etapa 3

| Coluna | Descrição |
|--------|-----------|
| `ano_mes` | `YYYY-MM` |
| `tributo` | rótulo original do XLSX, sem recuo (chave da série) |
| `rotulo` | nome amigável para exibição (ex.: `IMPOSTO SOBRE A RENDA-TOTAL` → `Imposto de Renda`) |
| `tributo_pai` | tributo do nível acima (vazio no nível 1) |
| `nivel` | 1 = tributo, 2 = abertura, 3 = sub-abertura |
| `tipo` | `componente`, `detalhe` ou `agregado` (ver abaixo) |
| `valor` | R$ milhões **correntes** |
| `valor_constante` | R$ milhões **constantes** (IPCA, base = último mês) |

**`tipo` evita dupla contagem:**
- `componente` — as **15 linhas de nível 1** que somam exatamente o `TOTAL GERAL`
  (Imposto de Importação, Imposto de Exportação, IPI, Imposto de Renda, IOF, ITR, COFINS,
  PIS/PASEP, CSLL, CIDE-Combustíveis, FUNDAF, PSS, Outras receitas administradas,
  Receita previdenciária, Administradas por outros órgãos). Base das participações e do ranking.
- `detalhe` — aberturas dentro de um componente (IPI-Fumo, IRRF-Rendimentos do trabalho…).
- `agregado` — linhas somatórias do próprio XLSX (`SUBTOTAL [A]`,
  `ADMINISTRADAS PELA RFB [C]`, `TOTAL GERAL [E]`). A Etapa 3 confere, mês a mês, se os
  componentes fecham com o `TOTAL GERAL` publicado (tolerância de 0,1%).

> **Rótulos ambíguos:** `ENTIDADES FINANCEIRAS` e `DEMAIS EMPRESAS` aparecem dentro de IRPJ,
> COFINS, PIS/PASEP e CSLL. A Etapa 3 os qualifica com o tributo pai (`COFINS · ENTIDADES
> FINANCEIRAS`) para não colapsar quatro séries distintas em uma.

> **Observação:** a `RECEITA PREVIDENCIÁRIA` aparece **zerada em todo o ano de 1994** na
> publicação da RFB — é o dado de origem, mantido como está.

---

## credito_modalidade — BCB · Crédito por modalidade (SGS)

- **Órgão:** Banco Central do Brasil (BCB) — Departamento de Estatísticas
- **API:** SGS (Sistema Gerenciador de Séries Temporais) — REST, sem chave
- **Endpoint (uma série por requisição):**
  ```
  https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial=01/03/2011
  ```
  > O SGS **não tem consulta multi-série**: a Etapa 2 itera sobre os 61 códigos
  > registrados em `src/config.py` (`series`) e concatena as respostas.
  > Formatos: `json` (usado), `csv`. Parâmetros opcionais `dataInicial`/`dataFinal`
  > em `DD/MM/AAAA`; `/dados/ultimos/{n}` traz só as últimas observações.
- **Periodicidade:** mensal · **Histórico:** mar/2011 → (183 meses em mai/2026)
- **Licença:** Open Database License (ODbL) — BCB
- **Portal:** https://dadosabertos.bcb.gov.br/dataset/20539-saldo-da-carteira-de-credito---total
- **Metadados por série:** a API CKAN do portal resolve código → título/periodicidade:
  `https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=codigo_sgs:"20539"`

### Geografia: nacional (⚪), verificado

O item A6 de [`fontes-candidatas.md`](fontes-candidatas.md) marcava o recorte por UF como
"a verificar". **Verificado: não existe.** O SGS publica crédito por UF apenas para
*porte de empresa* — "Saldo de crédito pessoa jurídica por estado" (microempresa `25747+`,
pequeno porte `25925+`) e "Saldo de crédito por estado — MEI" (`27327+`) — que é um corte
**diferente** do de modalidade e não se cruza com ele. Por isso o tidy desta fonte **não
tem coluna `uf`**, e o contrato genérico da seção 7 do `CONTEXTO.md` segue intacto.

### Dicionário de dados (resposta do SGS)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `data` | string `DD/MM/AAAA` | Mês de referência (sempre dia 01) |
| `valor` | string decimal | Valor da série; a unidade depende do código consultado |

### Séries usadas

Três medidas, combinadas por segmento × modalidade (mapa completo em `src/config.py`):

| Medida | Unidade | Cobertura |
|--------|---------|-----------|
| `saldo` | R$ milhões | agregados + todas as modalidades |
| `taxa` | % ao ano | agregados + todas as modalidades |
| `spread` | p.p. ao ano | **só os agregados** — o BCB não publica spread por modalidade |

Agregados (linha `Total` de cada segmento):

| Segmento | saldo | taxa | spread |
|----------|-------|------|--------|
| Total | 20539 | 20714 | 20783 |
| Pessoas físicas (PF) | 20541 | 20716 | 20785 |
| Pessoas jurídicas (PJ) | 20540 | 20715 | 20784 |

Modalidades detalhadas: **10 em PF** (cheque especial, crédito pessoal consignado e não
consignado, aquisição de veículos, cartão rotativo e parcelado, desconto de cheques,
crédito rural, financiamento imobiliário, microcrédito) e **16 em PJ** (desconto de
duplicatas, capital de giro, conta garantida, cheque especial, aquisição de veículos,
vendor, compror, cartão rotativo e parcelado, ACC, financiamentos a importações e
exportações, repasse externo, crédito rural, financiamento imobiliário, BNDES).

> **Recorte temporal:** o saldo existe desde 2007 (e o total, desde 1988), mas juros e
> spread só a partir de **mar/2011** — o corte em `01/03/2011` alinha as três medidas.

> **Cobertura parcial, por desenho:** as modalidades detalhadas não esgotam o segmento
> (somam ~82% do saldo PF e ~70% do PJ em mai/2026). A Etapa 4 calcula o resíduo
> (`saldo do segmento − soma das modalidades`) e o dashboard o exibe como
> *"Outras modalidades"*, para que as fatias fechem com o saldo real do segmento.

> **Estabilidade da API:** o gateway do SGS às vezes responde HTTP 200 com uma página HTML
> de "Requisição inválida" quando recebe muitas chamadas em sequência. A Etapa 2 trata isso
> com pausa entre séries e retry com espera crescente.

### Formato tidy após a Etapa 3

| Coluna | Descrição |
|--------|-----------|
| `ano_mes` | `YYYY-MM` |
| `segmento` | `Total` / `PF` / `PJ` |
| `modalidade_credito` | `Total` (agregado do segmento) ou o nome da modalidade |
| `saldo` | R$ milhões |
| `taxa_juros_aa` | % ao ano |
| `spread_pp` | p.p. ao ano — preenchido só nas linhas `modalidade_credito = Total` |

Mesma anatomia do contrato da seção 7 do `CONTEXTO.md` (dimensões em linha, medidas em
coluna), com `forma_pagamento` substituído pelo par `segmento` + `modalidade_credito`.

---

## Fontes candidatas (a documentar)

Levantamento completo em [`fontes-candidatas.md`](fontes-candidatas.md) — 19 fontes oficiais
e abertas (BCB, RFB, Tesouro/SICONFI, CGU, MDIC/Comex, IBGE, CVM, Ipea) com site, colunas,
histórico, granularidade geográfica (Brasil/UF/município) e priorização de importação.

Destaques de curto prazo:
- **BCB — Estatísticas do Pix** (nacional + **por município**): estende esta fonte e entrega recorte territorial.
- **BCB — SGS**: IPCA (deflacionar), SELIC, câmbio, crédito.
- **BCB — Meios de Pagamento trimestral** (`MeiosdePagamentosTrimestralDA`): inclui cartões.
- **RFB — Arrecadação** (nacional + por UF): tema impostos.
- **Comex Stat** e **Portal da Transparência**: dados mensais por município.
