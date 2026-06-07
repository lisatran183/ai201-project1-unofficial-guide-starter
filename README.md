# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Northeastern University co-op experiences shared by students across Reddit, Medium, and other platforms. This knowledge is hard to find otherwise because it's scattered across dozens of sources and not aggregated anywhere officially.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/NEU Reddit | Forum | https://www.reddit.com/r/NEU/comments/1ss0gjl/i_hate_my_final_coop/ |
| 2 | r/NEU Reddit | Forum | https://www.reddit.com/r/NEU/search/?q=coop+experience |
| 3 | NEU Experience Magazine | Article | https://experiencepoweredby.northeastern.edu/cooperative-education/page/2/ |
| 4 | Northeastern News | Article | https://news.northeastern.edu/2024/03/25/co-op-experience/ |
| 5 | COE Graduate Ambassadors | Blog | https://coegraduatestudentambassadors.sites.northeastern.edu/the-blog/page/4 |
| 6 | Medium - Mingle Li | Blog | https://medium.com/@minglethepringle/top-ten-tips-for-northeastern-university-co-op-b6fb7dfd0eee |
| 7 | Medium - Serena Wang | Blog | https://medium.com/@serenawang0210/behind-northeasterns-co-op-program-f4265614127a |
| 8 | Medium - Tiffany Nguyen | Blog | https://medium.com/@tiffanyn.3544/my-honest-northeastern-experience-personal-perspective-22f66e918ce7 |
| 9 | Medium - Grace Yeung | Blog | https://graceyg.medium.com/demystifying-college-co-ops-what-is-it-how-do-i-get-one-421544a637b2 |
| 10 | Huntington News | News | https://huntnewsnu.com/82523/campus/115-years-later-how-northeasterns-co-op-program-grew-with-the-university/ |
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 tokens

**Overlap:** 50 tokens

**Why these choices fit your documents:** Co-op reviews and blog posts are short and conversational. 500 tokens keeps individual experiences intact without splitting mid-thought. 50-token overlap ensures context isn't lost at chunk boundaries.

**Final chunk count:** 25

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:** If cost wasn't a constraint, I would consider OpenAI's text-embedding-3-large for better accuracy. Tradeoffs include higher accuracy vs. higher latency and API cost. For multilingual support (international NU students), paraphrase-multilingual-MiniLM-L12-v2 would be worth exploring.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** "Answer the question using ONLY the information provided in the documents below. If the documents don't contain enough information to answer, say 'I don't have enough information in my documents to answer that.' Always cite which document(s) your answer came from."

**How source attribution is surfaced in the response:** The system appends [Source: filename.txt] to each retrieved chunk passed to the LLM, and the model is instructed to cite sources in its answer. The "Retrieved from" box in the UI also shows all source filenames used.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the average co-op pay at Northeastern? | ~$26/hr | $26/hr (Source: 06_medium_mingle_li.txt) | Relevant | Accurate |
| 2 | Is co-op required at Northeastern? | No, but highly encouraged | "Don't have enough info" but mentions 90% participate | Partially relevant | Partially accurate |
| 3 | What mistakes do students make during their first co-op search? | Focusing on pay over experience | Listed 4 correct mistakes from source | Relevant | Accurate |
| 4 | What companies have NU students co-oped at in healthcare? | Mass General, BWH, etc. | "Specific names not in documents" | Partially relevant | Partially accurate |
| 5 | How long is a co-op at Northeastern? | 6 months | "4, 6, or 8 months" | Relevant | Accurate |

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "Is co-op required at Northeastern?"

**What the system returned:** "I don't have enough information in my documents to answer that. The documents mention that 90% of students complete at least one co-op, but they do not explicitly state whether co-op is required or not."

**Root cause (tied to a specific pipeline stage):** The chunking stage split the relevant information across multiple chunks. The sentence stating co-op is "not required but highly encouraged" appeared in a chunk that was not retrieved in the top-5 results because the distance scores were too high (weak semantic match).

**What you would change to fix it:** Reduce chunk size to 200-300 tokens so individual facts are not buried in larger chunks, or increase top-k from 5 to 10 to retrieve more candidates.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The planning.md chunking strategy section gave clear direction on chunk size (500 tokens) and overlap (50 tokens), which made it easy to implement the chunking code without guessing.

**One way your implementation diverged from the spec, and why:** The spec assumed documents would be longer and richer, resulting in 50+ chunks. Our corpus only produced 25 chunks because the source documents were shorter blog posts and Reddit threads rather than long guides or FAQs.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**
- *What I gave the AI:* My planning.md with the Domain, Chunking Strategy (500 tokens, 50 overlap), and Document Sources sections, plus a description of my pipeline diagram. I asked Claude to generate Python code to load .txt files from the documents/ folder and split them into chunks.
- *What it produced:* A complete ingest.py with two functions — load_documents() that reads all .txt files and stores filename metadata, and chunk_text() that splits by word count with overlap. It also printed 5 sample chunks for verification.
- *What I changed or overrode:* The sample chunks revealed that 02_reddit_neu_coop2.txt still had HTML artifacts (CSS class names from Reddit's UI). I went back and manually cleaned that file before re-running, which the AI did not catch automatically.

**Instance 2**
- *What I gave the AI:* My completed ingest.py, the Retrieval Approach section from planning.md (all-MiniLM-L6-v2, top-k=5, ChromaDB), and the architecture diagram. I asked it to generate embedding and generation code plus a Gradio UI.
- *What it produced:* embed.py with SentenceTransformer embedding, ChromaDB storage with source metadata, and a retrieve() function. Then app.py wiring retrieval to Groq llama-3.3-70b with a grounding prompt and a Gradio interface with answer and sources boxes.
- *What I changed or overrode:*  The initial app.py failed because gradio wasn't installed. I also noticed the grounding prompt said "suggest" rather than enforce — I verified it actually refused to answer out-of-scope questions before accepting it.