from pathlib import Path

app_js_path = Path(r"C:\Users\user\Desktop\words-app\webapp\js\app.js")
index_html_path = Path(r"C:\Users\user\Desktop\words-app\webapp\index.html")

# 1. Update index.html to add <audio id="globalAudioPlayer" preload="auto" playsinline></audio>
html = index_html_path.read_text(encoding="utf-8")
if 'id="globalAudioPlayer"' not in html:
    html = html.replace(
        '<main class="app-shell" id="appShell">',
        '<audio id="globalAudioPlayer" preload="auto" playsinline></audio>\n  <main class="app-shell" id="appShell">'
    )
    # bump cache buster
    html = html.replace("20261113_audio_v2", "20261113_audio_v3")
    index_html_path.write_text(html, encoding="utf-8")
    print("index.html updated with globalAudioPlayer!")

# 2. Update app.js
code = app_js_path.read_text(encoding="utf-8")

# Replace playNativeAudio function block
old_engine_marker = "  // Native English Audio Engine (Authentic American English Pronunciation)"
start_idx = code.find(old_engine_marker)
if start_idx == -1:
    print("ERROR: old_engine_marker not found in app.js")
    exit(1)

end_marker = "    if (dom.exampleSpeakBtn) {\n      dom.exampleSpeakBtn.addEventListener(\"click\", (e) => {\n        e.stopPropagation();\n        const word = state.activeWords[state.currentIndex];\n        if (word) playNativeAudio(word.example_en, dom.exampleSpeakBtn);\n      });\n    }\n"
end_idx = code.find(end_marker)
if end_idx == -1:
    print("ERROR: end_marker not found in app.js")
    exit(1)

