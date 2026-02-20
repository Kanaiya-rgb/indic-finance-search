from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="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"
)

res = client.chat.completions.create(
    model="HuggingFaceH4/zephyr-7b-beta",
    messages=[{"role": "user", "content": "Hello"}]
)

print(res.choices[0].message.content)