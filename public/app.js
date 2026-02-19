// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const selectBtn = document.getElementById('selectBtn');
const fileInfo = document.getElementById('fileInfo');
const generateBtn = document.getElementById('generateBtn');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

let selectedFile = null;

// Initialize Event Listeners
function initEventListeners() {
    // Click to select file
    selectBtn.addEventListener('click', () => {
        fileInput.click();
    });

    uploadBox.addEventListener('click', (e) => {
        if (e.target !== selectBtn) {
            fileInput.click();
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    // Drag and drop events
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('dragover');
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        handleFileSelect(file);
    });

    // Generate report button
    generateBtn.addEventListener('click', generateReport);
}

// Handle file selection
function handleFileSelect(file) {
    if (!file) return;

    // Validate file type
    const allowedTypes = ['text/csv', 'application/vnd.ms-excel', 
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    const allowedExtensions = ['.csv', '.xlsx', '.xls'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
        showError('지원하지 않는 파일 형식입니다. CSV 또는 XLSX 파일을 선택해주세요.');
        return;
    }

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
        showError('파일 크기가 너무 큽니다. 10MB 이하의 파일을 선택해주세요.');
        return;
    }

    selectedFile = file;

    // Display file info
    const fileSize = (file.size / 1024).toFixed(2);
    fileInfo.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <strong>선택된 파일:</strong> ${file.name}<br>
                <strong>파일 크기:</strong> ${fileSize} KB
            </div>
            <div style="font-size: 2em;">✅</div>
        </div>
    `;
    fileInfo.classList.add('show');

    // Enable generate button
    generateBtn.disabled = false;
}

// Generate report
async function generateReport() {
    if (!selectedFile) {
        showError('파일을 먼저 선택해주세요.');
        return;
    }

    // Disable button during generation
    generateBtn.disabled = true;
    progressSection.style.display = 'block';
    
    // Scroll to progress section
    progressSection.scrollIntoView({ behavior: 'smooth', block: 'center' });

    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);

        // Update progress: Upload
        updateProgress(20, '파일 업로드 중...');

        // Send request to server
        const response = await fetch('/api/generate-report', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '보고서 생성 중 오류가 발생했습니다.');
        }

        // Update progress: Processing
        updateProgress(40, 'Pandas로 데이터 분석 중...');
        await sleep(800);

        updateProgress(60, 'GPT API로 분석 보고서 생성 중...');
        await sleep(800);

        updateProgress(80, 'Matplotlib 차트 생성 중...');
        await sleep(800);

        updateProgress(90, 'ReportLab으로 PDF 생성 중...');
        await sleep(500);

        updateProgress(100, 'PDF 다운로드 중...');

        // Get the blob
        const blob = await response.blob();

        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sales-report-${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        // Show success message
        showSuccess('보고서가 성공적으로 생성되었습니다! 다운로드를 확인하세요.');

        // Reset after delay
        setTimeout(() => {
            resetUpload();
        }, 3000);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || '보고서 생성 중 오류가 발생했습니다.');
        generateBtn.disabled = false;
        progressSection.style.display = 'none';
    }
}

// Update progress bar
function updateProgress(percent, text) {
    progressFill.style.width = `${percent}%`;
    progressText.textContent = text;
}

// Show error message
function showError(message) {
    removeMessages();
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = `❌ ${message}`;
    progressSection.parentNode.insertBefore(errorDiv, progressSection);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Show success message
function showSuccess(message) {
    removeMessages();
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = `✅ ${message}`;
    progressSection.parentNode.insertBefore(successDiv, progressSection);
    
    setTimeout(() => {
        successDiv.remove();
    }, 5000);
}

// Remove existing messages
function removeMessages() {
    const messages = document.querySelectorAll('.error-message, .success-message');
    messages.forEach(msg => msg.remove());
}

// Reset upload state
function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.classList.remove('show');
    fileInfo.innerHTML = '';
    generateBtn.disabled = true;
    progressSection.style.display = 'none';
    updateProgress(0, '');
}

// Utility function for delays
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Check server health on load
async function checkServerHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('Server status:', data);
    } catch (error) {
        console.error('Server health check failed:', error);
        showError('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.');
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    checkServerHealth();
    console.log('Sales Report Generator initialized');
});

