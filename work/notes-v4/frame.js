      // ---------- the frame (v4: phone-first type, every word readable at arm's length) ----------
      // Type scale on a 1080 px frame, seen at about a third of that size on a phone:
      //   display 132 to 150 px (Playfair 900), hero numbers 360 px, labels 58 to 64 px (Inter 800),
      //   nothing under 48 px. All text in full ink or full plum. No thin hairline serif, no greys.
      const DISP = '"Playfair Display", Georgia, serif';
      var draw = function (t) {
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        const push = 1 + 0.02 * (t / DUR), ox = 540, oy = 900;
        ctx.setTransform(push, 0, 0, push, ox - ox * push, oy - oy * push);
        ctx.drawImage(paper, -80, -80);
        const lx = lerp(220, 760, t / DUR), ly = lerp(260, 420, t / DUR);
        let g = ctx.createRadialGradient(lx, ly, 0, lx, ly, 1500);
        g.addColorStop(0, 'rgba(255,250,242,0.5)'); g.addColorStop(1, 'rgba(255,240,225,0)');
        ctx.fillStyle = g; ctx.fillRect(-100, -100, W + 200, H + 200);
        ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';

        const H1 = `900 140px ${DISP}`;          // headlines
        const H1i = `italic 900 140px ${DISP}`;
        const LAB = `800 60px ${SANS}`;           // labels

        // ink rule above every headline
        const rule = (a, b) => { const k = ez('expo.out', t, a, a + 0.5) * (1 - ez('power2.in', t, b, b + 0.3)); if (k > 0) { ctx.fillStyle = INK; ctx.fillRect(ML, 300, 120 * k, 14); } };

        // 1. title (0 to 7.4)
        rule(0, C.brain - 0.3);
        maskWords(['What', 'never'], ML, 470, H1, INK, t, 0.1, C.notes - 0.35);
        maskWords(['makes', 'the'], ML, 610, H1, INK, t, 0.28, C.notes - 0.3);
        maskWords(['notes.'], ML, 750, H1i, ACC, t, 0.46, C.notes - 0.25, 0.09, 0);

        // 2. the comparison (3.6 to 7.4)
        {
          const k = ez('power3.out', t, C.notes - 0.15, C.notes + 0.3), o = ez('power2.in', t, C.brain - 0.4, C.brain - 0.1);
          if (k > 0 && o < 1) {
            ctx.save(); ctx.globalAlpha = k * (1 - o);
            ctx.font = LAB; ctx.fillStyle = ACC;
            ctx.fillText('1 online community', ML, 470 + 24 * (1 - k));
            ctx.fillStyle = INK; ctx.fillText('compared with', ML, 560 + 24 * (1 - k));
            const n = Math.round(2000000 * ez('expo.out', t, C.notes + 0.2, C.notes + 2.2));
            ctx.shadowColor = 'rgba(60,35,15,0.18)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 12;
            ctx.font = `900 172px ${DISP}`;
            const s = n.toLocaleString('en-GB');
            ctx.fillText(s, ML - 4, 780 + 30 * (1 - k));
            const sw = ctx.measureText(s).width;
            ctx.font = `900 110px ${DISP}`; ctx.fillText('+', ML + sw + 6, 760 + 30 * (1 - k));
            ctx.shadowColor = 'transparent';
            ctx.font = LAB; ctx.fillText('medical notes', ML, 880 + 24 * (1 - ez('power3.out', t, C.notes + 0.4, C.notes + 0.9)));
            ctx.restore();
            // notes stacking: thick record edges filling the space below, one per beat
            ctx.save(); ctx.globalAlpha = 1 - o;
            for (let i = 0; i < 9; i++) {
              const at = C.notes + 0.6 + i * 0.33, kk = ez('power3.out', t, at, at + 0.35);
              if (kk <= 0) continue;
              ctx.fillStyle = i % 2 ? '#E2CDBA' : '#D7BFA9';
              ctx.fillRect(ML + 8 * (i % 3), 960 + i * 34 + 20 * (1 - kk), (MR - ML - 30) * kk, 22);
            }
            ctx.restore();
          }
        }

        // 3. three symptoms, big, one per cue (7.44 to 12.29)
        {
          const o = ez('power2.in', t, C.four - 0.4, C.four - 0.05);
          const sym = [['Brain fog.', C.brain, 470], ['Memory slips.', C.memory, 640], ['Losing words', C.words, 810]];
          sym.forEach(([txt, at, y]) => {
            const k = ez('power3.out', t, at, at + 0.45);
            if (k <= 0 || o >= 1) return;
            ctx.save(); ctx.globalAlpha = 1 - o;
            ctx.beginPath(); ctx.rect(ML - 10, y - 150, MR - ML + 40, 190); ctx.clip();
            ctx.font = H1; ctx.fillStyle = INK; ctx.fillText(txt, ML, y + 150 * (1 - k));
            ctx.restore();
          });
          // "mid-sen" typed then the word goes missing; a plum caret blinks where it went
          const t0 = C.words + 0.9;
          if (t > t0 && o < 1) {
            const full = 'mid-sen';
            const n = Math.min(full.length, Math.floor((t - t0) / 0.07));
            ctx.save(); ctx.globalAlpha = 1 - o; ctx.font = H1i; ctx.fillStyle = ACC;
            ctx.fillText(full.slice(0, n), ML, 980);
            const w = ctx.measureText(full.slice(0, n)).width;
            if (Math.floor(t * 2.2) % 2 === 0 || t < t0 + 0.6) { ctx.fillRect(ML + w + 10, 870, 10, 130); }
            ctx.restore();
          }
        }

        // 4 and 5. the bars: notes vs online (12.29 to 20.23)
        {
          const o = ez('power2.in', t, C.real - 0.35, C.real - 0.05);
          const inA = ez('power3.out', t, C.four, C.four + 0.5);
          if (inA > 0 && o < 1) {
            ctx.save(); ctx.globalAlpha = 1 - o;
            const mood = ez('power3.inOut', t, C.mood, C.mood + 0.6);    // switch from the first group to mood
            const ratio = lerp(3.9, 2.9, ez('power3.inOut', t, C.three - 0.1, C.three + 0.9));
            const unit = 205;
            // group heading
            ctx.save(); ctx.beginPath(); ctx.rect(ML - 10, 380, MR - ML + 40, 120); ctx.clip();
            ctx.font = `800 64px ${SANS}`; ctx.fillStyle = INK;
            ctx.fillText('Brain fog, memory, words', ML, 470 + 120 * (1 - inA) - 120 * mood);
            ctx.fillText('Mood changes', ML, 470 + 120 * (1 - mood));
            ctx.restore();
            // hero multiplier
            const nk = ez('power3.out', t, C.four + 0.6, C.four + 1.1);
            const n1 = Math.max(1, Math.round(4 * ez('expo.out', t, C.four + 0.6, C.four + 1.8)));
            const n = mood < 0.5 ? n1 : Math.max(1, Math.round(3 * ez('expo.out', t, C.three, C.three + 1.0)));
            ctx.save(); ctx.globalAlpha = nk * (1 - o);
            ctx.font = `900 360px ${DISP}`; ctx.fillStyle = ACC;
            ctx.shadowColor = 'rgba(40,20,60,0.22)'; ctx.shadowBlur = 26; ctx.shadowOffsetY = 14;
            const wd = ctx.measureText(String(n)).width;
            ctx.fillText(String(n), ML - 8, 860);
            ctx.font = `900 170px ${DISP}`; ctx.fillText('×', ML + wd + 4, 860);
            ctx.shadowColor = 'transparent';
            ctx.font = LAB; ctx.fillStyle = INK; ctx.fillText('as often', ML + wd + 150, 780); ctx.fillText('online', ML + wd + 150, 856);
            ctx.restore();
            // two thick bars with their labels above
            const yA = 1010, yB = 1210;
            const lk = ez('power3.out', t, C.four + 0.2, C.four + 0.7);
            ctx.font = LAB; ctx.fillStyle = INK;
            ctx.globalAlpha = lk * (1 - o); ctx.fillText('In medical notes', ML, yA - 24);
            ctx.fillStyle = ACC; ctx.fillText('Online', ML, yB - 24);
            ctx.globalAlpha = 1 - o;
            const ib = ez('power3.out', t, C.four + 0.3, C.four + 0.9);
            ctx.fillStyle = INK; ctx.fillRect(ML, yA, unit * ib, 96);
            const grow = ez('power3.inOut', t, C.four + 0.9, C.four + 2.4);
            const len = lerp(unit, unit * ratio, grow);
            ctx.shadowColor = 'rgba(40,20,60,0.25)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 8;
            ctx.fillStyle = ACC; ctx.fillRect(ML, yB, len * ib, 96);
            ctx.shadowColor = 'transparent';
            // 1x ticks under the online bar so the multiple can be counted
            for (let u = 1; u < Math.floor(ratio + 0.05); u++) {
              const x = ML + unit * u; if (x > ML + len * ib - 8) continue;
              ctx.fillStyle = 'rgba(255,241,229,0.75)'; ctx.fillRect(x - 2, yB, 4, 96);
            }
            ring(ML + len, yB + 48, ACC, t, C.four + 2.4);
            ring(ML + len, yB + 48, ACC, t, C.three + 0.9);
            // light sweep once proven
            const sk = seg(t, 15.2, 16.6) || 0;
            if (sk > 0 && sk < 1) {
              const cx = lerp(ML - 300, MR + 300, E['power2.inOut'](sk));
              ctx.save(); ctx.beginPath(); ctx.rect(ML, yB, len, 96); ctx.clip();
              const lg = ctx.createLinearGradient(cx - 200, 0, cx + 200, 0);
              lg.addColorStop(0, 'rgba(255,255,255,0)'); lg.addColorStop(0.5, 'rgba(255,255,255,0.5)'); lg.addColorStop(1, 'rgba(255,255,255,0)');
              ctx.fillStyle = lg; ctx.fillRect(ML, yB, MR - ML, 96); ctx.restore();
            }
            ctx.restore();
          }
        }

        // 6. the point (20.23 to 24.22)
        rule(C.real, C.so - 0.4);
        maskWords(['The', 'symptoms'], ML, 470, H1, INK, t, C.real + 0.05, C.so - 0.45);
        maskWords(['are', 'real.'], ML, 610, H1, INK, t, C.real + 0.25, C.so - 0.42);
        maskWords(['Not', 'written'], ML, 820, H1i, ACC, t, C.written + 0.05, C.so - 0.4, 0.09, 0);
        maskWords(['down.'], ML, 960, H1i, ACC, t, C.written + 0.25, C.so - 0.38, 0.09, 0);
        {
          const k = ez('power2.inOut', t, C.written + 0.7, C.written + 1.5), o = ez('power2.in', t, C.so - 0.45, C.so - 0.1);
          if (k > 0 && o < 1) { ctx.save(); ctx.globalAlpha = 1 - o; ctx.fillStyle = ACC; ctx.fillRect(ML, 1000, 560 * k, 12); ctx.restore(); }
        }

        // 7. one week, logged (24.22 to 28.82)
        rule(C.so, C.take - 0.4);
        maskWords(['Write', 'it'], ML, 470, H1, INK, t, C.so + 0.05, C.take - 0.45);
        maskWords(['down.'], ML, 610, H1, INK, t, C.so + 0.2, C.take - 0.42);
        {
          const wkIn = ez('expo.out', t, C.so + 0.3, C.so + 1.0), wkOut = ez('power2.in', t, C.take - 0.4, C.take - 0.05);
          if (wkIn > 0 && wkOut < 1) {
            const days = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
            const cw = (MR - ML) / 7, top = 720, hgt = 600;
            ctx.save(); ctx.globalAlpha = 1 - wkOut;
            for (let d = 0; d < 7; d++) {
              const x = ML + d * cw, k = ez('power3.out', t, C.so + 0.3 + d * 0.22, C.so + 1.0 + d * 0.22);
              ctx.strokeStyle = '#D9C6B4'; ctx.lineWidth = 3;
              ctx.beginPath(); ctx.moveTo(x + cw, top + 90); ctx.lineTo(x + cw, lerp(top + 90, top + hgt, k)); ctx.stroke();
              ctx.globalAlpha = (1 - wkOut) * k;
              ctx.font = `800 52px ${SANS}`; ctx.fillStyle = INK; ctx.textAlign = 'center';
              ctx.fillText(days[d], x + cw / 2, top + 54 + 14 * (1 - k));
              ctx.globalAlpha = 1 - wkOut;
            }
            ctx.textAlign = 'left';
            ctx.fillStyle = INK; ctx.fillRect(ML, top + 84, (MR - ML) * wkIn, 5);
            const entries = [{ d: 1, y: 0.60, s: 2, at: C.when + 0.1 }, { d: 3, y: 0.25, s: 1, at: C.often + 0.15 }, { d: 5, y: 0.80, s: 3, at: C.often + 0.45 }];
            entries.forEach(en => {
              const k = E['back.out(2.2)'](seg(t, en.at, en.at + 0.35)); if (k <= 0) return;
              const x = ML + en.d * cw + cw / 2, y = top + 150 + en.y * (hgt - 230), sz = lerp(0.6, 1, k) * 52;
              const wk = ez('power3.out', t, en.at, en.at + 0.5);
              ctx.save(); ctx.globalAlpha = 0.18 * wk; ctx.fillStyle = ACC; ctx.fillRect(ML + en.d * cw + 3, top + 90, cw - 6, (hgt - 90) * wk); ctx.restore();
              ctx.save();
              ctx.shadowColor = 'rgba(60,35,15,0.28)'; ctx.shadowBlur = 12; ctx.shadowOffsetY = 6;
              ctx.fillStyle = PAPER; ctx.beginPath(); ctx.arc(x, y, sz + 10, 0, Math.PI * 2); ctx.fill();
              ctx.shadowColor = 'transparent';
              ctx.strokeStyle = ACC; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(x, y, sz, 0, Math.PI * 2); ctx.stroke();
              const f0 = Math.max(0.2, en.s / 3 * ez('power3.out', t, C.much, C.much + 0.6));
              ctx.beginPath(); ctx.arc(x, y, sz, 0, Math.PI * 2); ctx.clip();
              ctx.fillStyle = ACC; ctx.fillRect(x - sz, y + sz - 2 * sz * f0, 2 * sz, 2 * sz * f0);
              ctx.restore();
              ring(x, y, ACC, t, en.at);
            });
            ctx.restore();
          }
        }

        // 8. end card
        rule(C.take, 99);
        maskWords(['Take', 'it', 'with'], ML, 470, H1, INK, t, C.take + 0.05, null);
        maskWords(['you.'], ML, 610, H1i, ACC, t, C.take + 0.3, null, 0.09, 0);
        {
          const k = ez('power3.out', t, C.clari - 0.1, C.clari + 0.5);
          if (k > 0) {
            const y = 860 + 40 * (1 - k);
            ctx.save(); ctx.globalAlpha = k;
            ctx.shadowColor = 'rgba(40,20,60,0.25)'; ctx.shadowBlur = 22; ctx.shadowOffsetY = 10;
            moonMark(ML + 80, y, 80 * lerp(0.85, 1, E['back.out(1.2)'](seg(t, C.clari - 0.1, C.clari + 0.4))), 1);
            ctx.shadowColor = 'transparent';
            ctx.fillStyle = INK; ctx.font = `900 150px ${DISP}`; ctx.fillText('Clari', ML + 196, y + 52);
            ctx.restore();
            const lk = ez('power3.out', t, C.clari + 0.75, C.clari + 1.25);
            ctx.save(); ctx.globalAlpha = lk; ctx.font = `800 58px ${SANS}`; ctx.fillStyle = INK;
            ctx.fillText('The private', ML, 1060 + 16 * (1 - lk));
            ctx.fillText('perimenopause diary', ML, 1134 + 16 * (1 - lk));
            const ck = ez('power3.out', t, C.clari + 1.6, C.clari + 2.1);
            ctx.globalAlpha = ck; ctx.font = `600 44px ${SANS}`;
            ctx.fillText('Data: JAMA Network Open, 2026', ML, 1260);
            ctx.restore();
          }
        }
      };

      // ---------- captions (for people watching muted), timed to the voice ----------
      const CAP = [
        [0.0, 1.2, 'Researchers compared'], [1.2, 2.4, 'one of the biggest'], [2.4, 3.5, 'online menopause communities'],
        [3.6, 4.6, 'with more than'], [4.6, 6.5, 'two million medical notes.'],
        [7.44, 8.3, 'Brain fog.'], [8.6, 9.6, 'Memory slips.'], [9.96, 10.8, 'Losing words'], [10.8, 11.7, 'mid-sentence.'],
        [12.29, 13.3, 'Women talked about these'], [13.3, 14.6, 'nearly four times as often'], [14.6, 15.5, 'as they showed up'], [15.5, 16.45, 'in the notes.'],
        [16.94, 17.8, 'Mood changes?'], [18.13, 19.45, 'Nearly three times.'],
        [20.23, 21.6, 'The symptoms are real.'], [21.99, 22.8, 'They just don’t get'], [22.8, 23.5, 'written down.'],
        [24.22, 25.35, 'So write them down.'], [25.73, 26.6, 'When it happens,'], [26.6, 27.5, 'how often,'], [27.65, 28.4, 'how much.'],
        [28.82, 29.8, 'And take it with you.'], [30.29, 31.9, 'That’s what Clari is for.'],
      ];
      // captions sit on a solid ink plate: highest possible contrast, readable over anything
      function captions(t) {
        for (let i = 0; i < CAP.length; i++) {
          const [a, b0, txt] = CAP[i];
          const nxt = i + 1 < CAP.length ? CAP[i + 1][0] : 99;
          const b = Math.min(b0, nxt - 0.12);
          if (t < a || t >= b + 0.12) continue;
          const k = ez('power3.out', t, a, a + 0.18), o = ez('power2.in', t, b, b + 0.12);
          ctx.save(); ctx.globalAlpha = k * (1 - o);
          ctx.font = `800 58px ${SANS}`; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
          const w = ctx.measureText(txt).width, y = 1452 + 14 * (1 - k);
          ctx.fillStyle = INK; ctx.beginPath(); ctx.roundRect(ML - 22, y - 62, w + 44, 86, 14); ctx.fill();
          ctx.fillStyle = '#FFF1E5'; ctx.fillText(txt, ML, y);
          ctx.restore();
        }
      }
      const _draw = draw;
      draw = (t) => { _draw(t); ctx.setTransform(1, 0, 0, 1, 0, 0); captions(t); };

      const tl = gsap.timeline({ paused: true });
      const p = { t: 0 };
      tl.to(p, { t: DUR, duration: DUR, ease: 'none', onUpdate: () => draw(p.t) }, 0);
      window.__timelines['main'] = tl;
      draw(0);
      tl.seek(0);
      Promise.all(['900 140px "Playfair Display"', 'italic 900 140px "Playfair Display"', '800 60px "Inter"', '600 44px "Inter"']
        .map(f => document.fonts.load(f))).then(() => draw(p.t));
    </script>
  </body>
</html>
