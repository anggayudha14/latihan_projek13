/*
======================================================
AES-128 Encryption Simulator
Frontend JavaScript
======================================================
*/

"use strict";

// ======================================================
// ELEMENT
// ======================================================

const plaintext = document.getElementById("plaintext");

const ciphertext = document.getElementById("ciphertext");

const key = document.getElementById("key");

const encryptBtn = document.getElementById("encryptBtn");

const decryptBtn = document.getElementById("decryptBtn");

const resultCard = document.getElementById("resultCard");

const loading = document.getElementById("loading");

const alertBox = document.getElementById("alertBox");

const resultPlaintext =
    document.getElementById("resultPlaintext");

const resultCiphertext =
    document.getElementById("resultCiphertext");

const copyCipher =
    document.getElementById("copyCipher");

const copyPlain =
    document.getElementById("copyPlain");

const roundKeysContainer =
    document.getElementById("roundKeysContainer");

const keyExpansionContainer =
    document.getElementById("keyExpansionContainer");

const historyContainer =
    document.getElementById("historyContainer");

const matrixContainer =
    document.getElementById("matrixContainer");

    // ======================================================
// HELPER
// ======================================================

function showLoading() {

    loading.classList.remove("d-none");

    resultCard.classList.add("d-none");

}

function hideLoading() {

    loading.classList.add("d-none");

}

function showAlert(message) {

    alertBox.innerHTML = message;

    alertBox.classList.remove("d-none");

}

function hideAlert(){

    alertBox.classList.add("d-none");

    alertBox.innerHTML = "";

}

function showResult() {

    resultCard.classList.remove("d-none");

}

// ======================================================
// RESET PANEL
// ======================================================

function clearPanels(){

    roundKeysContainer.innerHTML="";

    keyExpansionContainer.innerHTML="";

    historyContainer.innerHTML="";

    matrixContainer.innerHTML="";

}

// ======================================================
// COPY
// ======================================================

copyCipher.addEventListener(

    "click",

    function(){

        navigator.clipboard.writeText(

            resultCiphertext.value

        );

        alert("Ciphertext berhasil disalin.");

    }

);

copyPlain.addEventListener(

    "click",

    function(){

        navigator.clipboard.writeText(

            resultPlaintext.value

        );

        alert("Plaintext berhasil disalin.");

    }

);

// ======================================================
// ENCRYPT
// ======================================================

async function encryptAES() {

    hideAlert();

    clearPanels();

    showLoading();

    try {

        const response = await fetch("/encrypt", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                plaintext: plaintext.value,

                key: key.value

            })

        });

       const result = await response.json();

       console.log(result);

hideAlert();

hideLoading();

if (!result.success) {

    showAlert(result.message);

    return;

}

const data = result.data;

console.log("AES RESULT");

console.log(data);

        // Tampilkan hasil
        resultPlaintext.value =
            plaintext.value;

        resultCiphertext.value =
            data.ciphertext ||
            data.ciphertext_hex ||
            "";

        showResult();

        // Simpan untuk Part 3
        window.aesResult = data;

        renderRoundKeys(data.round_keys || []);

        renderKeyExpansion(
            data.key_steps || []
        );

        renderHistory(
            data.history || []
        );

        renderMatrix(
            data.matrix ||
            data.final_state ||
            data.states ||
            []
        );

    }

    catch (err) {

    hideLoading();

    console.error(err);

    showAlert(
        "ERROR: " + err.message
    );

} 
}

// ======================================================
// DECRYPT
// ======================================================

async function decryptAES() {

    hideAlert();

    clearPanels();

    showLoading();

    try {

        const response = await fetch("/decrypt", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                ciphertext: ciphertext.value,

                key: key.value

            })

        });

        const result = await response.json();
        console.log(result);


        hideLoading();

        if (!result.success) {

            showAlert(

                result.message

            );

            return;

        }

        const data = result.data;



        resultCiphertext.value =
            ciphertext.value;

        resultPlaintext.value =
            data.plaintext || "";

        showResult();

        window.aesResult = data;

        console.log("AES RESULT");

        console.log(data);

renderRoundKeys(data.round_keys || []);

renderKeyExpansion(
    data.key_steps || []
);

renderHistory(
    data.history || []
);

renderMatrix(
    data.matrix ||
    data.final_state ||
    data.states ||
    []
);

    }

    catch (err) {

    hideLoading();

    console.error(err);

    showAlert(
        "Error: " + err.message
    );

}

}



// ======================================================
// RENDER ROUND KEYS
// ======================================================

