# Define the path for the backup file and directory
$backupDir = "D:\Flothers\Windows registry\watch\backup"
$backupPath = "$backupDir\full_registry_backup.reg"

# Function to restore the registry from the backup file
function Restore-Registry {
    if (Test-Path $backupPath) {
        try {
            reg import $backupPath
            Write-Output "Registry restored successfully from $backupPath"
        } catch {
            Write-Output "An error occurred while restoring the registry: $_"
        }
    } else {
        Write-Output "Backup file not found. Cannot restore the registry."
    }
}

# Execute the restore
Restore-Registry
