# Catálogo de Fontes Candidatas — Dados Financeiros Abertos (Brasil)

> **Objetivo:** mapear fontes **oficiais, abertas e legalizadas** relacionadas a
> **sistema financeiro, pagamentos/Pix, tributos/impostos, finanças públicas,
> comércio exterior e mercado de capitais**, para depois planejar quais importar e
> **combinar** com a fonte já existente (`meios_pagamento_mensal`).
>
> Este arquivo é exploratório (Etapa 1). Nenhuma fonte aqui foi importada ainda.
> Datas de cobertura marcadas com _(verificar)_ devem ser confirmadas na coleta.
> Última pesquisa: **jul/2026**.

---

## 0. Como ler este catálogo

- **Granularidade geográfica** é a chave para o objetivo "segregação por estado/cidade":
  🟢 = tem município, 🟡 = tem UF/estado, ⚪ = só nacional/agregado.
- **Integração** estima o atrito para encaixar no pipeline atual (contrato tidy da seção 7 do
  [CONTEXTO.md](../CONTEXTO.md)): 🟢 baixo (API JSON limpa, mensal), 🟡 médio (CSV grande/anual),
  🔴 alto (bases pesadas, layout complexo).
- **"Combina com o atual"** aponta como a fonte se cruza com `meios_pagamento_mensal`
  (mensal, Brasil, por forma de pagamento).

### Matriz-resumo

| # | Fonte | Órgão | Tema | Período | Freq. | Geo | Acesso | Integr. |
|---|-------|-------|------|---------|-------|-----|--------|---------|
| 1 | Estatísticas do Pix | BCB | Pagamentos/Pix | 11/2020→ | Mensal | 🟢 município | API Olinda/OData | 🟢 |
| 2 | Meios de Pagamento **trimestral** | BCB | Pagamentos (+cartões) | 2007→ _(verif.)_ | Trim. | ⚪ | API Olinda/OData | 🟢 |
| 3 | SGS — Séries Temporais | BCB | Juros/câmbio/inflação/crédito | varia p/ série | Diária→anual | ⚪/🟡 | API `api.bcb.gov.br` | 🟢 |
| 4 | PTAX — Câmbio | BCB | Câmbio | 1984→ | Diária | ⚪ | API Olinda/OData | 🟢 |
| 5 | Expectativas de Mercado (Focus) | BCB | Projeções macro | 2000→ | Diária/sem. | ⚪ | API Olinda/OData | 🟢 |
| 6 | Crédito / juros por modalidade | BCB | Crédito | 2011→ | Mensal | 🟡 UF _(verif.)_ | API/SGS | 🟢 |
| 7 | IF.data | BCB | Bancos/instituições | 1994→ | Trim. | ⚪ | API Olinda/OData | 🟡 |
| 8 | Arrecadação Federal (série histórica) | RFB | Impostos | 1970→ | Mensal/anual | ⚪ | XLSX dados abertos | 🟡 |
| 9 | Arrecadação por Estado | RFB | Impostos | ~2000→ _(verif.)_ | Mensal | 🟡 UF | CSV/XLSX | 🟡 |
| 10 | CNPJ — Cadastro de empresas | RFB | Empresas | atual (mensal) | Mensal | 🟢 município | CSV zip (pesado) | 🔴 |
| 11 | SICONFI | Tesouro | Finanças públicas | 2013→ _(verif.)_ | Bim./anual | 🟢 município | API `apidatalake` | 🟡 |
| 12 | Tesouro Direto | Tesouro | Títulos públicos | 2002/2005→ | Diária/mensal | 🟡 UF (investidores) | CSV/CKAN + API | 🟢 |
| 13 | Transferências constitucionais (FPM/FPE) | Tesouro | Repasses | 1990s→ _(verif.)_ | Mensal/decênd. | 🟢 município | CSV/API | 🟡 |
| 14 | Portal da Transparência | CGU | Benefícios/gastos | 2013→ | Mensal | 🟢 município | API (chave) + CSV | 🟡 |
| 15 | Comex Stat | MDIC | Comércio exterior | 1997→ | Mensal | 🟢 município | API + CSV | 🟡 |
| 16 | SIDRA (IPCA/INPC/PIB/PNAD) | IBGE | Inflação/PIB/renda | 1979→ | Mensal→anual | 🟢 município | API `servicodados` | 🟢 |
| 17 | CVM — Fundos e Companhias | CVM | Mercado de capitais | ~2000→ | Diária/mensal | ⚪ | CSV | 🟡 |
| 18 | IPEADATA | Ipea | Macro + regional | varia | Mensal→anual | 🟢 município | API OData | 🟢 |
| 19 | Base dos Dados (espelho) | comunidade | Agregador tratado | varia | varia | 🟢 município | BigQuery/SQL | 🟡 |

