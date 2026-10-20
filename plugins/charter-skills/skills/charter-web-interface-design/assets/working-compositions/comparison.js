// Original fictional dataset and application. No fetch, framework or backend.
const rooms = [
  { id: 'garden', name: 'Garden Room', location: 'Elm House / Ground floor', seats: 12, access: true, projector: true, price: 160 },
  { id: 'north', name: 'North Loft', location: 'Old Mill / Second floor', seats: 14, access: true, projector: true, price: 195 },
  { id: 'reading', name: 'Reading Room', location: 'Civic Library / Ground floor', seats: 12, access: true, projector: false, price: 125 },
  { id: 'east', name: 'East Studio', location: 'Old Mill / First floor', seats: 16, access: null, projector: true, price: 175 },
  { id: 'assembly', name: 'Assembly Hall', location: 'Foundry / Ground floor', seats: 24, access: true, projector: true, price: 180 },
  { id: 'print', name: 'The Printmakers’ Workshop & Community Meeting Room', location: 'Riverside Cooperative / Courtyard', seats: 10, access: true, projector: null, price: 150 },
  { id: 'west', name: 'West Attic', location: 'Station House / Third floor', seats: 14, access: false, projector: true, price: 110 },
  { id: 'map', name: 'Map Room', location: 'Civic Library / First floor', seats: 8, access: true, projector: false, price: 90 }
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
const $ = selector => document.querySelector(selector);
const booleanText = value => value === null ? 'Unconfirmed' : value ? 'Yes' : 'No';
// Text goes through textContent; the same renderer can safely carry long names.
function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function issues(room) {
  const gaps = [];
  if (room.seats < requirements.people) gaps.push(`${requirements.people - room.seats} seats short`);
  if (room.price > requirements.budget) gaps.push(`${money.format(room.price - requirements.budget)} over budget`);
  if (requirements.access && room.access !== true) gaps.push(room.access === null ? 'Access unconfirmed' : 'No step-free access');
  if (requirements.projector && room.projector !== true) gaps.push(room.projector === null ? 'Projector unconfirmed' : 'No projector');
  return gaps;
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
function roomCells(row, room) {
  const nameCell = element('th');
  nameCell.scope = 'row';
  nameCell.append(element('span', room.name, 'room-name'), element('span', room.location, 'room-location'));
  row.append(nameCell, element('td', room.seats, 'numeric'));
  for (const field of ['access', 'projector']) row.append(element('td', booleanText(room[field]), room[field] === null ? 'unknown' : ''));
  row.append(element('td', money.format(room.price), 'numeric'));
  const gaps = issues(room);
  const fitCell = element('td');
  fitCell.append(element('span', gaps.length ? gaps.join(' · ') : 'All requirements met', gaps.length ? 'gap' : 'fit'));
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
  $('#result-heading').textContent = requirements.matches ? 'Confirmed matches' : 'All spaces';
  $('#result-count').textContent = `${visible.length} of ${rooms.length} spaces shown · ${allMatches} confirmed ${allMatches === 1 ? 'match' : 'matches'}`;
  $('#active-requirements').textContent = [`${requirements.people} people`, `up to ${money.format(requirements.budget)} / session`, requirements.access ? 'step-free required' : null, requirements.projector ? 'projector required' : null].filter(Boolean).join(' / ');
  $('#empty').hidden = visible.length !== 0;
  $('.results > .table-region').hidden = visible.length === 0;
  $('#scroll-hint').hidden = visible.length === 0;
  renderSelection();
  updateScrollHint();
}
function sameSelection() { return savedIds.length === selected.size && savedIds.every(id => selected.has(id)); }
function renderSelection(message) {
  const hiddenCount = [...selected].filter(id => !visible.some(room => room.id === id)).length;
  $('#selection-count').textContent = selected.size ? `${selected.size} ${selected.size === 1 ? 'space' : 'spaces'} selected` : 'No spaces selected';
  $('#selection-scope').textContent = selected.size ? (hiddenCount ? `${hiddenCount} outside the current filters · included in compare and save.` : 'All selected spaces are shown above.') : 'Select a room to start your shortlist.';
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
  table.append(element('caption', 'Selected spaces against the applied requirements', 'sr-only'));
  const head = element('thead'); const headers = element('tr');
  for (const name of ['Room / Location', 'Seats', 'Step-free', 'Projector', 'Price', 'Fit']) {
    const cell = element('th', name, name === 'Room / Location' ? 'room-column' : name === 'Fit' ? 'fit-column' : ['Seats', 'Price'].includes(name) ? 'numeric' : ''); cell.scope = 'col'; headers.append(cell);
  }
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
