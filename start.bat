@echo off
title 버튜버 어시스턴트

echo GPT-SoVITS 서버 시작 중...
start "GPT-SoVITS" cmd /k "call C:\Users\bird8\miniconda3\Scripts\activate.bat GPTSoVits && cd E:\my_fun_boot\GPT-SoVITS && python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml"

echo 10초 대기 중... (GPT-SoVITS 로딩 시간)
timeout /t 10 /nobreak

echo 파이프라인 시작 중...
start "파이프라인" cmd /k "call C:\Users\bird8\miniconda3\Scripts\activate.bat vtuber-assistant && cd E:\mycoding_test\vtuber-assistant && python main.py"

echo 완료뿡빵띠

::@echo off
::title 버튜버 어시스턴트

::echo GPT-SoVITS 서버 시작 중...
::start "GPT-SoVITS" cmd /k "call C:\Users\bird8\miniconda3\Scripts\activate.bat GPTSoVits && cd E:\my_fun_boot\GPT-SoVITS && python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml"

::echo 완료뿡빵띠