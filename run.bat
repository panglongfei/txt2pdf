@echo off
:: 设置标题
title TXT转PDF工具

:: 设置控制台颜色（浅蓝底黑字）
color 1F

:: 设置编码为UTF-8
chcp 65001 > nul

echo ======================================
echo         TXT转PDF工具启动程序
echo ======================================
echo.

:: 检查Python是否安装
python --version > nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python！
    echo [提示] 请安装Python 3.7或更高版本...
    echo [提示] 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查是否存在虚拟环境
if not exist ".venv" (
    echo [信息] 首次运行，正在创建虚拟环境...
    echo [信息] 请稍候...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo [错误] 创建虚拟环境失败！
        echo [提示] 请确保已安装Python 3.7或更高版本
        echo [提示] 并已添加到系统环境变量
        pause
        exit /b 1
    )
    echo [成功] 虚拟环境创建完成！
    echo.
)

:: 激活虚拟环境
echo [信息] 正在启动虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo [错误] 激活虚拟环境失败！
    pause
    exit /b 1
)
echo [成功] 虚拟环境已启动！
echo.

:: 检查依赖是否已安装
if not exist "venv\Lib\site-packages\flask" (
    echo [信息] 正在安装必要的依赖包...
    echo [信息] 这可能需要几分钟时间，请耐心等待...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [错误] 安装依赖失败！
        echo [提示] 请检查以下可能的问题：
        echo    1. 网络连接是否正常
        echo    2. requirements.txt 文件是否存在
        echo    3. pip 是否正常工作
        echo.
        echo [建议] 您可以尝试手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo [成功] 依赖安装完成！
    echo.
)

:: 启动应用
echo [信息] 正在启动应用...
echo [信息] 启动成功后，请在浏览器中访问: http://localhost:5000
echo.
echo ======================================
echo         按 Ctrl+C 可停止服务
echo ======================================
echo.

python run.py

:: 如果程序异常退出，显示错误信息
if errorlevel 1 (
    echo.
    echo [错误] 程序异常退出！
    echo [提示] 请检查以下可能的问题：
    echo    1. 端口5000是否被占用
    echo    2. 是否有足够的系统权限
    echo    3. 查看上方是否有具体的错误信息
    echo.
    echo 按任意键退出...
    pause > nul
) 