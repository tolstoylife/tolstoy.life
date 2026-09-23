/* Read-along — per-section audio + sentence highlight-follow + click-to-seek.
   Data: window.READER.readalong = { timing: "build/timing.<version>.json" }.
   timing.json: { clips: {id: {section, begin, end}}, audio: {secId: path} },
   clip times are section-relative; ids are sentence spans (p-N-M-sK) or the
   narrated section heading (sec-N). */
(function () {
  'use strict';
  const R = window.READER || {};
  if (!R.readalong) return;

  const settings = window.readerSettings;
  const SPEEDS = [1, 1.25, 1.5, 0.75];

  fetch(R.readalong.timing).then(r => r.json()).then(init).catch(err => {
    console.error('read-along: timing load failed', err);
  });

  function init(timing) {
    const sections = Object.keys(timing.audio);             // sec-1 … sec-N, in order
    const bySection = {};                                   // secId → [{id, begin, end, el}]
    for (const [id, c] of Object.entries(timing.clips)) {
      const el = document.getElementById(id);
      if (!el) continue;
      (bySection[c.section] = bySection[c.section] || []).push({ id, begin: c.begin, end: c.end, el });
    }
    for (const sec of sections) (bySection[sec] || []).sort((a, b) => a.begin - b.begin);

    const audio = new Audio();
    audio.preload = 'metadata';
    const playBtn = document.getElementById('rl-play');
    const seek = document.getElementById('rl-seek');
    const timeOut = document.getElementById('rl-time');
    const secOut = document.getElementById('rl-sec');
    const speedBtn = document.getElementById('rl-speed');

    let curSec = sections[0];
    let activeEl = null;
    let lastUserScroll = 0;
    let seeking = false;
    // ⚠ the local serve.py can't answer HTTP Range requests, so on localhost sections load whole as blob URLs; the site (Netlify) streams.
    const wholeFiles = ['localhost', '127.0.0.1'].includes(location.hostname);
    const blobs = {};

    let speed = (settings && settings.load().speed) || 1;
    applySpeed(speed);

    function base(path) {
      // timing audio paths are relative to build/ (where timing.json lives)
      return R.readalong.timing.replace(/[^/]+$/, '') + path;
    }

    async function loadSection(sec, seekTo, autoplay) {
      curSec = sec;
      secOut.textContent = (sections.indexOf(sec) + 1) + '/' + sections.length;
      if (!wholeFiles) {
        audio.src = base(timing.audio[sec]);
      } else {
        if (!blobs[sec]) {
          const r = await fetch(base(timing.audio[sec]));
          blobs[sec] = URL.createObjectURL(await r.blob());
          if (curSec !== sec) return;   // superseded by a later click mid-fetch
        }
        audio.src = blobs[sec];
      }
      audio.playbackRate = speed;
      if (seekTo != null) {
        // ⚠ right after a src swap readyState still describes the old file, so a synchronous seek is dropped — always wait for the new metadata.
        audio.addEventListener('loadedmetadata',
          () => { audio.currentTime = seekTo; }, { once: true });
      }
      if (autoplay) audio.play();
      paint();
    }

    function applySpeed(v) {
      speed = v;
      audio.playbackRate = v;
      speedBtn.textContent = v + '×';
      if (settings) settings.save({ speed: v });
    }

    // ── Highlight-follow ──
    function highlight(el) {
      if (el === activeEl) return;
      if (activeEl) activeEl.classList.remove('rl-active');
      activeEl = el;
      if (!el) return;
      el.classList.add('rl-active');
      // Follow, unless the reader has scrolled on their own in the last 2.5 s.
      if (Date.now() - lastUserScroll < 2500) return;
      const r = el.getBoundingClientRect();
      if (r.top < innerHeight * 0.15 || r.bottom > innerHeight * 0.8) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }

    ['wheel', 'touchmove'].forEach(ev =>
      addEventListener(ev, () => { lastUserScroll = Date.now(); }, { passive: true }));

    function clipAt(t) {
      const clips = bySection[curSec] || [];
      for (let i = 0; i < clips.length; i++) {
        if (t >= clips[i].begin && t < clips[i].end) return clips[i];
      }
      return null;
    }

    function fmt(t) {
      t = Math.max(0, Math.round(t));
      return Math.floor(t / 60) + ':' + String(t % 60).padStart(2, '0');
    }

    const playIcon = document.getElementById('rl-play-icon');

    function paint() {
      const dur = audio.duration || 0;
      if (!seeking) {
        seek.max = dur || 100;
        seek.value = audio.currentTime;
        if (window.paintSlider) window.paintSlider(seek, '--accent-soft');
      }
      timeOut.textContent = fmt(audio.currentTime) + ' / ' + fmt(dur);
      playIcon.setAttribute('href', audio.paused ? '#i-play' : '#i-pause');
    }

    audio.addEventListener('timeupdate', () => {
      if (!audio.paused) {          // don't wash the heading before play starts
        const c = clipAt(audio.currentTime);
        if (c) highlight(c.el);
      }
      paint();
    });
    audio.addEventListener('loadedmetadata', paint);
    audio.addEventListener('play', paint);
    audio.addEventListener('pause', paint);
    audio.addEventListener('ended', () => {
      const i = sections.indexOf(curSec);
      if (i < sections.length - 1) loadSection(sections[i + 1], 0, true);
      else paint();
    });

    // ── Transport controls ──
    playBtn.addEventListener('click', () => {
      if (audio.paused) audio.play(); else audio.pause();
    });
    seek.addEventListener('input', () => {
      seeking = true;
      if (window.paintSlider) window.paintSlider(seek, '--accent-soft');
    });
    seek.addEventListener('change', () => {
      audio.currentTime = +seek.value;
      seeking = false;
    });
    speedBtn.addEventListener('click', () => {
      applySpeed(SPEEDS[(SPEEDS.indexOf(speed) + 1) % SPEEDS.length]);
    });

    // Space toggles play, except while typing or on a focused control (a focused button already toggles itself).
    addEventListener('keydown', e => {
      if (e.code !== 'Space' || e.target.closest('input, textarea, select, button, a, [contenteditable]')) return;
      e.preventDefault();                    // keep the page from scrolling
      if (e.repeat) return;
      if (audio.paused) audio.play(); else audio.pause();
    });

    // ── Click a sentence (or a section heading) to seek to it ──
    document.querySelector('main').addEventListener('click', e => {
      const span = e.target.closest('.sentence, h2[id^="sec-"]');
      if (!span || e.target.closest('a, mark.annotation')) return;
      if (!window.getSelection().isCollapsed) return;
      const clip = timing.clips[span.id];
      if (!clip) return;
      const wasPlaying = !audio.paused;
      if (clip.section !== curSec) loadSection(clip.section, clip.begin, wasPlaying);
      else audio.currentTime = clip.begin;
      highlight(span);
    });

    loadSection(curSec, 0, false);

    // Exposed for the sync check (docs/tests + preview verification).
    window.readerReadalong = {
      audio,
      get section() { return curSec; },
      get active() { return activeEl && activeEl.id; },
      clipAt,
    };
  }
})();
