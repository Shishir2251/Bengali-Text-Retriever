def clean_text(text):
    lines = text.split("\n")
    good = []
    for l in lines:
        if len(l) > 25 and "(ক)" not in l:
            good.append(l)
    return "\n".join(good)

raw = open("clean.txt",encoding="utf-8").read()
cleaned = clean_text(raw)
open("clean_final.txt","w",encoding="utf-8").write(cleaned)
