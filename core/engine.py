import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib3

# Suppress unverified HTTPS warning logs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DomainScraperEngine:
    def __init__(self, target_url: str):
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            self.base_url = f"https://{target_url}"
        else:
            self.base_url = target_url
            
        self.domain = urlparse(self.base_url).netloc
        self.visited_links = set()
        self.links_to_crawl = set() # FIXED: Dropped all static hardcoded college/school fallback seeds
        self.max_crawl_pages = 40  # Hard operational safety perimeter boundary
        
        # HIGH-COMPLIANCE GLOBAL REGEX EXTRACTORS
        self.email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        
        # UNIVERSAL INTERNATION TELEPHONY REGEX: Matches real global phone formats while discarding layout noise coords
        self.phone_regex = re.compile(r'\b(?:\+?\d{1,3}[-\s.]?)?\(?\d{2,4}\)?[-\s.]?\d{3,4}[-\s.]?\d{4,6}\b')
        self.social_keywords = ["linkedin.com", "twitter.com", "x.com", "facebook.com", "instagram.com", "youtube.com", "github.com", "tiktok.com"]

        self.harvested_intel = {
            "emails": set(),
            "phones": set(),
            "social_links": set()
        }
        
        # Establish a high-reputation web browser session handler
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        })

    def fetch_page_html_sync(self, url: str) -> str:
        """Fires a high-compliance browser-masked handshake to pull full text source bytes."""
        try:
            res = self.session.get(url, timeout=7, verify=False, allow_redirects=True)
            if res.status_code == 200:
                return res.text
        except Exception:
            pass
        return ""

    def parse_and_extract_intel(self, html_content: str, current_url: str):
        if not html_content:
            return

        # 1. High-Precision Email Processing Core
        emails_found = self.email_regex.findall(html_content)
        for email in emails_found:
            clean_email = email.strip().lower()
            if not clean_email.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.css', '.js', '.ico', '.woff')):
                if clean_email not in self.harvested_intel["emails"]:
                    self.harvested_intel["emails"].add(clean_email)
                    print(f"\033[92m[⚡ EMAIL FOUND] {clean_email}\033[0m")

        # 2. High-Precision Telephony Routing Intercept
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract dedicated tel links out of raw HTML attributes natively
            for tel_link in soup.find_all('a', href=True):
                if tel_link['href'].startswith('tel:'):
                    raw_tel = tel_link['href'].replace('tel:', '').strip()
                    if len(raw_tel) >= 7 and not raw_tel.startswith('-'):
                        if raw_tel not in self.harvested_intel["phones"]:
                            self.harvested_intel["phones"].add(raw_tel)
                            print(f"\033[93m[⚡ PHONE FOUND VIA TEL-LINK] {raw_tel}\033[0m")

            # Fallback text matrix scanning loop
            text_content = soup.get_text()
            phones_found = self.phone_regex.findall(text_content)
            for phone in phones_found:
                clean_phone = phone.strip()
                # Clean out punctuation artifacts from broad regex lookups
                clean_phone = re.sub(r'[^\d\+\-\(\)\s]', '', clean_phone).strip()
                if not clean_phone.startswith(('-', '.', '000', '12345')) and len(re.sub(r'\D', '', clean_phone)) >= 9:
                    if clean_phone not in self.harvested_intel["phones"]:
                        self.harvested_intel["phones"].add(clean_phone)
                        print(f"\033[93m[⚡ PHONE FOUND] {clean_phone}\033[0m")
        except Exception:
            pass

        # 3. Secure Social Media Extraction & Recursive Dynamic Link Discovery
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            for anchor in soup.find_all('a', href=True):
                href = anchor['href'].strip()
                if not href or href.startswith(('javascript:', '#', 'mailto:', 'tel:')):
                    continue
                    
                absolute_url = urljoin(current_url, href)
                parsed_abs = urlparse(absolute_url)

                # Match for explicit corporate social assets links profiles
                if any(keyword in absolute_url.lower() for keyword in self.social_keywords):
                    if "profile.php" in absolute_url or "watch" in absolute_url or "channel" in absolute_url:
                        clean_social = absolute_url.split('&extid=')[0].split('&mibextid=')[0].rstrip('/')
                    else:
                        clean_social = absolute_url.split('?')[0].rstrip('/')
                        
                    if len(clean_social) > 15:
                        if clean_social not in self.harvested_intel["social_links"]:
                            self.harvested_intel["social_links"].add(clean_social)
                            print(f"\033[96m[⚡ SOCIAL CONNECTION MATCH] {clean_social}\033[0m")
                    continue

                # FIXED: Pure dynamic crawler discovery. Explores internal page mappings on the fly
                if self.domain in parsed_abs.netloc and absolute_url not in self.visited_links:
                    if len(self.links_to_crawl) + len(self.visited_links) < self.max_crawl_pages:
                        self.links_to_crawl.add(absolute_url)
        except Exception:
            pass

    async def execute_asynchronous_crawl_pipeline(self):
        """Processes the link-harvesting post queue dynamically using browser-masked operations."""
        print(f"\033[34m[*] Seeding framework looppost via target homepage discovery pass... \033[0m")
        
        # Seed Phase: Read the home index page to dynamically harvest the true target link mappings tree
        initial_html = self.fetch_page_html_sync(self.base_url)
        if not initial_html:
            print(f"\033[31m[!] Critical Error: Target root connection rejected. WAF block suspected.\033[0m")
            return
            
        # Parse homepage layout metrics to find actual structural internal directories links
        self.visited_links.add(self.base_url)
        self.parse_and_extract_intel(initial_html, self.base_url)

        # Loop through the dynamically discovered link paths queue
        while self.links_to_crawl and len(self.visited_links) < self.max_crawl_pages:
            url = self.links_to_crawl.pop()
            if url in self.visited_links:
                continue
                
            self.visited_links.add(url)
            print(f"\033[90m[CRAWLING INTERFACE] Analyzing node assets path: {url}\033[0m")
            
            html = self.fetch_page_html_sync(url)
            if html:
                self.parse_and_extract_intel(html, url)
                
            time.sleep(0.2)
