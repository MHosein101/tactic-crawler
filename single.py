import requests, os, re
from bs4 import BeautifulSoup

print("# START CRAWLING #")

base_url = "http://wtharvey.com"

page = requests.get(f"{base_url}/index.html")
html = BeautifulSoup(page.content, 'html.parser')

print("# MAIN PAGE DOWNLOADED #")

anchors = html.find_all('a')

if not os.path.exists("output"):
    os.makedirs("output")

print("# PROCESSING SUB LINKS #")

el = len(os.listdir("output"))
i = el+1

for a in anchors[18+el:len(anchors)-110]:

    if re.match(r"[\w]+\.html", a.get('href')):

        try:
            p = requests.get(f"{base_url}/{a.get('href')}")
            c = BeautifulSoup(p.content, 'html.parser')

            text = c.get_text().strip()
            text = text.replace("\r", "")
            text = text.split("\n")

            del text[-2:]
            while not text[0].startswith("a)"):
                del text[0]

            _i = 0
            while _i < len(text):
                if text[_i] != "":
                    text[_i] = re.sub(r"[a-z]\) ", "", text[_i])
                    text[_i] = text[_i].replace("[","\n[")
                    r = re.search(r"[0-9]{4}", text[_i])
                    if r is not None:
                        text[_i] = text[_i].replace( r.group() ,f"{r.group()}\n")
                    _i += 1
                else:
                    del text[_i]

            _i = 0
            while _i < len(text):
                if len(text[_i].split("\n")) == 3:
                    _i += 1
                else:
                    del text[_i]

            text = "\n*****\n".join(s.strip() for s in text)

            file = open(os.path.join("output", f"{i} {a.text.strip()}.txt"), 'w')
            file.write(text)
            file.close()

            print(f"# {i} LINK {base_url}/{a.get('href')} SAVED #")
            i += 1
        except:
            pass

print("# FINISHED #")
