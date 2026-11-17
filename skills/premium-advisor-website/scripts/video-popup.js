(function () {
  const root = document.querySelector('ROOT_SELECTOR');
  const dialog = document.getElementById('DIALOG_ID');
  if (!root || !dialog || dialog.dataset.initialized) return;
  dialog.dataset.initialized = 'true';
  const player = dialog.querySelector('video');
  const title = dialog.querySelector('h2');
  const error = dialog.querySelector('[data-video-error]');
  const fallback = error.querySelector('a');
  let opener = null;
  let overflow = '';
  root.addEventListener('click', function (event) {
    const link = event.target.closest('a[href]');
    if (!link || !root.contains(link) || event.defaultPrevented || event.button !== 0 ||
        event.metaKey || event.ctrlKey || event.shiftKey || event.altKey ||
        typeof dialog.showModal !== 'function') return;
    let url;
    try { url = new URL(link.href); } catch (_) { return; }
    if (url.hostname !== 'player.vimeo.com' ||
        !/^\/progressive_redirect\/playback\/\d+\/rendition\/720p\//.test(url.pathname)) return;
    event.preventDefault();
    opener = link;
    const image = link.querySelector('img');
    title.textContent = (link.getAttribute('aria-label') || (image && image.alt) || 'Watch video')
      .replace(/^Watch\s+/i, '').replace(/^\s*\d{1,2}[.)]\s+/, '');
    error.hidden = true;
    fallback.href = link.href;
    if (image) player.poster = image.src;
    else player.removeAttribute('poster');
    player.src = link.href;
    overflow = document.documentElement.style.overflow;
    dialog.showModal();
    document.documentElement.style.overflow = 'hidden';
    dialog.querySelector('button').focus();
    const promise = player.play();
    if (promise) promise.catch(function () { /* Native controls allow manual playback. */ });
  });
  dialog.querySelector('button').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (event) {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', function () {
    player.pause();
    player.removeAttribute('src');
    player.load();
    error.hidden = true;
    document.documentElement.style.overflow = overflow;
    if (opener && opener.isConnected) opener.focus({ preventScroll: true });
  });
  player.addEventListener('error', function () {
    if (dialog.open && player.hasAttribute('src')) error.hidden = false;
  });
})();
