import requests, os, time
from bs4 import BeautifulSoup as bs

def nameChecker():
    url = f"https://www.hinatazaka46.com/s/official/diary/member?ima=0000"
    r = requests.get(url)
    s = bs(r.text, "html.parser")
    print("[Member's No] Name")
    for i in s.findAll("a", class_="p-blog-face__list"):
        ct = i["href"]
        name = i.text.strip()
        print(f"[{ct.split('ct=')[1]}] {name}")

def imgSaver():
    nameChecker()
    ct = input("Please choose member's No. >>> ")
    pageNo = 0
    os.makedirs(f"Folder Path/{ct}", exist_ok=True)
    if os.path.exists(f"Folder Path/{ct}/list.txt") == True:
        with open(f"Folder Path/{ct}/list.txt", "r") as f:
            img_list = f.readlines()
    else:
        with open(f"Folder Path/{ct}/list.txt", "w") as f:
            f.write("")
        with open(f"Folder Path/{ct}/list.txt", "r") as f:
            img_list = f.readlines()
    while True:
        url = f"https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&page={pageNo}&ct={ct}&cd=member"
        r = requests.get(url)
        s = bs(r.text, "html.parser")
        if s.findAll("div", class_="p-blog-group")[0].text.strip() == "記事がありません。":
            print("All images saved!")
            break
        else:
            img_facts = s.findAll("img")
            for img in img_facts:
                img_src = img["src"]
                if "https://cdn.hinatazaka46.com/files" and "/diary/official/member" in img_src:
                    img_name = img_src.split("/")[-1]
                    if img_name + "\n" in img_list:
                        print(f"[{img_name}] EXISTED!")
                    else:
                        img_src = requests.get(img_src)
                        with open(f"Folder Path/{ct}/{img_name}", "wb") as f:
                            f.write(img_src.content)
                        with open(f"Folder Path/{ct}/list.txt", "a") as f:
                            f.write(img_name + "\n")
                        print(f"[{img_name}] SAVED!")
                else:
                    pass
                time.sleep(0.1)
        pageNo += 1
        time.sleep(2)

imgSaver()