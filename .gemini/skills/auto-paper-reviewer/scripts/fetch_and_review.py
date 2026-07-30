import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from google import genai
from bs4 import BeautifulSoup

# --- Configuration ---
SEARCH_QUERY = 'all: "Large Language Models" OR all: "LLM"'
MAX_RESULTS = 10
TOP_INSTITUTIONS = [
    'Google', 'DeepMind', 'OpenAI', 'Meta', 'Facebook', 'Microsoft', 
    'Anthropic', 'Mistral', 'Stanford', 'MIT', 'Berkeley', 
    'Carnegie Mellon', 'Harvard', 'Princeton', 'Oxford', 'Cambridge', 
    'Tsinghua', 'Peking'
]
TOP_CONFERENCES = ['NeurIPS', 'ACL', 'EMNLP', 'ICLR', 'ICML', 'CVPR', 'AAAI', 'IJCAI', 'NAACL', 'KDD', 'SIGIR']

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REPO_ROOT = Path(__file__).resolve().parents[4]
TARGET_DIR = REPO_ROOT / "_posts"
TEMPLATE_PATH = REPO_ROOT / ".gemini/skills/auto-paper-reviewer/assets/templates/paper-review-template.md"

# --- Functions ---

def fetch_arxiv_papers(query, max_results=10):
    url = f'https://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending'
    response = requests.get(url, timeout=30)
    if response.status_code != 200:
        print(f"Error fetching from arXiv: {response.status_code}")
        return []
    
    root = ET.fromstring(response.content)
    papers = []
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
    
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
        published = entry.find('atom:published', ns).text
        link = entry.find("atom:link[@title='pdf']", ns)
        pdf_url = link.attrib['href'] if link is not None else entry.find('atom:id', ns).text
        
        comment = entry.find('arxiv:comment', ns)
        comment_text = comment.text if comment is not None else ""
        
        papers.append({
            'title': title,
            'summary': summary,
            'authors': authors,
            'published': published,
            'pdf_url': pdf_url,
            'comment': comment_text
        })
    return papers

