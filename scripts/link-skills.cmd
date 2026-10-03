@echo off
setlocal
cd /d "%~dp0.."
if exist ".claude\skills" rmdir ".claude\skills"
if exist ".cursor\skills" rmdir ".cursor\skills"
mklink /J ".claude\skills" ".agents\skills"
if errorlevel 1 exit /b 1
mklink /J ".cursor\skills" ".agents\skills"
if errorlevel 1 exit /b 1
echo OK: .claude\skills e .cursor\skills apontam para .agents\skills
