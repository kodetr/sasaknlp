// SasakNLP Client-side Morphological Engine (Pure JS)

function normalizeText(text) {
    if (!text) return "";
    return text.normalize("NFC").toLowerCase().trim();
}

function tokenizeText(text) {
    if (!text) return [];
    // Split by whitespace and punctuation except hyphen for reduplication
    const rawTokens = text.match(/[a-zA-Z0-9\u00C0-\u024F]+(-[a-zA-Z0-9\u00C0-\u024F]+)*|[.,!?;:()]/g) || [];
    return rawTokens.filter(t => t && !/^[.,!?;:()]+$/.test(t));
}

function detectDialect(tokens) {
    if (!tokens || tokens.length === 0) return { dialect: "general", name: "General Sasak", confidence: 0.5, region: "Seluruh Lombok", matchedMarkers: [] };
    
    const tokenSet = new Set(tokens.map(t => t.toLowerCase()));
    const dialects = SASAK_DIALECTS.dialects || {};
    let bestDialect = "general";
    let bestCount = 0;
    let matchedMarkers = [];
    
    for (const [code, info] of Object.entries(dialects)) {
        if (code === "general") continue;
        const markers = (info.markers || []).map(m => m.toLowerCase());
        const found = markers.filter(m => tokenSet.has(m));
        if (found.length > bestCount) {
            bestCount = found.length;
            bestDialect = code;
            matchedMarkers = found;
        }
    }
    
    const dInfo = dialects[bestDialect] || { name: "General Sasak", region: "Seluruh Pulau Lombok" };
    const conf = bestCount === 0 ? 0.50 : Math.min(0.95, 0.50 + bestCount * 0.15);
    return { 
        dialect: bestDialect, 
        name: dInfo.name || bestDialect, 
        confidence: conf, 
        region: dInfo.region || "Lombok",
        matchedMarkers: matchedMarkers
    };
}

