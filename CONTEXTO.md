# CONTEXTO DO PROJETO — Dados Financeiros Abertos (Brasil)

> Arquivo-mestre de contexto. Serve de referência para todos os prompts futuros.
> Ao pedir uma tarefa, cite a **Etapa** correspondente (ex.: "trabalhar na **Etapa 4**",
> "ajustar a **Etapa 6** sem quebrar a **Etapa 5**").

---

## 1. Visão geral

Projeto de **exploração de dados financeiros públicos brasileiros**, com consumo via **API**,
tratamento e **análise estatística**, culminando em **páginas HTML + CSS** com **dashboards e
displays analíticos**.

- **Fontes**: Banco Central do Brasil (BCB), Portal de Dados Abertos e demais fontes
  brasileiras oficiais, abertas e legalizadas.
- **Enfoque**: analítico e estatístico (séries temporais, participação, crescimento,
  distribuições, comparações).
- **Estudo inicial (start)**: BCB — *Estatísticas de Meios de Pagamento (mensal)*:
  quantidade e valor de movimentação por `AnoMes` por forma de pagamento no Brasil.

## 2. Objetivos

1. Criar uma base reutilizável para incorporar **novas fontes** com o mínimo de atrito.
2. Manter um **pipeline integrado** (coleta → tratamento → análise → publicação → visualização)
   em que cada etapa consome a saída padronizada da anterior.
3. Publicar **dashboards estáticos** (GitHub Pages) que consomem JSON gerado pelo pipeline.

## 3. Princípios de trabalho

- **Integração acima de tudo**: cada etapa tem contrato de entrada/saída bem definido
  (ver seção 7). Alterações devem respeitar esses contratos.
- **Não quebrar**: ao ajustar uma etapa, verificar as etapas vizinhas (a que produz a entrada
  e a que consome a saída). O pipeline completo (`run_pipeline.py`) deve continuar rodando.
- **Reprodutibilidade**: qualquer JSON publicado deve ser regenerável rodando o pipeline.
- **Idioma do código**: nomes de funções/variáveis e comentários em português.
- **Novas fontes** seguem a mesma anatomia de módulos por etapa (um arquivo por fonte).

## 4. Stack tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Coleta / tratamento / análise | **Python 3.13** (`requests`, `pandas`) |
| Camada de publicação | JSON estático gerado pelo Python |
| Front-end / dashboards | **HTML + CSS + JavaScript** com **Chart.js** (via CDN) |
| Hospedagem | **GitHub Pages** (pasta `/docs`) |
| Versionamento | Git + GitHub (`gfvdata-web`) |

## 5. Estrutura de pastas

```
DadosFinanceirosBancoCentral/
├── CONTEXTO.md              # este arquivo
├── README.md
├── requirements.txt
├── run_pipeline.py          # orquestra as Etapas 2→5 para uma fonte
├── src/
│   ├── config.py            # caminhos e registro de fontes/endpoints
│   ├── coleta/              # Etapa 2 — coletores de API
│   ├── tratamento/          # Etapa 3 — limpeza e padronização (tidy)
│   ├── analise/             # Etapa 4 — estatística e métricas
│   └── publicacao/          # Etapa 5 — gera JSON para o front
├── dados/
│   ├── brutos/              # respostas cruas da API (regeneráveis; fora do git)
│   └── processados/         # dados tratados (CSV tidy)
├── docs/                    # Etapa 6 — site publicado (GitHub Pages)
│   ├── index.html           # uma página por fonte (+ nav .nav-paineis entre elas)
│   ├── css/estilo.css       # CSS único, compartilhado por todas as páginas
│   ├── js/app.js            # um JS por página (js/<slug-com-hifen>.js)
│   └── dados/               # JSON consumido pelos dashboards
├── prompts/                 # um prompt por fonte nova (ver seção 12)
└── catalogo/
    ├── fontes.md            # Etapa 1 — catálogo de fontes e dicionário de dados
    └── fontes-candidatas.md # Etapa 1 — levantamento de fontes ainda não implementadas
```

## 6. As Etapas

Cada etapa tem número e nome fixos. Use-os como referência nos prompts.

