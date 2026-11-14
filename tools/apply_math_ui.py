from pathlib import Path

app_js_path = Path(r"C:\Users\user\.gemini\antigravity\scratch\words-app\webapp\js\app.js")
index_html_path = Path(r"C:\Users\user\.gemini\antigravity\scratch\words-app\webapp\index.html")

# 1. Update index.html cache busters
html = index_html_path.read_text(encoding="utf-8")
html = html.replace("20261113_audio_v3", "20261114_math_v1")
index_html_path.write_text(html, encoding="utf-8")
print("Updated index.html cache buster to 20261114_math_v1")

# 2. Update app.js
code = app_js_path.read_text(encoding="utf-8")

# Add isMathWord helper before render()
is_math_helper = """  function isMathWord(word) {
    if (!word) return false;
    const desc = getActiveDeckDescriptor();
    if (desc && desc.group === "math") return true;
    return !!(
      word.category &&
      (word.category.includes("karra") ||
        word.category.includes("Boʻlish") ||
        word.category.includes("Qoʻshish") ||
        word.category.includes("Ayirish"))
    );
  }

"""

if "function isMathWord(" not in code:
    code = code.replace("  function render() {", is_math_helper + "  function render() {")
    print("Added isMathWord helper to app.js")

# Update render() body
old_render_block = """    // Front Face
    dom.frontCategoryTag.textContent = catTag;
    dom.frontIndexBadge.textContent = formattedIndex;
    dom.englishWord.textContent = currentWord.english;
    if (dom.ipaText) {
      dom.ipaText.textContent = currentWord.ipa || `/${currentWord.english}/`;
    }
    dom.pronunciationText.textContent = `[ ${currentWord.pronunciation_uz} ]`;
    dom.posBadge.textContent = POS_LABELS[currentWord.pos] || currentWord.pos;

    // Back Face
    dom.backCategoryTag.textContent = `${catTag} • Tarjima`;
    dom.backIndexBadge.textContent = formattedIndex;
    dom.uzbekWord.textContent = currentWord.uzbek;
    dom.exampleEn.textContent = currentWord.example_en;
    dom.exampleUz.textContent = currentWord.example_uz;
    const ipaOrUz = currentWord.ipa || `[ ${currentWord.pronunciation_uz} ]`;
    dom.backPosBadge.textContent = `${currentWord.english} • ${ipaOrUz}`;"""

new_render_block = """    const isMath = isMathWord(currentWord);

    // Audio controls & IPA visibility based on whether it is Math (per user request: no audio for math)
    if (dom.speakBtn) dom.speakBtn.classList.toggle("hidden", isMath);
    if (dom.exampleSpeakBtn) dom.exampleSpeakBtn.classList.toggle("hidden", isMath);
    if (dom.ipaPill) dom.ipaPill.classList.toggle("hidden", isMath);

    // Front Face
    dom.frontCategoryTag.textContent = catTag;
    dom.frontIndexBadge.textContent = formattedIndex;
    dom.englishWord.textContent = currentWord.english;
    if (dom.ipaText) {
      dom.ipaText.textContent = currentWord.ipa || `/${currentWord.english}/`;
    }
    dom.pronunciationText.textContent = `[ ${currentWord.pronunciation_uz} ]`;
    dom.posBadge.textContent = POS_LABELS[currentWord.pos] || currentWord.pos;

    // Back Face
    dom.backCategoryTag.textContent = isMath ? `${catTag} • Javob` : `${catTag} • Tarjima`;
    dom.backIndexBadge.textContent = formattedIndex;
    dom.uzbekWord.textContent = currentWord.uzbek;
    dom.exampleEn.textContent = currentWord.example_en;
    dom.exampleUz.textContent = currentWord.example_uz;
    const ipaOrUz = currentWord.ipa ? ` • ${currentWord.ipa}` : (isMath ? "" : ` • [ ${currentWord.pronunciation_uz} ]`);
    dom.backPosBadge.textContent = `${currentWord.english.replace(/\\s*=\\s*\\?$/, "")} = ${currentWord.uzbek}${ipaOrUz}`;"""

if old_render_block in code:
    code = code.replace(old_render_block, new_render_block)
    print("Updated render() in app.js for math card presentation")
else:
    print("WARNING: old_render_block not found in app.js!")

# Update fitCardTypography
old_fit_block = """    const uzLen = word.uzbek.length;
    let uzSize = 31;"""

new_fit_block = """    const isMath = isMathWord(word);
    const uzLen = word.uzbek.length;
    let uzSize = isMath && uzLen <= 6 ? 44 : 31;"""

if old_fit_block in code:
    code = code.replace(old_fit_block, new_fit_block)
    print("Updated fitCardTypography in app.js")

# Update renderCategoryList
old_cat_search_end = """    const matchedTopics = topicDecks.filter(matchesSearch);
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

    if (renderedCount === 0) {"""

new_cat_search_end = """    const matchedTopics = topicDecks.filter(matchesSearch);
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

    // Matematika & Karra jadvali (strictly at the very bottom)
    const mathDecks = state.manifest.decks.filter((d) => d.group === "math");
    const matchedMath = mathDecks.filter(matchesSearch);
    if (matchedMath.length > 0) {
      const hdr = document.createElement("div");
      hdr.className = "sheet-section-header";
      hdr.textContent = `Matematika & Karra jadvali (${matchedMath.length})`;
      dom.categoryList.appendChild(hdr);

      matchedMath.forEach((d) => {
        const badge = d.badge || getDeckShortCode(d);
        const isSub = !d.isMathSummary;
        dom.categoryList.appendChild(createDeckRow(d, badge, isSub));
        renderedCount += 1;
      });
    }

    if (renderedCount === 0) {"""

if old_cat_search_end in code:
    code = code.replace(old_cat_search_end, new_cat_search_end)
    print("Updated renderCategoryList in app.js with bottom Math section")
else:
    print("WARNING: old_cat_search_end not found in app.js!")

# Update audio click handlers in bindEvents
old_bind_speak = """    if (dom.speakBtn) {
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
    }"""

new_bind_speak = """    if (dom.speakBtn) {
      dom.speakBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const word = state.activeWords[state.currentIndex];
        if (word && !isMathWord(word)) playNativeAudio(word.english, dom.speakBtn);
      });
    }

    if (dom.ipaPill) {
      dom.ipaPill.addEventListener("click", (e) => {
        e.stopPropagation();
        const word = state.activeWords[state.currentIndex];
        if (word && !isMathWord(word)) playNativeAudio(word.english, dom.speakBtn);
      });
    }

    if (dom.pronunciationPill) {
      dom.pronunciationPill.addEventListener("click", (e) => {
        e.stopPropagation();
        const word = state.activeWords[state.currentIndex];
        if (word && !isMathWord(word)) playNativeAudio(word.english, dom.speakBtn);
      });
    }

    if (dom.exampleSpeakBtn) {
      dom.exampleSpeakBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const word = state.activeWords[state.currentIndex];
        if (word && !isMathWord(word)) playNativeAudio(word.example_en, dom.exampleSpeakBtn);
      });
    }"""

if old_bind_speak in code:
    code = code.replace(old_bind_speak, new_bind_speak)
    print("Updated bindEvents in app.js to suppress audio for math")
else:
    print("WARNING: old_bind_speak not found in app.js!")

app_js_path.write_text(code, encoding="utf-8")
print("SUCCESS: app.js fully updated for Math decks!")
