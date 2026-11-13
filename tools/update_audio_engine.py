import re
from pathlib import Path

app_js_path = Path(r"C:\Users\user\Desktop\words-app\webapp\js\app.js")
code = app_js_path.read_text(encoding="utf-8")

# 1. Update toggleFlip
code = code.replace(
    "function toggleFlip() {\n    if (state.isEndState || state.isAnimating) return;\n    state.isFlipped = !state.isFlipped;",
    "function toggleFlip() {\n    if (state.isEndState || state.isAnimating) return;\n    stopAllAudio();\n    state.isFlipped = !state.isFlipped;"
)

# 2. Update goNext
code = code.replace(
    "function goNext() {\n    if (state.isAnimating) return;\n    triggerHaptic(\"light\");",
    "function goNext() {\n    if (state.isAnimating) return;\n    stopAllAudio();\n    triggerHaptic(\"light\");"
)

# 3. Update goPrev
code = code.replace(
    "function goPrev() {\n    if (state.isAnimating) return;\n    if (!state.isEndState && state.currentIndex <= 0) return;\n\n    triggerHaptic(\"light\");",
    "function goPrev() {\n    if (state.isAnimating) return;\n    if (!state.isEndState && state.currentIndex <= 0) return;\n\n    stopAllAudio();\n    triggerHaptic(\"light\");"
)

# 4. Update restartDeck
code = code.replace(
    "function restartDeck() {\n    triggerHaptic(\"light\");",
    "function restartDeck() {\n    stopAllAudio();\n    triggerHaptic(\"light\");"
)

# 5. Update toggleShuffle
code = code.replace(
    "function toggleShuffle() {\n    triggerHaptic(\"light\");",
    "function toggleShuffle() {\n    stopAllAudio();\n    triggerHaptic(\"light\");"
)

# 6. Update openCategorySheet
code = code.replace(
    "function openCategorySheet() {\n    triggerHaptic(\"light\");",
    "function openCategorySheet() {\n    stopAllAudio();\n    triggerHaptic(\"light\");"
)

# 7. Update selectDeckFromSheet
code = code.replace(
    "async function selectDeckFromSheet(deckId) {\n    triggerHaptic(\"light\");",
    "async function selectDeckFromSheet(deckId) {\n    stopAllAudio();\n    triggerHaptic(\"light\");"
)

# Replace the entire audio implementation block
old_pattern = re.compile(
    r"  // =========================================================================\n"
    r"  // English Pronunciation Speech \(Web Speech API \+ HTML5 Audio Fallback\)\n"
    r"  // =========================================================================\n"
    r".*?"
    r"    if \(dom\.exampleSpeakBtn\) \{\n"
    r"      dom\.exampleSpeakBtn\.addEventListener\(\"click\", \(e\) => \{\n"
    r"        e\.stopPropagation\(\);\n"
    r"        const word = state\.activeWords\[state\.currentIndex\];\n"
    r"        if \(word\) speakText\(word\.example_en, dom\.exampleSpeakBtn\);\n"
    r"      \}\);\n"
    r"    \}\n",
    re.DOTALL
)

new_audio_block = """  // =========================================================================
  // Native English Audio Engine (Authentic American English Pronunciation)
  // - 100% Native English voice (Youdao American Studio + Google Translate TTS)
  // - NEVER uses system-default or Russian device voice
  // - Single audio stream with instant cancellation (prevents dual/overlapping audio)
  // - Debounced button clicks with pulsing visual feedback
  // =========================================================================
  let currentAudio = null;
  let currentAudioBtn = null;
  let audioThrottleTime = 0;

  function stopAllAudio() {
    if (currentAudio) {
      try {
        currentAudio.pause();
        currentAudio.currentTime = 0;
      } catch (_) {}
      currentAudio = null;
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

    // Throttle rapid clicks (prevent rapid sound pileup)
    const now = Date.now();
    if (now - audioThrottleTime < 280) return;
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
    }
    // High-quality Google Translate native English TTS (works for both words and full sentences)
    candidateUrls.push(`https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=${encodeURIComponent(clean)}`);

    let candidateIndex = 0;

    function tryNextCandidate() {
      if (candidateIndex >= candidateUrls.length) {
        // As a last-resort fallback: only use SpeechSynthesis IF an explicit English voice exists!
        fallbackVerifiedSpeechSynthesis(clean, btnEl);
        return;
      }

      const audioUrl = candidateUrls[candidateIndex++];
      const audio = new Audio();
      currentAudio = audio;

      const finishPlayback = () => {
        if (currentAudio === audio) {
          currentAudio = null;
        }
        if (btnEl) btnEl.classList.remove("is-speaking");
        if (currentAudioBtn === btnEl) currentAudioBtn = null;
      };

      audio.onended = finishPlayback;
      audio.onerror = () => {
        if (currentAudio === audio) {
          tryNextCandidate();
        }
      };

      audio.play().catch(() => {
        if (currentAudio === audio) {
          tryNextCandidate();
        }
      });
    }

    tryNextCandidate();
  }

  function fallbackVerifiedSpeechSynthesis(clean, btnEl) {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      if (btnEl) btnEl.classList.remove("is-speaking");
      return;
    }

    try {
      const voices = window.speechSynthesis.getVoices();
      // STRICT FILTER: ONLY allow speech synthesis if an explicit ENGLISH voice exists!
      // NEVER fall back to Russian, Uzbek, or system-default non-English voices!
      const enVoice =
        voices.find((v) => v.lang === "en-US" && (v.name.includes("Google") || v.name.includes("Natural") || v.name.includes("Samantha") || v.name.includes("English"))) ||
        voices.find((v) => v.lang && (v.lang === "en-US" || v.lang === "en-GB")) ||
        voices.find((v) => v.lang && v.lang.startsWith("en"));

      if (!enVoice) {
        // Refuse to speak in Russian/non-English voice
        if (btnEl) btnEl.classList.remove("is-speaking");
        return;
      }

      const utter = new SpeechSynthesisUtterance(clean);
      utter.voice = enVoice;
      utter.lang = enVoice.lang || "en-US";
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

if not old_pattern.search(code):
    print("ERROR: old audio pattern not found!")
    exit(1)

code = old_pattern.sub(lambda m: new_audio_block, code)
app_js_path.write_text(code, encoding="utf-8")
print("SUCCESS: app.js updated with new Native English Audio Engine!")
