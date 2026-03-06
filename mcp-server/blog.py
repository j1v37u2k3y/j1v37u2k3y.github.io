"""Blog content parsing helpers for the j1v37u2k3y Jekyll blog."""

import os
import re
from datetime import date
from pathlib import Path
from typing import Optional

import yaml

BLOG_ROOT = Path(os.environ.get("BLOG_ROOT", Path(__file__).parent.parent))
POSTS_DIR = BLOG_ROOT / "_posts"
PAGES_DIR = BLOG_ROOT / "pages"
CHEATSHEET_PATH = PAGES_DIR / "cheatsheet.md"

# Regex for YAML front matter delimited by ---
_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
# Post filename pattern: YYYY-MM-DD-slug.md
_POST_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")


# ---------------------------------------------------------------------------
# Front matter / content splitting
# ---------------------------------------------------------------------------

def _parse_file(path: Path) -> tuple[dict, str]:
  """Return (front_matter_dict, body_content) for a markdown file."""
  text = path.read_text(encoding="utf-8")
  m = _FRONT_MATTER_RE.match(text)
  if m:
    fm = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
  else:
    fm = {}
    body = text
  return fm, body


def _slug_from_filename(filename: str) -> Optional[str]:
  m = _POST_FILENAME_RE.match(filename)
  return m.group(2) if m else None


def _date_from_filename(filename: str) -> Optional[str]:
  m = _POST_FILENAME_RE.match(filename)
  return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Posts
# ---------------------------------------------------------------------------

def list_posts() -> list[dict]:
  """Return metadata for every post."""
  posts = []
  for f in sorted(POSTS_DIR.glob("*.md")):
    fm, _ = _parse_file(f)
    slug = _slug_from_filename(f.name)
    posts.append({
      "filename": f.name,
      "slug": slug,
      "date": _date_from_filename(f.name),
      "title": fm.get("title", ""),
      "category": fm.get("category", ""),
      "tags": fm.get("tags", []),
      "published": fm.get("published", True),
    })
  return posts


def read_post(identifier: str) -> Optional[dict]:
  """Read a post by slug or filename. Returns dict with front_matter + content."""
  for f in POSTS_DIR.glob("*.md"):
    slug = _slug_from_filename(f.name)
    if identifier in (f.name, slug, f.stem):
      fm, body = _parse_file(f)
      return {
        "filename": f.name,
        "slug": slug,
        "front_matter": fm,
        "content": body,
      }
  return None


def create_post(
  title: str,
  content: str,
  category: str = "ctfs",
  tags: Optional[list[str]] = None,
  published: bool = True,
  post_date: Optional[str] = None,
) -> str:
  """Create a new post file. Returns the created filename."""
  if post_date is None:
    post_date = date.today().isoformat()
  slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
  filename = f"{post_date}-{slug}.md"
  fm = {
    "layout": "post",
    "title": title,
    "category": category,
    "tags": tags or [],
    "published": published,
    "author": "j1v37u2k3y",
    "show_sidebar": True,
    "toc": True,
    "searchable": True,
  }
  text = "---\n" + yaml.dump(fm, default_flow_style=False, sort_keys=False) + "---\n\n" + content + "\n"
  path = POSTS_DIR / filename
  path.write_text(text, encoding="utf-8")
  return filename


def update_post(identifier: str, front_matter: Optional[dict] = None, content: Optional[str] = None) -> Optional[str]:
  """Update an existing post. Returns filename or None if not found."""
  for f in POSTS_DIR.glob("*.md"):
    slug = _slug_from_filename(f.name)
    if identifier in (f.name, slug, f.stem):
      fm, body = _parse_file(f)
      if front_matter:
        fm.update(front_matter)
      if content is not None:
        body = content
      text = "---\n" + yaml.dump(fm, default_flow_style=False, sort_keys=False) + "---\n\n" + body.lstrip("\n") + "\n"
      f.write_text(text, encoding="utf-8")
      return f.name
  return None


# ---------------------------------------------------------------------------
# Tags & categories
# ---------------------------------------------------------------------------

def list_tags() -> dict[str, int]:
  counts: dict[str, int] = {}
  for f in POSTS_DIR.glob("*.md"):
    fm, _ = _parse_file(f)
    for tag in fm.get("tags", []):
      counts[tag] = counts.get(tag, 0) + 1
  return dict(sorted(counts.items()))


def list_categories() -> dict[str, int]:
  counts: dict[str, int] = {}
  for f in POSTS_DIR.glob("*.md"):
    fm, _ = _parse_file(f)
    cat = fm.get("category", "")
    if cat:
      counts[cat] = counts.get(cat, 0) + 1
  return dict(sorted(counts.items()))


# ---------------------------------------------------------------------------
# Cheatsheet
# ---------------------------------------------------------------------------

