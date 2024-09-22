using namespace System.Runtime.InteropServices

[CmdletBinding()]
param (
    [Parameter(Mandatory)]
    [string]$HivePath,

    [Parameter()]
    [string]$LogPath = "$PSScriptRoot\RegMon-$(Get-Date -Format 'yyyyMMdd-HHmmss').log",

    [Parameter()]
    [int]$Timeout = 0xFFFFFFFF # INFINITE
)

$signature = @'
using System;
using System.Runtime.InteropServices;

namespace Win32
{
    public class Regmon
    {
        [DllImport("Advapi32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern int RegOpenKeyExW(
            IntPtr hKey,
            string lpSubKey,
            uint ulOptions,
            uint samDesired,
            out IntPtr phkResult
        );

        [DllImport("Advapi32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern int RegNotifyChangeKeyValue(
            IntPtr hKey,
            bool bWatchSubtree,
            uint dwNotifyFilter,
            IntPtr hEvent,
            bool fAsynchronous
        );

        [DllImport("Advapi32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern int RegCloseKey(IntPtr hKey);

        [DllImport("Advapi32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern int CloseHandle(IntPtr hKey);

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern IntPtr CreateEventW(
            IntPtr lpEventAttributes,
            bool bManualReset,
            bool bInitialState,
            string lpName
        );

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern uint WaitForSingleObject(
            IntPtr hHandle,
            uint dwMilliseconds
        );
    }
}
'@

Add-Type -TypeDefinition $signature

# Registry Hive Map
$hiveMap = @{
    'HKEY_CLASSES_ROOT' = 0x80000000
    'HKEY_CURRENT_USER' = 0x80000001
    'HKEY_LOCAL_MACHINE' = 0x80000002
    'HKEY_USERS' = 0x80000003
}

# Trim and standardize the input HivePath
$HivePath = $HivePath.Trim().ToUpper()

# Debugging: Output the provided HivePath
Write-Host "Provided HivePath: $HivePath"

if (-not $hiveMap.ContainsKey($HivePath)) { 
    throw "Unsupported registry hive. Valid options are: $($hiveMap.Keys -join ', ')."
}

$rootKey = $hiveMap[$HivePath]
$handle = [IntPtr]::Zero

# Open the registry root key
$result = [Win32.Regmon]::RegOpenKeyExW($rootKey, [null], 0, 0x0010, [ref]$handle)
if ($result -ne 0) { throw "Failed to open registry key." }

# Create an event for notification
$event = [Win32.Regmon]::CreateEventW([IntPtr]::Zero, $true, $false, [null])
if ($event -eq [IntPtr]::Zero) { throw "Failed to create event." }

function Monitor-SubKeys {
    param (
        [string]$KeyPath
    )

    # Open the key to be monitored
    $handle = [IntPtr]::Zero
    $result = [Win32.Regmon]::RegOpenKeyExW($rootKey, $KeyPath, 0, 0x0010, [ref]$handle)
    if ($result -ne 0) { throw "Failed to open registry key $KeyPath." }

    while ($true) {
        $result = [Win32.Regmon]::RegNotifyChangeKeyValue(
            $handle,
            $true,
            0x00000001 -bor # REG_NOTIFY_CHANGE_NAME
            0x00000002 -bor # REG_NOTIFY_CHANGE_ATTRIBUTES
            0x00000004 -bor # REG_NOTIFY_CHANGE_LAST_SET
            0x00000008, # REG_NOTIFY_CHANGE_SECURITY
            $event,
            $true
        )
        if ($result -ne 0) { throw "Failed to set up notification for $KeyPath." }

        $wait = [Win32.Regmon]::WaitForSingleObject($event, $Timeout)

        switch ($wait) {
            0xFFFFFFFF { break } # WAIT_FAILED
            0x00000102 { # WAIT_TIMEOUT
                $outp = "Timeout reached on key $KeyPath."
                Write-Host $outp -ForegroundColor DarkGreen
                Add-Content -Path $LogPath -Value $outp
                break
            }
            0 { # WAIT_OBJECT_0 - Change detected
                $outp = "Change detected on the key $KeyPath. Timestamp: $(Get-Date -Format 'hh:mm:ss - dd/MM/yyyy')."
                Write-Host $outp -ForegroundColor DarkGreen
                Add-Content -Path $LogPath -Value $outp

                # Recursively monitor subkeys
                Monitor-SubKeys -KeyPath $KeyPath
            }
        }
    }

    [Win32.Regmon]::CloseHandle($handle)
}

# Start monitoring subkeys under the root key
Monitor-SubKeys -KeyPath ""

# Clean up
[Win32.Regmon]::CloseHandle($event)
[Win32.Regmon]::RegCloseKey($handle)
