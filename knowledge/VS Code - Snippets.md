---
foam_template:
  filepath: "0 - INBOX/VS Code - Snippets.md"
  description: "New note"
created: "2026-03-16"
bloggable: true
---

# VS Code - Snippets

https://www.deepanseeralan.com/tech/insert-datetime-vscode-using-snippets/

Snippets can now be scoped to a project and shared with your team. Use the Preferences: Configure User Snippets command or create *.code-snippets file in the .vscode folder.


Create a snippet :

```json
{
    "Insert Current Date": {
        "prefix": ["date", "cdate"],
        "body": "$CURRENT_MONTH/$CURRENT_DATE/$CURRENT_YEAR_SHORT",
        "description": "Insert current date in DD/MM/YY format"
    }
}
```

Affect a shortcut to the snippet : 

```json
{
    "key": "cmd+k /",
    "command": "editor.action.insertSnippet",
    "when": "editorTextFocus",
    "args": {
        "langId": "markdown",
        "name": "Insert Current Date"
    }
}
```
