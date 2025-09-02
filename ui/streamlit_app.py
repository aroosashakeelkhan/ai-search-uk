# ui/streamlit_app.py
import requests
import streamlit as st


st.title("AI Search UK — MVP")
backend = st.text_input("FastAPI base URL", "http://localhost:8000")
query = st.text_input("Search UK docs (FTS5)")


if st.button("Search") and query:
    r = requests.get(f"{backend}/search", params={"q": query, "limit": 5})
    if r.status_code == 200:
        data = r.json()
        st.write(f"Total hits: {data['total']}")
        for i, item in enumerate(data['results'], 1):
            st.markdown(f"### {i}. {item['title']}")
            st.write(item['snippet'], unsafe_allow_html=True)
    else:
        st.error(r.text)
