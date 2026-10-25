/**
 * English -> Uzbek Minimal Word Cards (Telegram Mini App)
 * Scalable multi-deck architecture (5,000+ words, instant startup, lazy background loading).
 */
(function () {
  "use strict";

  const STORAGE_KEY = "uz_words_app_state_v3";
  const ALL_DECK_ID = "ALL";

  // 10 Gradient Accent Palettes (cycled via deck.accentIndex % 10)
  const ACCENT_PALETTES = [
    { name: "indigo", start: "#4F46E5", end: "#6366F1", rgb: "79, 70, 229" },
    { name: "teal", start: "#0D9488", end: "#14B8A6", rgb: "13, 148, 136" },
    { name: "amber", start: "#D97706", end: "#F59E0B", rgb: "217, 119, 6" },
    { name: "rose", start: "#E11D48", end: "#F43F5E", rgb: "225, 29, 72" },
    { name: "violet", start: "#7C3AED", end: "#8B5CF6", rgb: "124, 58, 237" },
    { name: "sky", start: "#0284C7", end: "#0EA5E9", rgb: "2, 132, 199" },
    { name: "emerald", start: "#059669", end: "#10B981", rgb: "5, 150, 105" },
    { name: "pink", start: "#DB2777", end: "#EC4899", rgb: "219, 39, 119" },
    { name: "slate", start: "#475569", end: "#64748B", rgb: "71, 85, 105" },
    { name: "orange", start: "#EA580C", end: "#F97316", rgb: "234, 88, 12" },
  ];

  const POS_LABELS = {
    noun: "noun • ot",
    verb: "verb • feʻl",
    adj: "adj • sifat",
    adv: "adv • ravish",
    prep: "prep • koʻmakchi",
    pron: "pron • olmosh",
    conj: "conj • bogʻlovchi",
    phr: "phr • ibora feʻl",
    idiom: "idiom • ibora",
  };

  // DOM Elements
  const dom = {
    categoryChipBtn: document.getElementById("categoryChipBtn"),
    chipLabel: document.getElementById("chipLabel"),
    progressCounter: document.getElementById("progressCounter"),
    progressTrack: document.getElementById("progressTrack"),
    progressFill: document.getElementById("progressFill"),
    shuffleBtn: document.getElementById("shuffleBtn"),
    openCategoriesBtn: document.getElementById("openCategoriesBtn"),

    cardScene: document.getElementById("cardScene"),
    wordCard: document.getElementById("wordCard"),
    endStateCard: document.getElementById("endStateCard"),
    endSubtitle: document.getElementById("endSubtitle"),
    restartBtn: document.getElementById("restartBtn"),

    frontCategoryTag: document.getElementById("frontCategoryTag"),
    frontIndexBadge: document.getElementById("frontIndexBadge"),
    englishWord: document.getElementById("englishWord"),
    pronunciationText: document.getElementById("pronunciationText"),
    posBadge: document.getElementById("posBadge"),

    backCategoryTag: document.getElementById("backCategoryTag"),
    backIndexBadge: document.getElementById("backIndexBadge"),
    uzbekWord: document.getElementById("uzbekWord"),
    exampleEn: document.getElementById("exampleEn"),
    exampleUz: document.getElementById("exampleUz"),
    backPosBadge: document.getElementById("backPosBadge"),

    prevBtn: document.getElementById("prevBtn"),
    nextBtn: document.getElementById("nextBtn"),

    sheetBackdrop: document.getElementById("sheetBackdrop"),
    categorySheet: document.getElementById("categorySheet"),
    closeSheetBtn: document.getElementById("closeSheetBtn"),
    deckSearchInput: document.getElementById("deckSearchInput"),
    clearSearchBtn: document.getElementById("clearSearchBtn"),
    categoryList: document.getElementById("categoryList"),
  };

  // In-memory cache of loaded deck files: { [relPath]: Array<Word> }
  const fileCache = Object.create(null);

  // Application State
  const state = {
    manifest: null,
    decksById: Object.create(null),
    selectedDeckId: ALL_DECK_ID,
    activeWords: [],
    expectedTotal: 0,
    isShuffled: false,
    shuffleSeed: 104729,
    positions: Object.create(null), // { [deckId]: number }
    currentIndex: 0,
    isFlipped: false,
    isEndState: false,
    isAnimating: false,
    loadToken: 0, // Cancels stale background lazy-loading tasks when switching decks
    searchQuery: "",
  };

  // =========================================================================
  // Telegram WebApp SDK & Theme & Haptics
  // =========================================================================
  const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;

  function initTelegram() {
    if (tg) {
      try {
        tg.ready();
        tg.expand();
      } catch (_) {}
    }
    applyTheme();
    if (tg && typeof tg.onEvent === "function") {
      tg.onEvent("themeChanged", applyTheme);
    }
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", applyTheme);
  }

  function applyTheme() {
    const params = new URLSearchParams(window.location.search);
    const forced = params.get("theme");
    let scheme = "light";

    if (forced === "dark" || forced === "light") {
      scheme = forced;
    } else if (tg && tg.colorScheme) {
      scheme = tg.colorScheme;
    } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      scheme = "dark";
    }

    document.documentElement.setAttribute("data-theme", scheme);
    if (tg && typeof tg.setHeaderColor === "function") {
      try {
        tg.setHeaderColor(scheme === "dark" ? "#0b101e" : "#f5f7fb");
        tg.setBackgroundColor(scheme === "dark" ? "#0b101e" : "#f5f7fb");
      } catch (_) {}
    }
  }

  function triggerHaptic(style = "light") {
    try {
      if (tg && tg.HapticFeedback && typeof tg.HapticFeedback.impactOccurred === "function") {
        tg.HapticFeedback.impactOccurred(style);
      }
    } catch (_) {}
  }

  // =========================================================================
  // Persistence: Telegram CloudStorage + localStorage fallback
  // =========================================================================
  function serializeState() {
    return JSON.stringify({
      selectedDeckId: state.selectedDeckId,
      isShuffled: state.isShuffled,
      shuffleSeed: state.shuffleSeed,
      positions: state.positions,
      isEndState: state.isEndState,
    });
  }

  function saveState() {
    state.positions[state.selectedDeckId] = state.currentIndex;
    const raw = serializeState();
    try {
      localStorage.setItem(STORAGE_KEY, raw);
    } catch (_) {}

    try {
      if (tg && tg.CloudStorage && typeof tg.CloudStorage.setItem === "function") {
        tg.CloudStorage.setItem(STORAGE_KEY, raw, function () {});
      }
    } catch (_) {}
  }

  function parseSaved(raw) {
    if (!raw) return null;
    try {
      const obj = JSON.parse(raw);
      return obj && typeof obj === "object" ? obj : null;
    } catch (_) {
      return null;
    }
  }

  function applySavedState(saved) {
    if (!saved) return;
    if (typeof saved.selectedDeckId === "string") {
      state.selectedDeckId = saved.selectedDeckId;
    }
    if (typeof saved.isShuffled === "boolean") {
      state.isShuffled = saved.isShuffled;
    }
    if (typeof saved.shuffleSeed === "number") {
      state.shuffleSeed = saved.shuffleSeed;
    }
    if (saved.positions && typeof saved.positions === "object") {
      state.positions = Object.assign(Object.create(null), saved.positions);
    }
    if (typeof saved.isEndState === "boolean") {
      state.isEndState = saved.isEndState;
    }
  }

  function loadSavedState(callback) {
    try {
      const local = parseSaved(localStorage.getItem(STORAGE_KEY));
      if (local) applySavedState(local);
    } catch (_) {}

    try {
      if (tg && tg.CloudStorage && typeof tg.CloudStorage.getItem === "function") {
        tg.CloudStorage.getItem(STORAGE_KEY, function (err, val) {
          if (!err && val) {
            const cloud = parseSaved(val);
            if (cloud) {
              applySavedState(cloud);
              try {
                localStorage.setItem(STORAGE_KEY, val);
              } catch (_) {}
            }
          }
          callback();
        });
        return;
      }
    } catch (_) {}

    callback();
  }

  // =========================================================================
  // Deterministic Seeded Shuffle
  // =========================================================================
  function seededShuffle(array, seed) {
    const copy = array.slice();
    let s = seed >>> 0;
    for (let i = copy.length - 1; i > 0; i--) {
      s = (Math.imul(1664525, s) + 1013904223) >>> 0;
      const j = s % (i + 1);
      const tmp = copy[i];
      copy[i] = copy[j];
      copy[j] = tmp;
    }
    return copy;
  }

  // =========================================================================
  // Accent Palette & Auto-Fit Typography
  // =========================================================================
  function applyAccentByIndex(accentIndex) {
    const palette = ACCENT_PALETTES[((accentIndex % ACCENT_PALETTES.length) + ACCENT_PALETTES.length) % ACCENT_PALETTES.length];
    const rootStyle = document.documentElement.style;
    rootStyle.setProperty("--accent-start", palette.start);
    rootStyle.setProperty("--accent-end", palette.end);
    rootStyle.setProperty("--accent-solid", palette.start);
    rootStyle.setProperty("--accent-rgb", palette.rgb);
  }

  function fitCardTypography(word) {
    const enLen = word.english.length;
    let enSize = 42;
    if (enLen >= 22) enSize = 22;
    else if (enLen >= 18) enSize = 25;
    else if (enLen >= 14) enSize = 28;
    else if (enLen >= 11) enSize = 33;
    else if (enLen >= 8) enSize = 38;
    dom.englishWord.style.fontSize = `${enSize}px`;

    const uzLen = word.uzbek.length;
    let uzSize = 31;
    if (uzLen >= 28) uzSize = 20;
    else if (uzLen >= 22) uzSize = 23;
    else if (uzLen >= 16) uzSize = 26;
    else if (uzLen >= 12) uzSize = 29;
    dom.uzbekWord.style.fontSize = `${uzSize}px`;

    const totalExLen = word.example_en.length + word.example_uz.length;
    if (totalExLen > 140) {
      dom.exampleEn.style.fontSize = "13px";
      dom.exampleUz.style.fontSize = "12px";
    } else if (totalExLen > 100) {
      dom.exampleEn.style.fontSize = "14px";
      dom.exampleUz.style.fontSize = "12.8px";
    } else {
      dom.exampleEn.style.fontSize = "15px";
      dom.exampleUz.style.fontSize = "13.5px";
    }

    requestAnimationFrame(() => {
      const frontBody = dom.englishWord.parentElement;
      if (frontBody && dom.englishWord.scrollWidth > frontBody.clientWidth - 8) {
        const ratio = (frontBody.clientWidth - 12) / dom.englishWord.scrollWidth;
        const adjusted = Math.max(18, Math.floor(enSize * ratio));
        dom.englishWord.style.fontSize = `${adjusted}px`;
      }
    });
  }

  // =========================================================================
  // Deck & Manifest Loading (Instant First Deck + Background Lazy Loader)
  // =========================================================================
  async function fetchDeckFile(relPath) {
    if (fileCache[relPath]) {
      return fileCache[relPath];
    }
    const resp = await fetch(`./${relPath}`);
    if (!resp.ok) {
      throw new Error(`Failed to load deck file: ${relPath}`);
    }
    const json = await resp.json();
    const words = Array.isArray(json) ? json : json.words || [];
    fileCache[relPath] = words;
    return words;
  }

  function getActiveDeckDescriptor() {
    if (state.selectedDeckId === ALL_DECK_ID) {
      return {
        id: ALL_DECK_ID,
        title: "Hammasi",
        category: "All Decks",
        group: "all",
        wordCount: state.manifest.totalWords,
        accentIndex: 0,
        files: state.manifest.allFiles,
      };
    }
    return (
      state.decksById[state.selectedDeckId] ||
      state.manifest.decks[0]
    );
  }

  async function activateDeck(deckId, resetPosition = false) {
    state.loadToken += 1;
    const token = state.loadToken;

    if (!state.decksById[deckId] && deckId !== ALL_DECK_ID) {
      deckId = state.manifest.decks[0] ? state.manifest.decks[0].id : ALL_DECK_ID;
    }
    state.selectedDeckId = deckId;

    const desc = getActiveDeckDescriptor();
    state.expectedTotal = desc.wordCount;

    const savedPos = state.positions[deckId];
    if (!resetPosition && typeof savedPos === "number" && savedPos >= 0 && savedPos < desc.wordCount) {
      state.currentIndex = savedPos;
    } else {
      state.currentIndex = 0;
      state.isEndState = false;
    }

    dom.shuffleBtn.classList.toggle("is-active", state.isShuffled);
    dom.shuffleBtn.setAttribute("aria-pressed", state.isShuffled ? "true" : "false");
    applyAccentByIndex(desc.accentIndex || 0);

    const filesToLoad = state.isShuffled
      ? seededShuffle(desc.files, state.shuffleSeed)
      : desc.files.slice();

    if (filesToLoad.length === 0) return;

    // 1. Load ONLY the first needed file(s) so the current card renders immediately!
    state.activeWords = [];
    let initialFileIdx = 0;

    while (initialFileIdx < filesToLoad.length && state.activeWords.length <= state.currentIndex) {
      const wordsChunk = await fetchDeckFile(filesToLoad[initialFileIdx]);
      if (token !== state.loadToken) return;
      const chunkOrdered = state.isShuffled
        ? seededShuffle(wordsChunk, state.shuffleSeed + initialFileIdx)
        : wordsChunk;
      state.activeWords.push(...chunkOrdered);
      initialFileIdx += 1;
    }

    if (desc.limit && state.activeWords.length > desc.limit) {
      state.activeWords.length = desc.limit;
    }

    render();

    // 2. Lazily load any remaining files in the background without blocking the UI
    if (initialFileIdx < filesToLoad.length && (!desc.limit || state.activeWords.length < desc.limit)) {
      loadRemainingFilesLazily(filesToLoad, initialFileIdx, desc.limit, token);
    }
  }

  function loadRemainingFilesLazily(filesList, startIdx, maxLimit, token) {
    let idx = startIdx;

    function loadNextChunk() {
      if (token !== state.loadToken) return;
      if (idx >= filesList.length) return;
      if (maxLimit && state.activeWords.length >= maxLimit) return;

      const filePath = filesList[idx];
      const chunkIdx = idx;
      idx += 1;

      fetchDeckFile(filePath)
        .then((wordsChunk) => {
          if (token !== state.loadToken) return;
          const ordered = state.isShuffled
            ? seededShuffle(wordsChunk, state.shuffleSeed + chunkIdx)
            : wordsChunk;
          state.activeWords.push(...ordered);
          if (maxLimit && state.activeWords.length > maxLimit) {
            state.activeWords.length = maxLimit;
          }
          if (idx < filesList.length && (!maxLimit || state.activeWords.length < maxLimit)) {
            setTimeout(loadNextChunk, 25);
          }
        })
        .catch(() => {});
    }

    setTimeout(loadNextChunk, 40);
  }

  // =========================================================================
  // Rendering the Single Screen
  // =========================================================================
  function render() {
    const desc = getActiveDeckDescriptor();
    const total = state.expectedTotal || state.activeWords.length || 1;
    const currentWord = state.activeWords[state.currentIndex] || state.activeWords[0];
    if (!currentWord) return;

    // Top bar chip & accent
    dom.chipLabel.textContent = desc.title.replace(/\s*—.*$/, "");
    applyAccentByIndex(desc.accentIndex || 0);

    const displayNum = Math.min(total, state.currentIndex + 1);
    dom.progressCounter.textContent = `${displayNum} / ${total}`;
    dom.progressTrack.setAttribute("aria-valuemax", String(total));
    dom.progressTrack.setAttribute("aria-valuenow", String(displayNum));
    const pct = state.isEndState ? 100 : Math.min(100, Math.max(1.5, (displayNum / total) * 100));
    dom.progressFill.style.width = `${pct}%`;

    if (state.isEndState) {
      dom.wordCard.classList.add("hidden");
      dom.endStateCard.classList.remove("hidden");
      dom.endSubtitle.textContent = `Siz "${desc.title}" boʻlimidagi barcha ${total} ta soʻzni muvaffaqiyatli koʻrib chiqdingiz!`;
      dom.prevBtn.disabled = false;
      dom.nextBtn.disabled = false;
      return;
    }

    dom.endStateCard.classList.add("hidden");
    dom.wordCard.classList.remove("hidden");

    const catTag = currentWord.category || desc.title;
    const formattedIndex = `#${String(displayNum).padStart(3, "0")}`;

    // Front Face
    dom.frontCategoryTag.textContent = catTag;
    dom.frontIndexBadge.textContent = formattedIndex;
    dom.englishWord.textContent = currentWord.english;
    dom.pronunciationText.textContent = `[ ${currentWord.pronunciation_uz} ]`;
    dom.posBadge.textContent = POS_LABELS[currentWord.pos] || currentWord.pos;

    // Back Face
    dom.backCategoryTag.textContent = `${catTag} • Tarjima`;
    dom.backIndexBadge.textContent = formattedIndex;
    dom.uzbekWord.textContent = currentWord.uzbek;
    dom.exampleEn.textContent = currentWord.example_en;
    dom.exampleUz.textContent = currentWord.example_uz;
    dom.backPosBadge.textContent = `${currentWord.english} • [ ${currentWord.pronunciation_uz} ]`;

    fitCardTypography(currentWord);
    dom.prevBtn.disabled = state.currentIndex <= 0;
  }

  function resetCardToFrontInstant() {
    state.isFlipped = false;
    dom.wordCard.classList.add("no-transition");
    dom.wordCard.classList.remove("is-flipped");
    void dom.wordCard.offsetWidth;
    dom.wordCard.classList.remove("no-transition");
  }

  // =========================================================================
  // Card Flip, Next, Previous & Shuffle
  // =========================================================================
  function toggleFlip() {
    if (state.isEndState || state.isAnimating) return;
    state.isFlipped = !state.isFlipped;
    dom.wordCard.classList.toggle("is-flipped", state.isFlipped);
    triggerHaptic("light");
  }

  function goNext() {
    if (state.isAnimating) return;
    triggerHaptic("light");

    if (state.isEndState) {
      restartDeck();
      return;
    }

    const total = state.expectedTotal || state.activeWords.length;
    const isLastWord = state.currentIndex >= total - 1;

    state.isAnimating = true;
    dom.cardScene.classList.remove("anim-in-right", "anim-in-left", "anim-out-right");
    dom.cardScene.classList.add("anim-out-left");

    setTimeout(() => {
      resetCardToFrontInstant();
      if (isLastWord) {
        state.isEndState = true;
      } else if (state.currentIndex + 1 < state.activeWords.length) {
        state.currentIndex += 1;
      }
      saveState();
      render();

      dom.cardScene.classList.remove("anim-out-left");
      dom.cardScene.classList.add("anim-in-right");

      setTimeout(() => {
        dom.cardScene.classList.remove("anim-in-right");
        state.isAnimating = false;
      }, 210);
    }, 145);
  }

  function goPrev() {
    if (state.isAnimating) return;
    if (!state.isEndState && state.currentIndex <= 0) return;

    triggerHaptic("light");
    state.isAnimating = true;
    dom.cardScene.classList.remove("anim-in-right", "anim-in-left", "anim-out-left");
    dom.cardScene.classList.add("anim-out-right");

    setTimeout(() => {
      resetCardToFrontInstant();
      if (state.isEndState) {
        state.isEndState = false;
      } else if (state.currentIndex > 0) {
        state.currentIndex -= 1;
      }
      saveState();
      render();

      dom.cardScene.classList.remove("anim-out-right");
      dom.cardScene.classList.add("anim-in-left");

      setTimeout(() => {
        dom.cardScene.classList.remove("anim-in-left");
        state.isAnimating = false;
      }, 210);
    }, 145);
  }

  function restartDeck() {
    triggerHaptic("light");
    resetCardToFrontInstant();
    state.currentIndex = 0;
    state.isEndState = false;
    saveState();
    render();
  }

  function toggleShuffle() {
    triggerHaptic("light");
    state.isShuffled = !state.isShuffled;
    if (state.isShuffled) {
      state.shuffleSeed = Math.floor(Math.random() * 899999) + 100000;
    }
    resetCardToFrontInstant();
    state.positions[state.selectedDeckId] = 0;
    state.isEndState = false;
    saveState();
    activateDeck(state.selectedDeckId, true);
  }

  // =========================================================================
  // 50+ Deck Picker Bottom Sheet (Grouped Sections + Search + Saved Position)
  // =========================================================================
  function getDeckShortCode(deck, index) {
    if (deck.id === ALL_DECK_ID) return "ALL";
    if (deck.badge) return deck.badge;
    if (deck.isMilestone) {
      return deck.id.replace("top-", "");
    }
    return String(index).padStart(2, "0");
  }

  function renderCategoryList() {
    if (!state.manifest) return;
    const query = state.searchQuery.trim().toLowerCase();
    dom.categoryList.innerHTML = "";

    const allOption = {
      id: ALL_DECK_ID,
      title: "Hammasi (Barcha soʻzlar)",
      category: `Barcha ${state.manifest.totalDeckFiles} ta umumiy toʻplam`,
      group: "all",
      wordCount: state.manifest.totalWords,
      accentIndex: 0,
    };

    const bookDecks = state.manifest.decks.filter((d) => d.group === "book");
    const freqDecks = state.manifest.decks.filter((d) => d.group === "freq");
    const topicDecks = state.manifest.decks.filter((d) => d.group === "topic");

    function matchesSearch(d) {
      if (!query) return true;
      return (
        d.title.toLowerCase().includes(query) ||
        (d.category && d.category.toLowerCase().includes(query)) ||
        d.id.toLowerCase().includes(query) ||
        (d.badge && d.badge.toLowerCase().includes(query))
      );
    }

    function createDeckRow(deck, badgeText, isSubItem = false) {
      const palette = ACCENT_PALETTES[(deck.accentIndex || 0) % ACCENT_PALETTES.length];
      const savedIdx = state.positions[deck.id];
      const posNum = typeof savedIdx === "number" ? Math.min(deck.wordCount, savedIdx + 1) : 1;
      const progressLabel = `${posNum} / ${deck.wordCount}`;

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "sheet-item" + (isSubItem ? " sheet-sub-item" : "") + (state.selectedDeckId === deck.id ? " is-selected" : "");
      btn.style.setProperty("--item-accent", palette.start);
      btn.setAttribute("role", "option");
      btn.setAttribute("aria-selected", state.selectedDeckId === deck.id ? "true" : "false");
      btn.dataset.deckId = deck.id;

      btn.innerHTML = `
        <div class="sheet-item-left">
          <div class="sheet-swatch" style="background: linear-gradient(135deg, ${palette.start} 0%, ${palette.end} 100%)">${badgeText}</div>
          <div class="sheet-item-titles">
            <span class="sheet-item-uz">${deck.title}</span>
            <span class="sheet-item-en">${deck.category}</span>
          </div>
        </div>
        <div class="sheet-item-right">
          <span class="sheet-count">${progressLabel}</span>
        </div>
      `;

      btn.addEventListener("click", () => selectDeckFromSheet(deck.id));
      return btn;
    }

    let renderedCount = 0;

    if (matchesSearch(allOption)) {
      dom.categoryList.appendChild(createDeckRow(allOption, "ALL"));
      renderedCount += 1;
    }

    // 1500 Essential English Words books (strictly below Hammasi)
    const matchedBooks = bookDecks.filter(matchesSearch);
    if (matchedBooks.length > 0) {
      const hdr = document.createElement("div");
      hdr.className = "sheet-section-header";
      hdr.textContent = `Kitoblar: 1500 Essential English Words (${matchedBooks.length})`;
      dom.categoryList.appendChild(hdr);

      matchedBooks.forEach((d) => {
        const badge = d.badge || getDeckShortCode(d);
        const isSub = !d.isBookSummary;
        dom.categoryList.appendChild(createDeckRow(d, badge, isSub));
        renderedCount += 1;
      });
    }

    const matchedFreq = freqDecks.filter(matchesSearch);
    if (matchedFreq.length > 0) {
      const hdr = document.createElement("div");
      hdr.className = "sheet-section-header";
      hdr.textContent = `Eng kerakli soʻzlar (${matchedFreq.length})`;
      dom.categoryList.appendChild(hdr);

      matchedFreq.forEach((d, idx) => {
        dom.categoryList.appendChild(createDeckRow(d, getDeckShortCode(d, idx + 1)));
        renderedCount += 1;
      });
    }

    const matchedTopics = topicDecks.filter(matchesSearch);
    if (matchedTopics.length > 0) {
      const hdr = document.createElement("div");
      hdr.className = "sheet-section-header";
      hdr.textContent = `Mavzular (${matchedTopics.length})`;
      dom.categoryList.appendChild(hdr);

      matchedTopics.forEach((d, idx) => {
        dom.categoryList.appendChild(createDeckRow(d, String(idx + 1).padStart(2, "0")));
        renderedCount += 1;
      });
    }

    if (renderedCount === 0) {
      const empty = document.createElement("div");
      empty.className = "sheet-empty";
      empty.textContent = "Hech qanday boʻlim topilmadi.";
      dom.categoryList.appendChild(empty);
    }
  }

  function openCategorySheet() {
    triggerHaptic("light");
    state.searchQuery = "";
    dom.deckSearchInput.value = "";
    dom.clearSearchBtn.classList.add("hidden");
    renderCategoryList();
    dom.sheetBackdrop.classList.remove("hidden");
    dom.categorySheet.classList.remove("hidden");
    requestAnimationFrame(() => {
      dom.sheetBackdrop.classList.add("is-open");
      dom.categorySheet.classList.add("is-open");
    });
  }

  function closeCategorySheet() {
    dom.sheetBackdrop.classList.remove("is-open");
    dom.categorySheet.classList.remove("is-open");
    setTimeout(() => {
      dom.sheetBackdrop.classList.add("hidden");
      dom.categorySheet.classList.add("hidden");
    }, 260);
  }

  async function selectDeckFromSheet(deckId) {
    triggerHaptic("light");
    state.positions[state.selectedDeckId] = state.currentIndex;
    state.isEndState = false;
    resetCardToFrontInstant();
    closeCategorySheet();
    await activateDeck(deckId, false);
    saveState();
  }

  // =========================================================================
  // Swipe & Pointer Gestures
  // =========================================================================
  function bindCardGestures() {
    let startX = 0;
    let startY = 0;
    let tracking = false;
    let swiped = false;

    dom.cardScene.addEventListener(
      "pointerdown",
      (e) => {
        if (state.isEndState && e.target.closest("#restartBtn")) return;
        startX = e.clientX;
        startY = e.clientY;
        tracking = true;
        swiped = false;
      },
      { passive: true }
    );

    dom.cardScene.addEventListener(
      "pointerup",
      (e) => {
        if (!tracking) return;
        tracking = false;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;

        if (Math.abs(dx) >= 48 && Math.abs(dx) > Math.abs(dy) * 1.25) {
          swiped = true;
          if (dx < 0) goNext();
          else goPrev();
        }
      },
      { passive: true }
    );

    dom.wordCard.addEventListener("click", () => {
      if (swiped) {
        swiped = false;
        return;
      }
      toggleFlip();
    });

    dom.wordCard.addEventListener("keydown", (e) => {
      if (e.key === " " || e.key === "Enter") {
        e.preventDefault();
        toggleFlip();
      }
    });
  }

  function bindEvents() {
    bindCardGestures();

    dom.nextBtn.addEventListener("click", goNext);
    dom.prevBtn.addEventListener("click", goPrev);
    dom.restartBtn.addEventListener("click", restartDeck);
    dom.shuffleBtn.addEventListener("click", toggleShuffle);

    dom.categoryChipBtn.addEventListener("click", openCategorySheet);
    dom.openCategoriesBtn.addEventListener("click", openCategorySheet);
    dom.closeSheetBtn.addEventListener("click", closeCategorySheet);
    dom.sheetBackdrop.addEventListener("click", closeCategorySheet);

    dom.deckSearchInput.addEventListener("input", () => {
      state.searchQuery = dom.deckSearchInput.value;
      dom.clearSearchBtn.classList.toggle("hidden", !state.searchQuery);
      renderCategoryList();
    });

    dom.clearSearchBtn.addEventListener("click", () => {
      state.searchQuery = "";
      dom.deckSearchInput.value = "";
      dom.clearSearchBtn.classList.add("hidden");
      renderCategoryList();
      dom.deckSearchInput.focus();
    });

    window.addEventListener("keydown", (e) => {
      if (!dom.categorySheet.classList.contains("hidden")) {
        if (e.key === "Escape") closeCategorySheet();
        return;
      }
      if (e.key === "ArrowRight") goNext();
      else if (e.key === "ArrowLeft") goPrev();
    });

    window.addEventListener("resize", () => {
      const currentWord = state.activeWords[state.currentIndex];
      if (currentWord && !state.isEndState) {
        fitCardTypography(currentWord);
      }
    });
  }

  async function bootstrap() {
    initTelegram();
    bindEvents();

    const resp = await fetch("./data/index.json?t=" + Date.now());
    if (!resp.ok) {
      throw new Error("Could not load data/index.json manifest.");
    }
    const manifest = await resp.json();
    state.manifest = manifest;
    for (const d of manifest.decks) {
      state.decksById[d.id] = d;
    }

    loadSavedState(async () => {
      const params = new URLSearchParams(window.location.search);
      const urlDeck = params.get("deck");
      const urlIndex = params.get("index");
      const urlFlipped = params.get("flip");
      const urlPicker = params.get("picker");

      if (urlDeck && (state.decksById[urlDeck] || urlDeck === ALL_DECK_ID)) {
        state.selectedDeckId = urlDeck;
      }
      if (urlIndex !== null && !isNaN(parseInt(urlIndex, 10))) {
        state.positions[state.selectedDeckId] = parseInt(urlIndex, 10);
      }

      await activateDeck(state.selectedDeckId, false);

      if (urlFlipped === "1" || urlFlipped === "true") {
        setTimeout(toggleFlip, 100);
      }
      if (urlPicker === "1" || urlPicker === "true") {
        setTimeout(openCategorySheet, 150);
      }
    });
  }

  bootstrap();
})();