### Etapa 0 — Fundação & Infraestrutura
Setup do repositório, estrutura de pastas, ambiente Python, `config.py`, git + GitHub Pages.
**Saída:** projeto versionado e executável. **Status:** ✅ concluída.

### Etapa 1 — Catálogo de Fontes
Mapear e documentar fontes/endpoints (URL, parâmetros, colunas, unidades, periodicidade,
licença). Vive em [`catalogo/fontes.md`](catalogo/fontes.md).
**Saída:** dicionário de dados por fonte. **Status:** 🟡 em andamento (fonte inicial documentada).

### Etapa 2 — Ingestão / Coleta via API
Coletores que consultam as APIs e salvam a resposta crua em `dados/brutos/`.
Código em `src/coleta/`. Um módulo por fonte.
**Entrada:** endpoint (de `config.py`). **Saída:** JSON bruto. **Status:** ✅ fonte inicial.

### Etapa 3 — Tratamento & Modelagem
Limpeza, conversão para formato **tidy/long** padronizado, tipagem, ordenação.
Código em `src/tratamento/`.
**Entrada:** `dados/brutos/`. **Saída:** CSV tidy em `dados/processados/`. **Status:** ✅ fonte inicial.

### Etapa 4 — Análise Exploratória & Estatística
Estatística descritiva, participação (%), crescimento (YoY, CAGR), séries temporais, rankings.
Código em `src/analise/`.
**Entrada:** `dados/processados/`. **Saída:** estruturas/metricas (dicts/DataFrames). **Status:** ✅ fonte inicial.

### Etapa 5 — Camada de Publicação de Dados
Consolida dados + métricas em **JSON compacto** para o front, gravado em `docs/dados/`.
Código em `src/publicacao/`.
**Entrada:** saídas das Etapas 3 e 4. **Saída:** `docs/dados/*.json`. **Status:** ✅ fonte inicial.

### Etapa 6 — Dashboards & Visualização
Páginas HTML + CSS + JS (Chart.js) que consomem o JSON e exibem KPIs, gráficos e tabelas.
Código em `docs/`.
**Entrada:** `docs/dados/*.json`. **Saída:** site interativo. **Status:** ✅ dashboard inicial.

### Etapa 7 — Documentação & Deploy
`README`, publicação via GitHub Pages, revisão de qualidade e (opcional) automação (CI).
**Saída:** site no ar e docs atualizadas. **Status:** 🟡 em andamento.

## 7. Fluxo de dados (contratos entre etapas)

```
[API]  ──Etapa 2──▶  dados/brutos/<fonte>.json
                         │
                    ──Etapa 3──▶  dados/processados/<fonte>.csv   (tidy: uma linha por AnoMes×forma)
                         │
        ┌────────────────┴─────────────────┐
   ──Etapa 4──▶ métricas            ──Etapa 5──▶ docs/dados/<fonte>.json
                                          │
                                     ──Etapa 6──▶ dashboard (docs/index.html)
```

**Formato tidy padrão (Etapa 3):** colunas `ano_mes` (YYYY-MM), `forma_pagamento`,
`quantidade`, `valor`. Esse contrato deve ser mantido por todas as fontes similares.

**Anatomia do contrato (para fontes com outras dimensões):** o que se mantém é a *forma* —
**dimensões em linha, medidas em coluna**, sempre com `ano_mes` como primeira dimensão.
Uma fonte com outro recorte troca as colunas de dimensão e de medida sem mudar a forma;
ex.: `credito_modalidade` usa `ano_mes` + `segmento` + `modalidade_credito` como dimensões
e `saldo` / `taxa_juros_aa` / `spread_pp` como medidas. Nenhuma fonte implementada tem
recorte geográfico ainda — quando a primeira tiver, a coluna `uf` entra como mais uma
dimensão, sem afetar as fontes que não a têm.

## 8. Fontes de dados

Cada fonte tem seu dicionário de dados completo (URL, parâmetros, colunas, unidades,
periodicidade, licença) em [`catalogo/fontes.md`](catalogo/fontes.md), uma seção por fonte.
Este arquivo (`CONTEXTO.md`) não replica esse conteúdo — ao trabalhar em uma fonte específica,
leia só a seção correspondente em `catalogo/fontes.md`, não o catálogo inteiro.

