```bat
@echo off
setlocal EnableDelayedExpansion

title CityScience - Instalador e Executor

echo ==========================================
echo          CITYSCIENCE
echo     INSTALADOR E EXECUTOR AUTOMATICO
echo ==========================================
echo.

REM ============================================================
REM 1. VERIFICAR PYTHON
REM ============================================================

echo [1/5] Verificando Python...

where py >nul 2>&1

if %errorlevel%==0 (
    set "PY=py"
    goto PYTHON_OK
)

where python >nul 2>&1

if %errorlevel%==0 (
    set "PY=python"
    goto PYTHON_OK
)

echo.
echo [AVISO] Python nao encontrado.
echo Tentando instalar automaticamente...
echo.

REM ============================================================
REM 2. VERIFICAR WINGET
REM ============================================================

where winget >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] winget nao encontrado.
    echo.
    echo Instale o Python manualmente:
    echo https://www.python.org/downloads/windows/
    echo.
    pause
    exit /b 1
)

echo [OK] winget encontrado.
echo.
echo Instalando Python 3.12...
echo.

winget install --id Python.Python.3.12 -e --scope user --accept-source-agreements --accept-package-agreements

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar Python.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Python instalado.
echo.

REM ============================================================
REM ATUALIZAR PATH DA SESSAO
REM ============================================================

set "PATH=%PATH%;%LocalAppData%\Programs\Python\Python312;%LocalAppData%\Programs\Python\Python312\Scripts"

REM ============================================================
REM VERIFICAR PYTHON NOVAMENTE
REM ============================================================

where py >nul 2>&1

if %errorlevel%==0 (
    set "PY=py"
    goto PYTHON_OK
)

where python >nul 2>&1

if %errorlevel%==0 (
    set "PY=python"
    goto PYTHON_OK
)

echo.
echo [ERRO] Python instalado, mas nao foi encontrado.
echo Execute este arquivo novamente.
echo.
pause
exit /b 1


:PYTHON_OK

echo [OK] Python encontrado:
%PY% --version
echo.


REM ============================================================
REM 3. CRIAR AMBIENTE VIRTUAL
REM ============================================================

echo [2/5] Verificando ambiente virtual...

if not exist ".venv" (

    echo Criando ambiente virtual...

    %PY% -m venv .venv

    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao criar ambiente virtual.
        echo.
        pause
        exit /b 1
    )

    echo [OK] Ambiente virtual criado.

) else (

    echo [OK] Ambiente virtual ja existe.

)

echo.


REM ============================================================
REM 4. INSTALAR DEPENDENCIAS
REM ============================================================

echo [3/5] Instalando dependencias...

if not exist "requirements.txt" (
    echo.
    echo [ERRO] requirements.txt nao encontrado!
    echo.
    pause
    exit /b 1
)

call ".venv\Scripts\python.exe" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar dependencias.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Dependencias instaladas.
echo.


REM ============================================================
REM 5. EXECUTAR APP.PY
REM ============================================================

echo [4/5] Iniciando CityScience...

if not exist "app.py" (
    echo.
    echo [ERRO] app.py nao encontrado!
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo        CITYSCIENCE INICIADO
echo ==========================================
echo.
echo Aguardando 10 segundos para o servidor iniciar...
echo.

start "CityScience Server" cmd /k ".venv\Scripts\python.exe app.py"

REM ============================================================
REM ESPERAR 10 SEGUNDOS
REM ============================================================

timeout /t 10 /nobreak >nul


REM ============================================================
REM ABRIR LOCALHOST:5500
REM ============================================================

echo [5/5] Abrindo http://localhost:5500...
echo.

start "" "http://localhost:5500"

echo ==========================================
echo       CITYSCIENCE EXECUTANDO
echo ==========================================
echo.
echo http://localhost:5500
echo.
echo Mantenha a janela do servidor aberta.
echo ==========================================
echo.

pause
```
