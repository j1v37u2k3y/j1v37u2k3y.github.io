# MCP Server for j1v37u2k3y Blog

An MCP (Model Context Protocol) server that provides read/write CMS tools for the j1v37u2k3y Jekyll blog.

## Setup

```bash
cd mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
source .venv/bin/activate
python server.py
```

The server uses stdio transport and is meant to be configured as an MCP server in a client like Claude Code.

## Claude Code Configuration

Add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "blog": {
      "command": "mcp-server/.venv/bin/python",
      "args": [
        "mcp-server/server.py"
      ]
    }
  }
}
```

Or with a custom blog root:

```json
{
  "mcpServers": {
    "blog": {
      "command": "mcp-server/.venv/bin/python",
      "args": [
        "mcp-server/server.py"
      ],
      "env": {
        "BLOG_ROOT": "/path/to/blog"
      }
    }
  }
}
```

## Available Tools

### Read Tools

| Tool                       | Description                                          |
|----------------------------|------------------------------------------------------|
| `search_blog`              | Full-text search across all posts and the cheatsheet |
| `list_posts`               | List all posts with metadata                         |
| `read_post`                | Read a post by slug or filename                      |
| `search_cheatsheet`        | Search cheatsheet by keyword                         |
| `list_cheatsheet_sections` | List all H1 sections in the cheatsheet               |
| `read_cheatsheet_section`  | Read a cheatsheet section by heading                 |
| `list_tags`                | List all tags with counts                            |
| `list_categories`          | List all categories with counts                      |
| `read_page`                | Read any page by name                                |

### Write Tools

| Tool                   | Description                                                  |
|------------------------|--------------------------------------------------------------|
| `create_post`          | Create a new blog post with proper front matter              |
| `update_post`          | Update an existing post's content or front matter            |
| `add_cheatsheet_entry` | Append content to a cheatsheet section (or create a new one) |
