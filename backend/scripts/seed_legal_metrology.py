import sys
import os
import re
import json

# Add backend directory to sys.path so we can import from database and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
import models

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

def seed_data():
    markdown_path = r"C:\Users\rusha\.gemini\antigravity-ide\brain\fb47bff0-3789-4a61-88ff-d598c1328eff\.system_generated\steps\187\content.md"
    
    if not os.path.exists(markdown_path):
        print(f"File not found: {markdown_path}")
        return

    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find markdown links that look like downloads
    # Format: [Download Title](url) or [Title](url) but specifically extracting the ones with URLs
    # Also finding general links that seem to be PDFs
    links = re.findall(r'\[(.*?)\]\((http[^\)]+)\)', content)
    
    db = SessionLocal()
    
    added_count = 0
    seen_urls = set()
    
    for title, url in links:
        # Clean up title (remove "Download " or other common prefixes)
        clean_title = title.replace("Download ", "").replace("View ", "").strip()
        
        # We only want legal metrology related docs or general acts
        # Or just take everything that ends with pdf
        if url in seen_urls:
            continue
            
        is_legal_metrology = "Metrology" in clean_title or "Commodities" in clean_title or "Standards" in clean_title or "Act" in clean_title or "Rules" in clean_title
        
        # We also specifically want PDF documents if possible, or important links
        is_pdf = url.lower().endswith('.pdf')
        
        if is_legal_metrology or is_pdf:
            # Determine Category
            category = "General"
            if "Packaged Commodities" in clean_title or "PCR" in clean_title:
                category = "Packaged Commodities Rules"
            elif "General" in clean_title and "Rules" in clean_title:
                category = "General Rules"
            elif "Act" in clean_title and "Metrology" in clean_title:
                category = "The Legal Metrology Act"
            elif "Approval of Models" in clean_title:
                category = "Approval of Models"
            elif "Government Approved Test Centre" in clean_title or "GATC" in clean_title:
                category = "GATC Rules"
            elif "Act" in clean_title:
                category = "Acts"

            # Check if it already exists
            existing = db.query(models.LegalMetrologyDocument).filter(models.LegalMetrologyDocument.url == url).first()
            if not existing:
                doc = models.LegalMetrologyDocument(
                    title=clean_title,
                    url=url,
                    category=category
                )
                db.add(doc)
                seen_urls.add(url)
                added_count += 1
                print(f"Adding: [{category}] {clean_title}")

    db.commit()
    db.close()
    print(f"Successfully added {added_count} new documents.")

if __name__ == "__main__":
    seed_data()
