# tplr

Extremely simple, zero dependency Python package for template rendering.

## Example

`./content.txt`:

```
Hello {{ NAME }}!

<file src="./welcome.txt" />
```

`./welcome.txt`:

```
Welcome to `tplr`, bye now.
```

Command:

```
NAME=World tplr ./content.txt
```

Output:

```
Hello World!

Welcome to `tplr`, bye now.
```

## Motivation

There are countless templating libraries out there. But this one is mine. Also,
it meets the following criteria:

* Zero dependencies
* Extremely simple
* Installable via `pipx`
* Modern Python packaging style

## Installation

You can install the `tplr` CLI via `pipx`:

```bash
pipx install "git+https://github.com/owahltinez/tplr"
```

Alternatively, `tplr` can be used as a library. You may install it with `pip`:

```bash
python -m pip install "git+https://github.com/owahltinez/tplr"
```

## CLI Usage

Once installed via `pipx`, run it from your terminal using the `tplr` command:

```bash
tplr --help
```

Flags:
* `-f`, `--file`: Path to template file.
* `-o`, `--output`: Path to output file.
* `-e`, `--env`: Path to env file.
* `-k`, `--keep-tags`: Keep file content wrapped in `<file>` tags.

The template content might also be provided as a string via stdin.
If no output file is provided, the content will be sent to stdout.
A special value `-` can be used for the env file to use the shell's env vars.

## Library Usage

Once installed via `pip`, you can use the `process_template_content` function:

```python
import pathlib
import tplr

output = tplr.process_template_content(
    content="...",
    root_path=pathlib.Path(...),
    variables=dict(...),
    keep_tags=False,
)
```