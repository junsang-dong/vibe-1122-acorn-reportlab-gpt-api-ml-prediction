const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8080;

// 미들웨어 설정
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// 업로드 디렉토리 생성
const uploadDir = path.join(__dirname, 'uploads');
const outputDir = path.join(__dirname, 'output');
const tempChartsDir = path.join(__dirname, 'temp_charts');

[uploadDir, outputDir, tempChartsDir].forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

// Multer 설정 (파일 업로드)
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, 'upload-' + uniqueSuffix + path.extname(file.originalname));
    }
});

const upload = multer({
    storage: storage,
    fileFilter: (req, file, cb) => {
        const allowedTypes = ['.csv', '.xlsx', '.xls'];
        const ext = path.extname(file.originalname).toLowerCase();
        if (allowedTypes.includes(ext)) {
            cb(null, true);
        } else {
            cb(new Error('지원하지 않는 파일 형식입니다. CSV 또는 XLSX 파일만 업로드 가능합니다.'));
        }
    },
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB 제한
    }
});

// Python 스크립트 실행 함수
function runPythonScript(scriptPath, args = []) {
    return new Promise((resolve, reject) => {
        const python = spawn('python3', [scriptPath, ...args]);
        let stdout = '';
        let stderr = '';

        python.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        python.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        python.on('close', (code) => {
            if (code !== 0) {
                console.error('Python script stderr:', stderr);
                reject(new Error(`Python script error: ${stderr}`));
            } else {
                try {
                    // stdout에서 JSON 부분만 추출
                    const lines = stdout.split('\n');
                    let jsonContent = '';
                    
                    // JSON 시작과 끝을 찾아서 추출
                    let inJson = false;
                    for (const line of lines) {
                        const trimmedLine = line.trim();
                        if (trimmedLine.startsWith('{')) {
                            inJson = true;
                            jsonContent = trimmedLine;
                        } else if (inJson) {
                            jsonContent += '\n' + line;
                            if (trimmedLine.endsWith('}')) {
                                break;
                            }
                        }
                    }
                    
                    if (jsonContent) {
                        const result = JSON.parse(jsonContent);
                        resolve(result);
                    } else {
                        // JSON을 찾지 못한 경우 전체 stdout을 시도
                        const trimmedStdout = stdout.trim();
                        if (trimmedStdout.startsWith('{') && trimmedStdout.endsWith('}')) {
                            const result = JSON.parse(trimmedStdout);
                            resolve(result);
                        } else {
                            console.error('No valid JSON found in stdout:', stdout);
                            reject(new Error('Python script did not return valid JSON'));
                        }
                    }
                } catch (e) {
                    console.error('JSON parse error:', e.message);
                    console.error('Raw stdout:', stdout);
                    reject(new Error(`JSON parse error: ${e.message}`));
                }
            }
        });

        python.on('error', (err) => {
            reject(new Error(`Failed to start Python script: ${err.message}`));
        });
    });
}

