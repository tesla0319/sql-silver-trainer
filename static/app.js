'use strict';

/* ==========================================================
   定数（config.py の値と同期させること）
   ========================================================== */
const MIN_ANSWERS    = 3;
const WEAK_THRESHOLD = 0.5;

/* localStorage キー */
const LS_USER_NAME = 'sql_silver_user_name';
const LS_THEME     = 'sql_silver_theme';

/* ==========================================================
   状態管理
   ========================================================== */
const state = {
  mode:        'normal',   // 'normal' | 'weak' | 'review'
  question:    null,       // 現在の問題オブジェクト
  selectedIds: new Set(),  // 選択中の choice_id

  // セッション除外制御（同一問題連続防止・問題暗記防止）
  // セッション中に出題済みの question_id を保持する
  // 全問消化後はリセットし、直前問題IDのみ残す（連続防止）
  sessionExcludeIds: new Set(),
  lastQuestionId:    null,

  // セッション統計（ページリロードまで累積）
  sessionAnswered: 0,
  sessionCorrect:  0,
  streak:          0,  // 連続正解数

  // ユーザー名（localStorage から読み込む。未設定時は入力画面を表示）
  userName: 'guest',

  view: 'quiz',  // 'quiz' | 'result' | 'stats' | 'training-result'

  // 10問トレーニング セッション状態
  trainingCount:     0,   // 現セッションの回答数 (0–10)
  trainingCorrect:   0,   // 正答数
  trainingLog:       [],  // [{category, is_correct}, ...] 直近10問（テーマ判定に使用）
  trainingCatCounts: {},  // normal mode 偏り抑制: { 'VIEW': 2, ... }
  trainingLastCats:  [],  // 3連続チェック用: 直近2カテゴリ
  trainingFinished:  false, // 10問完了フラグ（btn-next の動作切替に使用）
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
  el('btn-review').addEventListener('click', () => setMode('review'));
  el('btn-stats').addEventListener('click',  loadStats);
  el('btn-submit').addEventListener('click', submitAnswer);
  el('btn-next').addEventListener('click',   onNextClick);
  el('btn-back').addEventListener('click',   loadQuestion);
  el('btn-retry').addEventListener('click',  onRetry);
  el('btn-end').addEventListener('click',    onEnd);

  el('btn-set-username').addEventListener('click', onSetUsername);
  el('input-username').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') onSetUsername();
  });

  // キーボードショートカット: Enter キーで「次の問題へ」または「結果を見る」
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && state.view === 'result' && !e.repeat) {
      onNextClick();
    }
  });

  // localStorage からテーマを復元（ユーザー名より先に適用してレイアウトシフトを防ぐ）
  const savedTheme = localStorage.getItem(LS_THEME);
  if (savedTheme) applyTheme(savedTheme);

  // localStorage からユーザー名を復元
  const saved = localStorage.getItem(LS_USER_NAME);
  if (saved) {
    state.userName = saved;
    updateUserDisplay();
    loadQuestion();
  } else {
    showUsernameSection();
  }
});

/* ==========================================================
   ニックネーム設定
   ========================================================== */
function showUsernameSection() {
  el('section-username').hidden = false;
  el('section-quiz').hidden     = true;
  el('section-result').hidden   = true;
  el('section-stats').hidden    = true;
}

function onSetUsername() {
  const raw  = el('input-username').value;
  const name = raw.trim();
  const errEl = el('username-error');

  if (!name) {
    errEl.textContent = 'ニックネームを入力してください（空白のみは不可）。';
    errEl.hidden = false;
    return;
  }

  errEl.hidden = true;
  state.userName = name;
  localStorage.setItem(LS_USER_NAME, name);
  updateUserDisplay();
  loadQuestion();
}

function updateUserDisplay() {
  el('user-display').textContent = `👤 ${state.userName}`;
}

/* ==========================================================
   モード切替
   ========================================================== */
function setMode(mode) {
  state.mode = mode;
  el('btn-normal').classList.toggle('active', mode === 'normal');
  el('btn-weak').classList.toggle('active',   mode === 'weak');
  el('btn-review').classList.toggle('active', mode === 'review');
  resetTrainingSession();  // モード切替 = 新しい10問セッション開始
  loadQuestion();
}

/* ==========================================================
   問題取得・表示
   ========================================================== */
