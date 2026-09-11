from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

qr_script = '<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js" defer></script>'

analytics_block = '''<script>
(function () {
  const queue = [];

  function sanitize(value) {
    return String(value || 'altro').toLowerCase().replace(/[^a-z0-9_-]/g, '-');
  }

  function send(path, title) {
    const event = { path, title, event: true, no_session: true };
    if (window.goatcounter && typeof window.goatcounter.count === 'function') {
      window.goatcounter.count(event);
    } else {
      queue.push(event);
    }
  }

  window.__flushGoatCounter = function () {
    if (!window.goatcounter || typeof window.goatcounter.count !== 'function') return;
    while (queue.length) window.goatcounter.count(queue.shift());
  };

  if (typeof window.gtag !== 'function') {
    window.gtag = function (command, eventName, params) {
      if (command !== 'event') return;
      params = params || {};

      if (eventName === 'nuova_opportunita_quiz_view') {
        return; // La visualizzazione viene già registrata automaticamente da GoatCounter.
      }

      if (eventName === 'nuova_opportunita_quiz_start') {
        send('quiz-start', 'Quiz iniziato');
        return;
      }

      if (eventName === 'nuova_opportunita_quiz_complete') {
        const score = Number.isFinite(params.score) ? params.score : 'n';
        send('quiz-complete', 'Quiz completato');
        send('quiz-score-' + score, 'Punteggio quiz: ' + score + '/10');
        return;
      }

      if (eventName === 'nuova_opportunita_contact_click') {
        const type = sanitize(params.contact_type);
        send('contact-' + type, 'Contatto: ' + type);
      }
    };
  }
})();
</script>
<script data-goatcounter="https://comunicazioneporticonlus.goatcounter.com/count"
        async
        onload="window.__flushGoatCounter && window.__flushGoatCounter()"
        src="https://gc.zgo.at/count.js"></script>'''

if 'https://comunicazioneporticonlus.goatcounter.com/count' not in text:
    if qr_script not in text:
        raise SystemExit('QRCode script marker not found')
    text = text.replace(qr_script, qr_script + '\n' + analytics_block, 1)

copy_old = '<button class="small-btn" type="button" onclick="copyCurrentLink()" id="copy-btn">Copia link</button>'
copy_new = '<button class="small-btn" type="button" onclick="copyCurrentLink()" id="copy-btn" data-goatcounter-click="share-copy-link" data-goatcounter-title="Copia link quiz" data-goatcounter-no-session="1">Copia link</button>'
if copy_old in text:
    text = text.replace(copy_old, copy_new, 1)

share_old = '<button class="small-btn" type="button" onclick="shareQuiz()" id="share-btn">Condividi</button>'
share_new = '<button class="small-btn" type="button" onclick="shareQuiz()" id="share-btn" data-goatcounter-click="share-button" data-goatcounter-title="Condividi quiz" data-goatcounter-no-session="1">Condividi</button>'
if share_old in text:
    text = text.replace(share_old, share_new, 1)

p.write_text(text, encoding='utf-8')
