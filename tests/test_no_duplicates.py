import re
from collections import Counter
from pathlib import Path


def test_no_tool_is_defined_twice():
    source = Path("nina_advanced_mcp/__init__.py").read_text()
    names = Counter(re.findall(r"^async def (nina_\w+)\(", source, flags=re.M))
    assert [n for n, c in names.items() if c > 1] == []
