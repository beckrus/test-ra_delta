import re


def get_missing_fk(err_text: str) -> str | None:
    key_pattern = "FOREIGN KEY \\(`(.*)`\\) "
    key_match = re.search(key_pattern, err_text)
    err_key = key_match.group(1) if key_match else None
    return err_key
