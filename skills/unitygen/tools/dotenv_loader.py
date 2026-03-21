from pathlib import Path


def load_dotenv_from_tree():
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    start = Path.cwd().resolve()
    chain = [start]
    chain.extend(list(start.parents)[:16])
    for d in chain:
        p = d / ".env"
        if p.is_file():
            load_dotenv(p, override=False)
            return
