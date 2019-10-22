import re

import requests


def dump(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36"})
    data = r.text
    p_question = re.compile(r".*вопрос\s*(?:\d+)\s*\(вес.*%\)", re.I)
    matches = [e.span()[0] for e in p_question.finditer(data)] + [len(data)]
    questions = [data[matches[i]:matches[i + 1]] for i in range(len(matches) - 1)]
    p_qa_ok = re.compile(r".*вопрос\s*(?:\d+)\s*\(вес.*%\)\s+([^¢]+?)((?:\[(?:x|\s+)\]|\((?:x|\s+)\))[^¢]+?)балл: 100%", re.I)
    p_ans = re.compile(r"\[(?:x|\s+)\]|\((?:x|\s+)\)", re.I)
    db = []
    for qa in questions:
        m = p_qa_ok.match(qa)
        if m:
            q, a = m.groups()
            q = q.lower().strip().strip(":")
            q = re.sub(r'\(выб.+?ответа\)|блок "тем[аы]: ?.+?"', "", q)
            q = re.sub(r"\s+", " ", q).strip()
            
            matches = [e.span()[0] for e in p_ans.finditer(a)] + [len(a)]
            answers = [a[matches[i]:matches[i + 1]] for i in range(len(matches) - 1)]

            def normalize(ans):
                ans = ans[3:].lower()
                ans = re.sub(r"<-\s+?правильный\s+ответ[^¢]*", "", ans)
                ans = re.sub(r"\s+", " ", ans)
                ans = re.sub(r"^ *[абвгде123456]\)", "", ans).strip().rstrip(".")
                return ans

            a_ok = [normalize(ans) for ans in answers if ans[1] == "x"]
            db.append((q, a_ok))
    return db

tests_2016_2018 = [
"https://pastebin.com/raw/46mVzekA",
"https://pastebin.com/raw/ds4q7t8q",
"https://pastebin.com/raw/BzUS80wC",
"https://pastebin.com/raw/LSzPTN1Z",
"https://pastebin.com/raw/URV9KhSU",
"https://pastebin.com/raw/a3RheFB3",
"https://pastebin.com/raw/CCyteWTj",
"https://pastebin.com/raw/L3RR404a",
"https://pastebin.com/raw/bTDZA8j3",
"https://pastebin.com/raw/zHukgLvM",
"https://pastebin.com/raw/fuZwY7p0",
"https://pastebin.com/raw/KvcDBNvw",
"https://pastebin.com/raw/N8bgfr2G",
"https://pastebin.com/raw/9CTGmqAY",
"https://pastebin.com/raw/zdGtWF9C",
"https://pastebin.com/raw/LSZZeBqZ",
"https://pastebin.com/raw/aAKWW6Tu",
"https://pastebin.com/raw/0WmmrAKM",
"https://pastebin.com/raw/7xhKL2tv",
"https://pastebin.com/raw/uu2nYUmE",
"https://pastebin.com/raw/Z2FTr78A",
"https://pastebin.com/raw/zaPaX0jr",
"https://pastebin.com/raw/nqyMfBNq",
"https://pastebin.com/raw/6L1hBUe4",
"https://pastebin.com/raw/b6NigW22",
"https://pastebin.com/raw/9YdBZVpd",
"https://raw.githubusercontent.com/serjtroshin/main/master/examall"
]

tests_2019 = [
"https://pastebin.com/raw/K6RYMPGB",
"https://pastebin.com/raw/R1DKuUA9",
"https://pastebin.com/raw/r50rrucK",
"https://pastebin.com/raw/PbnKpTQ2",
"https://pastebin.com/raw/2Ukazs9C",
"https://pastebin.com/raw/ks4g7hKb",
"https://pastebin.com/raw/bDsWNKQV",
"https://pastebin.com/raw/xEa8G1cH",
"https://pastebin.com/raw/rAkfUhhM",
"https://pastebin.com/raw/AjW29ueU",
"https://pastebin.com/raw/fvzirynx",
"https://pastebin.com/raw/qNAnVg0g",
"https://pastebin.com/raw/piLG8dvf",
"https://pastebin.com/raw/0pFbyfY9",
"https://pastebin.com/raw/zHsKEYhB",
"https://pastebin.com/raw/Y2LKwR2F",
]

urls = tests_2019

db = {}
unsure = {}
for url in urls:
    part = dump(url)
    for k, v_ in part:
        v = sorted(v_)
        if k not in db:
            if k not in unsure:
                db[k] = v
            elif v not in unsure[k]:
                unsure[k].append(v)
        else:
            if v != db[k]:
                unsure[k] = [db[k], v]
                print("CONFLICT")
                print(k)
                print(db[k])
                print(v)
                del db[k]

print("{} questions ok, {} with different answers".format(len(db), len(unsure)))

data = []
for k, v in db.items():
    data.append("{}\n\n{}\n".format(k, "\n".join(v)))
data = ("-" * 30 + "\n").join(data)

data2 = []
for k, v in unsure.items():
    data2.append("{}\n\n{}\n".format(k, "\n\n".join(["\n".join(e) for e in v])))
data2 = ("-" * 30 + "\n").join(data2)

with open("dump.txt", "w") as f:
    f.write(data)
with open("dump2.txt", "w") as f:
    f.write(data2)
