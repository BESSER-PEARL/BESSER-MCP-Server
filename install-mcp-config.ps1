# PowerShell script to install BESSER MCP Server configuration
# Run this script as Administrator or with appropriate permissions

param(
    [Parameter(Mandatory=$false)]
    [string]$Client = "cursor",
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = $PSScriptRoot
)

Write-Host "BESSER MCP Server Configuration Installer" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Get the absolute path to the project
if ([string]::IsNullOrEmpty($ProjectPath) -or $ProjectPath -eq $PSScriptRoot) {
    $ProjectPath = (Get-Location).Path
} else {
    $ProjectPath = Resolve-Path $ProjectPath
}
Write-Host "Project path: $ProjectPath" -ForegroundColor Yellow

# Configuration template
$ConfigTemplate = @{
    mcpServers = @{
        "besser-mcp" = @{
            type = "sse"
            url = "http://127.0.0.1:8000/sse"
        }
    }
}

# Convert to JSON
$ConfigJson = $ConfigTemplate | ConvertTo-Json -Depth 10

function Install-CursorConfig {
    $CursorConfigDir = "$env:USERPROFILE\.cursor"
    $CursorConfigFile = "$CursorConfigDir\mcp.json"
    
    Write-Host "Installing Cursor configuration..." -ForegroundColor Cyan
    
    # Create directory if it doesn't exist
    if (!(Test-Path $CursorConfigDir)) {
        New-Item -ItemType Directory -Path $CursorConfigDir -Force | Out-Null
        Write-Host "Created directory: $CursorConfigDir" -ForegroundColor Green
    }
    
    # Write configuration
    $ConfigJson | Out-File -FilePath $CursorConfigFile -Encoding UTF8
    Write-Host "Configuration saved to: $CursorConfigFile" -ForegroundColor Green
}

function Install-ClaudeConfig {
    $ClaudeConfigDir = "$env:APPDATA\Claude"
    $ClaudeConfigFile = "$ClaudeConfigDir\claude_desktop_config.json"
    
    Write-Host "Installing Claude Desktop configuration..." -ForegroundColor Cyan
    
    # Create directory if it doesn't exist
    if (!(Test-Path $ClaudeConfigDir)) {
        New-Item -ItemType Directory -Path $ClaudeConfigDir -Force | Out-Null
        Write-Host "Created directory: $ClaudeConfigDir" -ForegroundColor Green
    }
    
    # Write configuration
    $ConfigJson | Out-File -FilePath $ClaudeConfigFile -Encoding UTF8
    Write-Host "Configuration saved to: $ClaudeConfigFile" -ForegroundColor Green
}

# Install based on client parameter
switch ($Client.ToLower()) {
    "cursor" {
        Install-CursorConfig
    }
    "claude" {
        Install-ClaudeConfig
    }
    "both" {
        Install-CursorConfig
        Install-ClaudeConfig
    }
    default {
        Write-Host "Invalid client specified. Use 'cursor', 'claude', or 'both'" -ForegroundColor Red
        Write-Host "Example: .\install-mcp-config.ps1 -Client cursor" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart your MCP client ($Client)" -ForegroundColor White
Write-Host "2. Look for 'besser-mcp-server' in the available tools" -ForegroundColor White
Write-Host "3. Test by asking: 'What is BESSER?'" -ForegroundColor White 