@echo off
REM Активация виртуальной среды
call venv\Scripts\activate.bat

REM Запуск main.py
python main.py

REM Проверка, был ли main.py выполнен успешно
if %errorlevel% neq 0 (
    echo Ошибка при запуске main.py
    goto end
)

REM Запуск app.py
start python app.py

REM Проверка, был ли app.py выполнен успешно
if %errorlevel% neq 0 (
    echo Ошибка при запуске app.py
    goto end
)

REM Задержка в 20 секунд
echo Ожидание 20 секунд перед открытием веб-страницы...
timeout /t 20 /nobreak >nul

REM Открытие веб-страницы
start http://127.0.0.1:5000/

:end
echo Все скрипты выполнены. Нажмите любую клавишу для выхода.
pause