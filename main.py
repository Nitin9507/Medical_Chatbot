from flask import Flask, request, jsonify
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from groq import Groq
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
pdf_folder = "pdf"  # Assuming your embeddings are stored in this directory
embedding_function = SentenceTransformerEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Groq API client
groq_client = Groq(api_key="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")

# Global variable to hold the vector store (temporary, in-memory store)
vector_store = Chroma(
    embedding_function=embedding_function,
    persist_directory=pdf_folder,  # Assuming embeddings are already persisted here
)


@app.route("/chat/completion", methods=["POST"])
def chat_completion():
    """
    Handles chat queries using embeddings and LLM.
    """
    if not vector_store:
        return jsonify({"error": "No documents uploaded. Please upload a file first."}), 400

    # Get the user prompt from the request
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in the request body"}), 400

    query = data["prompt"]

    # Search for the most relevant documents in the vector store
    docs = vector_store.similarity_search(query, k=3)  # Adjust 'k' as needed
    print(f"Retrieved {len(docs)} documents for query.")

    if not docs:
        return jsonify({"error": "No relevant documents found in the uploaded files."}), 404

    # Combine the documents into a prompt for the LLM
    prompt = "\n".join([doc.page_content for doc in docs])
    prompt += f"\nAnswer the following question based on the above documents: {query}"

    # Call the Groq API for chat completion
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            max_tokens=1024,
            top_p=1.0,
            stop=None,
        )

        response_content = completion.choices[0].message.content
        return jsonify({"response": response_content})

    except Exception as e:
        print(f"Error generating completion: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500


# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
