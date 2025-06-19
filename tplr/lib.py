import functools
import os
import pathlib
import re
import urllib.request


def load_env_file(file_path: str) -> dict[str, str]:
  # Special case: read from env vars.
  if file_path == "-":
    return dict(os.environ)
  # Otherwise, process it as a file path.
  pairs = []
  for line in open(file_path):
    pairs.append(line.split("=", 2))
  return dict(pairs)


def _replace_file_tag(
    match: re.match,
    root_path: pathlib.Path,
    variables: dict[str, str],
    keep_tags: bool,
) -> str:
  src = match.group(1)
  if src.startswith("http://") or src.startswith("https://"):
    # Fetch from network
    relpath = root_path
    with urllib.request.urlopen(src) as response:
      content = response.read().decode()
  else:
    # Read local file.
    resolved_path = (
        pathlib.Path(src)
        if pathlib.Path(src).is_absolute()
        else (root_path / src).resolve()
    )
    relpath = resolved_path.parent
    with open(resolved_path) as local_file:
      content = local_file.read()

  # If requested, wrap the content in HTML-like tags. Useful for LLMs.
  if keep_tags:
    content = f'<file src="{src}">\n{content}\n</file>'

  return process_template_content(
      content=content,
      root_path=relpath,
      variables=variables,
      keep_tags=keep_tags,
  )


def process_template_content(
    content: str,
    root_path: pathlib.Path | None = None,
    variables: dict[str, str] | None = None,
    keep_tags: bool = False,
) -> str:
  """
  Parses a text file, replacing `<file src="..." />` tags with the contents of
  the referenced files, and substituting `{{ variable }}` instances with the
  corresponding values from the environment variables.

  Args:
      content (str): Content with <file src="..." /> and {{ var }} references.
      root_path (pathlib.Path): Root directory to use for relative paths.
      variables (dict[str, str]): Variables to subtitute within the template.
      keep_tags (bool): Whether to keep the file content in a <file> tag.

  Returns:
      str: The parsed content string.
  """
  # Default values when not provided.
  root_path = root_path or pathlib.Path.cwd()
  variables = variables or dict()

  # Bake the arguments into the function that will be used for subtitution.
  re_fn = functools.partial(
      _replace_file_tag,
      root_path=root_path,
      variables=variables,
      keep_tags=keep_tags,
  )

  # Replace all the self-closing <file src="..." /> tags.
  content = re.sub(r"<file src=\"(.*?)\"\s?/>", re_fn, content)

  # Replace all the empty <file src="..."></file> tags.
  content = re.sub(r"<file src=\"(.*?)\"\s?>[\n\s]*</file>", re_fn, content)

  # Replace all instances of {{ variable }}.
  for key, val in variables.items():
    try:
      content = re.sub(r"{{\s?" + key + r"\s?}}", val, content)
    except re.PatternError:
      # Some env vars cannot be processed.
      pass

  return content