---

## LISTA A — Banco Central (BCB): núcleo do sistema financeiro

> Mesma família da fonte atual. Todas via portal <https://dadosabertos.bcb.gov.br> e
> APIs Olinda/OData (`https://olinda.bcb.gov.br/olinda/servico/...`) ou a API SGS
> (`https://api.bcb.gov.br/dados/serie/...`). Licença: dados abertos BCB.

### A1. Estatísticas do Pix ⭐ (prioridade máxima)
- **Site:** <https://dadosabertos.bcb.gov.br/dataset/pix> · <https://www.bcb.gov.br/estabilidadefinanceira/estatisticaspix>
- **API:** `https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/`
- **Recursos e colunas:**
  - **Estatísticas de Transações Pix** — quantidade e volume financeiro mensal. Geo: ⚪ nacional. **Desde 30/11/2020.**
  - **Transações Pix por Município** 🟢 — transações liquidadas por município e por PF/PJ
    (campos: ano-mês, UF, município/código IBGE, natureza pagador/recebedor PF/PJ, quantidade, valor).
  - **Estoque de Chaves Pix por Participante** — chaves por tipo (CPF, CNPJ, e-mail, telefone, aleatória), PF/PJ.
  - **Usuários cadastrados no DICT** — estoque mensal por natureza.
  - **Estatísticas de Fraude no Pix (MED)** — transações contestadas.
- **Freq.:** mensal · **Histórico:** desde nov/2020 (municipal começou depois — _verificar_).
- **Geo:** 🟢 município + UF (no recurso por município).
- **Combina com o atual:** *encaixe perfeito* — a fonte atual já traz `quantidadePix`/`valorPix`
  nacional; este dataset abre o Pix por **município/UF** e por **PF/PJ**. Primeiro candidato para
  entregar a "segregação por estado/cidade".

### A2. Meios de Pagamento — trimestral (com cartões)
- **Site:** <https://dadosabertos.bcb.gov.br/dataset/estatisticas-meios-pagamentos>
- **Recurso:** `MeiosdePagamentosTrimestralDA` (serviço `MPV_DadosAbertos`, parâmetro `trimestre`).
- **Colunas:** trimestre + quantidade/valor por instrumento, **incluindo cartões**
  (crédito, débito, pré-pago) — que faltam na série mensal.
- **Freq.:** trimestral · **Geo:** ⚪ nacional.
- **Combina:** complementa `meios_pagamento_mensal` adicionando a dimensão **cartões**.

### A3. SGS — Sistema Gerenciador de Séries Temporais ⭐
- **Site:** <https://www3.bcb.gov.br/sgspub/> · portal dados abertos por série.
- **API:** `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial=dd/MM/aaaa&dataFinal=dd/MM/aaaa`
  (também `/dados/ultimos/{N}`).
