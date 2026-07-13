/* ===== Painel Meios de Pagamento — Etapa 6 =====
   Consome docs/dados/meios_pagamento_mensal.json (gerado pela Etapa 5). */

const ARQUIVO_DADOS = "dados/meios_pagamento_mensal.json";
const CORES = {
  Pix: "#0ea5a4", TED: "#2563eb", Boleto: "#f59e0b",
  Cheque: "#8b5cf6", TEC: "#ec4899", DOC: "#94a3b8",
};
const OCULTAR_INICIAL = ["DOC", "TEC"]; // legados ~zerados: começam desligados no gráfico

let dados = null;
let metrica = "valor"; // "valor" | "quantidade"
let graficoEvolucao = null;
let graficoParticipacao = null;

// ---------- Formatação ----------
const nf = (casas = 1) => new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: casas, maximumFractionDigits: casas,
});

/** valor em R$ milhões -> texto compacto. */
function fmtValor(x) {
  if (x == null) return "—";
  const abs = Math.abs(x);
  if (abs >= 1e6) return `R$ ${nf(2).format(x / 1e6)} tri`;
  if (abs >= 1e3) return `R$ ${nf(1).format(x / 1e3)} bi`;
  return `R$ ${nf(0).format(x)} mi`;
}

/** quantidade em milhares -> texto compacto. */
function fmtQtd(x) {
  if (x == null) return "—";
  const abs = Math.abs(x);
  if (abs >= 1e6) return `${nf(2).format(x / 1e6)} bi`;
  if (abs >= 1e3) return `${nf(1).format(x / 1e3)} mi`;
  return `${nf(0).format(x)} mil`;
}

const fmtMetrica = (x) => (metrica === "valor" ? fmtValor(x) : fmtQtd(x));

function fmtPct(x, comSinal = false) {
  if (x == null) return "—";
  const s = comSinal && x > 0 ? "+" : "";
  return `${s}${nf(1).format(x)}%`;
}

function fmtMesAno(anoMes) {
  const [a, m] = anoMes.split("-");
  const meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
  return `${meses[Number(m) - 1]}/${a}`;
}

const cssVar = (nome) => getComputedStyle(document.body).getPropertyValue(nome).trim();

// ---------- Renderização ----------
function renderCabecalho() {
  const meta = dados.meta;
  document.getElementById("descricao-fonte").textContent = meta.descricao;
  document.getElementById("meta-info").textContent =
    `Período: ${fmtMesAno(meta.periodo.inicio)} – ${fmtMesAno(meta.periodo.fim)} · `
    + `${dados.kpis.totais.meses_cobertos} meses · Atualizado em `
    + `${new Date(meta.gerado_em).toLocaleDateString("pt-BR")}`;
  document.getElementById("rodape-fonte").textContent = `Fonte: ${meta.fonte}.`;
}

function renderKpis() {
  const t = dados.kpis.totais;
  const lider = dados.kpis.por_forma[0];
  const alvo = document.getElementById("kpis");
  const cartoes = [
    {
      rotulo: `Valor movimentado (${fmtMesAno(t.mes_ref)})`,
      valor: fmtValor(t.valor_ultimo_mes),
      apoio: "Soma de todas as formas no mês de referência",
    },
    {
      rotulo: `Transações (${fmtMesAno(t.mes_ref)})`,
      valor: fmtQtd(t.qtd_ultimo_mes),
      apoio: "Total de transações no mês de referência",
    },
    {
      rotulo: "Forma líder (valor acumulado)",
      valor: lider.forma,
      apoio: `${fmtPct(lider.part_valor_pct)} do valor no período`,
    },
    {
      rotulo: `Líder — crescimento YoY`,
      valor: fmtPct(lider.yoy_valor_pct, true),
      apoio: `${lider.forma} vs. mesmo mês do ano anterior`,
      classe: lider.yoy_valor_pct == null ? "" : (lider.yoy_valor_pct >= 0 ? "pos" : "neg"),
    },
  ];
  alvo.innerHTML = cartoes.map((c) => `
    <div class="kpi">
      <p class="rotulo">${c.rotulo}</p>
      <p class="valor">${c.valor}</p>
      <p class="apoio ${c.classe || ""}">${c.apoio}</p>
    </div>`).join("");
}

function renderEvolucao() {
  const ctx = document.getElementById("gEvolucao");
  const datasets = dados.formas.map((forma) => ({
    label: forma,
    data: dados.series[forma][metrica],
    borderColor: CORES[forma],
    backgroundColor: CORES[forma],
    borderWidth: 2,
    pointRadius: 0,
    pointHoverRadius: 4,
    tension: 0.3,
    hidden: OCULTAR_INICIAL.includes(forma),
  }));

  document.getElementById("titulo-evolucao").textContent =
    metrica === "valor"
      ? "Valor movimentado por forma (R$), por mês."
      : "Quantidade de transações por forma, por mês.";

  if (graficoEvolucao) graficoEvolucao.destroy();
  graficoEvolucao = new Chart(ctx, {
    type: "line",
    data: { labels: dados.labels.map(fmtMesAno), datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { labels: { color: cssVar("--texto"), usePointStyle: true, boxWidth: 8 } },
        tooltip: {
          callbacks: { label: (i) => `${i.dataset.label}: ${fmtMetrica(i.parsed.y)}` },
        },
      },
      scales: {
        x: {
          ticks: { color: cssVar("--texto-suave"), maxTicksLimit: 12, autoSkip: true },
          grid: { display: false },
        },
        y: {
          ticks: { color: cssVar("--texto-suave"), callback: (v) => fmtMetrica(v) },
          grid: { color: cssVar("--borda") },
        },
      },
    },
  });
}

