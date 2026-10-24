This script:

- Recursively prints a directory tree using Unicode branch characters.

- Skips the "node_modules" folder to keep the output clean.

```ps
function Show-Tree($path, $prefix = "") {
    $items = Get-ChildItem -LiteralPath $path | Where-Object { $_.Name -ne "node_modules" -and $_.Name -ne "myvenv"
}
    $count = $items.Count

    for ($i = 0; $i -lt $count; $i++) {
        $item = $items[$i]
        $connector = if ($i -eq $count - 1) { "└── " } else { "├── " }
        Write-Output "$prefix$connector$($item.Name)"

        if ($item.PSIsContainer) {
            $extension = if ($i -eq $count - 1) { "    " } else { "│   " }
            Show-Tree $item.FullName ($prefix + $extension)
        }
    }
}
```
`Press Enter`

```ps
Show-Tree "DRIVE:\Path\To\Your\Project"
```

### To save to a file

```ps
Show-Tree "DRIVE:\Path\To\Your\Project" > tree.txt
```
