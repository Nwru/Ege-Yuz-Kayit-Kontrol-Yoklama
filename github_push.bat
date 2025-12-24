@echo off
echo GitHub'a yukleme scripti
echo.
echo Lutfen GitHub repository URL'inizi girin (ornek: https://github.com/kullaniciadi/repo-adi.git)
set /p REPO_URL="Repository URL: "

if "%REPO_URL%"=="" (
    echo Hata: Repository URL gerekli!
    pause
    exit /b 1
)

echo.
echo Remote repository ekleniyor...
git remote add origin %REPO_URL% 2>nul
if errorlevel 1 (
    echo Remote zaten mevcut, guncelleniyor...
    git remote set-url origin %REPO_URL%
)

echo Branch main olarak ayarlaniyor...
git branch -M main

echo.
echo GitHub'a yukleniyor...
git push -u origin main

if errorlevel 1 (
    echo.
    echo Hata: Push islemi basarisiz oldu!
    echo Lutfen GitHub hesabiniza giris yaptiginizdan ve repository'nin var oldugundan emin olun.
) else (
    echo.
    echo Basarili! Proje GitHub'a yuklendi!
)

pause

