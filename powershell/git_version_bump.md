
# Git Version Bump Script

### Purpose

Increment semantic version tags (`major`, `minor`, `patch`) based on the latest Git tag.

---

### Behavior

- Reads the latest tag using:  
    `git describe --tags --abbrev=0`

- Assumes tag format:  
    `v<major>.<minor>.<patch>`

- Increments based on input:  
  - `major` → resets minor and patch
  - `minor` → resets patch
  - `patch` → increments patch only

- Creates a new annotated tag:  
    `git tag -a <newTag> -m "Bump <part> → <newTag>"`

--- 

### Usage

Run the script from the repository root.

```powershell\
.\git_version_bump.ps1 -Part <major|minor|patch>
```

### Script

```powershell
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("major", "minor", "patch")]
    [string]$Part
)

# Get all tags
$tags = git tag

# Filter valid semantic tags (vX.Y.Z)
$validTags = @()

foreach ($tag in $tags) {
    if ($tag -match '^v\d+\.\d+\.\d+$') {
        $validTags += $tag
    }
}

# Determine latest valid tag
if ($validTags.Count -eq 0) {
    $major = 0
    $minor = 0
    $patch = 0
} else {
    # Sort tags numerically
    $sorted = $validTags | Sort-Object {
        $parts = $_.TrimStart("v").Split(".")
        [int]$parts[0] * 1e6 + [int]$parts[1] * 1e3 + [int]$parts[2]
    }

    $latest = $sorted[-1]
    $parts = $latest.TrimStart("v").Split(".")

    [int]$major = $parts[0]
    [int]$minor = $parts[1]
    [int]$patch = $parts[2]
}

# Increment version
switch ($Part) {
    "major" {
        $major++
        $minor = 0
        $patch = 0
    }
    "minor" {
        $minor++
        $patch = 0
    }
    "patch" {
        $patch++
    }
}

$newTag = "v{0}.{1}.{2}" -f $major, $minor, $patch

git tag -a $newTag -m "Bump $Part -> $newTag"
Write-Output "Created tag $newTag"
```