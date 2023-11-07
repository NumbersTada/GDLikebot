print("GDLikebot - Comment Like/Dislike Bot")

import requests,random,base64,itertools,hashlib,threading,time,sys,os
from string import ascii_letters, digits

possibleLetters = ascii_letters + digits

args=sys.argv

if len(args) != 4:
    print("Usage: "+__file__.split(os.getcwd()+"\\")[1]+" <COMMENTID> <LEVELID> <TYPE>\nType: 1 for like, 0 for dislike")
    exit()
    
comid = int(args[1])
levelid = int(args[2])
liketype = int(args[3])

def readProxies(file):
    with open(file,"r") as file:
        proxies = [line.strip() for line in file]
    return proxies

def randomProxy(proxies):
    return random.choice(proxies)

proxies = readProxies("proxies.txt")

def readAccounts(filePath):
    gjuser = []
    gjpass = []
    gjaccid = []
    with open(filePath,"r") as file:
        for line in file:
            user,passw,accid = line.strip().split(";")
            gjuser.append(user)
            gjpass.append(passw)
            gjaccid.append(accid)
    return gjuser,gjpass,gjaccid

gjuser,gjpass,gjaccid = readAccounts("accounts.txt")

def xor(data, key):
    return "".join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, itertools.cycle(key)))

def gjpEncrypt(data):
    return base64.b64encode(xor(data,"37526").encode()).decode()

def chk(values: [int, str] = [], key: str = "", salt: str = "") -> str:
    values.append(salt)
    string = ("").join(map(str, values))
    hashed = hashlib.sha1(string.encode()).hexdigest()
    xored = xor(hashed, key)
    final = base64.urlsafe_b64encode(xored.encode()).decode()
    return final

def rs(n: int) -> str:
    return ("").join(random.choices(possibleLetters, k=n))

def uuid(parts: [int] = (8, 4, 4, 4, 10)) -> str:
    return ("-").join(map(rs, parts))

def udid(start: int = 100_000, end: int = 100_000_000) -> str:
    return "S" + str(random.randint(start, end))

def bot(proxy):
    rand = random.randint(0, len(gjuser) - 1)
    guuid = uuid()
    gudid = udid()
    grs = rs(10)
    data = {
        "gameVersion": "21",
        "binaryVersion": "35",
        "gdw": "0",
        "accountID": gjaccid[rand],
        "gjp": gjpEncrypt(gjpass[rand]),
        "udid": gudid,
        "uuid": guuid,
        "itemID": comid,
        "like": liketype,
        "type": "2",
        "secret": "Wmfd2893gb7",
        "special": levelid,
        "rs": grs,
        "chk": chk([levelid,comid,liketype,"2",grs,gjaccid[rand],gudid,guuid], "58281", "ysg6pUrtjn0J")
    }
    try:
      req = requests.post("http://www.boomlings.com/database/likeGJItem211.php", data=data, headers={"User-Agent": ""}, proxies=proxy)
      if req.text == "1":
          print(f"[SUCCESS]: {str(gjuser[rand])}")
      else:
          errorKeywords = ["</","Cloudflare","error code:","nginx","apache"]
          if any(keyword in req.text for keyword in errorKeywords):
              pass
          else:
              print(f"[ERROR]:   {str(gjuser[rand])} - {req.text}")
    except:
      pass

while True:
  try:
    proxy = {"http":randomProxy(proxies),"https":randomProxy(proxies)}
    threading.Thread(target=bot,args=(proxy,)).start()
  except:
    pass
