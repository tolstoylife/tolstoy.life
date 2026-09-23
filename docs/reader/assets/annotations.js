/* Annotations — W3C Web Annotation shape, localStorage, Notes panel.
   One record per note:
     { "@context": "http://www.w3.org/ns/anno.jsonld", id, type: "Annotation",
       created, motivation: "commenting",
       body: [ {TextualBody, purpose:"commenting", value} (+ needs-fix tag) ],
       target: { source: "<docKey>#<paraId>",
                 selector: [ TextQuoteSelector {exact,prefix,suffix},
                             TextPositionSelector {start,end} ] } }
   TextPosition offsets are relative to the target paragraph's text content —
   the paragraph id (p-N-M) is the stable cross-version coordinate. */
(function () {
  'use strict';
  const R = window.READER || {};
  const DOC_KEY = R.docKey || location.pathname;
  const STORE_KEY = 'tolstoy_annotations';
  const CONTEXT = 'http://www.w3.org/ns/anno.jsonld';

  // ── Storage ────────────────────────────────────────────────────────────
  function loadAll() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || '{}'); }
    catch { return {}; }
  }
  function saveAll(data) { localStorage.setItem(STORE_KEY, JSON.stringify(data)); }
  function loadDoc() { return (loadAll()[DOC_KEY] || []).map(migrate); }
  function saveDoc(anns) {
    const all = loadAll();
    if (anns.length === 0) delete all[DOC_KEY];
    else all[DOC_KEY] = anns;
    saveAll(all);
  }

  // Legacy {anchor:{paraId,text,before,after}, comment} → W3C shape.
  function migrate(a) {
    if (!a.anchor) return a;
    return makeAnnotation({
      paraId: a.anchor.paraId || '',
      exact: a.anchor.text,
      prefix: a.anchor.before || '',
      suffix: a.anchor.after || '',
      start: null, end: null,
    }, a.comment, !!a.needsFix, a.created);
  }

  function makeAnnotation(anchor, comment, needsFix, created) {
    const body = [{ type: 'TextualBody', value: comment, format: 'text/plain', purpose: 'commenting' }];
    if (needsFix) body.push({ type: 'TextualBody', value: 'needs-fix', purpose: 'tagging' });
    const selector = [{
      type: 'TextQuoteSelector',
      exact: anchor.exact, prefix: anchor.prefix, suffix: anchor.suffix,
    }];
    if (anchor.start != null) {
      selector.push({ type: 'TextPositionSelector', start: anchor.start, end: anchor.end });
    }
    return {
      '@context': CONTEXT,
      id: 'urn:uuid:' + (crypto.randomUUID ? crypto.randomUUID() : Date.now() + '-' + Math.random().toString(36).slice(2)),
      type: 'Annotation',
      created: created || new Date().toISOString(),
      motivation: 'commenting',
      body,
      target: {
        source: DOC_KEY + (anchor.paraId ? '#' + anchor.paraId : ''),
        selector,
      },
    };
  }

  function setComment(ann, value) {
    const b = bodies(ann).find(b => b.purpose !== 'tagging');
    if (b) b.value = value;
    else ann.body = [{ type: 'TextualBody', value, format: 'text/plain', purpose: 'commenting' }].concat(bodies(ann));
    ann.modified = new Date().toISOString();
    return ann;
  }

  // ── Accessors ──────────────────────────────────────────────────────────
  const sel = (ann, type) => ((ann.target && ann.target.selector) || []).find(s => s.type === type);
  const quoteSel = ann => sel(ann, 'TextQuoteSelector');
  const posSel = ann => sel(ann, 'TextPositionSelector');
  const paraIdOf = ann => ((ann.target && ann.target.source) || '').split('#')[1] || '';
  const bodies = ann => Array.isArray(ann.body) ? ann.body : (ann.body ? [ann.body] : []);
  const commentOf = ann => (bodies(ann).find(b => b.purpose !== 'tagging') || {}).value || '';
  const needsFix = ann => bodies(ann).some(b => b.purpose === 'tagging' && b.value === 'needs-fix');

  // ── Anchor capture from a selection ────────────────────────────────────
  function getContext(range) {
    const selected = range.toString();
    let el = range.commonAncestorContainer;
    if (el.nodeType === 3) el = el.parentNode;
    // anchor to the enclosing paragraph — or a heading (they carry ids too)
    const para = el.closest('[id^="p-"], h2[id], h3[id]');
    if (!para) return null;
    const full = para.textContent || '';
    const start = full.indexOf(selected);
    if (start === -1) return null;
    return {
      paraId: para.id,
      exact: selected,
      prefix: full.slice(Math.max(0, start - 30), start),
      suffix: full.slice(start + selected.length, start + selected.length + 30),
      start,
      end: start + selected.length,
    };
  }

  // ── Re-anchor + render: wrap the quote in <mark>, preferring the match
  //    nearest the stored TextPosition. Single-text-node quotes only (v1). ──
  function findAndWrap(ann, exactOverride) {
    const q = quoteSel(ann);
    if (!q || !q.exact) return;
    const exact = exactOverride || q.exact;
    const para = paraIdOf(ann) ? document.getElementById(paraIdOf(ann)) : null;
    const scope = para || document.querySelector('main');
    if (!scope) return;
    const pos = posSel(ann);
    const walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT);
    let node, offset = 0, best = null;
    while ((node = walker.nextNode())) {
      if (node.parentNode.closest('mark.annotation')) { offset += node.textContent.length; continue; }
      let idx = node.textContent.indexOf(exact);
      while (idx !== -1) {
        const abs = offset + idx;
        const dist = pos ? Math.abs(abs - pos.start) : (best ? Infinity : 0);
        if (!best || dist < best.dist) best = { node, idx, dist };
        if (!pos) break; // no position stored: first match wins
        idx = node.textContent.indexOf(exact, idx + 1);
      }
      if (!pos && best) break;
      offset += node.textContent.length;
    }
    if (!best) {
      // a quote with edge whitespace can start in the gap BETWEEN sentence
      // spans (its own text node) — retry with the trimmed quote
      if (!exactOverride && exact !== exact.trim()) findAndWrap(ann, exact.trim());
      return;
    }
    const { node: n, idx } = best;
    const after = n.textContent.slice(idx + exact.length);
    const mark = document.createElement('mark');
    mark.className = 'annotation' + (needsFix(ann) ? ' needs-fix' : '');
    mark.dataset.annId = ann.id;
    mark.textContent = exact;
    const afterNode = document.createTextNode(after);
    n.textContent = n.textContent.slice(0, idx);
    n.parentNode.insertBefore(mark, n.nextSibling);
    n.parentNode.insertBefore(afterNode, mark.nextSibling);
    attachMark(mark, ann);
  }

  function renderAll() {
    document.querySelectorAll('mark.annotation').forEach(m => {
      m.replaceWith(document.createTextNode(m.textContent));
    });
    document.querySelector('main') && document.querySelector('main').normalize();
    loadDoc().forEach(a => findAndWrap(a));
    renderPanel();
  }

  // ── Marks: hover tooltip, click → Notes panel entry ────────────────────
  const tooltip = document.getElementById('ann-tooltip');

  function attachMark(mark, ann) {
    mark.addEventListener('mouseenter', e => {
      tooltip.textContent = commentOf(ann);
      tooltip.style.display = 'block';
      positionTooltip(e);
    });
    mark.addEventListener('mousemove', positionTooltip);
    mark.addEventListener('mouseleave', () => { tooltip.style.display = 'none'; });
    mark.addEventListener('click', e => {
      e.stopPropagation();
      const panel = document.getElementById('notes-panel');
      if (panel && window.readerPanels) {
        if (!panel.classList.contains('open')) window.readerPanels.toggle(panel);
        renderPanel();
        const entry = panel.querySelector(`[data-ann-id="${CSS.escape(ann.id)}"]`);
        if (entry) { entry.scrollIntoView({ block: 'center' }); flash(entry); }
      }
    });
  }

  function positionTooltip(e) {
    const pad = 12;
    let x = e.clientX + pad;
    let y = e.clientY - tooltip.offsetHeight - pad;
    if (x + tooltip.offsetWidth > innerWidth - pad) x = e.clientX - tooltip.offsetWidth - pad;
    if (y < pad) y = e.clientY + pad;
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
  }

  function flash(el) {
    el.classList.remove('flash');
    void el.offsetWidth;
    el.classList.add('flash');
  }

  // ── Notes panel ────────────────────────────────────────────────────────
  function renderPanel() {
    const list = document.getElementById('notes-list');
    if (!list) return;
    const anns = loadDoc();
    list.innerHTML = '';
    if (!anns.length) {
      list.innerHTML = '<li class="notes-empty">No notes on this page yet — select some text to make one.</li>';
    }
    anns.forEach(ann => {
      const li = document.createElement('li');
      li.className = 'note-entry';
      li.dataset.annId = ann.id;
      const q = quoteSel(ann) || { exact: '' };
      const quote = document.createElement('p');
      quote.className = 'note-quote';
      quote.textContent = q.exact;
      const body = document.createElement('p');
      body.className = 'note-body';
      body.textContent = commentOf(ann);
      const meta = document.createElement('div');
      meta.className = 'note-meta';
      const when = document.createElement('span');
      when.textContent = (ann.created || '').slice(0, 10) + (needsFix(ann) ? ' · 🔧 needs fix' : '');
      const edit = document.createElement('button');
      edit.className = 'note-edit';
      edit.textContent = 'Edit';
      edit.addEventListener('click', e => { e.stopPropagation(); startEdit(); });
      const del = document.createElement('button');
      del.className = 'note-del';
      del.textContent = 'Delete';
      del.addEventListener('click', e => {
        e.stopPropagation();
        if (!confirm('Delete this note?\n\n"' + commentOf(ann) + '"')) return;
        saveDoc(loadDoc().filter(a => a.id !== ann.id));
        renderAll();
      });
      meta.append(when, edit, del);

      // Edit in place: the body text becomes a textarea, Save/Cancel replace the meta row.
      function startEdit() {
        const ta = document.createElement('textarea');
        ta.value = commentOf(ann);
        ta.addEventListener('click', e => e.stopPropagation());
        ta.addEventListener('keydown', e => {
          e.stopPropagation();               // Esc cancels the edit, not the panel
          if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) save();
          if (e.key === 'Escape') renderPanel();
        });
        const row = document.createElement('div');
        row.className = 'note-meta';
        const saveBtn = document.createElement('button');
        saveBtn.className = 'note-save';
        saveBtn.textContent = 'Save';
        saveBtn.addEventListener('click', e => { e.stopPropagation(); save(); });
        const cancelBtn = document.createElement('button');
        cancelBtn.className = 'note-cancel';
        cancelBtn.textContent = 'Cancel';
        cancelBtn.addEventListener('click', e => { e.stopPropagation(); renderPanel(); });
        row.append(saveBtn, cancelBtn);
        body.replaceWith(ta);
        meta.replaceWith(row);
        ta.focus();
        function save() {
          const v = ta.value.trim();
          if (!v) return;                    // emptying a note isn't deleting it
          setComment(ann, v);
          saveDoc(loadDoc().map(a => a.id === ann.id ? ann : a));
          renderAll();
        }
      }
      li.append(quote, body, meta);
      li.addEventListener('click', () => {
        const mark = document.querySelector(`mark.annotation[data-ann-id="${CSS.escape(ann.id)}"]`);
        if (mark) { mark.scrollIntoView({ behavior: 'smooth', block: 'center' }); flash(mark); }
      });
      list.appendChild(li);
    });
  }
  document.addEventListener('notes-panel-open', renderPanel);

  // ── Export / import (W3C JSON-LD AnnotationCollection) ────────────────
  function exportCollection() {
    const anns = loadDoc();
    return {
      '@context': CONTEXT,
      type: 'AnnotationCollection',
      label: 'tolstoy.life notes — ' + DOC_KEY,
      total: anns.length,
      items: anns,
    };
  }

  function importAny(obj) {
    let items = [];
    if (Array.isArray(obj)) items = obj;
    else if (obj && Array.isArray(obj.items)) items = obj.items;          // AnnotationCollection
    else if (obj && Array.isArray(obj[DOC_KEY])) items = obj[DOC_KEY];    // legacy export
    items = items.map(migrate).filter(a => a.target && quoteSel(a));
    if (!items.length) { alert('No annotations for this document in that JSON.'); return; }
    const anns = loadDoc();
    const key = a => paraIdOf(a) + '|' + (quoteSel(a) || {}).exact + '|' + commentOf(a);
    const seen = new Set(anns.map(key));
    items.forEach(a => { if (!seen.has(key(a))) { anns.push(a); seen.add(key(a)); } });
    saveDoc(anns);
    renderAll();
  }

  // Human-readable export — for pasting notes straight into a chat.
  function exportText() {
    const anns = loadDoc();
    const lines = ['Notes — ' + DOC_KEY, ''];
    anns.forEach((a, i) => {
      const q = ((quoteSel(a) || {}).exact || '').trim();
      lines.push(`${i + 1}. [${paraIdOf(a) || '—'}] "${q}"${needsFix(a) ? ' 🔧' : ''}`);
      lines.push('   ' + commentOf(a).replace(/\n/g, '\n   '));
      lines.push('');
    });
    return lines.join('\n');
  }

  function copyFeedback(btn) {
    const orig = btn.textContent;
    btn.textContent = 'Copied!';
    setTimeout(() => { btn.textContent = orig; }, 1800);
  }
  bindClick('notes-copytext', btn => {
    navigator.clipboard.writeText(exportText()).then(() => copyFeedback(btn));
  });
  bindClick('notes-export', btn => {
    const payload = JSON.stringify(exportCollection(), null, 2);
    navigator.clipboard.writeText(payload).then(() => copyFeedback(btn));
  });
  bindClick('notes-import', () => {
    const pasted = prompt('Paste annotation JSON (W3C collection or a previous export):');
    if (pasted) { try { importAny(JSON.parse(pasted)); } catch { alert('Not valid JSON.'); } }
  });
  bindClick('notes-clear', () => {
    if (confirm('Delete all notes on this page?')) { saveDoc([]); renderAll(); }
  });

  // ⚠ Send only works on the published site (Netlify handles the form); locally it would 404, so the button is hidden.
  const sendRow = document.getElementById('notes-send-row');
  const sendBtn = document.getElementById('notes-send');
  if (sendBtn && !/(^|\.)(tolstoy\.life|netlify\.app)$/.test(location.hostname)) sendBtn.hidden = true;
  bindClick('notes-send', () => { sendRow.hidden = !sendRow.hidden; });
  bindClick('notes-send-go', btn => {
    if (!loadDoc().length) { alert('There are no notes on this page yet.'); return; }
    const body = new URLSearchParams({
      'form-name': 'reader-notes',
      page: location.pathname,
      email: document.getElementById('notes-email').value,
      text: exportText(),
      jsonld: JSON.stringify(exportCollection()),
      'bot-field': '',
    });
    btn.disabled = true;
    // ⚠ Posts to the page's own address, not "/" — the site rewrites "/" to INDEX.html, which can swallow the submission.
    fetch(location.pathname, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body })
      .then(r => { btn.textContent = r.ok ? 'Sent, thank you' : 'Sending failed — try again later'; })
      .catch(() => { btn.textContent = 'Sending failed — try again later'; })
      .finally(() => { setTimeout(() => { btn.disabled = false; btn.textContent = 'Send'; sendRow.hidden = true; }, 4000); });
  });

  function bindClick(id, fn) {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', () => fn(el));
  }

  // ── Popover (select text → write a note) ───────────────────────────────
  const popover = document.getElementById('ann-popover');
  const annText = document.getElementById('ann-text');
  const annQuote = document.getElementById('ann-quote');
  let pendingAnchor = null;

  document.getElementById('ann-save').addEventListener('click', () => {
    const comment = annText.value.trim();
    if (!comment || !pendingAnchor) { hidePopover(); return; }
    const anns = loadDoc();
    anns.push(makeAnnotation(pendingAnchor, comment, document.getElementById('ann-fix').checked));
    saveDoc(anns);
    hidePopover();
    renderAll();
  });
  document.getElementById('ann-cancel').addEventListener('click', hidePopover);

  annText.addEventListener('keydown', e => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) document.getElementById('ann-save').click();
    if (e.key === 'Escape') hidePopover();
  });

  function hidePopover() {
    popover.style.display = 'none';
    annText.value = '';
    document.getElementById('ann-fix').checked = false;
    if (pendingAnchor) window.getSelection().removeAllRanges();
    pendingAnchor = null;
  }

  function showPopover(x, y, anchor, focus = true) {
    pendingAnchor = anchor;
    annQuote.textContent = '"' + anchor.exact.slice(0, 120) + (anchor.exact.length > 120 ? '…' : '') + '"';
    popover.style.display = 'block';
    let px = x, py = y + 12;
    if (px + popover.offsetWidth > innerWidth - 16) px = innerWidth - popover.offsetWidth - 16;
    if (py + popover.offsetHeight > innerHeight - 16) py = y - popover.offsetHeight - 12;
    popover.style.left = px + 'px';
    popover.style.top = py + 'px';
    if (focus) setTimeout(() => annText.focus(), 50);
  }

  // The current selection as a note anchor, or null when it isn't a selection in the text.
  function selectionAnchor() {
    const s = window.getSelection();
    if (!s || s.isCollapsed || s.toString().trim().length < 3) return null;
    const main = document.querySelector('main');
    const range = s.getRangeAt(0);
    if (!main || !main.contains(range.commonAncestorContainer)) return null;
    const anchor = getContext(range);
    return anchor ? { anchor, rect: range.getBoundingClientRect() } : null;
  }

  let lastPointer = 'mouse', settle;
  document.addEventListener('pointerdown', e => { lastPointer = e.pointerType; }, true);

  document.addEventListener('mouseup', e => {
    if (lastPointer !== 'mouse') return;
    if (e.target.closest('#ann-popover,#notes-panel,#tools-overlay,#toc-drawer,#topbar,#transport')) return;
    const sel = selectionAnchor();
    if (sel) showPopover(e.clientX, e.clientY, sel.anchor);
  });

  // ⚠ Touch and Pencil selection (iPad) never fire mouseup — open once the selection handles settle.
  document.addEventListener('selectionchange', () => {
    if (lastPointer === 'mouse' || popover.contains(document.activeElement)) return;
    clearTimeout(settle);
    settle = setTimeout(() => {
      const sel = selectionAnchor();
      if (sel) showPopover(sel.rect.left, sel.rect.bottom, sel.anchor, false);
    }, 600);
  });

  document.addEventListener('mousedown', e => {
    if (!popover.contains(e.target)) hidePopover();
  });

  // ── Init (persist any legacy-shape migration back to storage) ──────────
  const initial = loadDoc();
  if (initial.length) saveDoc(initial);
  renderAll();

  // Exposed for tests / preview verification.
  window.readerNotes = { exportText, exportCollection };
})();
