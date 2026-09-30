/**
 * DocuMorph Client Controller
 * Handles drag & drop, mode switching, dual-direction conversion,
 * progress tracking, and UI state management.
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements - Navigation & Theme
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const btnOpenPrompts = document.getElementById('btnOpenPrompts');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const promptsModal = document.getElementById('promptsModal');
  const copyPromptBtns = document.querySelectorAll('.btn-copy-prompt');

  // DOM Elements - Mode Switcher
  const modeWordToPdf = document.getElementById('modeWordToPdf');
  const modePdfToWord = document.getElementById('modePdfToWord');
  const dropSubtitle = document.getElementById('dropSubtitle');

  // DOM Elements - Drop Zone & File Selection
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const btnSelectFile = document.getElementById('btnSelectFile');
  const dropContent = document.getElementById('dropContent');

  // DOM Elements - Process View
  const processView = document.getElementById('processView');
  const fileTypeIcon = document.getElementById('fileTypeIcon');
  const selectedFileName = document.getElementById('selectedFileName');
  const selectedFileSize = document.getElementById('selectedFileSize');
  const badgeDirection = document.getElementById('badgeDirection');
  const btnCancelFile = document.getElementById('btnCancelFile');

  // Progress Bar & Actions
  const progressBarFill = document.getElementById('progressBarFill');
  const progressStatusText = document.getElementById('progressStatusText');
  const progressPercentage = document.getElementById('progressPercentage');
  const actionBtnRow = document.getElementById('actionBtnRow');
  const btnStartConvert = document.getElementById('btnStartConvert');

  // Result & Error Views
  const resultBox = document.getElementById('resultBox');
  const resultFileName = document.getElementById('resultFileName');
  const resultEngine = document.getElementById('resultEngine');
  const resultFileSize = document.getElementById('resultFileSize');
  const btnDownload = document.getElementById('btnDownload');
  const btnResetConverter = document.getElementById('btnResetConverter');
  const errorBanner = document.getElementById('errorBanner');
  const errorMessage = document.getElementById('errorMessage');
  const btnRetry = document.getElementById('btnRetry');

  // State Management
  let currentMode = 'word-to-pdf'; // 'word-to-pdf' | 'pdf-to-word'
  let currentFile = null;
  let progressInterval = null;

  // 1. Theme Toggle
  const savedTheme = localStorage.getItem('documorph_theme') || 'dark';
  if (savedTheme === 'light') {
    document.body.classList.remove('theme-dark');
    document.body.classList.add('theme-light');
  }

  themeToggleBtn.addEventListener('click', () => {
    const isLight = document.body.classList.toggle('theme-light');
    document.body.classList.toggle('theme-dark', !isLight);
    localStorage.setItem('documorph_theme', isLight ? 'light' : 'dark');
  });

  // 2. Mode Switcher
  function setMode(mode) {
    currentMode = mode;
    if (mode === 'word-to-pdf') {
      modeWordToPdf.classList.add('active');
      modePdfToWord.classList.remove('active');
      modeWordToPdf.setAttribute('aria-selected', 'true');
      modePdfToWord.setAttribute('aria-selected', 'false');
      dropSubtitle.textContent = 'Supports Microsoft Word (.docx, .doc)';
      fileInput.accept = '.docx,.doc';
      if (currentFile) badgeDirection.textContent = 'DOCX ➔ PDF';
    } else {
      modePdfToWord.classList.add('active');
      modeWordToPdf.classList.remove('active');
      modePdfToWord.setAttribute('aria-selected', 'true');
      modeWordToPdf.setAttribute('aria-selected', 'false');
      dropSubtitle.textContent = 'Supports Adobe PDF (.pdf)';
      fileInput.accept = '.pdf';
      if (currentFile) badgeDirection.textContent = 'PDF ➔ DOCX';
    }
  }

  modeWordToPdf.addEventListener('click', () => setMode('word-to-pdf'));
  modePdfToWord.addEventListener('click', () => setMode('pdf-to-word'));

  // DOM Elements - Sample Test Buttons
  const btnSampleDocx = document.getElementById('btnSampleDocx');
  const btnSamplePdf = document.getElementById('btnSamplePdf');

  // 3. File Input Triggers & Dropzone Handling
  fileInput.addEventListener('click', (e) => {
    // Prevent event from bubbling up to dropZone
    e.stopPropagation();
  });

  // Enable keyboard navigation on label
  btnSelectFile.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });

  dropZone.addEventListener('click', (e) => {
    // Prevent triggering if clicking on buttons, labels, or process view
    if (e.target.closest('#processView') || 
        e.target.closest('button') || 
        e.target.closest('label') || 
        e.target.closest('.sample-files-group')) {
      return;
    }
    if (!currentFile) {
      fileInput.click();
    }
  });

  // Sample Documents Generation for Instant Testing
  function createSyntheticFile(filename, mimeType, content) {
    const blob = new Blob([content], { type: mimeType });
    return new File([blob], filename, { type: mimeType, lastModified: Date.now() });
  }

  btnSampleDocx.addEventListener('click', (e) => {
    e.stopPropagation();
    setMode('word-to-pdf');
    // Provide a valid dummy document container
    const sampleWord = createSyntheticFile('Quarterly_Financial_Report.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'PK\x03\x04DocuMorph Sample Word Document Content Header');
    handleFileSelection(sampleWord);
  });

  btnSamplePdf.addEventListener('click', (e) => {
    e.stopPropagation();
    setMode('pdf-to-word');
    const samplePdf = createSyntheticFile('Annual_Invoice_Summary.pdf', 'application/pdf', '%PDF-1.4\n%DocuMorph Sample PDF Stream\n%%EOF');
    handleFileSelection(samplePdf);
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelection(e.target.files[0]);
    }
  });

  // 4. Drag & Drop Handlers
  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('dragover');
    });
  });

  dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    if (dt.files && dt.files[0]) {
      handleFileSelection(dt.files[0]);
    }
  });

  // 5. File Selection & Auto-Mode Detection
  function handleFileSelection(file) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    
    // Auto-detect mode if file doesn't match active mode
    if (ext === '.pdf' && currentMode === 'word-to-pdf') {
      setMode('pdf-to-word');
    } else if (['.docx', '.doc'].includes(ext) && currentMode === 'pdf-to-word') {
      setMode('word-to-pdf');
    }

    // Validate extension
    const validDocx = ['.docx', '.doc'].includes(ext);
    const validPdf = ext === '.pdf';

    if (!validDocx && !validPdf) {
      showError('Unsupported file type. Please upload a .docx, .doc, or .pdf file.');
      return;
    }

    // Size limit: 50MB
    if (file.size > 50 * 1024 * 1024) {
      showError('File exceeds 50MB limit. Please choose a smaller document.');
      return;
    }

    currentFile = file;
    hideError();

    // Update UI elements
    selectedFileName.textContent = file.name;
    selectedFileSize.textContent = formatBytes(file.size);
    fileTypeIcon.textContent = validPdf ? '📕' : '📄';
    badgeDirection.textContent = currentMode === 'word-to-pdf' ? 'DOCX ➔ PDF' : 'PDF ➔ DOCX';

    // Show processing card
    dropContent.classList.add('hidden');
    processView.classList.remove('hidden');
    resultBox.classList.add('hidden');
    actionBtnRow.classList.remove('hidden');

    resetProgress();
  }

  // 6. Reset & Cancel Actions
  function resetAll() {
    currentFile = null;
    fileInput.value = '';
    clearInterval(progressInterval);
    dropContent.classList.remove('hidden');
    processView.classList.add('hidden');
    resultBox.classList.add('hidden');
    hideError();
    resetProgress();
  }

  btnCancelFile.addEventListener('click', (e) => {
    e.stopPropagation();
    resetAll();
  });

  btnResetConverter.addEventListener('click', (e) => {
    e.stopPropagation();
    resetAll();
  });

  // 7. Conversion Execution
  btnStartConvert.addEventListener('click', async (e) => {
    e.stopPropagation();
    if (!currentFile) return;

    actionBtnRow.classList.add('hidden');
    hideError();
    startProgressAnimation();

    const endpoint = currentMode === 'word-to-pdf' 
      ? '/api/convert/word-to-pdf' 
      : '/api/convert/pdf-to-word';

    const formData = new FormData();
    formData.append('file', currentFile);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Conversion failed' }));
        throw new Error(errorData.detail || `Server returned code ${response.status}`);
      }

      const result = await response.json();
      finishProgressSuccess(result);
    } catch (err) {
      clearInterval(progressInterval);
      
      // Smart GitHub Pages Detection: If deployed on static GitHub Pages without backend
      const isGitHubPages = window.location.hostname.includes('github.io');
      if (isGitHubPages) {
        // Complete the simulation for live web preview
        const outputExt = currentMode === 'word-to-pdf' ? '.pdf' : '.docx';
        const simulatedName = currentFile.name.replace(/\.[^/.]+$/, "") + outputExt;
        
        finishProgressSuccess({
          output_filename: simulatedName,
          engine: currentMode === 'word-to-pdf' ? 'ms-word-com' : 'pdf2docx-ai-layout',
          converted_size: formatBytes(Math.round(currentFile.size * 0.88)),
          download_url: '#'
        });

        showError('ℹ️ Note: Running in GitHub Pages static preview mode. To execute real-time document conversions with your local Word/PDF engines, run: python run.py');
        return;
      }

      showError(err.message || 'Conversion error occurred.');
      actionBtnRow.classList.remove('hidden');
      resetProgress();
    }
  });

  // 8. Progress Feedback Simulation
  function resetProgress() {
    progressBarFill.style.width = '0%';
    progressPercentage.textContent = '0%';
    progressStatusText.textContent = 'Ready to convert';
  }

  function startProgressAnimation() {
    let percent = 5;
    progressBarFill.style.width = '5%';
    progressPercentage.textContent = '5%';
    progressStatusText.textContent = 'Uploading document...';

    progressInterval = setInterval(() => {
      if (percent < 85) {
        percent += Math.floor(Math.random() * 8) + 3;
        if (percent > 85) percent = 85;

        progressBarFill.style.width = `${percent}%`;
        progressPercentage.textContent = `${percent}%`;

        if (percent > 25 && percent < 60) {
          progressStatusText.textContent = 'Parsing document layout & fonts...';
        } else if (percent >= 60) {
          progressStatusText.textContent = 'Reconstructing tables and vector pages...';
        }
      }
    }, 250);
  }

  function finishProgressSuccess(result) {
    clearInterval(progressInterval);
    progressBarFill.style.width = '100%';
    progressPercentage.textContent = '100%';
    progressStatusText.textContent = 'Conversion complete!';

    // Populate result card
    setTimeout(() => {
      resultFileName.textContent = result.output_filename;
      resultEngine.textContent = formatEngineName(result.engine);
      resultFileSize.textContent = result.converted_size;
      btnDownload.href = result.download_url;
      btnDownload.setAttribute('download', result.output_filename);

      resultBox.classList.remove('hidden');
    }, 350);
  }

  function formatEngineName(engine) {
    const map = {
      'ms-word-com': 'Native Word COM Engine',
      'libreoffice-headless': 'LibreOffice Vector Engine',
      'python-reportlab-fallback': 'ReportLab Flowable Engine',
      'pdf2docx-ai-layout': 'pdf2docx Layout Reconstructor',
      'pypdf-text-fallback': 'PyPDF Text Stream Engine'
    };
    return map[engine] || engine || 'Multi-Tier Engine';
  }

  // 9. Error Handling
  function showError(msg) {
    errorMessage.textContent = msg;
    errorBanner.classList.remove('hidden');
  }

  function hideError() {
    errorBanner.classList.add('hidden');
  }

  btnRetry.addEventListener('click', (e) => {
    e.stopPropagation();
    hideError();
    if (currentFile) {
      btnStartConvert.click();
    }
  });

  // 10. AI Prompts Modal
  btnOpenPrompts.addEventListener('click', () => {
    promptsModal.classList.remove('hidden');
  });

  btnCloseModal.addEventListener('click', () => {
    promptsModal.classList.add('hidden');
  });

  promptsModal.addEventListener('click', (e) => {
    if (e.target === promptsModal) {
      promptsModal.classList.add('hidden');
    }
  });

  copyPromptBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const textToCopy = document.getElementById(targetId).textContent;
      navigator.clipboard.writeText(textToCopy).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        btn.style.background = 'var(--accent-emerald)';
        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.background = '';
        }, 2000);
      });
    });
  });

  // Utility: Format bytes
  function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }
});
