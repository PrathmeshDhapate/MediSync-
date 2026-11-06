from sqlalchemy import select,or_
from datetime import date, datetime
import httpx
import re
import xml.etree.ElementTree as ET

from app.database import SessionLocal
from app.models import Paper

PUBMED_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

PMIDS = [
    "10196523",
    "19734903",
    "23150908",
    "27025652",
    "38821351",
]

def extract_clean_text(element):
    if element is None:
        return None

    text = " ".join(
        part.strip()
        for part in element.itertext()
        if part.strip()
    )

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)

    return text.strip()

def fetch_pubmed_records():
    params = {
        "db": "pubmed",
        "id": ",".join(PMIDS),
        "retmode": "xml",
        "tool": "medisync",
    }

    response = httpx.get(
        PUBMED_URL,
        params=params,
        timeout=30.0,
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    return root

def extract_paper_data(root):
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")

        title = extract_clean_text(
            article.find(".//ArticleTitle")
        )

        abstract_sections = article.findall(".//Abstract/AbstractText")

        abstract_parts = []

        for section in abstract_sections:
            section_text = extract_clean_text(section)

            if not section_text:
                continue

            label = section.get("Label")

            if label:
                abstract_parts.append(f"{label}: {section_text}")
            else:
                abstract_parts.append(section_text)

        abstract = "\n\n".join(abstract_parts)

        journal = article.findtext(".//Journal/Title")

        doi = None

        for article_id in article.findall(".//ArticleId"):
            if article_id.get("IdType") == "doi":
                doi = article_id.text
                break

        papers.append({
            "pmid": pmid,
            "title": title,
            "abstract": abstract or None,
            "doi": doi,
            "journal": journal,
            "publication_date": extract_publication_date(article),
            "source_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "source_type": "pubmed",
        })

    return papers


def extract_publication_date(article):
    pub_date = article.find(".//JournalIssue/PubDate")

    if pub_date is None:
        return None

    year = pub_date.findtext("Year")
    month = pub_date.findtext("Month")
    day = pub_date.findtext("Day")

    if not all([year, month, day]):
        return None

    try:
        if month.isdigit():
            month_number = int(month)
        else:
            month_number = datetime.strptime(
                month[:3], "%b"
            ).month

        return date(int(year), month_number, int(day))

    except ValueError:
        return None

def seed_papers():
    root = fetch_pubmed_records()
    papers_data = extract_paper_data(root)

    if len(papers_data) != len(PMIDS):
        raise RuntimeError(
            f"Expected {len(PMIDS)} papers, "
            f"but PubMed returned {len(papers_data)}."
        )

    for paper in papers_data:
        if not paper["pmid"] or not paper["title"]:
            raise RuntimeError("A paper is missing its PMID or title.")

    print(f"Fetched {len(papers_data)} papers from PubMed.")

    with SessionLocal() as db:
        for paper_data in papers_data:
            conditions = []

            if paper_data["doi"]:
                conditions.append(Paper.doi == paper_data["doi"])

            if paper_data["pmid"]:
                conditions.append(Paper.pmid == paper_data["pmid"])

            existing_paper = None

            if conditions:
                existing_paper = db.scalar(
                    select(Paper).where(or_(*conditions))
                )

            if existing_paper:
                print(f"Already exists: {paper_data['title']}")
                continue

            paper = Paper(**paper_data)
            db.add(paper)

        db.commit()

    print("Paper seeding completed!")


if __name__ == "__main__":
    seed_papers()
