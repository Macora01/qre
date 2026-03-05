// Beep sound utility - generates a WAV beep and manages mobile audio unlock
let beepAudio = null;

function init() {
  if (beepAudio) return;
  const sr = 8000, dur = 0.15, freq = 1200;
  const n = sr * dur;
  const buf = new ArrayBuffer(44 + n * 2);
  const v = new DataView(buf);
  const ws = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  ws(0,'RIFF'); v.setUint32(4,36+n*2,true); ws(8,'WAVE'); ws(12,'fmt ');
  v.setUint32(16,16,true); v.setUint16(20,1,true); v.setUint16(22,1,true);
  v.setUint32(24,sr,true); v.setUint32(28,sr*2,true); v.setUint16(32,2,true);
  v.setUint16(34,16,true); ws(36,'data'); v.setUint32(40,n*2,true);
  for (let i = 0; i < n; i++) {
    v.setInt16(44 + i * 2, Math.sin(2 * Math.PI * freq * i / sr) * 0.4 * 32767, true);
  }
  beepAudio = new Audio(URL.createObjectURL(new Blob([buf], { type: 'audio/wav' })));
  beepAudio.volume = 1.0;
}

// Call this from a user gesture (click/tap) to unlock audio on mobile
export function unlockBeep() {
  init();
  beepAudio.play().then(() => {
    beepAudio.pause();
    beepAudio.currentTime = 0;
  }).catch(() => {});
}

// Call this to play the beep (must be unlocked first)
export function playBeep() {
  if (!beepAudio) return;
  beepAudio.currentTime = 0;
  beepAudio.play().catch(() => {});
}