- **Conteúdo:** milhares de séries econômico-financeiras. Códigos úteis:
  - **SELIC meta** (432) e SELIC diária (11), **CDI** (12)
  - **IPCA** (433), **IGP-M** (189), **INPC** (188)
  - **Câmbio R$/US$** (1) — PTAX venda
  - **Saldo de crédito** (20539+), **taxa média de juros PF/PJ** (20740, 25471...)
  - **Endividamento das famílias** (29037), **inadimplência** (21082+)
- **Colunas:** `data` (dd/MM/aaaa), `valor`. Uma série por chamada.
- **Freq.:** varia (diária/mensal/anual) · **Histórico:** varia (algumas desde os anos 1990).
- **Geo:** ⚪ nacional (poucas séries regionais).
- **Combina:** camada de **contexto macro** — deflacionar valores (IPCA), cruzar volume de
  pagamentos com SELIC/crédito/inadimplência. API trivial de consumir.

### A4. PTAX / Câmbio
- **Site:** <https://dadosabertos.bcb.gov.br/dataset/dolar-americano-usd-todos-os-boletins-diarios>
- **API:** serviço Olinda `PTAX` (`CotacaoDolarPeriodo`, `CotacaoMoedaPeriodo`).
- **Colunas:** data/hora do boletim, cotação compra/venda, tipo de boletim.
- **Freq.:** diária · **Histórico:** desde 1984 (dólar) · **Geo:** ⚪.

### A5. Expectativas de Mercado (Relatório Focus)
- **Site:** <https://dadosabertos.bcb.gov.br/dataset/expectativas-mercado>
- **API:** serviço Olinda `Expectativas` (IPCA, PIB, câmbio, SELIC esperados).
- **Colunas:** data, indicador, base de cálculo, mediana, média, desvio-padrão, mín/máx, nº respondentes.
- **Freq.:** diária/semanal · **Histórico:** ~2000→ · **Geo:** ⚪.

### A6. Crédito — operações, juros e spread por modalidade ✅ implementada
- **Site:** <https://dadosabertos.bcb.gov.br/dataset/> (vários datasets "20xxx"); base "Estatísticas monetárias e de crédito".
- **Colunas:** modalidade (consignado, cartão, veículos, imobiliário...), taxa de juros, saldo, concessões, prazo, spread.
- **Freq.:** mensal · **Histórico:** 2011→ · **Geo:** ⚪ **nacional** _(verificado)_.
- **Geo — verificado:** **não há** recorte por UF por modalidade. O SGS só publica crédito
  por estado no corte de **porte de empresa** (PJ microempresa `25747+`, pequeno porte
  `25925+`, MEI `27327+`) — outro recorte, que não se cruza com o de modalidade.
  Fica como candidata separada, se um dia interessar o mapa de crédito por UF.
- **Combina:** relaciona **volume de pagamentos** com **crédito e inadimplência**.
- **Implementada como** `credito_modalidade` — dicionário em [`fontes.md`](fontes.md),
  painel em `docs/credito-modalidade.html`.

### A7. IF.data — dados de instituições financeiras
- **Site:** <https://www3.bcb.gov.br/ifdata/> · API Olinda.
- **Colunas:** por instituição/conglomerado — ativos, carteira de crédito, patrimônio, resultado, índice de Basileia.
- **Freq.:** trimestral · **Histórico:** 1994→ · **Geo:** ⚪ (mas instituições têm sede em UF).

> **Também no BCB (menor prioridade):** Open Finance (adesões/APIs), Reclamações contra
> instituições (ranking trimestral, por instituição), Moedas em circulação, Meios de pagamento
> por região do Selic/STR.

---

## LISTA B — Receita Federal (RFB): tributos e empresas

### B1. Arrecadação das Receitas Federais — série histórica ⭐
- **Site:** <https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos/receitadata/arrecadacao>
- **Arquivos:** `ARRECADAÇÃO DAS RECEITAS FEDERAIS - 1970 A 1993.xlsx` e `... 1994 A 2025.xlsx`.
- **Colunas:** período (mês/ano) + valor arrecadado por **tributo** (IRPF, IRPJ, IPI, IOF, COFINS,
  PIS/PASEP, CSLL, INSS/previdência, Imposto de Importação etc.), a preços correntes e/ou constantes.
