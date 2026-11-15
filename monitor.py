import os, re, json, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import requests

ROOT = Path(__file__).parent
BLOCK_TERMS = [
    "internet positif", "trustpositif", "nawala", "akses diblokir",
    "situs diblokir", "website blocked", "this site has been blocked",
    "kominfo", "komdigi"
]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; LinkMonitor/1.0; +https://github.com/)"}

def read_links():
    out=[]
    for line in (ROOT/"links.txt").read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if not line or line.startswith("#"): continue
        if not re.match(r"^https?://", line, re.I): line="https://"+line
        if line not in out: out.append(line)
    return out

def check(url):
    started=time.monotonic()
    now=datetime.now(timezone.utc).isoformat()
    try:
        p=urlparse(url)
        if p.scheme not in ("http","https") or not p.netloc:
            raise ValueError("URL tidak valid")
        response=requests.get(url,headers=HEADERS,timeout=(8,18),allow_redirects=True)
        elapsed=round((time.monotonic()-started)*1000)
        body=(response.text or "")[:500000].lower()
        title_match=re.search(r"<title[^>]*>(.*?)</title>",body,re.I|re.S)
        title=re.sub(r"\s+"," ",title_match.group(1)).strip()[:180] if title_match else ""
        hits=[term for term in BLOCK_TERMS if term in body]
        # Kata kunci saja adalah sinyal lemah; tandai sebagai indikasi agar diverifikasi.
        if hits:
            status="suspected_block"
            note="Teks halaman memuat kata: "+", ".join(hits[:4])
        elif response.status_code >= 500:
            status="unreachable"; note="Server mengembalikan HTTP "+str(response.status_code)
        elif response.status_code in (401,403,407,451):
            status="suspected_block"; note="Respons HTTP "+str(response.status_code)+"; perlu verifikasi manual"
        elif response.status_code >= 400:
            status="unreachable"; note="HTTP "+str(response.status_code)
        else:
            status="normal"; note="Halaman merespons; bukan jaminan bebas blokir di semua jaringan"
        return {"url":url,"status":status,"http_status":response.status_code,
                "response_ms":elapsed,"checked_at":now,"final_url":response.url,
                "title":title,"note":note}
    except requests.RequestException as e:
        return {"url":url,"status":"unreachable","http_status":None,
                "response_ms":round((time.monotonic()-started)*1000),
                "checked_at":now,"note":type(e).__name__+": "+str(e)[:180]}
    except Exception as e:
        return {"url":url,"status":"error","http_status":None,
                "response_ms":None,"checked_at":now,"note":str(e)[:180]}

def telegram(message):
    token=os.getenv("TELEGRAM_BOT_TOKEN")
    chat=os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat: return
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
          data={"chat_id":chat,"text":message},timeout=15).raise_for_status()
    except Exception as e:
        print("Telegram notification failed:",e)

def main():
    links=read_links()
    results=[check(url) for url in links]
    report={"checked_at":datetime.now(timezone.utc).isoformat(),
            "count":len(results),"results":results}
    (ROOT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    suspect=[x for x in results if x["status"]=="suspected_block"]
    failed=[x for x in results if x["status"] in ("unreachable","error")]
    print(f"Checked {len(results)} links; suspected={len(suspect)}, failed={len(failed)}")
    if suspect or failed:
        lines=["NAWALA LINK MONITOR","Indikasi pemblokiran / gangguan terdeteksi:"]
        for x in (suspect+failed)[:35]:
            lines.append(f'- {x["url"]}: {x["status"]} — {x["note"]}')
        lines.append("Catatan: hasil otomatis perlu diverifikasi manual.")
        telegram("\n".join(lines))

if __name__=="__main__": main()
