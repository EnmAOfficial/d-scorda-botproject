def build_messages(user_message: str):
    return [
        {
            "role": "system",
            "content": (
                "Sen profesyonel bir Discord yapay zeka asistanısın. "
                "Kısa, net ve doğru cevaplar ver."
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