function renderParticipacao() {
  const ctx = document.getElementById("gParticipacao");
  const campo = metrica === "valor" ? "valor_total" : "qtd_total";
  const itens = [...dados.kpis.por_forma].sort((a, b) => b[campo] - a[campo]);
  const total = itens.reduce((s, x) => s + x[campo], 0);

  document.getElementById("titulo-participacao").textContent =
    metrica === "valor"
      ? "Fatia de cada forma no valor acumulado."
      : "Fatia de cada forma na quantidade acumulada.";

  if (graficoParticipacao) graficoParticipacao.destroy();
  graficoParticipacao = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: itens.map((x) => x.forma),
      datasets: [{
        data: itens.map((x) => x[campo]),
        backgroundColor: itens.map((x) => CORES[x.forma]),
        borderColor: cssVar("--superficie"),
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "58%",
      plugins: {
        legend: { position: "bottom", labels: { color: cssVar("--texto"), usePointStyle: true, boxWidth: 8 } },
        tooltip: {
          callbacks: {
            label: (i) => {
              const pct = total ? (i.parsed / total) * 100 : 0;
              const bruto = metrica === "valor" ? fmtValor(i.parsed) : fmtQtd(i.parsed);
              return `${i.label}: ${bruto} (${fmtPct(pct)})`;
            },
          },
        },
      },
    },
  });
}

function pilulaForma(forma) {
  return `<span class="pilula"><span class="ponto" style="background:${CORES[forma]}"></span>${forma}</span>`;
}

function cls(x) { return x == null ? "nulo" : x >= 0 ? "pos" : "neg"; }

function renderTabelaRanking() {
  const corpo = document.querySelector("#tabela-ranking tbody");
  corpo.innerHTML = dados.kpis.por_forma.map((f) => `
    <tr>
      <td>${pilulaForma(f.forma)}</td>
      <td class="num">${fmtPct(f.part_valor_pct)}</td>
      <td class="num">${fmtPct(f.part_qtd_pct)}</td>
      <td class="num">${fmtValor(f.valor_ultimo)}</td>
      <td class="num ${cls(f.yoy_valor_pct)}">${fmtPct(f.yoy_valor_pct, true)}</td>
      <td class="num ${cls(f.cagr_valor_aa_pct)}">${fmtPct(f.cagr_valor_aa_pct, true)}</td>
      <td class="num">${f.ticket_medio_ultimo_rs == null ? "—" : "R$ " + nf(2).format(f.ticket_medio_ultimo_rs)}</td>
    </tr>`).join("");
}

function renderTabelaEstatistica() {
  const corpo = document.querySelector("#tabela-estatistica tbody");
  const fmt = metrica === "valor" ? fmtValor : fmtQtd;
  document.getElementById("titulo-estatistica").textContent =
    `Sobre a série mensal de cada forma — métrica: ${metrica === "valor" ? "valor (R$)" : "quantidade"}.`;
  corpo.innerHTML = dados.formas.map((forma) => {
    const e = dados.estatisticas[forma][metrica];
    return `
      <tr>
        <td>${pilulaForma(forma)}</td>
        <td class="num">${fmt(e.media)}</td>
        <td class="num">${fmt(e.mediana)}</td>
        <td class="num">${fmt(e.desvio_padrao)}</td>
        <td class="num">${fmtPct(e.coef_variacao_pct)}</td>
        <td class="num">${fmt(e.minimo)}</td>
        <td class="num">${fmt(e.maximo)}</td>
      </tr>`;
  }).join("");
}

function renderMetricaDependente() {
  renderEvolucao();
  renderParticipacao();
  renderTabelaEstatistica();
}

function ligarAlternador() {
  document.querySelectorAll(".alt-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (btn.dataset.metrica === metrica) return;
      document.querySelectorAll(".alt-btn").forEach((b) => b.classList.remove("ativo"));
      btn.classList.add("ativo");
      metrica = btn.dataset.metrica;
      renderMetricaDependente();
    });
  });
}

async function iniciar() {
  try {
    const resp = await fetch(ARQUIVO_DADOS);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    dados = await resp.json();
  } catch (erro) {
    document.getElementById("meta-info").textContent =
      "Não foi possível carregar os dados. Rode o pipeline (python run_pipeline.py) para gerar "
      + `${ARQUIVO_DADOS}.`;
    console.error(erro);
    return;
  }
  renderCabecalho();
  renderKpis();
  renderTabelaRanking();
  renderMetricaDependente();
  ligarAlternador();
}

iniciar();
