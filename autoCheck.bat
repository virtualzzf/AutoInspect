@echo off
secureCRT.exe /SCRIPT E:\AutoInspect\script\loginAndLogsession.vbs
python E:\AutoInspect\result_check\main.py
pause