def get_arxiv_image_url(pdf_url):
    # Convert PDF URL to HTML URL (arXiv feature)
    html_url = pdf_url.replace('/pdf/', '/html/').replace('.pdf', '')
    try:
        response = requests.get(html_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            imgs = soup.find_all('img')
            for img in imgs:
                src = img.get('src', '')
                alt = img.get('alt', '').lower()
                # Heuristic: Figure 1 or Architecture is often the most important
                if 'fig' in alt or 'arch' in alt or '1' in alt:
                    if src.startswith('http'):
                        return src
                    else:
                        # Construct absolute URL
                        return f"{html_url}/{src}"
    except Exception as e:
        print(f"Warning: Failed to fetch images from HTML: {e}")
    return None

def score_paper(paper):
    score = 0
    content_to_check = f"{paper['summary']} {paper['comment']}".lower()
    for inst in TOP_INSTITUTIONS:
        if inst.lower() in content_to_check:
            score += 10
            break
    for conf in TOP_CONFERENCES:
        if conf.lower() in content_to_check:
            score += 15
            break
    return score

def generate_review(paper):
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found.")
        return None

    # Try to find a real image URL from arXiv HTML
    real_image_url = get_arxiv_image_url(paper['pdf_url'])
    image_display = real_image_url if real_image_url else "INSERT_FIGURE_IMAGE_HERE"

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        if not os.path.exists(TEMPLATE_PATH):
            print(f"Error: Template not found at {TEMPLATE_PATH}")
            return None
            
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template = f.read()

        prompt = f"""
        You are a distinguished AI scientist and expert reviewer. Your task is to provide a deep technical review of the following paper.
        
        [Paper Information]
        Title: {paper['title']}
        Authors: {', '.join(paper['authors'])}
        URL: {paper['pdf_url']}
        Abstract: {paper['summary']}
        Institution/Conference: {paper['comment']}
        Detected Architecture Image URL: {real_image_url if real_image_url else "None"}
        
        [Jekyll Template]
        {template}
        
        [Detailed Instructions]
        1. **Front Matter Customization**:
           - Omit 'author'; the site-wide author is configured globally.
           - Put original authors in 'paper_authors' and the arXiv URL in 'paper_url'.
           - Set 'category' to "papers".
           - Determine a specific, lowercase 'subcategory'.
           - Add a factual one-sentence 'description' and 3-5 standardized tags.
           - Use the paper title without a date prefix.
        2. **Deep Technical Analysis (Section 3)**: Do not just summarize. Explain the internal mechanism deeply. 
           - Identify the core mathematical equations used in the paper.
           - Represent them in LaTeX format ($$ equation $$).
           - Explain every variable and the intuition behind the math.
        3. **Figure Integration (Section 4)**: 
           - You MUST include a section for the core architecture figure.
           - Use this image URL: {image_display}
           - If a URL was provided, explain in detail what the figure shows (components, data flow, etc.).
           - If no URL was provided, describe exactly which figure from the paper the user should capture (e.g., "Figure 1: Overall Architecture of Agents-K1") and provide a 300+ word detailed visual description of what that figure likely depicts so the user can understand it.
        4. **Tone & Language**: Use a highly professional, academic Korean tone. Keep technical terms in English.
        5. **Accuracy & Publication Safety**:
           - Never invent equations, metrics, affiliations, publication venues, or image URLs.
           - Mark information that requires manual verification as a plain-text review note.
        6. **Return ONLY the markdown content.**
        """
        
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error during Gemini generation: {e}")
        return None

def is_already_reviewed(title):
    if not os.path.exists(TARGET_DIR):
        return False
    
    clean_title = "".join([c if c.isalnum() else "-" for c in title.lower()]).replace("--", "-")[:50]
    existing_files = os.listdir(TARGET_DIR)
    for file in existing_files:
        if clean_title in file:
            return True
    return False

def main():
    print("Fetching papers from arXiv...")
    papers = fetch_arxiv_papers(SEARCH_QUERY, MAX_RESULTS)
    
    if not papers:
        print("No papers found.")
        return

    # Sort papers by score
    scored_papers = [(score_paper(p), p) for p in papers]
    scored_papers.sort(key=lambda x: x[0], reverse=True)
    
    # Identify top-tier conference papers vs regular papers
    conference_papers = []
    regular_papers = []
    
    for score, paper in scored_papers:
        if is_already_reviewed(paper['title']):
            print(f"Skipping already reviewed paper: {paper['title']}")
            continue
            
        # If score indicates a top-tier conference (score >= 15 based on our scoring logic)
        if score >= 15:
            conference_papers.append(paper)
        else:
            regular_papers.append(paper)

    papers_to_review = []
    
    if conference_papers:
        print(f"Found {len(conference_papers)} top-tier conference papers. Processing batch...")
        # Safety limit: max 5 conference papers per run to avoid quota issues
        papers_to_review = conference_papers[:5]
    elif regular_papers:
        print("No new conference papers found. Picking the best regular paper.")
        papers_to_review = [regular_papers[0]]
    else:
        print("No new papers to review today among the top results.")
        return
    
    for paper in papers_to_review:
        print(f"Reviewing: {paper['title']}")
        review_content = generate_review(paper)
        
        if review_content:
            date_str = datetime.now().strftime("%Y-%m-%d")
            clean_title = "".join([c if c.isalnum() else "-" for c in paper['title'].lower()]).replace("--", "-")[:50]
            filename = f"{date_str}-{clean_title}.md"
            filepath = TARGET_DIR / filename
            
            os.makedirs(TARGET_DIR, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(review_content)
            print(f"Successfully created review: {filepath}")
        else:
            print(f"Failed to generate review for: {paper['title']}")

if __name__ == "__main__":
    main()
