document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements Mapping
    const apiKeyInput = document.getElementById("api-key");
    const pdfFileInput = document.getElementById("pdf-file");
    const dropZone = document.getElementById("drop-zone");
    const fileChip = document.getElementById("file-chip");
    const removeFileBtn = document.getElementById("remove-file");
    const jsonDataArea = document.getElementById("json-data");
    const jsonStatus = document.getElementById("json-status");
    const generateBtn = document.getElementById("generate-btn");
    const downloadBtn = document.getElementById("download-btn");
    
    // Cards elements for active styling toggles
    const cardApi = document.getElementById("card-api");
    const cardUpload = document.getElementById("card-upload");
    const cardJson = document.getElementById("card-json");
    
    // Status Tracker pipeline layout steps
    const stepAuth = document.getElementById("step-auth");
    const stepGuide = document.getElementById("step-guide");
    const stepPayload = document.getElementById("step-payload");
    const stepReady = document.getElementById("step-ready");
    
    const line1 = document.getElementById("line-1");
    const line2 = document.getElementById("line-2");
    const line3 = document.getElementById("line-3");

    // Display Terminal Screens
    const welcomeScreen = document.getElementById("welcome-message");
    const processingScreen = document.getElementById("processing-message");
    const renderScreen = document.getElementById("render-view");
    const progressText = document.getElementById("progress-text");
    const progressFill = document.getElementById("progress-fill");
    const htmlPreview = document.getElementById("html-preview");

    // UI Tracker Object States
    let state = {
        apiValid: false,
        fileLoaded: false,
        jsonValid: false
    };

    // --- Verification Pipeline Trackers ---
    function updatePipelineTracker() {
        // Step 1 Check
        if (apiKeyInput.value.trim().length > 8) {
            state.apiValid = true;
            cardApi.classList.add("filled");
            stepAuth.className = "step completed";
            line1.className = "pipeline-line active";
            stepGuide.className = "step active";
        } else {
            state.apiValid = false;
            cardApi.classList.remove("filled");
            stepAuth.className = "step active";
            line1.className = "pipeline-line";
            stepGuide.className = "step";
        }

        // Step 2 Check
        if (pdfFileInput.files.length > 0) {
            state.fileLoaded = true;
            cardUpload.classList.add("filled");
            stepGuide.className = "step completed";
            line2.className = "pipeline-line active";
            stepPayload.className = "step active";
        } else {
            state.fileLoaded = false;
            cardUpload.classList.remove("filled");
            if(state.apiValid) {
                stepGuide.className = "step active";
            }
            line2.className = "pipeline-line";
            stepPayload.className = "step";
        }

        // Step 3 Check
        validateJSONInput();

        // System Core Authorization Validation 
        if (state.apiValid && state.fileLoaded && state.jsonValid) {
            generateBtn.disabled = false;
            stepReady.className = "step active";
            line3.className = "pipeline-line active";
        } else {
            generateBtn.disabled = true;
            stepReady.className = "step";
            line3.className = "pipeline-line";
        }
    }

    function validateJSONInput() {
        const value = jsonDataArea.value.trim();
        if (value === "") {
            state.jsonValid = false;
            cardJson.classList.remove("filled");
            jsonStatus.innerText = "Waiting for data";
            jsonStatus.className = "json-badge invalid";
            return;
        }

        try {
            JSON.parse(value);
            state.jsonValid = true;
            cardJson.classList.add("filled");
            jsonStatus.innerText = "Payload Valid";
            jsonStatus.className = "json-badge valid";
            
            if(state.apiValid && state.fileLoaded) {
                stepPayload.className = "step completed";
            }
        } catch (e) {
            state.jsonValid = false;
            cardJson.classList.remove("filled");
            jsonStatus.innerText = "Syntax Error";
            jsonStatus.className = "json-badge invalid";
            stepPayload.className = "step active";
        }
    }

    // --- Interaction Input Triggers ---
    apiKeyInput.addEventListener("input", updatePipelineTracker);
    jsonDataArea.addEventListener("input", updatePipelineTracker);

    // Click trigger on dropzone box wrapper
    dropZone.addEventListener("click", (e) => {
        if (e.target !== removeFileBtn) {
            pdfFileInput.click();
        }
    });

    pdfFileInput.addEventListener("change", () => {
        if (pdfFileInput.files.length > 0) {
            const fileName = pdfFileInput.files[0].name;
            document.querySelector(".drop-zone-text").style.display = "none";
            document.querySelector(".drop-zone-icon").style.display = "none";
            fileChip.style.display = "flex";
            fileChip.querySelector(".file-name").innerText = fileName;
            updatePipelineTracker();
        }
    });

    removeFileBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        pdfFileInput.value = "";
        document.querySelector(".drop-zone-text").style.display = "block";
        document.querySelector(".drop-zone-icon").style.display = "block";
        fileChip.style.display = "none";
        updatePipelineTracker();
    });

    // Drag over styling utilities
    ["dragenter", "dragover"].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add("dragover");
        }, false);
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove("dragover");
        }, false);
    });

    dropZone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if(files.length > 0 && files[0].type === "application/pdf") {
            pdfFileInput.files = files;
            const changeEvent = new Event("change");
            pdfFileInput.dispatchEvent(changeEvent);
        }
    });

    // --- Redirection Simulated Processing Environment ---
    generateBtn.addEventListener("click", () => {
        // Initialization display resets
        welcomeScreen.classList.add("hidden");
        renderScreen.classList.add("hidden");
        processingScreen.classList.remove("hidden");
        downloadBtn.classList.add("download-disabled");
        downloadBtn.disabled = true;

        // Stage 1 Loading Frame Emulation
        progressText.innerText = "Extracting Reference Data Matrix...";
        progressFill.style.width = "35%";

        setTimeout(() => {
            // Stage 2 Loading Frame Emulation
            progressText.innerText = "Gemini Core Analyzing Client Payload Data...";
            progressFill.style.width = "70%";
        }, 1500);

        setTimeout(() => {
            // Stage 3 Compilation Frame Emulation
            progressText.innerText = "Building Professional Struct Table HTML Layout...";
            progressFill.style.width = "95%";
        }, 3200);

        setTimeout(() => {
            // Processing Resolution Execution
            progressFill.style.width = "100%";
            processingScreen.classList.add("hidden");
            renderScreen.classList.remove("hidden");
            
            // Build temporary iframe report view injection layout
            const simulatedReportHTML = `
                <html>
                <head>
                    <style>
                        body { font-family: sans-serif; padding: 20px; color: #333; }
                        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                        th { background-color: #7D39EB; color: white; }
                    </style>
                </head>
                <body>
                    <h2>Tailored Engine Analysis Report</h2>
                    <p><strong>System Profile Target:</strong> ${JSON.parse(jsonDataArea.value).client_name || "John Doe"}</p>
                    <table>
                        <tr><th>Evaluation Sector</th><th>Strategy Recommendation Framework</th></tr>
                        <tr><td>Performance Priority</td><td>Optimized resource execution via architectural constraints layout guidelines.</td></tr>
                        <tr><td>Strategic Matrix Alignment</td><td>Verified alignment matching against provided internal reference criteria profile documentation.</td></tr>
                    </table>
                </body>
                </html>`;
            
            const doc = htmlPreview.contentWindow.document;
            doc.open();
            doc.write(simulatedReportHTML);
            doc.close();

            // Enable Final Compilation Download Option Button
            downloadBtn.classList.remove("download-disabled");
            downloadBtn.disabled = false;
            stepReady.className = "step completed";
        }, 4500);
    });
});
