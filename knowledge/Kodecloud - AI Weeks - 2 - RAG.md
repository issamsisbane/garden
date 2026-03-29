Le but est d'avoir un RAG qui connecte des documents de compliance AWS d'une entreprise pour rechercher plus vite.

# 1 - Setup RAG Dev Env
**📦 What Gets Installed:**

**ChromaDB:** Vector database for storing embeddings

**Sentence Transformers:** For creating text embeddings

**OpenAI:** LLM integration

**Tiktoken:** Token counting for smart chunking

✅ **Rank-BM25:** Keyword search for hybrid retrieval

**🚀 After Setup:**

- Virtual environment created at /root/rag-debugging/venv
- All RAG dependencies installed
- Ready to test the RAG system
Install Script

``` bash
#!/bin/bash

echo "============================================"
echo "🚀  Setting up RAG Development Environment"
echo "============================================"

# Navigate to the rag-debugging directory
cd /root/rag-debugging

# Create Python virtual environment
echo "📦  Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install UV package manager
echo "⚡  Installing UV package manager..."
pip install uv

# Install required packages
echo "📚  Installing RAG dependencies..."
uv pip install chromadb sentence-transformers openai tiktoken rank-bm25

# Create setup complete marker
echo "SETUP_COMPLETE" > /root/setup-complete.txt

echo ""
echo "============================================"
echo "✅  RAG Environment Setup Complete!"
echo "============================================"
echo ""
echo "📂  Working directory: /root/rag-debugging"
echo "🐍  Virtual environment: /root/rag-debugging/venv"
echo "📚  AWS compliance docs: /root/rag-debugging/aws-compliance-docs"
```

# 2 - Lancer un test avec le RAG

Le test : 
![[Pasted image 20250917092353.png]]

# 3 - Ask QWEN

Prompt : 
```
Analyze the RAG system at /root/rag-debugging/rag-system/rag_system.py
The system is only achieving 45% accuracy on compliance queries.

1. Identify the 4 main problems causing poor accuracy
2. For each problem, explain:
   - What's wrong
   - Why it impacts accuracy
   - How to fix it
3. Create a markdown report and save it as /root/rag-debugging/rag_issues.md

Focus on:
- Document chunking strategy
- Metadata extraction
- Search methodology
- Query processing
```

Response :
```
# RAG System Accuracy Issues Analysis                       │
 │                                                                │
 │    ## Executive Summary                                        │
 │    The RAG system is achieving only 45% accuracy on            │
 │    compliance queries due to several fundamental issues in     │
 │    its implementation. This analysis identifies four main      │
 │    problems and provides specific recommendations for          │
 │    improvement.                                                │
 │                                                                │
 │    ## Problem 1: Poor Document Chunking Strategy               │
 │    **What's Wrong:** The system uses fixed-size chunks of 120  │
 │    characters with a 100-character step, which frequently      │
 │    breaks sentences and semantic units mid-way.                │
 │                                                                │
 │    **Impact on Accuracy:** This leads to incomplete            │
 │    information retrieval where important context is split      │
 │    across chunks, making it difficult for the system to        │
 │    provide coherent and complete answers to compliance         │
 │    queries.                                                    │
 │                                                                │
 │    **How to Fix:** Implement semantic chunking that respects   │
 │    sentence boundaries and document structure. Use techniques  │
 │    like:                                                       │
 │    - Sentence-aware splitting                                  │
 │    - Section-based chunking for compliance documents           │
 │    - Overlapping chunks to maintain context                    │
 │    - Dynamic chunk sizes based on content type                 │
 │                                                                │
 │    ## Problem 2: Insufficient Metadata Extraction              │
 │    **What's Wrong:** The system only stores basic metadata     │
 │    (source filename and chunk index), missing critical         │
 │    semantic information.                                       │
 │                                                                │
 │    **Impact on Accuracy:** Without rich metadata, the system   │
 │    cannot filter or prioritize relevant compliance             │
 │    information, leading to poor retrieval of specific          │
 │    regulatory requirements or standards.                       │
 │                                                                │
 │    **How to Fix:** Extract and store comprehensive metadata    │
 │    including:                                                  │
 │    - Document titles and section headers                       │
 │    - Compliance standards (e.g., SOC 2, HIPAA, GDPR)           │
 │    - Document types and categories                             │
 │    - Last updated dates                                        │
 │    - Author/organization information                           │
 │                                                                │
 │    ## Problem 3: Degraded Search Methodology                   │
 │    **What's Wrong:** The search function intentionally adds    │
 │    noise to query embeddings and limits results to only 1,     │
 │    significantly degrading retrieval quality.                  │
 │                                                                │
 │    **Impact on Accuracy:** This prevents the system from       │
 │    finding the most relevant compliance information, as noise  │
 │    reduces embedding similarity and limited results miss       │
 │    potentially correct answers.                                │
 │                                                                │
 │    **How to Fix:** Implement proper similarity search:         │
 │    - Remove artificial noise from embeddings                   │
 │    - Return multiple relevant results (3-5 typically)          │
 │    - Use proper distance metrics (cosine similarity)           │
 │    - Implement re-ranking based on relevance scores            │
 │                                                                │
 │    ## Problem 4: Lack of Query Processing                      │
 │    **What's Wrong:** Queries are processed as raw text         │
 │    without any enhancement, preprocessing, or expansion.       │
 │                                                                │
 │    **Impact on Accuracy:** Users may use different             │
 │    terminology than the documents, and the system cannot       │
 │    understand synonyms, acronyms, or related concepts in       │
 │    compliance domains.                                         │
 │                                                                │
 │    **How to Fix:** Add comprehensive query processing:         │
 │    - Query expansion with synonyms and related terms           │
 │    - Acronym resolution (e.g., "PCI DSS" ↔ "Payment Card      │
 │    Industry Data Security Standard")                           │
 │    - Intent recognition for compliance queries                 │
 │    - Multi-turn conversation support                           │
 │                                                                │
 │    ## Recommendations                                          │
 │    1. **Immediate Priority:** Fix chunking strategy and        │
 │    remove search degradation                                   │
 │    2. **Short-term:** Implement rich metadata extraction       │
 │    3. **Medium-term:** Add query processing and enhancement    │
 │    4. **Long-term:** Implement advanced features like hybrid   │
 │    search and re-ranking                                       │
 │                                                                │
 │    Implementing these fixes should significantly improve       │
 │    accuracy from the current 45% baseline.
```

# 4 - Resolve

Prompt to ask qwen to resolve the probem : 

```
Based on the problems identified in rag_issues.md, create an improved RAG system that fixes all 4 issues:

1. **Smart Chunking**: Implement sentence-aware chunking with 512 tokens and 50 token overlap
2. **Metadata Filtering**: Extract AWS service, section, and policy IDs for each chunk
3. **Hybrid Search**: Combine 70% semantic + 30% keyword search with BM25
4. **Query Enhancement**: Add acronym expansion and synonym support

Create the improved system as /root/rag-debugging/improved_rag_system.py

Ensure the system:
- Uses tiktoken for proper token counting
- Implements BM25 for keyword search
- Extracts metadata for all AWS services
- Enhances queries with domain-specific terms
- Achieves 90%+ accuracy on the test cases
```

![[Pasted image 20250917092841.png]]

#### Key RAG Debugging Principles Learned

📏 **Measure First:** Always establish baseline metrics

🔄 **Incremental Fixes:** Apply and test one optimization at a time

📚 **Context is King:** Better chunking beats better models

🔀 **Hybrid Approach:** Combine multiple search strategies

🧪 **Test Continuously:** Validate improvements with diverse queries