function analyzeWord(surface) {
    const word = surface.toLowerCase().trim();
    
    // 1. Direct Lexicon Lookup
    if (SASAK_ROOTS.has(word)) {
        return {
            surface_form: surface,
            lemma: word,
            prefix: null,
            infix: null,
            suffix: null,
            reduplication: null,
            rule_applied: "direct_lexicon_lookup",
            confidence: 1.0,
            is_oov: false
        };
    }
    
    // 2. Reduplication
    if (word.includes("-")) {
        const parts = word.split("-");
        if (parts.length === 2 && parts[0] === parts[1]) {
            const root = parts[0];
            return {
                surface_form: surface,
                lemma: root,
                prefix: null,
                infix: null,
                suffix: null,
                reduplication: "full_hyphen",
                rule_applied: "full_reduplication_hyphen",
                confidence: SASAK_ROOTS.has(root) ? 0.98 : 0.85,
                is_oov: !SASAK_ROOTS.has(root)
            };
        }
    }
    
    // 3. Circumfix: ka-...-an, pe-...-an
    if (word.startsWith("ka") && word.endsWith("an") && word.length > 5) {
        const candidate = word.slice(2, -2);
        if (SASAK_ROOTS.has(candidate)) {
            return {
                surface_form: surface,
                lemma: candidate,
                prefix: "ka-",
                infix: null,
                suffix: "-an",
                reduplication: null,
                rule_applied: "circumfix_ka_an",
                confidence: 0.96,
                is_oov: false
            };
        }
    }
    if (word.startsWith("pe") && word.endsWith("an") && word.length > 5) {
        const candidate = word.slice(2, -2);
        if (SASAK_ROOTS.has(candidate)) {
            return {
                surface_form: surface,
                lemma: candidate,
                prefix: "pe-",
                infix: null,
                suffix: "-an",
                reduplication: null,
                rule_applied: "circumfix_pe_an",
                confidence: 0.96,
                is_oov: false
            };
        }
    }
    
    // 4. Infix: -in-, -er-, -el-
    if (word.length >= 5) {
        const infixes = [
            { inf: "in", rule: "passive_in" },
            { inf: "er", rule: "frequentative_er" },
            { inf: "el", rule: "frequentative_el" }
        ];
        for (const { inf, rule } of infixes) {
            if (word.slice(1, 1 + inf.length) === inf) {
                const candidate = word[0] + word.slice(1 + inf.length);
                if (SASAK_ROOTS.has(candidate)) {
                    return {
                        surface_form: surface,
                        lemma: candidate,
                        prefix: null,
                        infix: "-" + inf + "-",
                        suffix: null,
                        reduplication: null,
                        rule_applied: rule,
                        confidence: 0.95,
                        is_oov: false
                    };
                }
            }
        }
    }
    
    // 5. Prefix: te-, pe-, me-, be-, ke-, ny-, ng-
    const prefixes = [
        { p: "te", rule: "passive_te" },
        { p: "pe", rule: "causative_pe" },
        { p: "be", rule: "stative_be" },
        { p: "ke", rule: "passive_ke" },
        { p: "me", rule: "active_me" },
        { p: "se", rule: "numeral_se" }
    ];
    for (const { p, rule } of prefixes) {
        if (word.startsWith(p) && word.length > p.length + 2) {
            const candidate = word.slice(p.length);
            if (SASAK_ROOTS.has(candidate)) {
                return {
                    surface_form: surface,
                    lemma: candidate,
                    prefix: p + "-",
                    infix: null,
                    suffix: null,
                    reduplication: null,
                    rule_applied: rule,
                    confidence: 0.96,
                    is_oov: false
                };
            }
        }
    }
    
    // 6. Suffix: -ang, -an, -in, possessives (-ne, -ku, -de)
    const suffixes = [
        { s: "ang", rule: "transitive_ang" },
        { s: "an", rule: "locative_an" },
        { s: "in", rule: "iterative_in" },
        { s: "ne", rule: "possessive_ne" },
        { s: "ku", rule: "possessive_ku" },
        { s: "de", rule: "possessive_de" }
    ];
    for (const { s, rule } of suffixes) {
        if (word.endsWith(s) && word.length > s.length + 2) {
            const candidate = word.slice(0, -s.length);
            if (SASAK_ROOTS.has(candidate)) {
                return {
                    surface_form: surface,
                    lemma: candidate,
                    prefix: null,
                    infix: null,
                    suffix: "-" + s,
                    reduplication: null,
                    rule_applied: rule,
                    confidence: 0.96,
                    is_oov: false
                };
            }
        }
    }
    
    // 7. Combination Prefix + Suffix fallback
    for (const { p, rule: pRule } of prefixes) {
        if (word.startsWith(p)) {
            for (const { s, rule: sRule } of suffixes) {
                if (word.endsWith(s) && word.length > p.length + s.length + 2) {
                    const candidate = word.slice(p.length, -s.length);
                    if (SASAK_ROOTS.has(candidate)) {
                        return {
                            surface_form: surface,
                            lemma: candidate,
                            prefix: p + "-",
                            infix: null,
                            suffix: "-" + s,
                            reduplication: null,
                            rule_applied: `${pRule}_and_${sRule}`,
                            confidence: 0.93,
                            is_oov: false
                        };
                    }
                }
            }
        }
    }
    
    // OOV fallback
    return {
        surface_form: surface,
        lemma: word,
        prefix: null,
        infix: null,
        suffix: null,
        reduplication: null,
        rule_applied: "oov_verbatim_fallback",
        confidence: 0.40,
        is_oov: true
    };
}

function processText(text) {
    const t0 = performance.now();
    const norm = normalizeText(text);
    const tokens = tokenizeText(norm);
    const dialectResult = detectDialect(tokens);
    const analyses = tokens.map(analyzeWord);
    const lemmas = analyses.map(a => a.lemma);
    const t1 = performance.now();
    
    return {
        original: text,
        normalized: norm,
        tokens: tokens,
        lemmas: lemmas,
        analyses: analyses,
        dialect: dialectResult.dialect,
        dialectName: dialectResult.name,
        dialectRegion: dialectResult.region,
        dialectConfidence: dialectResult.confidence,
        matchedMarkers: dialectResult.matchedMarkers,
        latency_ms: Math.max(0.01, t1 - t0)
    };
}
