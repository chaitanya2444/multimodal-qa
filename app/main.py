
import streamlit as st
from app.qa import answer_query

st.set_page_config(page_title="Multimodal QA Demo")
st.title("Multimodal QA Demo")

q = st.text_input("Ask a question about your uploaded files:")
if st.button("Ask") and q.strip():
    with st.spinner("Retrieving answers..."):
        ans = answer_query(q)
    st.subheader("Answer")
    st.write(ans)

st.markdown("---")
st.write("To ingest documents, run `python app/ingest.py sample_data/` in your terminal.")
