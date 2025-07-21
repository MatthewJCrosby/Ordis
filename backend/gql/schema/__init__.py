from pathlib import Path
# loads all resolver files dynamically at runtime
def load_type_defs():
    base = Path(__file__).parent
    parts = sorted(base.glob("*.graphql"))
    return "\n".join(p.read_text() for p in parts)