function renderRoundKeys(roundKeys = []) {

    roundKeysContainer.innerHTML = "";

    if (!roundKeys.length) {

        roundKeysContainer.innerHTML =
            "<p class='text-muted'>Tidak ada Round Key.</p>";

        return;

    }

    roundKeys.forEach((key, index) => {

        const card = document.createElement("div");

        card.className = "round-key-card";

        card.innerHTML = `
            <h6>Round ${index}</h6>
            <pre>${JSON.stringify(key, null, 2)}</pre>
        `;

        roundKeysContainer.appendChild(card);

    });

}

// ======================================================
// RENDER KEY EXPANSION
// ======================================================

function renderKeyExpansion(steps = []) {

    keyExpansionContainer.innerHTML = "";

    if (!steps.length) {

        keyExpansionContainer.innerHTML =
            "<p class='text-muted'>Tidak ada proses Key Expansion.</p>";

        return;

    }

    steps.forEach((step) => {

        const item = document.createElement("div");

        item.className = "history-item";

        item.innerHTML = `
            <strong>${step.operation || "-"}</strong><br>
            Round : ${step.round ?? "-"}<br>
            Index : ${step.index ?? "-"}
        `;

        keyExpansionContainer.appendChild(item);

    });

}

// ======================================================
// RENDER HISTORY
// ======================================================

function renderHistory(history = []) {

    historyContainer.innerHTML = "";

    if (!history.length) {

        historyContainer.innerHTML =
            "<p class='text-muted'>Belum ada history.</p>";

        return;

    }

    history.forEach((item, index) => {

        const div = document.createElement("div");

        div.className = "history-item";

        div.innerHTML = `
            <strong>Step ${index + 1}</strong><br>
            ${item.operation || ""}
        `;

        historyContainer.appendChild(div);

    });

}

// ======================================================
// RENDER MATRIX
// ======================================================

function renderMatrix(matrix = []) {

    matrixContainer.innerHTML = "";

    if (!matrix.length) {

        matrixContainer.innerHTML =
            "<p>Tidak ada Matrix.</p>";

        return;

    }

    matrix.forEach((state, index) => {

        const title = document.createElement("h6");

        title.innerHTML = `Round ${index}`;

        matrixContainer.appendChild(title);

        const table = document.createElement("table");

        table.className = "matrix-table";

        state.forEach((row) => {

            const tr = document.createElement("tr");

            row.forEach((cell) => {

                const td = document.createElement("td");

                td.innerHTML = cell;

                tr.appendChild(td);

            });

            table.appendChild(tr);

        });

        matrixContainer.appendChild(table);

        matrixContainer.appendChild(document.createElement("br"));

    });

}

// ======================================================
// RESET FORM
// ======================================================

function resetForm() {

    plaintext.value = "";

    ciphertext.value = "";

    key.value = "";

    resultPlaintext.value = "";

    resultCiphertext.value = "";

    hideAlert();

    hideLoading();

    resultCard.classList.add("d-none");

    clearPanels();

}

// ======================================================
// VALIDATION
// ======================================================

function validateEncrypt() {

    if (plaintext.value.trim() === "") {

        showAlert("Plaintext tidak boleh kosong.");

        return false;

    }

    if (key.value.trim().length !== 32) {

        showAlert("Key AES-128 harus terdiri dari 32 digit hexadecimal.");

        return false;

    }

    return true;

}

function validateDecrypt() {

    if (ciphertext.value.trim() === "") {

        showAlert("Ciphertext tidak boleh kosong.");

        return false;

    }

    if (ciphertext.value.trim().length !== 32) {

        showAlert("Ciphertext harus terdiri dari 32 digit hexadecimal.");

        return false;

    }

    if (key.value.trim().length !== 32) {

        showAlert("Key AES-128 harus terdiri dari 32 digit hexadecimal.");

        return false;

    }

    return true;

}

// ======================================================
// BUTTON EVENT
// ======================================================

encryptBtn.addEventListener("click", () => {

    hideAlert();

    if (validateEncrypt()) {

        encryptAES();

    }

});

decryptBtn.addEventListener("click", () => {

    hideAlert();

    if (validateDecrypt()) {

        decryptAES();

    }

});

// ======================================================
// RESET BUTTON
// ======================================================

const resetBtn = document.querySelector("button[type='reset']");

if (resetBtn) {

    resetBtn.addEventListener("click", function (e) {

        e.preventDefault();

        resetForm();

    });

}

// ======================================================
// AUTO UPPERCASE KEY
// ======================================================

key.addEventListener("input", function () {

    this.value = this.value.toUpperCase();

});

// ======================================================
// AUTO UPPERCASE CIPHERTEXT
// ======================================================

ciphertext.addEventListener("input", function () {

    this.value = this.value.toUpperCase();

});

// ======================================================
// INITIALIZE
// ======================================================

hideAlert();

hideLoading();

resultCard.classList.add("d-none");

clearPanels();

console.log("AES-128 Encryption Simulator Loaded.");

