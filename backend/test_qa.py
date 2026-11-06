from app.services.qa import answer_question
from app.services.qa import validate_citations

def test_qa():
    question = "What is the role of TREM2 in Alzheimer's disease?"

    result = answer_question(question)

    print("\nResearch Question:")
    print(question)

    print("\nGenerated Answer:")
    print(result["answer"])

    print("\nCitations:")
    for citation in result["citations"]:
        print(f"Citation ID: [{citation['citation_id']}]")
        print(f"Paper ID: {citation['paper_id']}")
        print(f"Chunk ID: {citation['chunk_id']}")
        print(f"Paper Title: {citation['paper_title']}")
        print("-" * 50)

    print("\nCitation Validation:")
    print(result["citation_validation"])

def test_citation_validation():
    citations = [
        {"citation_id": "S1"},
        {"citation_id": "S2"},
        {"citation_id": "S3"},
    ]

    answer = "TREM2 is expressed on microglia [S2]. AD risk is associated with TREM2 variants [S1]. Unsupported claim [S9]."

    result = validate_citations(answer, citations)

    print("\nIndependent Citation Validation:")
    print(result)


if __name__ == "__main__":
    test_qa()