// 메인 API 엔드포인트
app.post('/api/generate-report', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: '파일이 업로드되지 않았습니다.' });
        }

        const filePath = req.file.path;
        const timestamp = Date.now();
        const outputPdfPath = path.join(outputDir, `sales-report-${timestamp}.pdf`);

        console.log('Step 1: Analyzing sales data...');
        
        // 1단계: 판매 데이터 분석 (Pandas + Matplotlib)
        const analysisResult = await runPythonScript(
            path.join(__dirname, 'analyze_sales.py'),
            [filePath]
        );

        if (!analysisResult.success) {
            throw new Error(analysisResult.error || '데이터 분석 중 오류가 발생했습니다.');
        }

        console.log('Step 2: Generating GPT analysis...');
        
        // 2단계: GPT API로 자연어 분석 보고서 생성
        const gptResult = await runPythonScript(
            path.join(__dirname, 'generate_gpt_report.py'),
            [JSON.stringify(analysisResult.stats)]
        );

        if (!gptResult.success) {
            console.warn('GPT analysis failed:', gptResult.error);
            // GPT 실패해도 계속 진행 (기본 보고서 생성)
            gptResult.analysis = 'AI 분석을 생성할 수 없습니다. OpenAI API 키를 확인해주세요.';
        }

        console.log('Step 3: Generating PDF report...');
        
        // 3단계: PDF 보고서 생성 (ReportLab)
        const pdfResult = await runPythonScript(
            path.join(__dirname, 'generate_pdf.py'),
            [
                JSON.stringify(analysisResult.stats),
                gptResult.analysis || '',
                JSON.stringify(analysisResult.charts || []),
                outputPdfPath
            ]
        );

        if (!pdfResult.success) {
            throw new Error(pdfResult.error || 'PDF 생성 중 오류가 발생했습니다.');
        }

        console.log('Step 4: Sending PDF to client...');

        // 4단계: PDF 파일 전송
        res.download(outputPdfPath, `sales-report-${timestamp}.pdf`, (err) => {
            if (err) {
                console.error('Error sending file:', err);
                if (!res.headersSent) {
                    res.status(500).json({ error: 'PDF 전송 중 오류가 발생했습니다.' });
                }
            }

            // 정리: 업로드된 파일 삭제
            setTimeout(() => {
                try {
                    if (fs.existsSync(filePath)) {
                        fs.unlinkSync(filePath);
                    }
                    // PDF는 일정 시간 후 삭제 (다운로드 완료 후)
                    setTimeout(() => {
                        if (fs.existsSync(outputPdfPath)) {
                            fs.unlinkSync(outputPdfPath);
                        }
                    }, 60000); // 1분 후 삭제
                } catch (cleanupError) {
                    console.error('Error cleaning up files:', cleanupError);
                }
            }, 1000);
        });

    } catch (error) {
        console.error('Error generating report:', error);
        res.status(500).json({
            error: '보고서 생성 중 오류가 발생했습니다.',
            details: error.message
        });

        // 에러 발생 시 업로드 파일 정리
        if (req.file && fs.existsSync(req.file.path)) {
            try {
                fs.unlinkSync(req.file.path);
            } catch (cleanupError) {
                console.error('Error cleaning up file:', cleanupError);
            }
        }
    }
});

// 상태 확인 엔드포인트
app.get('/api/health', (req, res) => {
    res.json({
        status: 'ok',
        message: 'Sales Report Generator API is running',
        version: '1.0.0'
    });
});

// 임시 차트 파일 정리 (주기적 실행)
setInterval(() => {
    try {
        if (fs.existsSync(tempChartsDir)) {
            const files = fs.readdirSync(tempChartsDir);
            const now = Date.now();
            files.forEach(file => {
                const filePath = path.join(tempChartsDir, file);
                const stats = fs.statSync(filePath);
                const fileAge = now - stats.mtimeMs;
                // 1시간 이상 된 파일 삭제
                if (fileAge > 60 * 60 * 1000) {
                    fs.unlinkSync(filePath);
                    console.log(`Deleted old chart file: ${file}`);
                }
            });
        }
    } catch (error) {
        console.error('Error cleaning up chart files:', error);
    }
}, 30 * 60 * 1000); // 30분마다 실행

// 서버 시작
app.listen(PORT, () => {
    console.log(`\n==============================================`);
    console.log(`🚀 Sales Report Generator Server is running`);
    console.log(`==============================================`);
    console.log(`📍 URL: http://localhost:${PORT}`);
    console.log(`📊 API Health: http://localhost:${PORT}/api/health`);
    console.log(`==============================================\n`);
    
    // OpenAI API 키 확인
    if (!process.env.OPENAI_API_KEY) {
        console.warn('⚠️  Warning: OPENAI_API_KEY is not set in .env file');
        console.warn('   GPT analysis will not be available\n');
    }
});

// 에러 핸들링
process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

