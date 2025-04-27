from pathlib import Path
import sys
from anyascii import anyascii
from os import linesep


def normalize_text(text: str) -> tuple[str, list[str]]:
    changes = []

    new_text = ""
    lines = text.splitlines()
    for i in range(len(lines)):
        line = lines[i]

        for c in line:
            ascii_char = anyascii(c)
            if ascii_char != c:
                changes.append(f"Line - {i + 1}: {c} -> {ascii_char}")
                new_text += ascii_char
            else:
                new_text += c

        new_text += linesep

    return new_text, changes


def process_file(path: Path, file_type='py', dry_run: bool = False) -> bool:
    if not path.is_file() or path.suffix != f'.{file_type}':
        return False

    with path.open('r', encoding='utf-8', errors='ignore', newline='') as f:
        content = f.read()

    normalized_content, changes = normalize_text(content)

    if normalized_content != content:
        if changes:
            print(f"File: {path}")
            for change in changes:
                print(f"  {change}")
            print("=" * 30)

        if not dry_run:
            with path.open('w', encoding='utf-8', newline='') as f:
                f.write(normalized_content)

        return True
    return False


def process_directory(directory: Path, file_type='py', dry_run: bool = True) -> None:
    for path in directory.rglob('*.py'):
        process_file(path, file_type, dry_run)


if __name__ == '__main__':
    # Command line version
    # arg 1: folder of .py files
    # arg 2: dry run only

    # e.g. ascii_clean.py C:/temp/Code/src True


    directory = Path(sys.argv[1])
    dry_run = True
    if sys.argv[2].lower() == 'false':
        dry_run = False

    target_dir = Path(directory)
    process_directory(target_dir, file_type='py', dry_run=dry_run)