async function loadQuestion() {
  // normal mode = session テーマを復元、weak/review = normal 固定（補助学習空間）
  if (state.mode === 'normal') {
    restoreSessionTheme();
  } else {
    applyThemeVisual('normal');
  }
  setView('quiz');
  el('question-loading').hidden = false;
  el('question-card').hidden    = true;
  el('btn-submit').hidden       = false;
  el('btn-submit').disabled     = true;
  el('btn-submit').textContent  = '回答する';
  state.selectedIds.clear();
  removeError();

  try {
    const url = buildQuestionUrl();
    const res = await fetch(url);
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail ?? `HTTP ${res.status}`);
    }
    state.question = await res.json();

    // セッション完了検知:
    // 返ってきた question.id が sessionExcludeIds に含まれている
    // → 全問消化してAPIがフォールバック → セッションリセット
    if (state.sessionExcludeIds.has(state.question.id)) {
      state.sessionExcludeIds = new Set();
      // 直前問題のみ残して連続出題を防ぐ
      if (state.lastQuestionId !== null) {
        state.sessionExcludeIds.add(state.lastQuestionId);
      }
    }
    state.lastQuestionId = state.question.id;

    renderQuestion();
  } catch (err) {
    showError(`問題の取得に失敗しました: ${err.message}`);
  } finally {
    el('question-loading').hidden = true;
  }
}

function buildQuestionUrl() {
  const params = new URLSearchParams({ mode: state.mode, user_name: state.userName });
  // セッション除外IDを全て exclude_ids として送信（同一問題の再出題防止）
  state.sessionExcludeIds.forEach(id => params.append('exclude_ids', id));
  // normal mode のみカテゴリ偏り抑制を適用
  if (state.mode === 'normal') {
    getBannedCategories().forEach(cat => params.append('excluded_categories', cat));
  }
  return `/api/questions/random?${params.toString()}`;
}

function getBannedCategories() {
  const banned = new Set();
  // 同カテゴリ2問到達したカテゴリを除外
  Object.entries(state.trainingCatCounts).forEach(([cat, count]) => {
    if (count >= 2) banned.add(cat);
  });
  // 3連続チェック: 直近2カテゴリが同じなら追加で除外
  if (state.trainingLastCats.length >= 2) {
    const [a, b] = state.trainingLastCats.slice(-2);
    if (a === b) banned.add(a);
  }
  return [...banned];
}

function renderQuestion() {
  const q = state.question;

  el('category-badge').textContent   = q.category;
  el('difficulty-badge').textContent = difficultyStars(q.difficulty);
  renderModeBadge();

  // 複数選択ヒント
  const hint = el('select-hint');
  if (q.multi_select_count > 1) {
    hint.textContent = `${q.multi_select_count}つ選んでください`;
    hint.hidden = false;
  } else {
    hint.hidden = true;
  }

  el('question-text').textContent = q.question_text;

  const choicesEl = el('choices');
  choicesEl.textContent = '';
  choicesEl.classList.toggle('is-multi', q.multi_select_count > 1);
  q.choices.forEach(c => choicesEl.appendChild(buildChoiceEl(c.id, c.choice_text)));

  el('question-card').hidden = false;
  updateSubmitButton();
}

function renderModeBadge() {
  const badge = el('mode-badge');
  if (state.mode === 'weak') {
    badge.textContent = '⚠ 苦手克服中';
    badge.className   = 'badge badge-mode badge-mode-weak';
    badge.hidden      = false;
  } else if (state.mode === 'review') {
    badge.textContent = '↩ 復習中';
    badge.className   = 'badge badge-mode badge-mode-review';
    badge.hidden      = false;
  } else {
    badge.hidden = true;
  }
}

function buildChoiceEl(id, text) {
  const div    = document.createElement('div');
  div.className    = 'choice';
  div.dataset.id   = String(id);

  const marker = document.createElement('span');
  marker.className = 'choice-marker';
  marker.setAttribute('aria-hidden', 'true');

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
        user_name:           state.userName,
      }),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail ?? `HTTP ${res.status}`);
    }

    const result = await res.json();

    // セッション除外リストに追加（回答後に追加することで、答える前に出題されることを防ぐ）
    state.sessionExcludeIds.add(state.question.id);

    // セッション統計を更新
    state.sessionAnswered++;
    if (result.is_correct) {
      state.sessionCorrect++;
      state.streak++;
    } else {
      state.streak = 0;
    }
    updateSessionStats();

    applyResultHighlights(result);
    renderResult(result);
    updateTrainingState(result.is_correct);  // トレーニング状態更新（テーマ・10問判定を含む）

  } catch (err) {
    showError(`回答の送信に失敗しました: ${err.message}`);
    el('btn-submit').disabled = false;
  }
}

