with open("data.json", "r", encoding="utf-8-sig") as f:
    data = f.read()

with open("data_clean.json", "w", encoding="utf-8") as f:
    f.write(data)