- **Freq.:** mensal (agregada em anual) · **Histórico:** **1970→2025** (atualização mar/2026).
- **Geo:** ⚪ nacional · **Licença:** CC-BY-ND 3.0.
- **Combina:** série de **impostos** mensal para cruzar com atividade econômica/pagamentos.

### B2. Arrecadação por Estado (UF) 🟡
- **Site:** portal ReceitaData → "Arrecadação" (arquivos "por UF").
- **Colunas:** ano-mês, **UF**, tributo, valor arrecadado.
- **Freq.:** mensal · **Histórico:** ~2000→ _(verificar início exato)_ · **Geo:** 🟡 UF.
- **Combina:** *chave* para "segregação por estado" no tema impostos.

### B3. CNPJ — Cadastro Nacional da Pessoa Jurídica (base completa)
- **Site:** <https://www.gov.br/receitafederal/dados/cnpj-metadados.pdf> ·
  arquivos em <https://arquivos.receitafederal.gov.br/dados/cnpj/> (também espelhos: dados.gov.br).
- **Tabelas:** Empresas, Estabelecimentos, Sócios, Simples, e tabelas de domínio (CNAE, município, natureza jurídica, país, motivo).
- **Colunas (estabelecimentos):** CNPJ, situação cadastral, data de abertura, **CNAE**, **UF**, **município (cód. IBGE)**, CEP, porte, opção Simples/MEI.
- **Freq.:** atualização mensal · **Histórico:** *snapshot* atual (não série temporal) · **Geo:** 🟢 município.
- **Integração:** 🔴 pesada (dezenas de arquivos ZIP, ~milhões de linhas). Bom para **contagem de
  empresas por município/CNAE**, não para série mensal.

> **Também na RFB:** Carga Tributária Bruta (estudos anuais), Simples Nacional (arrecadação),
> parcelamentos.

---

## LISTA C — Tesouro Nacional: finanças públicas e dívida

### C1. SICONFI — contas de estados, DF e municípios ⭐ (melhor p/ estado+cidade)
- **Site:** <https://siconfi.tesouro.gov.br/> · API: <http://apidatalake.tesouro.gov.br/docs/siconfi/>
- **Relatórios:** **RREO** (execução orçamentária, bimestral), **RGF** (gestão fiscal),
  **DCA** (balanço anual), **MSC** (matriz de saldos contábeis) + extratos de entrega.
- **Colunas:** ente (cód. IBGE), esfera (E/M/D/U), exercício, período/anexo, conta contábil, coluna, valor.
- **Freq.:** bimestral/quadrimestral/anual · **Histórico:** ~2013→ (DCA e demais) _(verificar)_.
- **Geo:** 🟢 município + 🟡 UF (cobre ~98% dos municípios).
- **Combina:** receitas/despesas e **receita tributária própria** de cada município/estado — cruza
  com arrecadação federal e com atividade de pagamentos.

### C2. Tesouro Direto
- **Site:** <https://www.tesourotransparente.gov.br/temas/divida-publica-federal/tesouro-direto> ·
  CKAN CSV: <https://www.tesourotransparente.gov.br/ckan/dataset?tags=Tesouro+Direto>
- **Datasets:** **Vendas** (diário, por título/vencimento), **Recompras**, **Estoque** (mensal),
  **Preços e Taxas** (diário, mercado secundário), **Investidores** (contas/operações).
- **Colunas:** data, tipo de título (Tesouro Selic/IPCA+/Prefixado), vencimento, PU compra/venda, taxa, quantidade, valor.
- **Freq.:** diária/mensal · **Histórico:** vendas/estoque desde ~2002; preços/taxas desde 2005.
- **Geo:** 🟡 há distribuição de **investidores por UF/faixa** em datasets específicos.

