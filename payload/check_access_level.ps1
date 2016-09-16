If(([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
  $(whoami) + "`nRunning with admin privs. All aboard, next stop: NT Authority\System" | Out-File "output.txt"
}
Else
{
  $(whoami) + "`nNo admin privs :(" | Out-File "output.txt"
}