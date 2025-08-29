import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("📄 Document Q&A")

st.subheader("Upload documents")
uploaded_files = st.file_uploader(
    "Choose files", type=["pdf", "txt", "csv"], accept_multiple_files=True
)
if st.button("Ingest files") and uploaded_files:
    for file in uploaded_files:
        files = {"files": (file.name, file.getvalue())}
        res = requests.post(f"{API_URL}/ingest", files=files)
        st.write(res.json())

st.subheader("Ask a question")
question = st.text_input("Question")
file_name = st.text_input("Restrict to filename (optional & experimental)")
if st.button("Ask") and question:
    payload = {"question": question}
    params = {"file_name": file_name} if file_name else {}
    res = requests.post(f"{API_URL}/query", json=payload, params=params)
    st.write("**Answer:**", res.json()["answer"])