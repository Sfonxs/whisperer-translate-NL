# Test script for Whisperer with Enter key as response trigger
# Save this as test-enter-response.ps1

# Load required assemblies
Add-Type -AssemblyName System.Windows.Forms

# Start the Python script in a new window
Start-Process python -ArgumentList "whisperer-translate-to-dutch.py"

# Wait for the script to initialize
Start-Sleep -Seconds 3

# Open Notepad to help with testing
Start-Process notepad
Start-Sleep -Seconds 2

# Bring Notepad to the foreground
$wshell = New-Object -ComObject WScript.Shell
$wshell.AppActivate("Notepad")
Start-Sleep -Seconds 1

# Type some sample text so we can see the results
$wshell.SendKeys("Testing whisperer with ChatGPT response: ")
Start-Sleep -Seconds 1

# Simulate holding down right CTRL key and pressing Enter
$wshell.SendKeys("^{ENTER}")
Start-Sleep -Seconds 2

# Keep recording for a few seconds (simulating speech)
Start-Sleep -Seconds 3

# Release CTRL key
$wshell.SendKeys("^")

# Wait for processing to complete
Start-Sleep -Seconds 5

Write-Host "Test complete. Check Notepad for the response."
