import json
import os
import re
import requests
from config import OLLAMA_CHAT_URL, OLLAMA_CHAT_MODEL

FACTS_FILE = "facts.json"
HISTORY_FILE = "conversation_history.json"
SUMMARY_FILE = "summary.json"
MAX_HISTORY = 20
SUMMARY_TRIGGER = 40


# ─────────────────────────────────────────
# L0 — 팩트 DB (영구 사실 저장)
# ─────────────────────────────────────────

def load_facts() -> dict:
    if os.path.exists(FACTS_FILE):
        try:
            with open(FACTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_facts(facts: dict):
    try:
        with open(FACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(facts, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ 팩트 저장 실패: {e}")

def extract_and_save_facts(user_text: str, rua_text: str):
    facts = load_facts()
    changed = False

    # 이름 패턴
    name_match = re.search(r'내\s*이름은\s*([가-힣a-zA-Z0-9_]{2,})', user_text)
    if not name_match:
        name_match = re.search(r'([가-힣a-zA-Z0-9_]{2,})(?:라고|이라고)\s*불러', user_text)
    if name_match:
        name = name_match.group(1).strip()
        name = re.sub(r'(?:야|이야|이에요|예요|입니다|이라고|라고)$', '', name).strip()
        if len(name) >= 2:
            facts["주인님_이름"] = name
            print(f"💾 팩트 저장: 주인님 이름 = {name}")
            changed = True

    # 직업 패턴
    job_match = re.search(
        r'(?:나는|저는)\s*(.+?)\s*(?:개발자|학생|직장인|디자이너|엔지니어)',
        user_text
    )
    if job_match:
        facts["주인님_직업"] = job_match.group(0).strip()
        print(f"💾 팩트 저장: 직업 정보")
        changed = True

    # 좋아하는 것 — "나는 XXX 좋아해" or "XXX 좋아해"
    like_match = re.search(
        r'(?:나는|저는)?\s*([가-힣a-zA-Z0-9\s]+?)\s*(?:을|를)?\s*좋아(?:해|함|한다)',
        user_text
    )
    if like_match:
        item = like_match.group(1).strip()
        # 앞에 붙은 "나는", "저는" 제거
        item = re.sub(r'^(?:나는|저는)\s*', '', item).strip()
        # "것을", "걸" 같은 후치사 제거
        item = re.sub(r'\s*(?:것을|걸|를|을)$', '', item).strip()
        if len(item) >= 2:
            likes = facts.get("주인님_좋아하는것", [])
            if item not in likes:
                likes.append(item)
                facts["주인님_좋아하는것"] = likes[-5:]
                print(f"💾 팩트 저장: 좋아하는 것 = {item}")
                changed = True

    # 싫어하는 것
    dislike_match = re.search(
        r'(?:나는|저는)?\s*([가-힣a-zA-Z0-9\s]+?)\s*(?:을|를)?\s*(?:싫어해|싫어함|싫어한다|못 먹어|못먹어)',
        user_text
    )
    if dislike_match:
        item = dislike_match.group(1).strip()
        item = re.sub(r'^(?:나는|저는)\s*', '', item).strip()
        item = re.sub(r'\s*(?:것을|걸|를|을)$', '', item).strip()
        if len(item) >= 2:
            dislikes = facts.get("주인님_싫어하는것", [])
            if item not in dislikes:
                dislikes.append(item)
                facts["주인님_싫어하는것"] = dislikes[-5:]
                print(f"💾 팩트 저장: 싫어하는 것 = {item}")
                changed = True

    if changed:
        save_facts(facts)

def build_facts_context() -> str:
    facts = load_facts()
    if not facts:
        return ""
    lines = ["[류아가 반드시 기억하고 활용해야 할 주인님에 대한 사실 — 대화에서 자연스럽게 녹여 쓸 것]"]
    for key, value in facts.items():
        if isinstance(value, list):
            lines.append(f"- {key}: {', '.join(value)}")
        else:
            lines.append(f"- {key}: {value}")
    return "\n".join(lines)


# ─────────────────────────────────────────
# L1 — 슬라이딩 윈도우 (단기 대화 기록)
# ─────────────────────────────────────────

def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"📖 대화 기록 불러옴 ({len(data)}개)")
                return data
        except:
            return []
    return []

def save_history(history: list):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history[-(MAX_HISTORY * 2):], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ 대화 기록 저장 실패: {e}")

def build_history_context(history: list, n: int = 10) -> str:
    recent = history[-(n * 2):]
    return "\n".join([
        f"{'주인님' if m['role'] == 'user' else '류아'}: {m['content']}"
        for m in recent
    ])


# ─────────────────────────────────────────
# L2 — 에피소딕 메모리 (LLM 요약 압축)
# ─────────────────────────────────────────

def load_summary() -> str:
    if os.path.exists(SUMMARY_FILE):
        try:
            with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("summary", "")
        except:
            return ""
    return ""

def save_summary(summary: str):
    try:
        with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
            json.dump({"summary": summary}, f, ensure_ascii=False, indent=2)
        print(f"📝 요약 저장 완료")
    except Exception as e:
        print(f"❌ 요약 저장 실패: {e}")

def compress_history(history: list) -> list:
    if len(history) < SUMMARY_TRIGGER:
        return history

    print(f"🗜️ 대화 압축 시작 ({len(history)}개)")

    old_count = len(history) - MAX_HISTORY * 2
    old_messages = history[:old_count]
    recent_messages = history[old_count:]

    existing_summary = load_summary()

    old_str = "\n".join([
        f"{'주인님' if m['role'] == 'user' else '류아'}: {m['content']}"
        for m in old_messages
    ])

    if existing_summary:
        prompt = (
            f"기존 요약:\n{existing_summary}\n\n"
            f"추가 대화:\n{old_str}\n\n"
            "규칙:\n"
            "1. 대화에서 실제로 언급된 사실만 써라\n"
            "2. 없는 내용 절대 지어내지 마라\n"
            "3. 주인님이 말한 정보(이름, 취향, 상황)와 류아의 반응만\n"
            "4. 3문장 이내\n"
            "5. '~했습니다' 체로 간결하게\n"
            "요약:"
        )
    else:
        prompt = (
            f"대화:\n{old_str}\n\n"
            "규칙:\n"
            "1. 대화에서 실제로 언급된 사실만 써라\n"
            "2. 없는 내용 절대 지어내지 마라\n"
            "3. 주인님이 말한 정보(이름, 취향, 상황)와 류아의 반응만\n"
            "4. 3문장 이내\n"
            "5. '~했습니다' 체로 간결하게\n"
            "요약:"
        )

    payload = {
        "model": OLLAMA_CHAT_MODEL,
        "system": (
            "너는 대화 요약 전문가야. "
            "대화에 실제로 등장한 내용만 사실 그대로 요약해. "
            "절대 없는 내용을 지어내거나 감정을 과장하지 마. "
            "3문장 이내로 짧게."
        ),
        "prompt": prompt,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=30)
        new_summary = res.json().get("response", "").strip()
        # "요약:" 접두어 제거
        new_summary = re.sub(r'^요약\s*[:：]\s*', '', new_summary).strip()
        if new_summary:
            save_summary(new_summary)
            print(f"📝 요약 내용: {new_summary[:80]}...")
    except Exception as e:
        print(f"❌ 요약 실패: {e}")

    return recent_messages

def build_summary_context() -> str:
    summary = load_summary()
    if not summary:
        return ""
    return f"[이전 대화 요약 — 류아가 기억하는 과거]\n{summary}"


# ─────────────────────────────────────────
# 통합 컨텍스트 빌드
# ─────────────────────────────────────────

def build_full_context(history: list) -> str:
    parts = []

    facts_ctx = build_facts_context()
    if facts_ctx:
        parts.append(facts_ctx)

    summary_ctx = build_summary_context()
    if summary_ctx:
        parts.append(summary_ctx)

    history_ctx = build_history_context(history)
    if history_ctx:
        parts.append(f"[최근 대화]\n{history_ctx}")

    return "\n\n".join(parts)