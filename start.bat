@echo off
title 버튜버 어시스턴트 런처

echo ============================================
echo   류아 VTuber Assistant 시작뿡빵띠
echo ============================================
echo.

echo [1/3] GPT-SoVITS 서버 시작...
wt new-tab --title "GPT-SoVITS" cmd /k "C:\Users\bird8\miniconda3\Scripts\activate.bat GPTSoVits & cd /d E:\my_fun_boot\GPT-SoVITS & python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml"

echo       10초 대기 중...
timeout /t 10 /nobreak > nul

echo [2/3] Electron 오버레이 시작...
wt -w 0 new-tab --title "Overlay" cmd /k "cd /d E:\mycoding_test\vtuber-assistant\overlay & npm start"

echo       5초 대기 중...
timeout /t 5 /nobreak > nul

echo [3/3] 파이프라인 시작...
wt -w 0 new-tab --title "Pipeline" cmd /k "C:\Users\bird8\miniconda3\Scripts\activate.bat vtuber-assistant & cd /d E:\mycoding_test\vtuber-assistant & python main.py"

echo.
echo ============================================
echo   모두 시작 완료뿡빵띠
echo   VTube Studio 켜고 Win+Ctrl+T로 고정하라구요~
echo ============================================
echo.
timeout /t 5
exit