### C3. Transferências constitucionais (FPM, FPE, royalties)
- **Site:** Tesouro Transparente / <https://www.gov.br/tesouronacional> (Transferências).
- **Colunas:** data, ente (UF/município cód. IBGE), fundo (FPM/FPE), valor bruto/líquido.
- **Freq.:** decendial/mensal · **Geo:** 🟢 município.
- **Combina:** dinheiro que entra em cada município — 🟢 recorte territorial forte.

> **Também no Tesouro:** Dívida Pública Federal (estoque/custo/prazo), Resultado do Tesouro,
> Estimativa da Carga Tributária, Boletim de Finanças dos Entes Subnacionais.

---

## LISTA D — CGU / Transparência: benefícios e gastos públicos

### D1. Portal da Transparência do Governo Federal ⭐
- **Site:** <https://portaldatransparencia.gov.br> · API: <https://api.portaldatransparencia.gov.br/>
  (**exige chave gratuita** por e-mail) · Dados Abertos (planilhas) para grandes volumes.
- **Conjuntos úteis:**
  - **Benefícios ao Cidadão** 🟢 — Novo Bolsa Família, BPC, Auxílio Gás, Seguro-Defeso, PETI
    (por município, mensal: nº beneficiários, valor).
  - **Transferências de recursos** 🟢 — convênios/repasses por município/órgão/programa.
  - **Despesas** (execução orçamentária), **Servidores**, **Cartões de pagamento**.
- **Colunas (benefícios):** ano-mês, UF, município (cód. IBGE), programa, qtd. beneficiários, valor pago.
- **Freq.:** mensal · **Histórico:** 2013→ · **Geo:** 🟢 município.
- **Combina:** renda de transferências por município — cruza com pagamentos/consumo local.

---

## LISTA E — Comércio exterior (MDIC)

### E1. Comex Stat ⭐
- **Site:** <https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/estatisticas> ·
  API: <https://api-comexstat.mdic.gov.br/docs> · base bruta (CSV `;`).
- **Colunas (base municípios):** ano, mês, **SH4**, cód. país, **UF** da empresa,
  **município** (cód. IBGE) da empresa, peso líquido (kg), valor FOB (US$).
  Base detalhada por NCM traz também via de transporte, URF, unidade estatística.
- **Freq.:** mensal · **Histórico:** **1997→** · **Geo:** 🟢 município + 🟡 UF.
- **Combina:** exportação/importação por município — atividade econômica territorial.

---

## LISTA F — IBGE: preços, PIB e renda

### F1. SIDRA / API de dados agregados ⭐
- **Site:** <https://sidra.ibge.gov.br/> · API: <https://servicodados.ibge.gov.br/api/docs/agregados>
  (formato `/agregados/{tabela}/periodos/{p}/variaveis/{v}?localidades=N6[all]`).
- **Pesquisas relevantes:**
  - **IPCA / INPC** — inflação mensal (nacional + 16 regiões metropolitanas). Desde 1979/1980.
  - **PIB / Contas Nacionais** — trimestral (nacional) e **PIB dos Municípios** (anual, por município). 🟢
  - **PNAD Contínua** — rendimento/ocupação (trimestral, nacional + UF). 🟡
  - **Pesquisa Mensal de Comércio / Serviços / Indústria** — volume por UF.
- **Colunas:** localidade (cód. IBGE), período, variável, unidade, valor.
- **Freq.:** mensal→anual · **Geo:** 🟢 até município (depende da tabela).
- **Combina:** **IPCA** para deflacionar todos os valores em R$; PIB/renda municipal para normalizar
  os recortes territoriais (per capita, % do PIB).

---

## LISTA G — Mercado de capitais (CVM)

