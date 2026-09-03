  // syntax highlighting
  if (window.hljs) { document.querySelectorAll('pre code').forEach(el => hljs.highlightElement(el)); }

  // theme toggle (three-state, matches token system)
  const root = document.documentElement;
  const btns = document.querySelectorAll('.tog button');
  function setTheme(mode){
    if (mode === 'auto') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', mode);
    btns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.set === mode)));
    try { localStorage.setItem('pp-theme', mode); } catch(e){}
  }
  btns.forEach(b => b.addEventListener('click', () => setTheme(b.dataset.set)));
  let saved = 'auto';
  try { saved = localStorage.getItem('pp-theme') || 'auto'; } catch(e){}
  setTheme(saved);
