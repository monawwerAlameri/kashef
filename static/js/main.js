/**
 * Kashef (كاشف) Client-Side JavaScript
 * Handlers: Mobile drawer, live image preview & dropzone, OCR text clipboard, table search, loading state.
 */
(function () {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => root.querySelectorAll(selector);

  // 1. Mobile Sidebar Drawer & Backdrop
  const sidebar = $('#sidebar');
  const backdrop = $('#backdrop');
  const menuBtn = $('#menuBtn');

  const toggleSidebar = (open) => {
    if (!sidebar) return;
    sidebar.classList.toggle('open', open);
    if (backdrop) backdrop.classList.toggle('show', open);
  };

  if (menuBtn) {
    menuBtn.addEventListener('click', () => {
      toggleSidebar(!sidebar.classList.contains('open'));
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', () => toggleSidebar(false));
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
      toggleSidebar(false);
    }
  });

  // 2. Packaging Image Upload Preview & Drag-and-Drop
  const imageInput = $('#imageInput');
  const dropzone = $('#dropzone');
  const preview = $('#preview');
  const clearBtn = $('#clearBtn');

  if (imageInput && dropzone) {
    const showImagePreview = (file) => {
      if (file && file.type.startsWith('image/')) {
        preview.src = URL.createObjectURL(file);
        preview.classList.remove('d-none');
        if (clearBtn) clearBtn.classList.remove('d-none');
      }
    };

    imageInput.addEventListener('change', () => {
      if (imageInput.files && imageInput.files[0]) {
        showImagePreview(imageInput.files[0]);
      }
    });

    ['dragenter', 'dragover'].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add('drag');
      });
    });

    ['dragleave', 'drop'].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove('drag');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      if (e.dataTransfer && e.dataTransfer.files.length) {
        imageInput.files = e.dataTransfer.files;
        showImagePreview(e.dataTransfer.files[0]);
      }
    });

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        imageInput.value = '';
        preview.src = '';
        preview.classList.add('d-none');
        clearBtn.classList.add('d-none');
      });
    }
  }

  // 3. Loading Overlay on Form Submit (Prevent Double Submission)
  const submitForms = ['uploadForm', 'analyzeForm'];
  submitForms.forEach((formId) => {
    const form = document.getElementById(formId);
    if (form) {
      form.addEventListener('submit', () => {
        if (form.checkValidity()) {
          const loading = $('#loading');
          if (loading) loading.classList.remove('d-none');
          const submitBtn = form.querySelector('button[type="submit"]');
          if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> جارٍ المعالجة…';
          }
        }
      });
    }
  });

  // 4. Copy OCR Text to Clipboard with Visual Feedback
  const copyBtn = $('#copyBtn');
  const ocrTextArea = $('#ocrText');
  if (copyBtn && ocrTextArea) {
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(ocrTextArea.value).then(() => {
        const originalHtml = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="bi bi-check2"></i> ' + (window.KT?.copied || 'تم النسخ');
        copyBtn.classList.remove('btn-kf-soft');
        copyBtn.classList.add('btn-success');
        setTimeout(() => {
          copyBtn.innerHTML = originalHtml;
          copyBtn.classList.remove('btn-success');
          copyBtn.classList.add('btn-kf-soft');
        }, 2200);
      });
    });
  }

  // 5. Accessible Confirm Dialogs for Sensitive Deletions
  $$('form[data-confirm]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      const confirmMsg = window.KT?.confirm || 'هل أنت متأكد من رغبتك في حذف هذا العنصر نهائياً؟';
      if (!confirm(confirmMsg)) {
        e.preventDefault();
      }
    });
  });

  // 6. Real-Time Table Filtering
  $$('.search[data-table]').forEach((input) => {
    input.addEventListener('input', () => {
      const query = input.value.trim().toLowerCase();
      const targetTable = $(input.dataset.table);
      if (!targetTable) return;

      const rows = targetTable.querySelectorAll('tbody tr');
      rows.forEach((row) => {
        const rowText = row.textContent.toLowerCase();
        row.style.display = rowText.includes(query) ? '' : 'none';
      });
    });
  });

  // 7. Public navigation: mobile collapse
  const kfNav = $('#kfNav');
  const navToggle = $('#navToggle');
  if (kfNav && navToggle) {
    navToggle.addEventListener('click', () => {
      const open = kfNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', (e) => {
      if (!kfNav.contains(e.target)) {
        kfNav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
    $$('.nav-pill', kfNav).forEach((a) => a.addEventListener('click', () => kfNav.classList.remove('open')));
  }

  // 8. Smooth line chart (dashboard statistics)
  const NS = 'http://www.w3.org/2000/svg';
  const el = (name, attrs = {}, text) => {
    const n = document.createElementNS(NS, name);
    Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v));
    if (text !== undefined) n.textContent = text;
    return n;
  };

  const drawChart = (host) => {
    const values = (host.dataset.values || '').split(',').filter(Boolean).map(Number);
    const labels = (host.dataset.labels || '').split(',');
    if (!values.length) return;

    const W = 600, H = 250, padL = 34, padR = 16, padT = 34, padB = 32;
    const max = Math.max(...values, 4);
    const top = Math.ceil(max / 4) * 4;
    const x = (i) => padL + (values.length === 1 ? (W - padL - padR) / 2 : i * (W - padL - padR) / (values.length - 1));
    const y = (v) => padT + (1 - v / top) * (H - padT - padB);

    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, 'aria-hidden': 'true' });
    const defs = el('defs');
    const lg = el('linearGradient', { id: 'kfArea', x1: 0, y1: 0, x2: 0, y2: 1 });
    lg.append(el('stop', { offset: 0, 'stop-color': '#7c3aed', 'stop-opacity': 0.28 }), el('stop', { offset: 1, 'stop-color': '#7c3aed', 'stop-opacity': 0.02 }));
    const lg2 = el('linearGradient', { id: 'kfLine', x1: 0, y1: 0, x2: 1, y2: 0 });
    lg2.append(el('stop', { offset: 0, 'stop-color': '#7c3aed' }), el('stop', { offset: 1, 'stop-color': '#4f6cf5' }));
    defs.append(lg, lg2);
    svg.append(defs);

    for (let g = 0; g <= 4; g++) {
      const gv = (top / 4) * g;
      svg.append(el('line', { class: 'grid', x1: padL, x2: W - padR, y1: y(gv), y2: y(gv) }));
      svg.append(el('text', { class: 'ax', x: padL - 8, y: y(gv) + 4, 'text-anchor': 'end' }, Math.round(gv)));
    }

    const pts = values.map((v, i) => [x(i), y(v)]);
    // Monotone-ish cubic smoothing (no overshoot)
    let d = `M${pts[0][0]},${pts[0][1]}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const [x0, y0] = pts[i], [x1, y1] = pts[i + 1];
      const dx = (x1 - x0) / 2.4;
      const lo = Math.min(y0, y1), hi = Math.max(y0, y1);
      const c1y = Math.min(hi, Math.max(lo, y0)), c2y = Math.min(hi, Math.max(lo, y1));
      d += ` C${x0 + dx},${c1y} ${x1 - dx},${c2y} ${x1},${y1}`;
    }
    const baseY = y(0);
    svg.append(el('path', { d: `${d} L${pts[pts.length - 1][0]},${baseY} L${pts[0][0]},${baseY}Z`, fill: 'url(#kfArea)' }));
    svg.append(el('path', { d, fill: 'none', stroke: 'url(#kfLine)', 'stroke-width': 3, 'stroke-linecap': 'round' }));

    pts.forEach(([px, py], i) => {
      const last = i === pts.length - 1;
      svg.append(el('circle', { cx: px, cy: py, r: last ? 5.5 : 3.5, fill: '#fff', stroke: '#6d4cf0', 'stroke-width': 2 }));
      svg.append(el('text', { class: 'ax', x: px, y: H - 8, 'text-anchor': 'middle' }, labels[i] || ''));
    });

    const [lx, ly] = pts[pts.length - 1];
    const tx = Math.min(lx, W - 26);
    svg.append(el('rect', { class: 'tip-bg', x: tx - 20, y: ly - 34, width: 40, height: 22, rx: 8 }));
    svg.append(el('text', { class: 'tip-tx', x: tx, y: ly - 19 }, values[values.length - 1]));

    host.replaceChildren(svg);
  };
  $$('.line-chart').forEach(drawChart);
})();
