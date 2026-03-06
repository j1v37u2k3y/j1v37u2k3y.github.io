"""MCP server for the j1v37u2k3y blog — read/write CMS over MCP."""

import json
from mcp.server.fastmcp import FastMCP

import blog

mcp = FastMCP("j1v37u2k3y-blog", instructions="CMS tools for the j1v37u2k3y Jekyll blog.")


# ---------------------------------------------------------------------------
# Read tools
# ---------------------------------------------------------------------------


@mcp.tool()
def search_blog(query: str) -> str:
  """Full-text search across all posts and the cheatsheet. Returns matching snippets with file paths."""
  results = blog.search_blog(query)
  if not results:
    return f"No results for '{query}'"
  return json.dumps(results, indent=2)


@mcp.tool()
def list_posts() -> str:
  """List all blog posts with title, date, category, tags, and published status."""
  posts = blog.list_posts()
  return json.dumps(posts, indent=2)


@mcp.tool()
def read_post(identifier: str) -> str:
  """Read a specific post by slug or filename. Returns front matter and content.

  Args:
      identifier: Post slug (e.g. 'htb-cap'), filename, or stem.
  """
  post = blog.read_post(identifier)
  if post is None:
    return f"Post '{identifier}' not found"
  return json.dumps(post, indent=2)


@mcp.tool()
def search_cheatsheet(query: str) -> str:
  """Search the cheatsheet by keyword. Returns matching sections with context."""
  results = blog.search_cheatsheet(query)
  if not results:
    return f"No cheatsheet results for '{query}'"
  return json.dumps(results, indent=2)


@mcp.tool()
def list_cheatsheet_sections() -> str:
  """List all H1 sections in the cheatsheet with line counts."""
  sections = blog.list_cheatsheet_sections()
  return json.dumps(sections, indent=2)


@mcp.tool()
def read_cheatsheet_section(heading: str) -> str:
  """Read a specific cheatsheet section by heading name (case-insensitive partial match).

  Args:
      heading: Full or partial H1 heading name (e.g. 'reverse shells', 'smb').
  """
  section = blog.read_cheatsheet_section(heading)
  if section is None:
    return f"Section '{heading}' not found"
  return json.dumps(section, indent=2)


@mcp.tool()
def list_tags() -> str:
  """List all unique tags across blog posts with counts."""
  tags = blog.list_tags()
  return json.dumps(tags, indent=2)


@mcp.tool()
def list_categories() -> str:
  """List all unique categories across blog posts with counts."""
  cats = blog.list_categories()
  return json.dumps(cats, indent=2)


@mcp.tool()
def read_page(name: str) -> str:
  """Read any page (about, cheatsheet, etc.) by name.

  Args:
      name: Page name without extension (e.g. 'about').
  """
  page = blog.read_page(name)
  if page is None:
    return f"Page '{name}' not found"
  return json.dumps(page, indent=2)


# ---------------------------------------------------------------------------
# Write tools
# ---------------------------------------------------------------------------


@mcp.tool()
def create_post(
  title: str,
  content: str,
  category: str = "ctfs",
  tags: list[str] | None = None,
  published: bool = True,
  post_date: str | None = None,
) -> str:
  """Create a new blog post with proper front matter.

  Args:
      title: Post title.
      content: Markdown body content.
      category: Post category (default: 'ctfs').
      tags: List of tags.
      published: Whether the post is published (default: True).
      post_date: Date in YYYY-MM-DD format (default: today).
  """
  filename = blog.create_post(
    title=title,
    content=content,
    category=category,
    tags=tags,
    published=published,
    post_date=post_date,
  )
  return f"Created post: {filename}"


@mcp.tool()
def update_post(
  identifier: str,
  content: str | None = None,
  front_matter: dict | None = None,
) -> str:
  """Update an existing post's content or front matter.

  Args:
      identifier: Post slug, filename, or stem.
      content: New markdown body (or None to keep existing).
      front_matter: Dict of front matter fields to update (merged with existing).
  """
  result = blog.update_post(identifier, front_matter=front_matter, content=content)
  if result is None:
    return f"Post '{identifier}' not found"
  return f"Updated post: {result}"


@mcp.tool()
def add_cheatsheet_entry(heading: str, content: str) -> str:
  """Append content under an existing cheatsheet H1 section, or create a new H1 section.

  Args:
      heading: H1 section heading to append to (or new heading to create).
      content: Markdown content to add.
  """
  return blog.add_cheatsheet_entry(heading, content)


if __name__ == "__main__":
  mcp.run()
