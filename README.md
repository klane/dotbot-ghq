# dotbot-ghq

Plugin for [`dotbot`](https://github.com/anishathalye/dotbot) to clone remote repositories with [`ghq`](https://github.com/motemen/ghq).

## Installation

1. Add `dotbot-ghq` as a submodule of your dotfiles repository.

```bash
git submodule add https://github.com/klane/dotbot-ghq.git
```

2. Modify your `install` script to enable the `ghq` plugin.

```bash
"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" --plugin-dir dotbot-ghq -c "${CONFIG}" "${@}"
```

## Usage

The plugin adds two new directives for use with `ghq`:

- `ghq`: List of repositories to clone with `ghq get`
- `ghqfile`: List of files containing repositories (one per line) to clone with `ghq get`

For example:

```yaml
- ghq:
  - anishathalye/dotbot
  - motemen/ghq
  - klane/dotbot-ghq

- ghqfile:
  - repos.txt
```

Flags for `ghq` can be passed with the `flags` keyword. When using this syntax, repositories must be specified with the `repo` keyword and files with the `file` keyword. For example:

```yaml
- ghq:
  - repo: anishathalye/dotbot
    flags: [--silent]
  - repo: motemen/ghq
    flags: [--update]
  - repo: klane/dotbot-ghq
    flags: [-p, --silent, --update]

- ghqfile:
  - file: repos.txt
    flags: [--silent]
```
