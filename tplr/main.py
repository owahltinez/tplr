import pathlib
import sys
import argparse
from . import lib as tplr


def main():
  desc = "Parse content with file inclusions and env var expansion."
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument("-f", "--file", help="Path to template file.")
  parser.add_argument("-o", "--output", help="Path to output file.")
  parser.add_argument("-e", "--env", help="Path to env file.")
  parser.add_argument(
    "-k",
    "--keep-tags",
    help="Keep file content wrapped in <file> tags.",
    action='store_true',
  )
  args = parser.parse_args()

  # Read the input template.
  if args.file:
    root_path = pathlib.Path(args.file).parent
    with open(args.file) as f:
      content = f.read()
  else:
    root_path = pathlib.Path(__file__).parent
    content = sys.stdin.read()

  # Process the content.
  content = tplr.process_template_content(
    content=content,
    root_path=root_path,
    variables=tplr.load_env_file(args.env) if args.env else None,
    keep_tags=args.tag,
  )

  # Output to file or stdout.
  if args.output and args.output != '-':
    with open(args.output, 'w') as fh:
      fh.write(content)
  else:
    print(content)


if __name__ == '__main__':
  main()
