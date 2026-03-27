/**
 * NER Tagger - Frontend Logic
 * Handles user input, API communication, and result rendering.
 */

const CATEGORIES = [
    { key: "Person",       cls: "cat-person", label: "Person"       },
    { key: "Organisation", cls: "cat-org",    label: "Organisation" },
    { key: "Location",     cls: "cat-loc",    label: "Location"     },
    { key: "Date",         cls: "cat-date",   label: "Date"         },
    { key: "Other",        cls: "cat-other",  label: "Other"        },
];

const elements = {
    input: document.getElementById("inputText"),
    analyseBtn: document.getElementById("analyseBtn"),
    clearBtn: document.getElementById("clearBtn"),
    status: document.getElementById("status"),
    resultsPanel: document.getElementById("resultsPanel")
};

/**
 * Updates the status message below the input.
 */
function setStatus(msg, type = "info") {
    if (type === "loading") {
        elements.status.innerHTML = `<span class="spinner"></span> ${msg}`;
    } else if (type === "error") {
        elements.status.innerHTML = `<span class="err-msg">⚠ ${msg}</span>`;
    } else {
        elements.status.textContent = msg;
    }
}

/**
 * Resets the UI to initial state.
 */
function clearAll() {
    elements.input.value = "";
    elements.status.innerHTML = "";
    showPlaceholder();
}

/**
 * Renders the initial placeholder in the results panel.
 */
function showPlaceholder() {
    elements.resultsPanel.innerHTML = `
      <div class="placeholder" id="placeholder">
        <div class="placeholder-icon">⬡</div>
        <p>Entities will appear here after analysis</p>
        <div class="legend" style="margin-top:16px;">
          <span class="legend-item"><span class="legend-dot" style="background:var(--person)"></span>Person</span>
          <span class="legend-item"><span class="legend-dot" style="background:var(--org)"></span>Organisation</span>
          <span class="legend-item"><span class="legend-dot" style="background:var(--loc)"></span>Location</span>
          <span class="legend-item"><span class="legend-dot" style="background:var(--date)"></span>Date</span>
        </div>
      </div>`;
}

/**
 * Escapes HTML characters to prevent XSS.
 */
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/**
 * Renders extraction results into categorized cards.
 */
function renderResults(entities) {
    const total = Object.values(entities).flat().length;
    
    let html = `
      <div class="results-header">
        <span class="panel-label">Extracted Entities</span>
        <span class="total-count">${total} found</span>
      </div>`;

    CATEGORIES.forEach((cat, i) => {
        const items = entities[cat.key] || [];
        
        // Skip 'Other' if empty to keep UI clean
        if (cat.key === "Other" && items.length === 0) return;

        const chips = items.length
            ? items.map((e, j) =>
                `<span class="chip" style="animation-delay:${j * 0.03}s">${escapeHtml(e)}</span>`
              ).join("")
            : `<span class="empty-note">No identified ${cat.label.toLowerCase()}s</span>`;

        html += `
            <div class="cat-card ${cat.cls}" style="animation-delay:${i * 0.05}s">
              <div class="cat-head">
                <div class="cat-label"><span class="dot"></span>${cat.label}</div>
                <span class="cat-count">${items.length}</span>
              </div>
              <div class="cat-body">${chips}</div>
            </div>`;
    });

    elements.resultsPanel.innerHTML = html;
}

/**
 * Orchestrates the analysis request.
 */
async function analyse() {
    const text = elements.input.value.trim();
    
    if (!text) {
        setStatus("Please enter some text first.", "error");
        return;
    }

    elements.analyseBtn.disabled = true;
    setStatus("Analysing with spaCy...", "loading");

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `Server error ${response.status}`);
        }

        renderResults(data.entities);
        const count = Object.values(data.entities).flat().length;
        setStatus(`Analysis complete: ${count} entities extracted.`);

    } catch (err) {
        console.error(err);
        setStatus(`Error: ${err.message}`, "error");
        // Don't clear results if there was an error, keep what was there
    } finally {
        elements.analyseBtn.disabled = false;
    }
}

// Event Listeners
elements.analyseBtn.addEventListener("click", analyse);
elements.clearBtn.addEventListener("click", clearAll);

// Keyboard shortcuts (Ctrl+Enter / Cmd+Enter)
document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        analyse();
    }
});
