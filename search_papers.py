import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os

def load_saved_data(cache_dir='cache'):
    """Load all saved data from cache directory"""
    print("Loading cached data...")
    # Load paper cache
    with open(os.path.join(cache_dir, 'paper_cache.pkl'), 'rb') as f:
        cache_data = pickle.load(f)
        paper_cache = cache_data['paper_cache']  # Access the actual cache from metadata
        print(f"Loaded paper cache containing {len(paper_cache)} papers")
    
    # Load FAISS index and related data
    print("Loading search index...")
    index = faiss.read_index(os.path.join(cache_dir, 'faiss_index.bin'))
    with open(os.path.join(cache_dir, 'pmids.pkl'), 'rb') as f:
        pmids = pickle.load(f)
        
    print("Setup complete!")
    return paper_cache, index, pmids

def search_therapeutic_papers(query, protein_names, paper_cache, model, index, pmids, top_k=10):
    """Search for papers using semantic similarity"""
    print(f"\nSearching for papers about '{query}' related to proteins {protein_names[0]} and {protein_names[1]}...")
    
    # Combine query with protein context
    enriched_query = f"Impact of {protein_names[0]} and {protein_names[1]} interaction on {query}"
    
    # Encode query
    print("Encoding search query...")
    query_vector = model.encode([enriched_query])
    faiss.normalize_L2(query_vector)
    
    # Perform similarity search
    print("Searching through papers...")
    scores, indices = index.search(query_vector, top_k)
    
    # Prepare results
    results = []
    for score, idx in zip(scores[0], indices[0]):
        pmid = pmids[idx]
        if str(pmid) in paper_cache:
            paper = paper_cache[str(pmid)]
            results.append({
                'pmid': pmid,
                'title': paper['title'],
                'year': paper['year'],
                'journal': paper['journal'],
                'score': float(score)
            })
    
    return results

def main():
    # 1. Make sure you have all required files in a directory
    cache_dir = 'cache'  # Directory containing your downloaded files
    
    # 2. Load the biomedical language model (required for new queries)
    print("Loading language model...")
    model = SentenceTransformer('pritamdeka/S-BioBERT-snli-multinli-stsb')
    
    # 3. Load saved data
    paper_cache, index, pmids = load_saved_data(cache_dir)
    
    # 4. Define your search parameters
    query = input("Enter your therapeutic query (e.g., 'cancer treatment resistance'): ")
    protein1 = input("Enter first protein name: ")
    protein2 = input("Enter second protein name: ")
    protein_pair = [protein1, protein2]
    
    # 5. Perform search
    results = search_therapeutic_papers(
        query=query,
        protein_names=protein_pair,
        paper_cache=paper_cache,
        model=model,
        index=index,
        pmids=pmids
    )
    
    # 6. Display results
    print("\nSearch Results:")
    print("-" * 80)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Title: {result['title']}")
        print(f"   PMID: {result['pmid']}")
        print(f"   Year: {result['year']}")
        print(f"   Journal: {result['journal']}")
        print(f"   Relevance Score: {result['score']:.3f}")
        print("-" * 80)

if __name__ == "__main__":
    # First install required packages if you haven't:
    # pip install pandas numpy faiss-cpu sentence-transformers

    main()