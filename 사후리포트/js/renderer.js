/* =============================================================
   DAKER 사후 리포트 렌더러 (Sprint 3)
   Vanilla JS — JSON 데이터를 DOM 섹션으로 주입
   ============================================================= */

/* ---------- 유틸 ---------- */

function esc(v) {
  if (v === null || v === undefined) return '';
  return String(v)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function isEmpty(v) {
  return v === null || v === undefined || (typeof v === 'string' && v.trim() === '');
}

function fmtDate(iso) {
  if (isEmpty(iso)) return '';
  const m = String(iso).match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return iso;
  return `${m[1]}.${m[2]}.${m[3]}`;
}

function fmtDateRange(start, end) {
  if (isEmpty(start)) return '';
  if (isEmpty(end) || start === end) return fmtDate(start);
  return `${fmtDate(start)} ~ ${fmtDate(end)}`;
}

function $(sel, root = document) {
  return root.querySelector(sel);
}

function byId(id) {
  return document.getElementById(id);
}

/* ---------- 순위 계산 (CR-3.3) ---------- */

function computeTeamRanks(report) {
  const teamMap = {};
  (report.teams || []).forEach(t => {
    teamMap[t.id] = { id: t.id, name: t.name, totalScore: 0, rank: 0 };
  });
  const criteria = (report.evaluation && report.evaluation.criteria) || [];
  criteria.forEach(c => {
    (c.teamScores || []).forEach(ts => {
      if (!teamMap[ts.teamId]) {
        teamMap[ts.teamId] = { id: ts.teamId, name: ts.teamId, totalScore: 0, rank: 0 };
      }
      teamMap[ts.teamId].totalScore += Number(ts.score) || 0;
    });
  });
  const ranked = Object.values(teamMap).sort((a, b) => b.totalScore - a.totalScore);
  ranked.forEach((t, i) => { t.rank = i + 1; });
  return ranked;
}

/* ---------- 섹션별 렌더러 ---------- */

function renderCover(data) {
  const root = $('.report-section.cover');
  if (!root) return;
  const ev = data.event || {};
  const titleEl = $('.cover-title', root);
  const subEl = $('.cover-subtitle', root);
  const kickerEl = $('.cover-kicker', root);
  const brandEl = $('.cover-top .brand', root);
  const kindEl = $('.cover-top .cover-kind');

  if (titleEl) titleEl.textContent = ev.eventName || '';
  if (subEl) {
    if (isEmpty(ev.coverSubtitle)) {
      subEl.style.display = 'none'; // CR-3.4 empty handling
    } else {
      subEl.style.display = '';
      subEl.textContent = ev.coverSubtitle;
    }
  }
  if (kickerEl) {
    const kickerLabel = eventTypeLabel(data.eventType);
    if (isEmpty(kickerLabel)) {
      kickerEl.hidden = true; // CR-3.4 empty handling
    } else {
      kickerEl.hidden = false;
      kickerEl.textContent = kickerLabel;
    }
  }
  if (brandEl) brandEl.textContent = `DAKER · ${ev.operator || '데이커'}`;

  const meta = $('.cover-meta', root);
  if (meta) {
    meta.innerHTML = `
      <div class="cell"><div class="k">주최</div><div class="v">${esc(ev.client || '-')}</div></div>
      <div class="cell"><div class="k">운영</div><div class="v">${esc(ev.operator || 'DAKER')}</div></div>
      <div class="cell"><div class="k">일정</div><div class="v">${esc(fmtDateRange(ev.startDate, ev.endDate))}</div></div>
    `;
  }
}

function eventTypeLabel(type) {
  switch (type) {
    case 'hackathon': return '해커톤 사후 리포트';
    case 'education': return '학습 프로그램 사후 리포트';
    case 'group-activity': return '그룹 활동 사후 리포트';
    default: return '사후 리포트';
  }
}

function renderTableOfContents(data) {
  const root = $('.report-section.toc');
  if (!root) return;
  const list = $('.toc-list', root);
  if (!list) return;

  const items = [
    { num: '01', label: '행사 개요', page: '03' },
    { num: '02', label: '참가자 · 팀 통계', page: '04' },
    { num: '03', label: '활동 타임라인', page: '05' },
    { num: '04', label: '우수 산출물 하이라이트', page: '06' },
    { num: '05', label: '평가 결과', page: '07' },
    { num: '06', label: '운영 회고', page: '08' },
    { num: '07', label: '부록 · 팀 카드', page: '09' },
    { num: '08', label: '부록 · 참가자 명단', page: '10' },
  ];
  list.innerHTML = items.map(it => `
    <li class="toc-row">
      <span class="num">${it.num}</span>
      <span class="label">${esc(it.label)}</span>
      <span class="dots"></span>
      <span class="pg">${it.page}</span>
    </li>
  `).join('');
}

function renderOverview(data) {
  const root = $('.report-section.overview');
  if (!root) return;
  const ov = data.overview || {};
  const ev = data.event || {};

  const grid = $('.grid-2', root);
  if (grid) {
    const cards = [
      { h: '행사 목적', p: ov.purpose },
      { h: '운영 일정', p: ov.scheduleSummary },
      { h: '장소', p: ev.location },
      { h: '주요 목표', p: (ov.goals || []).join(' · ') },
    ].filter(c => !isEmpty(c.p));
    grid.innerHTML = cards.map(c => `
      <div class="card">
        <h4>${esc(c.h)}</h4>
        <p>${esc(c.p)}</p>
      </div>
    `).join('');
  }

  const statsGrid = $('.grid-4', root);
  if (statsGrid) {
    const metrics = ov.keyMetrics || [];
    if (metrics.length === 0) {
      statsGrid.style.display = 'none'; // CR-3.4 empty handling
    } else {
      statsGrid.style.display = '';
      statsGrid.innerHTML = metrics.map(m => `
        <div class="stat-card">
          <div class="k">${esc(m.label)}</div>
          <div class="v">${esc(m.value)}${m.unit ? `<span class="u">${esc(m.unit)}</span>` : ''}</div>
        </div>
      `).join('');
    }
  }
}

function renderStats(data) {
  const root = $('.report-section.stats');
  if (!root) return;
  const stats = data.stats || {};

  const statGrid = $('.grid-4', root);
  if (statGrid) {
    const avgTeam = stats.totalTeams
      ? (stats.totalParticipants / stats.totalTeams).toFixed(1)
      : '-';
    const cards = [
      { k: '총 인원', v: stats.totalParticipants, u: '명' },
      { k: '참여 팀', v: stats.totalTeams, u: '팀' },
      { k: '완주율', v: stats.completionRate, u: '%' },
      { k: '참여율', v: stats.engagementRate, u: '%' },
    ];
    statGrid.innerHTML = cards.map(c => {
      if (isEmpty(c.v)) {
        return `<div class="stat-card" hidden><div class="k">${esc(c.k)}</div><div class="v">-</div></div>`;
      }
      return `<div class="stat-card"><div class="k">${esc(c.k)}</div><div class="v">${esc(c.v)}<span class="u">${esc(c.u)}</span></div></div>`;
    }).join('');
  }

  const bar = $('.bar-chart', root);
  if (bar) {
    const breakdown = stats.organizationBreakdown || [];
    const max = Math.max(1, ...breakdown.map(b => Number(b.count) || 0));
    bar.innerHTML = breakdown.map(b => {
      const pct = Math.round(((Number(b.count) || 0) / max) * 100);
      return `
        <div class="bar-row">
          <span class="name">${esc(b.organization)}</span>
          <span class="track"><span class="fill" style="width:${pct}%;"></span></span>
          <span class="val">${esc(b.count)}명</span>
        </div>
      `;
    }).join('');
  }
}

function renderTimeline(data) {
  const root = $('.report-section.timeline-section');
  if (!root) return;
  const tl = $('.timeline', root);
  if (!tl) return;
  const items = data.timeline || [];
  tl.innerHTML = items.map(it => {
    const hasDesc = !isEmpty(it.description);
    return `
      <div class="timeline-item">
        <div class="when">${esc(fmtDate(it.date))}${it.time ? ' · ' + esc(it.time) : ''}</div>
        <div class="label">${esc(it.label)}</div>
        ${hasDesc ? `<div class="desc">${esc(it.description)}</div>` : ''}
      </div>
    `;
  }).join('');
}

function renderHighlights(data) {
  const root = $('.report-section.highlights');
  if (!root) return;
  const highlights = data.highlights || [];
  const teamsById = {};
  (data.teams || []).forEach(t => { teamsById[t.id] = t; });

  // Clear existing cards and re-insert
  const cards = root.querySelectorAll('.highlight-card');
  cards.forEach(c => c.remove());

  const subtitle = $('.section-subtitle', root);
  const footer = $('.report-footer', root);
  const frag = document.createDocumentFragment();
  highlights.slice(0, 3).forEach((h, idx) => {
    const team = teamsById[h.teamId] || {};
    const card = document.createElement('div');
    card.className = `highlight-card rank-${idx + 1}`;
    card.innerHTML = `
      <span class="award">${esc(h.award || '-')}</span>
      <h4>${esc(h.title)}</h4>
      <div class="team-name">${esc(team.name || h.teamId || '')}</div>
      <p>${esc(h.description)}</p>
    `;
    frag.appendChild(card);
  });
  if (footer) {
    root.insertBefore(frag, footer);
  } else if (subtitle) {
    subtitle.parentNode.appendChild(frag);
  } else {
    root.appendChild(frag);
  }
}

function renderEvaluation(data) {
  const root = $('.report-section.evaluation');
  if (!root) return;
  const table = $('.eval-table', root);
  if (!table) return;
  const criteria = (data.evaluation && data.evaluation.criteria) || [];
  const teams = data.teams || [];
  const teamsById = {};
  teams.forEach(t => { teamsById[t.id] = t; });

  // header
  const thead = `
    <thead>
      <tr>
        <th>순위</th>
        <th>팀명</th>
        ${criteria.map(c => `<th class="num">${esc(c.criterion)}</th>`).join('')}
        <th class="num">총점</th>
      </tr>
    </thead>
  `;

  // compute ranks
  const ranks = computeTeamRanks(data); // sorted desc
  const teamIds = ranks.map(r => r.id);
  const rows = ranks.map(rEntry => {
    const scoresPerCriterion = criteria.map(c => {
      const ts = (c.teamScores || []).find(s => s.teamId === rEntry.id);
      return ts ? Number(ts.score) : 0;
    });
    const teamName = (teamsById[rEntry.id] && teamsById[rEntry.id].name) || rEntry.name || rEntry.id;
    return `
      <tr class="rank-row">
        <td>${rEntry.rank}</td>
        <td>${esc(teamName)}</td>
        ${scoresPerCriterion.map(s => `<td class="num">${s}</td>`).join('')}
        <td class="num">${rEntry.totalScore}</td>
      </tr>
    `;
  }).join('');

  table.innerHTML = thead + `<tbody>${rows}</tbody>`;
}

function renderRetrospective(data) {
  const root = $('.report-section.retrospective');
  if (!root) return;
  const items = data.retrospective || [];

  const groupsMap = {
    '성과': { cls: 'ok', label: '잘된 점' },
    '개선': { cls: 'fix', label: '보완할 점' },
    '제안': { cls: 'idea', label: '차기 행사 제안' },
  };

  const existing = root.querySelectorAll('.retro-group');
  existing.forEach(e => e.remove());

  const footer = $('.report-footer', root);
  const frag = document.createDocumentFragment();

  Object.keys(groupsMap).forEach(cat => {
    const entries = items.filter(it => it.category === cat);
    const group = document.createElement('div');
    group.className = `retro-group ${groupsMap[cat].cls}`;
    if (entries.length === 0) {
      group.hidden = true; // CR-3.4 empty handling
    }
    group.innerHTML = `
      <h4><span class="chip">${esc(cat)}</span> ${esc(groupsMap[cat].label)}</h4>
      ${entries.map(e => `<div class="retro-item">${esc(e.content)}</div>`).join('')}
    `;
    frag.appendChild(group);
  });

  if (footer) {
    root.insertBefore(frag, footer);
  } else {
    root.appendChild(frag);
  }
}

function renderTeamCards(data) {
  const root = $('.report-section.team-cards');
  if (!root) return;
  const grid = $('.team-grid', root);
  if (!grid) return;

  const ranks = computeTeamRanks(data);
  const rankById = {};
  ranks.forEach(r => { rankById[r.id] = r; });

  const teams = (data.teams || []).slice().sort((a, b) => {
    const ra = rankById[a.id] ? rankById[a.id].rank : 999;
    const rb = rankById[b.id] ? rankById[b.id].rank : 999;
    return ra - rb;
  });

  grid.innerHTML = teams.map(t => {
    const rank = rankById[t.id] ? rankById[t.id].rank : t.rank || '-';
    const total = rankById[t.id] ? rankById[t.id].totalScore : t.score || 0;
    const members = (t.members || []).map(m => m.name).join(', ');
    const output = t.output || {};
    return `
      <div class="team-card">
        <div class="team-head">
          <span class="team-name">${esc(t.name)}</span>
          <span class="team-rank">${esc(rank)}위 · ${esc(total)}점</span>
        </div>
        <div class="team-topic">${esc(output.title || '')}</div>
        <p class="team-desc">${esc(output.summary || t.highlight || '')}</p>
        <div class="team-members"><strong>구성원</strong> · ${esc(members)}</div>
      </div>
    `;
  }).join('');
}

function renderParticipants(data) {
  const root = $('.report-section.participants');
  if (!root) return;
  const table = $('.participants-table tbody', root);
  if (!table) return;
  const teamsById = {};
  (data.teams || []).forEach(t => { teamsById[t.id] = t; });
  const participants = data.participants || [];
  table.innerHTML = participants.map(p => {
    const teamLabel = (teamsById[p.team] && teamsById[p.team].name) || p.team || '-';
    return `
      <tr class="participant-row">
        <td>${esc(p.name)}</td>
        <td>${esc(teamLabel)}</td>
        <td>${esc(p.role)}</td>
        <td>${esc(p.organization)}</td>
      </tr>
    `;
  }).join('');
}

/* ---------- 파이프라인 ---------- */

function renderAll(data) {
  try {
    renderCover(data);
    renderTableOfContents(data);
    renderOverview(data);
    renderStats(data);
    renderTimeline(data);
    renderHighlights(data);
    renderEvaluation(data);
    renderRetrospective(data);
    renderTeamCards(data);
    renderParticipants(data);
    document.documentElement.setAttribute('data-report-ready', '1');
  } catch (err) {
    console.error('[renderer] render failed:', err);
  }
}

async function loadReport(jsonPath) {
  // CR-3.1: fetch → JSON.parse → render pipeline
  const res = await fetch(jsonPath, { cache: 'no-store' });
  if (!res.ok) throw new Error(`Failed to load ${jsonPath}: ${res.status}`);
  const text = await res.text();
  const data = JSON.parse(text);
  renderAll(data);
  return data;
}

function renderInline(data) {
  renderAll(data);
  return data;
}

/* ---------- 엔트리 ---------- */

function getDataPathFromQuery() {
  try {
    const qs = new URLSearchParams(window.location.search);
    return qs.get('data') || './data/sample-hackathon.json';
  } catch (_) {
    return './data/sample-hackathon.json';
  }
}

function boot() {
  // 인라인 데이터 스크립트가 있으면 우선 사용 (Sprint 4에서 사용)
  const inline = document.getElementById('report-data');
  if (inline && inline.textContent && inline.textContent.trim().length > 0) {
    try {
      const data = JSON.parse(inline.textContent);
      renderInline(data);
      return;
    } catch (e) {
      console.error('[renderer] inline JSON parse failed:', e);
    }
  }
  const path = getDataPathFromQuery();
  loadReport(path).catch(err => {
    console.error('[renderer] loadReport failed:', err);
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}

// Expose for testing
window.DakerReport = {
  loadReport,
  renderAll,
  renderInline,
  renderCover,
  renderTableOfContents,
  renderOverview,
  renderStats,
  renderTimeline,
  renderHighlights,
  renderEvaluation,
  renderRetrospective,
  renderTeamCards,
  renderParticipants,
  computeTeamRanks,
};