Lista de fontes implementadas (nome, status — detalhe em `catalogo/fontes.md`):

- `meios_pagamento_mensal` — ✅ concluída. Página: `docs/index.html`.
- `arrecadacao_federal` — ✅ concluída (RFB, XLSX, mensal 1994→2025, nacional).
  Página: `docs/arrecadacao-federal.html`. Primeira fonte por **download de arquivo**
  (não API) e primeira com **deflação por IPCA** (BCB/SGS 433) embutida no pipeline.
- `credito_modalidade` — ✅ concluída (BCB/SGS, mensal mar/2011→, nacional).
  Página: `docs/credito-modalidade.html`. Primeira fonte **multi-série** (61 códigos do
  SGS, uma requisição cada) e primeira com **duas dimensões** (segmento PF/PJ × modalidade)
  — ver a nota sobre o contrato tidy na seção 7.

## 9. Convenções

- **Nome da fonte** (chave): slug em minúsculas, ex.: `meios_pagamento_mensal`.
- **Arquivos por fonte**: mesmo slug em `coleta/`, `tratamento/`, `publicacao/` e em `dados/`.
- **Datas**: `AnoMes` normalizado para string `YYYY-MM`.
- **JSON do front**: sempre com bloco `meta` (fonte, url, gerado_em, unidades, período).

## 10. Como referenciar as etapas nos prompts

- "Adicionar a fonte X seguindo a **Etapa 1 e 2**."
- "Melhorar as métricas da **Etapa 4** (adicionar sazonalidade), atualizando a **Etapa 5**."
- "Redesenhar o dashboard da **Etapa 6** sem alterar o contrato de dados da **Etapa 5**."
- Sempre que uma mudança afetar o contrato da seção 7, avise para eu ajustar as etapas vizinhas.

## 11. Roadmap curto

- [ ] Etapa 1: documentar mais fontes (SGS/BCB, Tesouro, IBGE financeiro).
      Feitas: `meios_pagamento_mensal`, `arrecadacao_federal`, `credito_modalidade`.
- [ ] Etapa 3: avaliar reaproveitar o deflator IPCA (hoje interno à `arrecadacao_federal`)
      como utilitário compartilhado quando uma segunda fonte precisar dele.
- [ ] Etapa 4: sazonalidade, médias móveis, testes de tendência.
- [ ] Etapa 6: filtros interativos, seletor de métrica (quantidade/valor), tema claro/escuro.
- [ ] Etapa 7: automação de atualização (agendada) e melhorias de acessibilidade.

## 12. Como abrir uma sessão para uma fonte nova

Cada fonte nova (novo "braço" do projeto, com sua própria página de dashboard) tem um
prompt dedicado em `prompts/fonte-XX-<slug>.md`. Esse arquivo é a unidade de contexto que
se cola inteiro em uma sessão nova (normalmente modelo Opus) — ele já aponta exatamente o
que ler, para não gastar tokens com o histórico de outras fontes.

**Ao criar um prompt de fonte nova, sempre:**
- Apontar só as seções necessárias deste `CONTEXTO.md` (tipicamente 5, 6, 7 e 9) — nunca
  pedir para ler o arquivo inteiro.
- Apontar só a seção correspondente em `catalogo/fontes.md` (a fonte de referência
  `meios_pagamento_mensal`) e o item específico em `catalogo/fontes-candidatas.md` — nunca
  o catálogo inteiro.
- Descrever as Etapas 1→7 só para a fonte nova, reaproveitando `meios_pagamento_mensal`
  como modelo de código/estilo (sem copiar detalhes de outras fontes já implementadas).

**Prompts existentes:**
- `prompts/fonte-06-credito-modalidade.md` — Crédito por modalidade (BCB/SGS).
- `prompts/fonte-08-arrecadacao-federal.md` — Arrecadação Federal (RFB).

**Para rodar:** abra uma conversa nova, cole o conteúdo do arquivo `prompts/fonte-XX-*.md`
inteiro como primeira mensagem. Cada prompt é independente — pode rodar em paralelo, em
janelas/sessões diferentes, sem uma interferir na outra.