new_engine_code = """  // Native English Audio Engine (Authentic American English Pronunciation)
  // - 100% Native English voice (Youdao American Studio + Google Translate TTS)
  // - NEVER uses system-default or Russian device voice
  // - Single persistent audio element with instant stop (prevents dual/overlapping audio)
  // - Debounced button clicks with pulsing visual feedback
  // =========================================================================
  let audioPlayer = null;
  let currentAudioBtn = null;
  let audioThrottleTime = 0;
  let cachedEnVoice = null;

  function initAudioEngine() {
    if (typeof document !== "undefined") {
      audioPlayer = document.getElementById("globalAudioPlayer");
      if (!audioPlayer) {
        audioPlayer = new Audio();
        audioPlayer.id = "globalAudioPlayer";
        audioPlayer.preload = "auto";
        document.body.appendChild(audioPlayer);
      }
    }

    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      const pickVoice = () => {
        try {
          const voices = window.speechSynthesis.getVoices() || [];
          cachedEnVoice =
            voices.find((v) => v.lang === "en-US" && (v.name.includes("Google") || v.name.includes("Natural") || v.name.includes("Samantha") || v.name.includes("English"))) ||
            voices.find((v) => v.lang && (v.lang === "en-US" || v.lang === "en-GB")) ||
            voices.find((v) => v.lang && v.lang.startsWith("en")) ||
            null;
        } catch (_) {}
      };
      pickVoice();
      window.speechSynthesis.onvoiceschanged = pickVoice;
    }
  }

  function stopAllAudio() {
    if (audioPlayer) {
      try {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        audioPlayer.removeAttribute("src");
      } catch (_) {}
    }
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      try {
        window.speechSynthesis.cancel();
      } catch (_) {}
    }
    if (currentAudioBtn) {
      currentAudioBtn.classList.remove("is-speaking");
      currentAudioBtn = null;
    }
  }

  function cleanTextForAudio(text) {
    if (!text) return "";
    return text
      .replace(/\\(.* *?\\)/g, "") // remove parenthetical expressions
      .replace(/[\\/\\[\\]]/g, "") // remove phonetic slashes/brackets
      .replace(/["'’]/g, "") // remove quotation marks
      .replace(/[.,!?;:]/g, " ") // replace sentence punctuation with space
      .replace(/\\s+/g, " ") // normalize spacing
      .trim();
  }

  function playNativeAudio(text, btnEl) {
    const clean = cleanTextForAudio(text);
    if (!clean) return;

    if (!audioPlayer) {
      initAudioEngine();
    }

    // Throttle rapid clicks (prevent rapid sound pileup)
    const now = Date.now();
    if (now - audioThrottleTime < 250) return;
    audioThrottleTime = now;

    // Immediately stop any currently playing sound or speech
    stopAllAudio();
    triggerHaptic("light");

    if (btnEl) {
      currentAudioBtn = btnEl;
      btnEl.classList.add("is-speaking");
    }

    const wordsCount = clean.split(" ").length;
    const candidateUrls = [];

    // For single words and short phrases: authentic American English dictionary recording
    if (wordsCount <= 4) {
      candidateUrls.push(`https://dict.youdao.com/dictvoice?audio=${encodeURIComponent(clean)}&type=2`);
      candidateUrls.push(`https://dict.youdao.com/dictvoice?audio=${encodeURIComponent(clean)}&type=1`);
    }
    // Google Translate native English TTS (works for words and full sentences)
    candidateUrls.push(`https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=${encodeURIComponent(clean)}`);

    let candidateIndex = 0;

    function tryNextCandidate() {
      if (candidateIndex >= candidateUrls.length) {
        // Fallback: Web Speech API ONLY IF an explicit verified English voice is present
        fallbackVerifiedSpeechSynthesis(clean, btnEl);
        return;
      }

      const audioUrl = candidateUrls[candidateIndex++];
      if (!audioPlayer) return;

      const finishPlayback = () => {
        cleanup();
        if (btnEl) btnEl.classList.remove("is-speaking");
        if (currentAudioBtn === btnEl) currentAudioBtn = null;
      };

      const onError = () => {
        cleanup();
        tryNextCandidate();
      };

      function cleanup() {
        audioPlayer.removeEventListener("ended", finishPlayback);
        audioPlayer.removeEventListener("error", onError);
      }

      audioPlayer.addEventListener("ended", finishPlayback, { once: true });
      audioPlayer.addEventListener("error", onError, { once: true });

      try {
        audioPlayer.src = audioUrl;
        audioPlayer.load();
        const playPromise = audioPlayer.play();
        if (playPromise !== undefined) {
          playPromise.catch(() => {
            cleanup();
            tryNextCandidate();
          });
        }
      } catch (_) {
        cleanup();
        tryNextCandidate();
      }
    }

    tryNextCandidate();
  }

  function fallbackVerifiedSpeechSynthesis(clean, btnEl) {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      if (btnEl) btnEl.classList.remove("is-speaking");
      return;
    }

    try {
      if (!cachedEnVoice) {
        const voices = window.speechSynthesis.getVoices() || [];
        cachedEnVoice =
          voices.find((v) => v.lang === "en-US" && (v.name.includes("Google") || v.name.includes("Natural") || v.name.includes("Samantha") || v.name.includes("English"))) ||
          voices.find((v) => v.lang && (v.lang === "en-US" || v.lang === "en-GB")) ||
          voices.find((v) => v.lang && v.lang.startsWith("en")) ||
          null;
      }

      if (!cachedEnVoice) {
        // STRICT: Never speak with Russian or non-English system voice
        if (btnEl) btnEl.classList.remove("is-speaking");
        return;
      }

      const utter = new SpeechSynthesisUtterance(clean);
      utter.voice = cachedEnVoice;
      utter.lang = cachedEnVoice.lang || "en-US";
      utter.rate = 0.88;

      utter.onend = () => {
        if (btnEl) btnEl.classList.remove("is-speaking");
      };
      utter.onerror = () => {
        if (btnEl) btnEl.classList.remove("is-speaking");
      };

      window.speechSynthesis.speak(utter);
    } catch (_) {
      if (btnEl) btnEl.classList.remove("is-speaking");
    }
  }

  function bindEvents() {
    initAudioEngine();
    bindCardGestures();

    if (dom.speakBtn) {
      dom.speakBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const word = state.activeWords[state.currentIndex];
        if (word) playNativeAudio(word.english, dom.speakBtn);
      });
    }

    if (dom.ipaPill) {
      dom.ipaPill.addEventListener("click", (e) => {
        e.stopPropagation();
        const word = state.activeWords[state.currentIndex];
        if (word) playNativeAudio(word.english, dom.speakBtn);
      });
    }

    if (dom.pronunciationPill) {
      dom.pronunciationPill.addEventListener("click", (e) => {
        e.stopPropagation();
        const word = state.activeWords[state.currentIndex];
        if (word) playNativeAudio(word.english, dom.speakBtn);
      });
    }

    if (dom.exampleSpeakBtn) {
      dom.exampleSpeakBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const word = state.activeWords[state.currentIndex];
        if (word) playNativeAudio(word.example_en, dom.exampleSpeakBtn);
      });
    }
"""

code = code[:start_idx] + new_engine_code + code[end_idx + len(end_marker):]
app_js_path.write_text(code, encoding="utf-8")
print("SUCCESS: app.js updated with working Audio player!")
