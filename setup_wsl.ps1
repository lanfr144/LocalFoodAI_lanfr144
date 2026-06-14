#ident "@(#)$Format:Food:setup_wsl.ps1:Francois Lange:lanfr144@school.lu:2026/06/14 19:15:22:Francois Lange:lanfr144@school.lu:2026/06/14 19:15:22:980a319e59134ca6511a42ecad9297::$""
# ==============================================================================
# Local Food AI - Windows WSL Setup Script
# Run in Administrator PowerShell on the Windows Host
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Blue
Write-Host " Starting Windows WSL Setup for Local Food AI..."
Write-Host "==========================================================" -ForegroundColor Blue

# 1. Enable Windows Subsystem for Linux (WSL) and Virtual Machine Platform
Write-Host "`n[1/4] Enabling WSL and Virtual Machine Platform features..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 2. Update WSL kernel
Write-Host "`n[2/4] Updating WSL kernel to the latest version..." -ForegroundColor Yellow
wsl --update

# 3. Install Ubuntu 22.04 LTS with instance name Dopro1
Write-Host "`n[3/4] Installing Ubuntu-22.04 LTS instance named 'Dopro1'..." -ForegroundColor Yellow
Write-Host "This will spawn a terminal window to configure your Unix username & password." -ForegroundColor Cyan
Write-Host "Please set the username to 'lanfr144' when prompted!" -ForegroundColor Cyan
wsl --install -d Ubuntu-22.04 --name Dopro1

# 4. Networking and DNS Configuration instructions
Write-Host "`n[4/4] Installation initiated successfully!" -ForegroundColor Green
Write-Host "----------------------------------------------------------"
Write-Host "POST-INSTALLATION DIRECTIVES:"
Write-Host "1. In the newly opened WSL terminal, complete the Unix account creation."
Write-Host "2. Once logged into WSL, run the following to navigate to your home directory:"
Write-Host "   cd ~"
Write-Host "3. Execute the setup_app.sh script inside WSL to configure Docker and launch the project."
Write-Host "----------------------------------------------------------"
Write-Host "==========================================================" -ForegroundColor Blue
