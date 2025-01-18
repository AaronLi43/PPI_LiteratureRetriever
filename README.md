# PPI Literature Search System

This system allows you to search through protein-protein interaction (PPI) literature based on protein pairs and therapeutic queries. It uses semantic search powered by BioBERT to find the most relevant papers.

## Prerequisites

Before using the system, make sure you have Python 3.7+ installed and the following packages:

```bash
pip install pandas numpy faiss-cpu sentence-transformers
```

## File Structure

Your directory should look like this:
```
.
├── cache/
│   ├── paper_cache.pkl
│   ├── faiss_index.bin
│   └── pmids.pkl
├── search_papers.py
└── README.md
```
You could download all the files in cache through [Cache](https://drive.google.com/drive/folders/1qW5E2py2XIIaY-Qrn3mnGFNiWP5mF2Xc?usp=sharing).
## Quick Start

1. Place all downloaded cache files in the `cache` directory
2. Run the search script:
```bash
python search_papers.py
```
3. Follow the prompts to enter your search query and protein names

## Example Usage

Here are some example searches you can try:

### Example 1: Cancer Treatment Resistance
```
Enter your therapeutic query: cancer treatment resistance
Enter first protein name: MAP2K4
Enter second protein name: FLNC
```

### Example 2: Drug Response
```
Enter your therapeutic query: drug response pathway regulation
Enter first protein name: BRCA1
Enter second protein name: BARD1
```

### Example 3: Disease Mechanisms
```
Enter your therapeutic query: inflammatory response signaling
Enter first protein name: TNF
Enter second protein name: TNFRSF1A
```

## Understanding the Results

For each paper, the system will display:
- Title
- PubMed ID (PMID)
- Publication Year
- Journal
- Relevance Score (higher scores indicate better matches)

Example output:
```
Search Results:
--------------------------------------------------------------------------------

1. Title: [Paper title here]
   PMID: 12345678
   Year: 2022
   Journal: Nature Cell Biology
   Relevance Score: 0.856
--------------------------------------------------------------------------------
```

## Advanced Usage

You can modify the code to:
1. Change the number of results returned (default is 10):
```python
results = search_therapeutic_papers(..., top_k=20)  # Get top 20 results
```

2. Save results to a file:
```python
# Add to your script
with open('search_results.txt', 'w') as f:
    for i, result in enumerate(results, 1):
        f.write(f"{i}. {result['title']}\n")
        f.write(f"   PMID: {result['pmid']}\n")
        f.write(f"   Score: {result['score']:.3f}\n\n")
```

## Search Tips

1. **Therapeutic Queries**:
   - Be specific about the therapeutic context
   - Include relevant biological processes
   - Consider including disease names

2. **Protein Names**:
   - Use official gene symbols
   - Case sensitive (use correct capitalization)
   - Make sure proteins are known to interact

### Good Query Examples:
- "cancer drug resistance mechanism"
- "inflammatory pathway regulation"
- "cell death signaling pathway"
- "disease progression biomarker"

## Troubleshooting

1. If you get a "Model not found" error:
   ```bash
   pip install --upgrade sentence-transformers
   ```

2. If you get a memory error:
   - Reduce the batch size in the code
   - Close other applications
   - Use a machine with more RAM

3. If the search seems irrelevant:
   - Try rephrasing your query
   - Make sure protein names are correct
   - Use more specific therapeutic terms

## Technical Details

The system uses:
- BioBERT for semantic understanding of biomedical text
- FAISS for efficient similarity search
- Pre-processed PubMed abstracts
- Normalized vector representations

## Cache Files Explanation

- `paper_cache.pkl`: Contains paper metadata and abstracts
- `faiss_index.bin`: FAISS index for fast similarity search
- `pmids.pkl`: Mapping of index positions to PubMed IDs

## Citation

If you use this system in your research, please cite the relevant papers:
1. BioBERT
2. FAISS
3. The original PPI database used

## License

This project is licensed under the MIT License - see the LICENSE file for details