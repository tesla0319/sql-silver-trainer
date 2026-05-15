'use strict';

/* ==========================================================
   定数（config.py の値と同期させること）
   フロントエンドで弱点判定ロジックを再現するために必要。
   config.py の値を変更した場合はここも合わせて更新する。
   ========================================================== */
const MIN_ANSWERS    = 3;    // config.MIN_ANSWERS
const WEAK_THRESHOLD = 0.5;  // config.WEAK_THRESHOLD

/* ==========================================================
   状態管理
   ========================================================== */
const state = {
  mode:        'normal',  // 'normal' | 'weak'
  question:    null,      // 現在の問題オブジェクト（API レスポンス）
  selectedIds: new Set(), // 選択中の choice_id
  view:        'quiz',    // 'quiz' | 'result' | 'stats'
};

/* ==========================================================
   DOM ヘルパー
   ========================================================== */
const el = (id) => document.getElementById(id);

/* ==========================================================
   初期化
   ========================================================== */
document.addEventListener('DOMContentLoaded', () => {
  el('btn-normal').addEventListener('click', () => setMode('normal'));
  el('btn-weak').addEventListener('click',   () => setMode('weak'));
  el('btn-stats').addEventListener('click',  loadStats);
  el('btn-submit').addEventListener('click', submitAnswer);
  el('btn-next').addEventListener('click',   loadQuestion);
  el('btn-back').addEventListener('click',   loadQuestion);

  loadQuestion();
});

/* ==========================================================
   モード切替
   ========================================================== */
function setMode(mode) {
  state.mode = mode;
  el('btn-normal').classList.toggle('active', mode === 'normal');
  el('btn-weak').classList.toggle('active',   mode === 'weak');
  loadQuestion();
}

/* ==========================================================
   問題取得・表示
   ========================================================== */
async function loadQuestion() {
  setView('quiz');
  el('question-loading').hidden = false;
  el('question-card').hidden    = true;
  el('btn-submit').hidden       = false;
  el('btn-submit').disabled     = true;
  el('btn-submit').textContent  = '回答する';
  state.selectedIds.clear();
  removeError();

  try {
    const res = await fetch(`/api/questions/random?mode=${state.mode}`);
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail ?? `HTTP ${res.status}`);
    }
    state.question = await res.json();
    renderQuestion();
  } catch (err) {
    showError(`問題の取得に失敗しました: ${err.message}`);
  } finally {
    el('question-loading').hidden = true;
  }
}

function renderQuestion() {
  const q = state.question;

  // バッジ
  el('category-badge').textContent   = q.category;
  el('difficulty-badge').textContent = difficultyStars(q.difficulty);

  // 複数選択ヒント
  const hint = el('select-hint');
  if (q.multi_select_count > 1) {
    hint.textContent = `${q.multi_select_count}つ選んでください`;
    hint.hidden = false;
  } else {
    hint.hidden = true;
  }

  // 問題文（textContent: XSS 対策。white-space: pre-wrap でフォーマット保持）
  el('question-text').textContent = q.question_text;

  // 選択肢
  const choicesEl = el('choices');
  choicesEl.textContent = '';
  choicesEl.classList.toggle('is-multi', q.multi_select_count > 1);
  q.choices.forEach(c => choicesEl.appendChild(buildChoiceEl(c.id, c.choice_text)));

  el('question-card').hidden = false;
  updateSubmitButton();
}

function buildChoiceEl(id, text) {
  const div    = document.createElement('div');
  div.className    = 'choice';
  div.dataset.id   = String(id);

  const marker = document.createElement('span');
  marker.className = 'choice-marker';
  marker.setAttribute('aria-hidden', 'true');

  // textContent: XSS 対策（choice_text はユーザーに直接関係しないが念のため）
  const label      = document.createElement('span');
  label.className  = 'choice-label';
  label.textContent = text;

  div.append(marker, label);
  div.addEventListener('click', () => onChoiceClick(id));
  return div;
}

function onChoiceClick(id) {
  const isMulti = state.question.multi_select_count > 1;
  if (!isMulti) {
    state.selectedIds.clear();
    state.selectedIds.add(id);
  } else {
    if (state.selectedIds.has(id)) state.selectedIds.delete(id);
    else                           state.selectedIds.add(id);
  }

  document.querySelectorAll('.choice').forEach(c => {
    c.classList.toggle('is-selected', state.selectedIds.has(Number(c.dataset.id)));
  });

  updateSubmitButton();
}

function updateSubmitButton() {
  const q     = state.question;
  const count = state.selectedIds.size;
  const btn   = el('btn-submit');

  btn.disabled = (count === 0);

  if (q && q.multi_select_count > 1 && count > 0) {
    // 選択数カウンターで残り選択数を可視化
    btn.textContent = `回答する（${count} / ${q.multi_select_count} 選択中）`;
  } else {
    btn.textContent = '回答する';
  }
}

/* ==========================================================
   回答送信・判定
   ========================================================== */
async function submitAnswer() {
  el('btn-submit').disabled = true;

  try {
    const res = await fetch('/api/answers', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        question_id:         state.question.id,
        selected_choice_ids: [...state.selectedIds],
      }),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail ?? `HTTP ${res.status}`);
    }

    const result = await res.json();
    applyResultHighlights(result);
    renderResult(result);

  } catch (err) {
    showError(`回答の送信に失敗しました: ${err.message}`);
    el('btn-submit').disabled = false;
  }
}

