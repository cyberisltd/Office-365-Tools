$UserCredential = Get-Credential
$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri https://outlook.office365.com/powershell-liveid/ -Credential $UserCredential -Authentication Basic -AllowRedirection
Import-PSSession $Session
$ErrorActionPreference = "Stop"

$OutputFile = "REPLACE"
$currentdate = get-date
$Start = $currentdate.AddDays(-7)
$EndDate = $currentdate

$operation = "UserLoggedIn"

"Window is $Start -> $EndDate"
do {
    #download 3 hours at a time, until the start date/time is reached
    $StartDate = $EndDate.AddHours(-3)
    "Running search for $StartDate -> $EndDate"
    
    do {

        $time = get-date
        # Search the defined date(s), SessionId + SessionCommand in combination with the loop will return and append 5000 object per iteration until all objects are returned (maximum limit is 50k objects)
        do {

            try {
                $AuditOutput = Search-UnifiedAuditLog -StartDate $StartDate -EndDate $EndDate -SessionId "$StartDate -> $EndDate" -operations $operation -SessionCommand ReturnLargeSet -ResultSize 5000 
                $errorvar = $false
            }
            catch {
                $errorvar = $true
                "An error occured. Trying again."
            }

        } while ($errorvar)

        if ($auditOutput) {
            "Results received (" + ($(get-date) - $time) + "), writing to file..."
            $filename = "$StartDate-$EndDate.csv".Replace(":",".").Replace("/","-")

            $auditOutput| Export-Csv "$Outputfile\$filename" -NoTypeInformation -Append
        }

    } while ($AuditOutput)

    $endDate = $EndDate.AddHours(-3)

} while ($Start -lt $StartDate)
