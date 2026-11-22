@echo off
REM TikToks de Sciences éco (francés, voz gratis). Ejecutar en el PC (necesita internet para edge-tts).
REM Requisitos: pip install edge-tts pillow  y ffmpeg en el PATH
cd /d "%~dp0"
set VOZ=fr-FR-DeniseNeural
set VOZ_RATE=-10%%
for %%f in (specs\eco\*.json) do (
  python tts_gratis.py %%f
  python render.py %%f
  python publicar.py %%f --no-push
)
echo.
echo Listo. Para subirlos: git pull --rebase ^&^& git add -A ^&^& git commit -m "Videos eco" ^&^& git push
pause