/* 選択肢に正誤ハイライトを適用し、送信ボタンを非表示にする */
function applyResultHighlights(result) {
  const correctSet = new Set(result.correct_choice_ids);

  document.querySelectorAll('.choice').forEach(c => {
    const id = Number(c.dataset.id);
    c.classList.add('is-answered'); // pointer-events: none

    if (correctSet.has(id)) {
      c.classList.add('is-correct');  // 緑: 正解選択肢
    } else if (state.selectedIds.has(id)) {
      c.classList.add('is-wrong');    // 赤: 誤選択した選択肢
    }
    // 選択していない不正解選択肢はそのまま（グレーアウトしない）
  });

  el('btn-submit').hidden = true;
}

/* 結果バナー・解説・trap_reason をレンダリングして結果ビューに切り替える */
function renderResult(result) {
  const banner = el('result-banner');
  banner.textContent = result.is_correct ? '✓ 正解！' : '✗ 不正解';
  banner.className   = `result-banner ${result.is_correct ? 'is-correct' : 'is-wrong'}`;

  // explanation: 開発者が登録したコンテンツのため innerHTML でレンダリング
  // <pre><code>...</code></pre> の SQL コードブロックが有効になる
  el('explanation').innerHTML = result.explanation;

  // trap_reason: textContent で安全に表示
  const trapBox = el('trap-reason-box');
  if (result.trap_reason) {
    el('trap-reason-text').textContent = result.trap_reason;
    trapBox.hidden = false;
  } else {
    trapBox.hidden = true;
  }

  setView('result');
  // 結果セクションへスムーズスクロール（クイズセクションの下に続く）
  el('section-result').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ==========================================================
   苦手分析
   ========================================================== */
async function loadStats() {
  removeError();
  try {
    const res = await fetch('/api/stats/categories');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderStats(data.stats);
    setView('stats');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } catch (err) {
    showError(`統計の取得に失敗しました: ${err.message}`);
  }
}

function renderStats(stats) {
  const container = el('stats-content');
  container.textContent = '';

  if (stats.length === 0) {
    const msg = document.createElement('p');
    msg.className   = 'no-data';
    msg.textContent =
      'まだ回答データがありません。\n問題を解くとカテゴリ別の正答率が表示されます。\n（各カテゴリ3問以上の回答で苦手判定の対象になります）';
    container.appendChild(msg);
    return;
  }

  // 正答率の低い順にソート（苦手が上に表示される）
  const sorted = [...stats].sort((a, b) => a.accuracy - b.accuracy);

  sorted.forEach(s => {
    const pct        = Math.round(s.accuracy * 100);
    const enoughData = s.answered_count >= MIN_ANSWERS;
    const isWeak     = enoughData && s.accuracy < WEAK_THRESHOLD;

    const row = document.createElement('div');
    row.className = 'stat-row';

    // ラベル行
    const labelLine = document.createElement('div');
    labelLine.className = 'stat-label-line';

    const name = document.createElement('span');
    name.className   = 'stat-name';
    name.textContent = s.category;
    if (isWeak) {
      // 苦手カテゴリを視覚的に強調
      name.textContent = `⚠ ${s.category}`;
      name.style.color = 'var(--c-wrong)';
    }

    const detail = document.createElement('span');
    detail.className   = 'stat-detail';
    detail.textContent = `${pct}% (${s.correct_count} / ${s.answered_count})`;

    if (!enoughData) {
      const remaining = MIN_ANSWERS - s.answered_count;
      const note      = document.createElement('span');
      note.className   = 'stat-note';
      note.textContent = ` — あと${remaining}問で判定対象`;
      detail.appendChild(note);
    }

    labelLine.append(name, detail);

    // バー
    const track = document.createElement('div');
    track.className = 'stat-bar-track';

    const fill = document.createElement('div');
    fill.className = 'stat-bar-fill';
    fill.classList.add(!enoughData ? 'bar-pending' : isWeak ? 'bar-weak' : 'bar-good');
    fill.style.width = `${pct}%`;

    track.appendChild(fill);
    row.append(labelLine, track);
    container.appendChild(row);
  });
}

/* ==========================================================
   ビュー切替
   ========================================================== */
function setView(view) {
  state.view = view;
  // quiz セクションは quiz・result 両方で表示（選択肢ハイライトを見せるため）
  el('section-quiz').hidden   = (view === 'stats');
  el('section-result').hidden = (view !== 'result');
  el('section-stats').hidden  = (view !== 'stats');
}

/* ==========================================================
   ユーティリティ
   ========================================================== */
function difficultyStars(level) {
  const filled = Math.max(0, Math.min(3, level));
  return '★'.repeat(filled) + '☆'.repeat(3 - filled);
}

function showError(msg) {
  removeError();
  const div = document.createElement('div');
  div.id          = 'error-msg';
  div.className   = 'error-msg';
  div.textContent = msg;
  el('section-quiz').prepend(div);
  setTimeout(removeError, 6000);
}

function removeError() {
  const prev = el('error-msg');
  if (prev) prev.remove();
}
