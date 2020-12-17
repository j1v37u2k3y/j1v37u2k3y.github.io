$date = date
ForEach ($result in Get-ChildItem | select Name, BaseName) {
  pandoc.exe -f docx -t markdown_strict -i $result.Name -o "$($date.Year)-$($date.Month)-$($date.Day)-$($result.BaseName).md" --wrap=none --markdown-headings=atx --extract-media="$($result.BaseName.ToLower())"
}