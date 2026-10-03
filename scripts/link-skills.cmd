@echo off
setlocal
cd /d "%~dp0.."
if exist ".claude\skills" rmdir ".claude\skills"
if exist ".cursor\skills" rmdir ".cursor\skills"
mklink /J ".claude\skills" ".agents\skills"
if errorlevel 1 exit /b 1
mklink /J ".cursor\skills" ".agents\skills"
if errorlevel 1 exit /b 1
if exist "CLAUDE.md" del "CLAUDE.md"
mklink "CLAUDE.md" "AGENTS.md" >nul 2>&1
if errorlevel 1 mklink /H "CLAUDE.md" "AGENTS.md"
if errorlevel 1 exit /b 1
echo OK: skills junctions + CLAUDE.md aponta para AGENTS.md