function applyResultHighlights(result) {
  const correctSet = new Set(result.correct_choice_ids);

  document.querySelectorAll('.choice').forEach(c => {
    const id = Number(c.dataset.id);
    c.classList.add('is-answered');
    if (correctSet.has(id))               c.classList.add('is-correct');
    else if (state.selectedIds.has(id))   c.classList.add('is-wrong');
  });

  el('btn-submit').hidden = true;
}

function renderResult(result) {
  const banner = el('result-banner');
  banner.textContent = result.is_correct ? '✓ 正解！' : '✗ 不正解';
  banner.className   = `result-banner ${result.is_correct ? 'is-correct' : 'is-wrong'}`;

  el('explanation').innerHTML = result.explanation;

  const trapBox = el('trap-reason-box');
  if (result.trap_reason) {
    el('trap-reason-text').textContent = result.trap_reason;
    trapBox.hidden = false;
  } else {
    trapBox.hidden = true;
  }

  setView('result');
  el('section-result').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ==========================================================
   10問トレーニング制御
   ========================================================== */
function updateTrainingState(is_correct) {
  const cat = state.question.category;

  state.trainingCount++;
  if (is_correct) state.trainingCorrect++;

  // trainingLog: 直近10問を常に保持（テーマ判定用）
  state.trainingLog.push({ category: cat, is_correct });
  if (state.trainingLog.length > 10) state.trainingLog.shift();

  // normal mode: カテゴリ偏り抑制のための追跡
  if (state.mode === 'normal') {
    state.trainingCatCounts[cat] = (state.trainingCatCounts[cat] || 0) + 1;
    state.trainingLastCats.push(cat);
    if (state.trainingLastCats.length > 2) state.trainingLastCats.shift();
  }

  if (state.trainingCount >= 10) {
    state.trainingFinished = true;
    el('btn-next').textContent = '結果を見る';
  }
}

function showTrainingResult() {
  updateThemeFromTraining();  // セッション結果確定時のみテーマを更新
  const log    = state.trainingLog;
  const total  = log.length;
  const correct = log.filter(r => r.is_correct).length;
  const pct    = total > 0 ? Math.round(correct / total * 100) : 0;

  // セッション内の不正解をカテゴリ別に集計（上位3件）
  const catErrors = {};
  log.forEach(r => {
    if (!r.is_correct) catErrors[r.category] = (catErrors[r.category] || 0) + 1;
  });
  const weakCats = Object.entries(catErrors)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3);

  const summary = el('training-summary');
  summary.textContent = '';

  const score = document.createElement('p');
  score.className   = 'training-score';
  score.textContent = `正解 ${correct} / ${total}問（${pct}%）`;
  summary.appendChild(score);

  if (weakCats.length > 0) {
    const label = document.createElement('p');
    label.className   = 'training-weak-label';
    label.textContent = '今回の苦手カテゴリ';
    summary.appendChild(label);

    const list = document.createElement('ul');
    list.className = 'training-weak-list';
    weakCats.forEach(([cat, count]) => {
      const item = document.createElement('li');
      item.className   = 'training-weak-item';
      item.textContent = `⚠ ${cat}（${count}問ミス）`;
      list.appendChild(item);
    });
    summary.appendChild(list);
  } else {
    const perfect = document.createElement('p');
    perfect.className   = 'training-all-good';
    perfect.textContent = '苦手カテゴリなし！素晴らしい！';
    summary.appendChild(perfect);
  }

  setView('training-result');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetTrainingSession() {
  state.trainingCount     = 0;
  state.trainingCorrect   = 0;
  state.trainingLog       = [];
  state.trainingCatCounts = {};
  state.trainingLastCats  = [];
  state.trainingFinished  = false;
  state.sessionExcludeIds = new Set();
  state.lastQuestionId    = null;
  state.sessionAnswered   = 0;
  state.sessionCorrect    = 0;
  state.streak            = 0;
  updateSessionStats();
  // btn-next テキストをデフォルトに戻す
  el('btn-next').innerHTML = '次の問題へ <span class="key-hint">Enter</span>';
}

function onNextClick() {
  if (state.trainingFinished) {
    showTrainingResult();
  } else {
    loadQuestion();
  }
}

function onRetry() {
  resetTrainingSession();
  loadQuestion();
}

function onEnd() {
  resetTrainingSession();
  if (state.mode !== 'normal') {
    state.mode = 'normal';
    el('btn-normal').classList.add('active');
    el('btn-weak').classList.remove('active');
    el('btn-review').classList.remove('active');
  }
  loadQuestion();
}

/* ==========================================================
   テーマ切替（正答率連動）
   ========================================================== */
function applyTheme(theme) {
  document.body.classList.remove('theme-normal', 'theme-dark');
  document.body.classList.add(`theme-${theme}`);
  localStorage.setItem(LS_THEME, theme);  // セッション結果を永続保存
}

function applyThemeVisual(theme) {
  document.body.classList.remove('theme-normal', 'theme-dark');
  document.body.classList.add(`theme-${theme}`);
  // localStorage は変更しない（保存済み session テーマを保持）
}

function restoreSessionTheme() {
  const saved = localStorage.getItem(LS_THEME);
  if (saved) applyThemeVisual(saved);
}

function updateTheme(stats) {
  const totalAnswered = stats.reduce((s, r) => s + r.answered_count, 0);
  const totalCorrect  = stats.reduce((s, r) => s + r.correct_count, 0);
  if (totalAnswered === 0) return;               // 未回答: 変更しない
  const acc = totalCorrect / totalAnswered;
  if      (acc < 0.40)  applyTheme('dark');     // 39%以下 → dark
  else if (acc >= 0.70) applyTheme('normal');   // 70%以上 → normal
  // 40〜69%: 何もしない（現在テーマ維持・ヒステリシス）
}

function updateThemeFromTraining() {
  const log = state.trainingLog;
  if (log.length === 0) return;
  const acc = log.filter(r => r.is_correct).length / log.length;
  if      (acc < 0.40)  applyTheme('dark');    // 直近10問が40%未満 → dark
  else if (acc >= 0.70) applyTheme('normal');  // 直近10問が70%以上 → normal
  // 40〜69%: 現在テーマ維持（ヒステリシス）
}

/* ==========================================================
   苦手分析
   ========================================================== */
async function loadStats() {
  removeError();
  try {
    const url = `/api/stats/categories?user_name=${encodeURIComponent(state.userName)}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    applyThemeVisual('normal');  // stats 画面は補助空間: normal 表示固定
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

  const sorted = [...stats].sort((a, b) => a.accuracy - b.accuracy);

  sorted.forEach(s => {
    const pct        = Math.round(s.accuracy * 100);
    const enoughData = s.answered_count >= MIN_ANSWERS;
    const isWeak     = enoughData && s.accuracy < WEAK_THRESHOLD;

    const row = document.createElement('div');
    row.className = 'stat-row';

    const labelLine = document.createElement('div');
    labelLine.className = 'stat-label-line';

    const name = document.createElement('span');
    name.className   = 'stat-name';
    name.textContent = isWeak ? `⚠ ${s.category}` : s.category;
    if (isWeak) name.style.color = 'var(--c-wrong)';

    const detail = document.createElement('span');
    detail.className   = 'stat-detail';
    detail.textContent = `${pct}% (${s.correct_count} / ${s.answered_count})`;

    labelLine.append(name, detail);

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
   セッション統計
   ========================================================== */
function updateSessionStats() {
  const statsEl = el('session-stats');
  if (state.sessionAnswered === 0) {
    statsEl.textContent = '';
    return;
  }

  let text = `${state.sessionCorrect} / ${state.sessionAnswered}問 正解`;
  if (state.streak >= 3) {
    text += ` 🔥${state.streak}連続`;
  }
  statsEl.textContent = text;
}

/* ==========================================================
   ビュー切替
   ========================================================== */
function setView(view) {
  state.view = view;
  el('section-username').hidden          = true;
  el('section-quiz').hidden              = (view === 'stats' || view === 'training-result');
  el('section-result').hidden            = (view !== 'result');
  el('section-stats').hidden             = (view !== 'stats');
  el('section-training-result').hidden   = (view !== 'training-result');
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
