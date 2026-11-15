// Original fictional dataset and application. No fetch, framework or backend.
const rooms = [
  { id: 'garden', name: 'Garden Room', location: 'Elm House, ground floor', seats: 12, access: true, projector: true, price: 160 },
  { id: 'north', name: 'North Loft', location: 'Old Mill, second floor', seats: 14, access: true, projector: true, price: 195 },
  { id: 'reading', name: 'Reading Room', location: 'Civic Library, ground floor', seats: 12, access: true, projector: false, price: 125 },
  { id: 'east', name: 'East Studio', location: 'Old Mill, first floor', seats: 16, access: null, projector: true, price: 175 },
  { id: 'assembly', name: 'Assembly Hall', location: 'Foundry, ground floor', seats: 24, access: true, projector: true, price: 180 },
  { id: 'print', name: 'The Printmakers’ Workshop & Community Meeting Room', location: 'Riverside Cooperative, courtyard', seats: 10, access: true, projector: null, price: 150 },
  { id: 'west', name: 'West Attic', location: 'Station House, third floor', seats: 14, access: false, projector: true, price: 110 },
  { id: 'map', name: 'Map Room', location: 'Civic Library, first floor', seats: 8, access: true, projector: false, price: 90 }
];
const byId = new Map(rooms.map(room => [room.id, room]));
const storageKey = 'charter-fieldwork-shortlist-v1';
const form = document.querySelector('#filters');
const sort = document.querySelector('#sort');
const dialog = document.querySelector('#comparison-dialog');
const selected = new Set();
let savedIds = [];
let visible = [];
let storageError = '';
const defaults = { people: 12, budget: 180, access: true, projector: true, matches: false, sort: 'fit' };
let requirements;
const money = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP', maximumFractionDigits: 0 });
const list = new Intl.ListFormat('en-GB', { type: 'conjunction' });
const $ = selector => document.querySelector(selector);
const booleanText = value => value === null ? 'Unconfirmed' : value ? 'Yes' : 'No';
// Text goes through textContent; the same renderer can safely carry long names.
function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
// One judgement per requirement, in column order. A required feature that is
// unconfirmed is a gap of its own kind, never a No.
function judge(room) {
  const feature = (required, value) => !required ? 'off' : value === true ? 'met' : value === null ? 'unknown' : 'short';
  return {
    people: room.seats < requirements.people ? 'short' : 'met',
    access: feature(requirements.access, room.access),
    projector: feature(requirements.projector, room.projector),
    budget: room.price > requirements.budget ? 'short' : 'met'
  };
}
function issues(room) {
  const state = judge(room);
  const gaps = [];
  if (state.people === 'short') gaps.push({ kind: 'short', text: `${requirements.people - room.seats} seats short` });
  if (state.budget === 'short') gaps.push({ kind: 'short', text: `${money.format(room.price - requirements.budget)} over budget` });
  if (state.access !== 'met' && state.access !== 'off') gaps.push(state.access === 'unknown' ? { kind: 'unknown', text: 'Access unconfirmed' } : { kind: 'short', text: 'No step-free access' });
  if (state.projector !== 'met' && state.projector !== 'off') gaps.push(state.projector === 'unknown' ? { kind: 'unknown', text: 'Projector unconfirmed' } : { kind: 'short', text: 'No projector' });
  return gaps;
}
const ruleText = {
  people: () => `${requirements.people} or more`,
  access: () => requirements.access ? 'required' : 'not required',
  projector: () => requirements.projector ? 'required' : 'not required',
  budget: () => `up to ${money.format(requirements.budget)}`
};
function headerCell(name, key, className) {
  const cell = element('th', name, className);
  cell.scope = 'col';
  if (key) cell.append(element('span', ruleText[key](), 'rule'));
  return cell;
}
function readURL() {
  const query = new URLSearchParams(location.search);
  const boundedNumber = (key, min, max) => {
    const value = Number(query.get(key));
    return query.has(key) && Number.isInteger(value) && value >= min && value <= max ? value : defaults[key];
  };
  requirements = { people: boundedNumber('people', 1, 100), budget: boundedNumber('budget', 0, 10000), access: query.get('access') !== '0', projector: query.get('projector') !== '0', matches: query.get('matches') === '1', sort: ['fit', 'price', 'seats'].includes(query.get('sort')) ? query.get('sort') : 'fit' };
  for (const key of ['people', 'budget']) form.elements[key].value = requirements[key];
  for (const key of ['access', 'projector', 'matches']) form.elements[key].checked = requirements[key];
  sort.value = requirements.sort;
}
function writeURL() {
  const url = new URL(location.href);
  for (const [key, value] of Object.entries(requirements)) url.searchParams.set(key, typeof value === 'boolean' ? Number(value) : value);
  if (url.href !== location.href) history.pushState(null, '', url);
}
// The fit marks: one 12px square per requirement, in column order. Filled
// meets it, a red cross falls short, a dashed outline is unconfirmed and a
// short dash was not asked for.
const svgNS = 'http://www.w3.org/2000/svg';
const markShapes = {
  met: [['rect', { x: 0, y: 0, width: 12, height: 12, class: 'm-met' }]],
  short: [['rect', { x: .75, y: .75, width: 10.5, height: 10.5, class: 'm-short' }], ['path', { d: 'M3 3L9 9M9 3L3 9', class: 'm-short' }]],
  unknown: [['rect', { x: .75, y: .75, width: 10.5, height: 10.5, class: 'm-unknown' }]],
  off: [['rect', { x: 0, y: 5, width: 12, height: 2, class: 'm-off' }]]
};
function markStrip(states) {
  const svg = document.createElementNS(svgNS, 'svg');
  svg.setAttribute('class', 'marks');
  svg.setAttribute('width', states.length * 16 - 4);
  svg.setAttribute('height', 12);
  svg.setAttribute('aria-hidden', 'true');
  states.forEach((state, index) => {
    const group = document.createElementNS(svgNS, 'g');
    group.setAttribute('transform', `translate(${index * 16} 0)`);
    for (const [tag, attributes] of markShapes[state]) {
      const shape = document.createElementNS(svgNS, tag);
      for (const [name, value] of Object.entries(attributes)) shape.setAttribute(name, value);
      group.append(shape);
    }
    svg.append(group);
  });
  return svg;
}
for (const slot of document.querySelectorAll('[data-mark]')) slot.replaceWith(markStrip([slot.dataset.mark]));
// Each fact is drawn against the applied requirement: red where it falls
// short, a dashed box where it is unconfirmed, plain ink otherwise.
function roomCells(row, room) {
  const state = judge(room);
  const nameCell = element('th');
  nameCell.scope = 'row';
  nameCell.append(element('span', room.name, 'room-name'), element('span', room.location, 'room-location'));
  row.append(nameCell, element('td', room.seats, state.people === 'short' ? 'numeric short' : 'numeric'));
  for (const field of ['access', 'projector']) {
    const cell = element('td', undefined, state[field] === 'short' ? 'short' : '');
    cell.append(room[field] === null ? element('span', booleanText(null), 'unknown') : booleanText(room[field]));
    row.append(cell);
  }
  row.append(element('td', money.format(room.price), state.budget === 'short' ? 'numeric short' : 'numeric'));
  const fitCell = element('td', undefined, 'fit-cell');
  const marks = markStrip(['people', 'access', 'projector', 'budget'].map(key => state[key]));
  const lines = element('span', undefined, 'fit-lines');
  const gaps = issues(room);
  if (gaps.length) for (const gap of gaps) lines.append(element('span', gap.text, gap.kind === 'short' ? 'short' : 'unknown-gap'));
  else lines.append(element('span', 'All requirements met', 'met-all'));
  fitCell.append(marks, lines);
  row.append(fitCell);
}
function renderRows() {
  const allMatches = rooms.filter(room => issues(room).length === 0).length;
  visible = rooms.filter(room => !requirements.matches || issues(room).length === 0).sort((a, b) => {
    if (requirements.sort === 'price') return a.price - b.price;
    if (requirements.sort === 'seats') return b.seats - a.seats || a.price - b.price;
    return issues(a).length - issues(b).length || a.price - b.price;
  });
  $('#room-rows').replaceChildren();
  for (const room of visible) {
    const row = element('tr');
    row.dataset.id = room.id;
    row.classList.toggle('selected', selected.has(room.id));
    const pick = element('td');
    const label = element('label', undefined, 'row-check');
    const input = element('input');
    input.type = 'checkbox';
    input.checked = selected.has(room.id);
    input.dataset.id = room.id;
    input.setAttribute('aria-label', `Shortlist ${room.name}`);
    label.append(input); pick.append(label); row.append(pick);
    roomCells(row, room);
    $('#room-rows').append(row);
  }
  $('#result-heading').textContent = requirements.matches ? 'Confirmed matches' : 'All rooms';
  $('#result-count').textContent = `${visible.length} of ${rooms.length} rooms shown, ${allMatches} confirmed ${allMatches === 1 ? 'match' : 'matches'}`;
  $('#active-requirements').textContent = `Fit is judged against ${list.format([`${requirements.people} people`, `up to ${money.format(requirements.budget)} a session`, requirements.access ? 'step-free access' : null, requirements.projector ? 'a projector' : null].filter(Boolean))}.`;
  for (const rule of document.querySelectorAll('.results thead .rule')) rule.textContent = ruleText[rule.dataset.rule]();
  $('#empty').hidden = visible.length !== 0;
  $('.results > .table-region').hidden = visible.length === 0;
  $('#scroll-hint').hidden = visible.length === 0;
  renderSelection();
  updateScrollHint();
}
function sameSelection() { return savedIds.length === selected.size && savedIds.every(id => selected.has(id)); }
function renderSelection(message) {
  const hiddenCount = [...selected].filter(id => !visible.some(room => room.id === id)).length;
  $('#selection-count').textContent = selected.size ? `${selected.size} ${selected.size === 1 ? 'room' : 'rooms'} selected` : 'No rooms selected';
  $('.selection-bar').classList.toggle('has-selection', selected.size > 0);
  $('#selection-scope').textContent = selected.size ? (hiddenCount ? `${hiddenCount} outside the current filters, included in compare and save.` : 'All selected rooms are shown above.') : 'Select a room to start your shortlist.';
  for (const id of ['compare', 'save', 'download', 'clear']) $(`#${id}`).disabled = selected.size === 0;
  // Empty selection may overwrite a saved shortlist, but only via Save.
  $('#save').disabled = sameSelection();
  $('#save').textContent = selected.size === 0 && savedIds.length ? 'Save empty shortlist' : 'Save shortlist locally';
  $('#save-status').textContent = message || storageError || (sameSelection() && savedIds.length ? 'Saved in this browser. Changes to requirements do not change the shortlist.' : selected.size || savedIds.length ? 'Selection has unsaved changes.' : 'Shortlist stays in this browser when saved.');
  $('#saved-note').hidden = savedIds.length === 0 || sameSelection();
  $('#saved-note').textContent = savedIds.length ? `Saved shortlist still contains ${savedIds.map(id => byId.get(id).name).join(', ')} until you save this selection.` : '';
}
$('#room-rows').addEventListener('change', event => {
  const id = event.target.dataset.id;
  if (!byId.has(id)) return;
  event.target.checked ? selected.add(id) : selected.delete(id);
  event.target.closest('tr').classList.toggle('selected', event.target.checked);
  renderSelection(); // Do not replace the focused checkbox.
});
form.addEventListener('submit', event => {
  event.preventDefault();
  for (const key of ['people', 'budget']) requirements[key] = Number(form.elements[key].value);
  for (const key of ['access', 'projector', 'matches']) requirements[key] = form.elements[key].checked;
  writeURL(); renderRows();
});
$('#reset').addEventListener('click', () => { requirements = { ...defaults }; writeURL(); readURL(); renderRows(); });
$('#show-all').addEventListener('click', () => { requirements.matches = false; writeURL(); readURL(); renderRows(); $('#result-heading').tabIndex = -1; $('#result-heading').focus(); });
sort.addEventListener('change', () => { requirements.sort = sort.value; writeURL(); renderRows(); });
window.addEventListener('popstate', () => { readURL(); renderRows(); });
$('#clear').addEventListener('click', () => { selected.clear(); renderRows(); $('#result-heading').tabIndex = -1; $('#result-heading').focus(); });
$('#save').addEventListener('click', () => {
  try {
    localStorage.setItem(storageKey, JSON.stringify([...selected]));
    savedIds = [...selected]; storageError = '';
    renderSelection(selected.size ? 'Shortlist saved in this browser.' : 'Saved shortlist cleared.');
  } catch {
    storageError = 'Browser storage is unavailable. Your selection is still here; download it before leaving.';
    renderSelection();
  }
});
$('#download').addEventListener('click', () => {
  const file = new Blob([JSON.stringify({ study: 'Fieldwork fictional rooms', rooms: [...selected].map(id => byId.get(id)), requirements }, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(file);
  const link = element('a'); link.href = url; link.download = 'fieldwork-shortlist.json'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
$('#compare').addEventListener('click', () => {
  const table = $('#selected-table'); table.replaceChildren();
  table.append(element('caption', 'Selected rooms against the applied requirements', 'sr-only'));
  const head = element('thead'); const headers = element('tr');
  headers.append(headerCell('Room and building', null, 'room-column'), headerCell('Seats', 'people', 'numeric'), headerCell('Step-free', 'access'), headerCell('Projector', 'projector'), headerCell('Price', 'budget', 'numeric'), headerCell('Fit', null, 'fit-column'));
  head.append(headers); table.append(head);
  const body = element('tbody');
  for (const id of selected) { const row = element('tr'); roomCells(row, byId.get(id)); body.append(row); }
  table.append(body);
  $('#dialog-summary').textContent = $('#active-requirements').textContent;
  dialog.showModal();
});
$('#close-dialog').addEventListener('click', () => dialog.close());
function readSaved(raw) {
  const stored = JSON.parse(raw || '[]');
  if (!Array.isArray(stored)) throw new Error('Invalid shortlist');
  return [...new Set(stored.filter(id => byId.has(id)))];
}
window.addEventListener('storage', event => {
  if (event.key !== storageKey && event.key !== null) return;
  try {
    savedIds = readSaved(event.newValue); storageError = '';
    renderSelection('The saved shortlist changed in another tab. Your current selection is unchanged.');
  } catch { storageError = 'The saved shortlist in another tab could not be read. Download your current selection to keep it.'; renderSelection(); }
});
try {
  savedIds = readSaved(localStorage.getItem(storageKey));
  savedIds.forEach(id => selected.add(id));
} catch { storageError = 'The saved shortlist could not be read. New selections remain usable; save again or download them.'; }
readURL(); renderRows(); $('#workbench').hidden = false;
const tableRegion = $('.results > .table-region');
function updateScrollHint() {
  const tableRegion = $('.results > .table-region');
  const scrolls = visible.length > 0 && tableRegion.scrollWidth > tableRegion.clientWidth;
  $('#scroll-hint').hidden = !scrolls;
  tableRegion.tabIndex = scrolls ? 0 : -1;
}
new ResizeObserver(updateScrollHint).observe(tableRegion);
