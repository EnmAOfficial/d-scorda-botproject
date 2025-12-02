import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def _read_file(relative_path: str) -> str:
    path = os.path.join(BASE_DIR, relative_path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[WARN] Dosya bulunamadı: {path}")
        return ""
    except Exception as e:
        print(f"[ERROR] Dosya okunamadı ({path}): {e}")
        return ""


def build_messages(user_message: str):
    system_prompt = _read_file("ai/system_prompt.txt")
    knowledge_base = _read_file("ai/knowledge_base.txt")

    system_full = system_prompt.strip()

    if knowledge_base.strip():
        system_full += "\n\n---\nKnowledge Base:\n" + knowledge_base.strip()

    return [
        {"role": "system", "content": system_full},
        {"role": "user", "content": user_message},
    ]