def _parse_cheatsheet_sections() -> list[dict]:
  """Parse the cheatsheet into H1 sections, skipping # lines inside fenced code blocks."""
  if not CHEATSHEET_PATH.exists():
    return []

  fm, body = _parse_file(CHEATSHEET_PATH)
  lines = body.split("\n")
  sections: list[dict] = []
  current_heading = None
  current_lines: list[str] = []
  in_fence = False

  for line in lines:
    # Track fenced code blocks
    stripped = line.strip()
    if stripped.startswith("```"):
      in_fence = not in_fence
      if current_heading is not None:
        current_lines.append(line)
      continue

    if not in_fence and line.startswith("# ") and not line.startswith("## "):
      # New H1 section
      if current_heading is not None:
        sections.append({
          "heading": current_heading,
          "content": "\n".join(current_lines).strip(),
        })
      current_heading = line[2:].strip()
      current_lines = []
    else:
      if current_heading is not None:
        current_lines.append(line)

  # Last section
  if current_heading is not None:
    sections.append({
      "heading": current_heading,
      "content": "\n".join(current_lines).strip(),
    })

  return sections


def list_cheatsheet_sections() -> list[dict]:
  """Return list of {heading, line_count} for each H1 section."""
  sections = _parse_cheatsheet_sections()
  return [{"heading": s["heading"], "line_count": s["content"].count("\n") + 1} for s in sections]


def read_cheatsheet_section(heading: str) -> Optional[dict]:
  """Return a cheatsheet section by heading name (case-insensitive partial match)."""
  heading_lower = heading.lower()
  for s in _parse_cheatsheet_sections():
    if heading_lower in s["heading"].lower():
      return s
  return None


def search_cheatsheet(query: str) -> list[dict]:
  """Search cheatsheet sections for a keyword. Returns matching sections with snippets."""
  query_lower = query.lower()
  results = []
  for s in _parse_cheatsheet_sections():
    content_lower = s["content"].lower()
    if query_lower in s["heading"].lower() or query_lower in content_lower:
      # Extract a snippet around the first match
      idx = content_lower.find(query_lower)
      if idx >= 0:
        start = max(0, idx - 100)
        end = min(len(s["content"]), idx + len(query) + 200)
        snippet = s["content"][start:end]
      else:
        snippet = s["content"][:300]
      results.append({
        "heading": s["heading"],
        "snippet": snippet.strip(),
      })
  return results


def add_cheatsheet_entry(heading: str, content: str) -> str:
  """Append content under an existing H1 section, or create a new one. Returns status message."""
  if not CHEATSHEET_PATH.exists():
    return "Cheatsheet file not found"

  full_text = CHEATSHEET_PATH.read_text(encoding="utf-8")
  lines = full_text.split("\n")

  # Find the section by heading (outside code fences)
  in_fence = False
  # Track whether we're past front matter
  fm_count = 0
  section_start = None
  section_end = None

  for i, line in enumerate(lines):
    if line.strip() == "---":
      fm_count += 1
      continue
    if fm_count < 2:
      continue

    stripped = line.strip()
    if stripped.startswith("```"):
      in_fence = not in_fence
      continue

    if not in_fence and line.startswith("# ") and not line.startswith("## "):
      if section_start is not None:
        # We found the next H1 after our target — insert before it
        section_end = i
        break
      if heading.lower() in line[2:].strip().lower():
        section_start = i

  if section_start is not None:
    # Append to existing section
    insert_at = section_end if section_end is not None else len(lines)
    new_lines = lines[:insert_at] + ["", content, ""] + lines[insert_at:]
    CHEATSHEET_PATH.write_text("\n".join(new_lines), encoding="utf-8")
    return f"Appended content under '{heading}'"
  else:
    # Create new section at the end
    full_text = full_text.rstrip("\n") + f"\n\n# {heading}\n\n{content}\n"
    CHEATSHEET_PATH.write_text(full_text, encoding="utf-8")
    return f"Created new section '{heading}'"


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def read_page(name: str) -> Optional[dict]:
  """Read a page by name (without extension)."""
  for f in PAGES_DIR.glob("*.md"):
    if name.lower() in f.stem.lower():
      fm, body = _parse_file(f)
      return {"filename": f.name, "front_matter": fm, "content": body}
  return None


# ---------------------------------------------------------------------------
# Full-text search
# ---------------------------------------------------------------------------

def search_blog(query: str) -> list[dict]:
  """Full-text search across posts and cheatsheet. Returns matching snippets."""
  query_lower = query.lower()
  results = []

  # Search posts
  for f in sorted(POSTS_DIR.glob("*.md")):
    fm, body = _parse_file(f)
    text = (fm.get("title", "") + " " + body).lower()
    if query_lower in text:
      idx = text.find(query_lower)
      start = max(0, idx - 100)
      end = min(len(text), idx + len(query) + 200)
      # Use original case body for snippet
      full = fm.get("title", "") + " " + body
      snippet = full[start:end].strip()
      results.append({
        "source": "post",
        "filename": f.name,
        "title": fm.get("title", ""),
        "snippet": snippet,
      })

  # Search cheatsheet
  for match in search_cheatsheet(query):
    results.append({
      "source": "cheatsheet",
      "heading": match["heading"],
      "snippet": match["snippet"],
    })

  return results