### G1. Portal de Dados Abertos CVM
- **Site:** <https://dados.cvm.gov.br/>
- **Conjuntos:** **Fundos de Investimento** (Informe Diário — patrimônio líquido, cotas,
  captação/resgate; cadastro; composição de carteira; perfil mensal), **Companhias Abertas**
  (DFP anual, ITR trimestral, FRE, fatos relevantes).
- **Colunas (informe diário):** CNPJ do fundo, data, VL_TOTAL, VL_QUOTA, VL_PATRIM_LIQ,
  captação/resgate do dia, nº de cotistas.
- **Freq.:** diária/mensal/trimestral · **Histórico:** informe diário no layout atual desde ~2017; DFP/ITR há mais tempo.
- **Geo:** ⚪ nacional · **Formato:** CSV (zip mensal).
- **Combina:** captação de fundos vs. movimentação financeira/juros.

---

## LISTA H — Agregadores (facilitam, mas confirme a fonte primária)

### H1. IPEADATA
- **Site:** <http://www.ipeadata.gov.br/> · API OData: `http://www.ipeadata.gov.br/api/odata4/`
- **Conteúdo:** ~milhares de séries **macro** + ~**1.500 séries regionais** (UF e município, com
  Áreas Mínimas Comparáveis para consistência temporal). Bibliotecas: `ipeadatapy` (Python), `ipeadatar` (R).
- **Geo:** 🟢 até município · **Combina:** atalho para muitas séries já consolidadas.

### H2. Base dos Dados
- **Site:** <https://basedosdados.org/> (BigQuery / pacote `basedosdados`).
- **Conteúdo:** *datalake* com tabelas **tratadas e padronizadas** que espelham RFB, Comex, BCB,
  SICONFI, IBGE etc. Útil para prototipagem rápida com SQL.
- **Atenção:** não é órgão oficial; para publicar, referencie sempre a **fonte primária** oficial.

---

## Sugestão de priorização (para a etapa de planejamento)

**Onda 1 — mesma família, integração trivial, alto valor:**
1. **Pix (BCB)** — estende a fonte atual + entrega segregação por município. ⭐
2. **SGS (BCB)** — IPCA (deflacionar), SELIC, câmbio, crédito/inadimplência como contexto macro.
3. **Meios de Pagamento trimestral (BCB)** — adiciona cartões.

**Onda 2 — impostos e território:**
4. **Arrecadação RFB (nacional + por UF)** — tema "impostos" com recorte estadual.
5. **Comex Stat** — exportação/importação por município (mensal, histórico longo).
6. **Portal da Transparência (benefícios)** — renda transferida por município.

**Onda 3 — finanças públicas e normalização:**
7. **SICONFI** — receitas/despesas por município e estado.
8. **IBGE SIDRA (PIB municipal, PNAD)** — normalizar per capita / % do PIB.

**Onda 4 — bases pesadas / nicho:**
9. **CNPJ (RFB)** — empresas por município/CNAE (snapshot).
10. **CVM**, **Tesouro Direto**, **IF.data** — aprofundamentos de mercado.

### Observações de integração
- O contrato tidy atual (`ano_mes`, `forma_pagamento`, `quantidade`, `valor`) atende bem
  Pix/meios de pagamento. Para fontes com **dimensão geográfica** (UF/município), será preciso
  **estender o contrato** com colunas `uf` e/ou `cod_municipio`/`municipio` — avaliar na Etapa 3
  sem quebrar as fontes existentes (seção 7 do CONTEXTO.md).
- **Chave geográfica comum:** código de município **IBGE (7 dígitos)** — usado por BCB Pix,
  Comex, SICONFI, Transparência e IBGE. Padronizar por ele permite cruzamentos.
- **Deflação:** adotar IPCA (SGS 433 ou SIDRA) como padrão para comparar valores em R$ ao longo do tempo.
- **Chaves/limites de API:** só o Portal da Transparência exige chave (gratuita). BCB, Tesouro,
  IBGE, Comex e CVM são abertos sem cadastro (respeitar rate limits).
