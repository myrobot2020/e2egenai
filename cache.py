def get_cached_results(cur, query):
    cur.execute("SELECT merged_chunks FROM merged_cache WHERE query = %s", (query,))
    result = cur.fetchone()
    if result:
        return json.loads(result[0])
    return None

cached = get_cached_results(cur, query)
if cached:
    print("[Cached Result]")
    print(cached["generated_answer"])
else:
    # --- FORMAT PROMPT ---
    context = "\n\n".join([f"Chunk {i+1}:\n{chunk}" for i, (_, _, chunk) in enumerate(top_results)])

    prompt = f"""You are an expert summarizer. Given the following context chunks, generate a clear, coherent, and informative paragraph answering the query: "{query}"

Context:
{context}

Answer:"""

    # --- GENERATE TEXT ---
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are an expert scientific summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=300
    )

    generated_answer = response['choices'][0]['message']['content']

    print("[Generated Answer]")
    print(generated_answer)

    # --- CACHE RESULT ---
    cur.execute("""
        INSERT INTO merged_cache (query, merged_chunks)
        VALUES (%s, %s)
        ON CONFLICT (query) DO UPDATE SET merged_chunks = EXCLUDED.merged_chunks
    """, (query, json.dumps({
        "chunks": top_results,
        "generated_answer": generated_answer
    })))
    conn.commit()
