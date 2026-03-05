[![Jekyll site CI](https://github.com/j1v37u2k3y/j1v37u2k3y.github.io/actions/workflows/jekyll.yml/badge.svg?branch=master)](https://github.com/j1v37u2k3y/j1v37u2k3y.github.io/actions)

# j1v37u2k3y.github.io

Personal security blog hosted at [jiveturkey.rocks](https://jiveturkey.rocks). Focused on offensive security, penetration testing writeups, and cybersecurity education.

## Content

- **Hack The Box & VulnHub writeups** - Walkthroughs of vulnerable machines
- **SANS Holiday Hack Challenge** - CTF challenge solutions
- **Security cheatsheets** - Reverse shells, file transfers, enumeration techniques
- **Tools & tutorials** - HTTP servers, nmap reporting, code snippets

## Tech Stack

- [Jekyll](https://jekyllrb.com/) static site generator
- [Minima](https://github.com/jekyll/minima) theme
- Hosted on [GitHub Pages](https://pages.github.com/)

## Local Development

### Docker (recommended)

Requires [Docker](https://docs.docker.com/get-docker/).

```sh
make serve
```

This builds the Docker image, installs all dependencies, and starts a local dev server with live reload and drafts enabled.

Open [http://localhost:4000](http://localhost:4000).

| Command | Description |
|---|---|
| `make serve` | Build and start the dev server |
| `make up` | Start in detached (background) mode |
| `make down` | Stop the running containers |
| `make logs` | Tail logs from a detached container |
| `make clean` | Remove containers, volumes, and generated files |

### Without Docker

Requires Ruby and Bundler.

```sh
script/bootstrap   # install dependencies
script/server      # start dev server
script/build       # production build
```

Open [http://localhost:4000](http://localhost:4000).

## License

[MIT](LICENSE)