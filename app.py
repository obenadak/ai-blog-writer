import streamlit as st
import requests
from datetime import datetime


st.set_page_config(page_title="AI Blog Yazarı", layout="wide", initial_sidebar_state="collapsed")

NGROK_BASE_URL = "https://6691c25e8282.ngrok-free.app"
API_ARTICLES_URL = f"{NGROK_BASE_URL}/articles/"

st.markdown("""
<style>
    /* Google'dan modern bir font import etme */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Genel font ayarları */
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Ana uygulama konteynerini ortalama ve genişliğini sınırlama */
    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Butonları modernleştirme */
    .stButton > button {
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        background-color: #FF4B4B; /* Streamlit'in kırmızısı */
        color: white;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 14px 0 rgba(255, 75, 75, 0.39);
    }

    .stButton > button:hover {
        transform: scale(1.02);
        background-color: #E03C3C;
        box-shadow: 0 6px 20px 0 rgba(255, 75, 75, 0.45);
    }
    
    .stButton > button:disabled {
        background-color: #cccccc;
        box-shadow: none;
        color: #666666;
    }

    /* Konteynerları kart gibi gösterme */
    [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlock"] {
         border: 1px solid rgba(255, 255, 255, 0.1);
         border-radius: 10px;
         padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def get_all_articles():
    try:
        response = requests.get(API_ARTICLES_URL)
        return response.json() if response.status_code == 200 else []
    except requests.RequestException:
        st.error("API'ye bağlanılamadı. Colab sunucusunun çalıştığından emin olun.")
        return []

def render_compact_markdown(text):
    if not text:
        st.warning("Gösterilecek içerik yok.")
        return
    lines = text.split('\n')
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            if stripped_line.startswith('###'):
                st.markdown(f"**{stripped_line.replace('###', '').strip()}**")
            elif stripped_line.startswith('##'):
                st.subheader(stripped_line.replace('##', '').strip())
            elif stripped_line.startswith('#'):
                st.header(stripped_line.replace('#', '').strip())
            else:
                st.write(line)

def reset_session():
    st.session_state.step = "start"
    st.session_state.current_article = None
    st.session_state.processing = False
    st.rerun()

if 'step' not in st.session_state:
    st.session_state.step = "start"
    st.session_state.current_article = None
    st.session_state.processing = False

col1, col2 = st.columns([3, 1])
with col1:
    st.title("AI Blog Yazarı")
with col2:
    if st.session_state.step != "start":
        if st.button("Yeni Yazı Başlat", use_container_width=True):
            reset_session()
st.markdown("---")

if st.session_state.step == "start":
    st.subheader("Yeni Bir Blog Yazısı Başlatın")
    with st.form(key="topic_form"):
        topic_input = st.text_input("Blog Konusu:", placeholder="Örn: Yapay zekanın sanata etkileri")
        submitted = st.form_submit_button(
            "Plan Oluştur ve Başla",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.processing 
        )

    if submitted and topic_input:
        st.session_state.processing = True
        st.rerun()

    if st.session_state.processing and st.session_state.step == "start":
        with st.spinner("Planlama ajanı çalışıyor, lütfen bekleyin..."):
            try:
                response = requests.post(f"{API_ARTICLES_URL}?title={topic_input}")
                if response.status_code == 200:
                    st.session_state.current_article = response.json()
                    st.session_state.step = "edit_plan"
                else:
                    st.error(f"Hata: {response.text}")
            except requests.RequestException as e:
                st.error(f"API'ye bağlanılamadı: {e}")
            finally:
                st.session_state.processing = False 
                st.rerun()

    st.markdown("---")
    st.subheader("Önceki Yazılarınız")
    all_articles = get_all_articles()
    if not all_articles:
        st.info("Henüz oluşturulmuş bir yazınız bulunmuyor.")
    else:
        for article in all_articles:
            with st.container():
                col1, col2, col3 = st.columns([4, 2, 1])
                with col1:
                    st.markdown(f"**{article['title']}**")
                    created_time = datetime.fromisoformat(article['created_at']).strftime('%d %B %Y, %H:%M')
                    st.caption(f"ID: {article['id']} | {created_time}")
                with col2:
                    status_map = {"writing_pending": "Plan Düzenlemede", "completed": "Tamamlandı"}
                    st.text(f"Durum: {status_map.get(article['status'], article['status'])}")
                with col3:
                    if st.button("Görüntüle", key=f"view_{article['id']}", use_container_width=True):
                        st.session_state.current_article = article
                        st.session_state.step = 'done' if article['status'] == 'completed' else 'edit_plan'
                        st.rerun()

elif st.session_state.step == "edit_plan":
    article = st.session_state.current_article
    st.subheader(f"Planı Gözden Geçirin: '{article['title']}'")
    
    col_view, col_edit = st.columns(2)
    with col_view:
        st.markdown("**Oluşturulan Plan**")
        with st.container(border=True, height=500):
            render_compact_markdown(article.get('plan_content'))
    with col_edit:
        st.markdown("**Plan Düzenleyici**")
        edited_plan = st.text_area("Planı burada düzenleyebilirsiniz:", value=article.get('plan_content'), height=500, label_visibility="collapsed")

    if st.button("Bu Planla Yazıyı Oluştur", type="primary", use_container_width=True, disabled=st.session_state.processing):
        st.session_state.processing = True
        with st.spinner("Plan güncelleniyor ve yazarlar çalışmaya başlıyor..."):
            try:
                plan_update_response = requests.put(f"{API_ARTICLES_URL}{article['id']}/plan", json={"new_plan": edited_plan})
                if plan_update_response.status_code == 200:
                    write_response = requests.post(f"{API_ARTICLES_URL}{article['id']}/write")
                    if write_response.status_code == 200:
                        st.session_state.current_article = write_response.json()
                        st.session_state.step = "done"
                    else:
                        st.error(f"Yazı oluşturulamadı: {write_response.text}")
                else:
                    st.error(f"Plan güncellenemedi: {plan_update_response.text}")
            except requests.RequestException as e:
                st.error(f"API hatası: {e}")
            finally:
                st.session_state.processing = False
                st.rerun()

elif st.session_state.step == "done":
    article = st.session_state.current_article
    st.subheader(f"Yazınız Hazır: '{article['title']}'")
    st.success("Blog yazınız başarıyla tamamlandı ve veritabanına kaydedildi.")
    
    tab1, tab2 = st.tabs(["Karşılaştırmalı Görünüm", "Oluşturulan Plan"])

    with tab1:
        col_draft, col_final = st.columns(2)
        with col_draft:
            st.markdown("**İlk Taslak**")
            with st.container(border=True, height=600):
                render_compact_markdown(article.get('draft_content'))
        with col_final:
            st.markdown("**Nihai Metin**")
            with st.container(border=True, height=600):
                render_compact_markdown(article.get('final_content'))
    
    with tab2:
        st.markdown("**Yazının Oluşturulduğu Plan**")
        with st.container(border=True):
             render_compact_markdown(article.get('plan_content'))