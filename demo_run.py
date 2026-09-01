import sys
from pathlib import Path
from semantica.semantic_extract import NamedEntityRecognizer, RelationExtractor, TripletExtractor

# Ensure UTF-8 output encoding for Windows terminal
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_demo():
    print("=" * 65)
    print("Semantica Knowledge Graph Extraction Demo")
    print("=" * 65)

    # Initialize extraction engines (works locally without API keys!)
    ner = NamedEntityRecognizer(confidence_threshold=0.5)
    rel_extractor = RelationExtractor(confidence_threshold=0.5)
    triplet_extractor = TripletExtractor()

    demo_dir = Path("examples/demo_data")
    files = sorted(list(demo_dir.glob("*.md")))

    for file_path in files:
        print(f"\nProcessing File: {file_path.name}")
        print("-" * 50)
        text = file_path.read_text(encoding="utf-8")

        # 1. Extract Entities
        entities = ner.extract_entities(text)
        print(f"[*] Found {len(entities)} Entities:")
        for e in entities[:6]:
            name = getattr(e, "text", str(e))
            label = getattr(e, "label", "ENTITY")
            print(f"    - [{label}] {name}")
        if len(entities) > 6:
            print(f"    ... and {len(entities) - 6} more")

        # 2. Extract Relations / Triplets
        triplets = triplet_extractor.extract_triplets(text)
        print(f"\n[*] Found {len(triplets)} Graph Triplets / Relations:")
        for t in triplets[:6]:
            s = getattr(t, "subject", "")
            p = getattr(t, "predicate", "")
            o = getattr(t, "object", "")
            print(f"    - ({s}) --[{p}]--> ({o})")
        if len(triplets) > 6:
            print(f"    ... and {len(triplets) - 6} more")

    print("\n" + "=" * 65)
    print("Extraction Complete! You can also upload these files into")
    print("the Knowledge Explorer UI at http://127.0.0.1:8000")
    print("=" * 65)

if __name__ == "__main__":
    run_demo()
