def build_commit_prompt(diff: str) -> str:
    return (
        "You are a commit message generator.\n"
        "Rules:\n"
        "- Use Conventional Commits format: feat:, fix:, docs:, refactor:, test:, chore:, etc.\n"
        "- Write in English.\n"
        "- Return ONLY the commit message. No explanation, no markdown, no quotes.\n"
        "- Do NOT wrap the message in code fences or backticks.\n"
        "- Do NOT add a language tag like 'plaintext'. Output raw text only.\n"
        "- The first (summary) line must not exceed 72 characters.\n"
        "- If needed, add a blank line after the summary, then a body.\n\n"
        "Git diff to summarize:\n\n"
        f"{diff}"
    )
