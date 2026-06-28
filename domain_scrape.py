import os
import sys
import asyncio
import json
import time
from core.engine import DomainScraperEngine

# Terminal ANSI Color Escape Constants (Crimson DedSec Theme)
C_RED   = "\033[31m"
C_BOLD  = "\033[1m"
C_CYAN  = "\033[96m"
C_GREEN = "\033[92m"
C_YEL   = "\033[93m"
C_WHITE = "\033[97m"
C_RESET = "\033[0m"

def print_dedsec_canvas():
    os.system("clear")
    print(f"{C_RED}{C_BOLD}")
    print(r"      __,_,  ")
    print(r"     [_|_/      < DomainScrapeX >  ")
    print(r"      // ")
    print(r"    _//    __ ")
    print(r"   (_|)   |@@|      << DEDSEC >> ")
    print(r"    \ \__ \--/ __  ")
    print(r"     \o__|----|  |   __")
    print(r"         \ }{ /\ )_ / _\ ")
    print(r"         /\__/\ \__O (__  <<Unknownx007>> ")
    print(r"        (--/\--)    \__/ ")
    print(r"        _)(  )(_     ")
    print(r"       `---''---`  ")
    print(f"                {C_WHITE}    [ D O M A I N   S C R A P E   X ]  ☠️")
    print(f"                [   PRODUCED BY DEVELOPER: Unknownx007   ]{C_RED}{C_BOLD}")
    print(f"================================================================================{C_RESET}")

async def main():
    print_dedsec_canvas()
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input(f"{C_WHITE}[+] Enter Target Corporate Domain URL to Profile (e.g., company.com): {C_RESET}").strip()
        
    if not target:
        print(f"{C_RED}[!] Error: No target domain address input found.{C_RESET}")
        return

    # Enforce formatting cleanup
    clean_domain = target.replace("http://", "").replace("https://", "").strip("/")
    
    print(f"\n{C_YEL}[*] Spawning asynchronous extraction threads core against target perimeter...{C_RESET}\n")
    time.sleep(1.0)

    # Initialize the Scraper Engine Core
    scraper = DomainScraperEngine(clean_domain)
    await scraper.execute_asynchronous_crawl_pipeline()

    # Save compiled intelligence profiles to disk natively
    json_out_path = f"db/intel_{clean_domain.replace('.', '_')}.json"
    serializable_intel = {
        "metadata": {
            "domain": clean_domain,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        },
        "emails": list(scraper.harvested_intel["emails"]),
        "phones": list(scraper.harvested_intel["phones"]),
        "social_links": list(scraper.harvested_intel["social_links"])
    }
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(serializable_intel, f, indent=4)

    # Output final classified footprint dashboard card
    print_dedsec_canvas()
    print(f"{C_WHITE}[✦] DEDSEC CLASSIFIED RECON DOSSIER PROFILE: {clean_domain.upper()}{C_RESET}")
    print(f"{C_WHITE}├── Local Target Database Extraction Backup Node: {json_out_path}{C_RESET}")
    print(f"{C_WHITE}├── Total System Map Links Audited and Parsed   : {len(scraper.visited_links)}{C_RESET}")
    print(f"{C_RED}================================================================================{C_RESET}")

    # 1. Output Harvested Emails Node Table
    print(f"\n{C_GREEN}[✦] HARVESTED IDENTITY COMMUNICATIONS AGENT LIST ({len(serializable_intel['emails'])} Items Uncovered):{C_RESET}\n")
    if not serializable_intel["emails"]:
        print(f"    {C_YEL}[-] Zero active corporate email communication anchors mapped.{C_RESET}")
    else:
        for email in sorted(serializable_intel["emails"]):
            print(f"    └── [EMAIL COORD] : {email}")

    # 2. Output Harvested Phone System Vectors
    print(f"\n{C_YEL}[✦] EXPOSED TELEPHONY ROUTING MATRIX PANELS ({len(serializable_intel['phones'])} Items Uncovered):{C_RESET}\n")
    if not serializable_intel["phones"]:
        print(f"    {C_YEL}[-] Zero direct telephone routing coordinates uncovered.{C_RESET}")
    else:
        for phone in sorted(serializable_intel["phones"]):
            print(f"    └── [TEL COORDINATE] : {phone}")

    # 3. Output Harvested Social Anchor Maps
    print(f"\n{C_CYAN}[✦] EXTRACTED EXECUTIVE SOCIAL FOOTPRINT LINKS ({len(serializable_intel['social_links'])} Items Uncovered):{C_RESET}\n")
    if not serializable_intel["social_links"]:
        print(f"    {C_YEL}[-] No external organizational profile channels mapped.{C_RESET}")
    else:
        for social in sorted(serializable_intel["social_links"]):
            print(f"    └── [SOCIAL ANCHOR] : {social}")

    print(f"\n{C_RED}================================================================================{C_RESET}")
    print(f"{C_GREEN}[✅] Operational intelligence gathering task successfully complete.{C_RESET}\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Operation aborted by user command interception.{C_RESET}\n")
