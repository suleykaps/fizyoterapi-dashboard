import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

# Başlık ve Açıklama
st.title("📋 Fizyoterapist Danışma ve Skolyoz Yönetim Paneli")
with st.expander("ℹ️ Bilgilendirme"):
    st.caption(
        """Bu panel, fizyoterapistler için skolyoz tedavisinde analiz, veri görselleştirme ve danışmanlık sağlamak amacıyla tasarlanmıştır.
        - **Skolyoz Analizi**: Hasta raporlarından faydalı bilgiler çıkarır.
        - **Veri Görselleştirme**: Skolyoz ölçüm cihazı verilerini grafiklere dönüştürür.
        - **Sohbet**: Sıkça sorulan sorulara yanıt verir."""
    )

# OpenAI istemcisi oluşturma
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Başlangıç ayarları
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "max_messages" not in st.session_state:
    st.session_state.max_messages = 20

# --- Dashboard ve Analiz ---
st.sidebar.title("🛠️ Menü")
tab = st.sidebar.radio("Bölümler", ["Skolyoz Analiz", "Veri Görselleştirme", "Sohbet"])

# 1. Skolyoz Analiz
if tab == "Skolyoz Analiz":
    st.subheader("🏋️‍♂️ Skolyoz Analizi")
    uploaded_file = st.file_uploader("📄 Hasta verilerini yükleyin (ör. skolyoz raporu, eğrilik açıları vb.)", type=("txt", "md"))

    if uploaded_file is not None:
        # Yüklenen dosyanın içeriğini okuma
        file_content = uploaded_file.read().decode("utf-8")
        
        st.text_area("📜 Yüklenen Dosya İçeriği", value=file_content, height=200)
        
        if st.button("🔍 Analiz Et"):
            try:
                # OpenAI ile analiz
                analysis_prompt = (
                    f"Bu metin skolyoz ile ilgili bir hasta raporudur:\n{file_content}\n\n"
                    "Lütfen aşağıdaki bilgileri çıkarın:\n"
                    "1. Eğrilik derecesi (varsa belirtilen).\n"
                    "2. Önerilen tedavi yöntemleri.\n"
                    "3. Hangi egzersizler veya fizyoterapi protokolleri faydalı olabilir?"
                )
                response = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[{"role": "user", "content": analysis_prompt}],
                )
                st.subheader("🩺 Analiz Sonuçları")
                st.write(response["choices"][0]["message"]["content"])
            except Exception as e:
                st.error(f"Hata oluştu: {e}")

# 2. Veri Görselleştirme
elif tab == "Veri Görselleştirme":
    st.subheader("📊 Skolyoz Ölçüm Verileri Grafikleri")
    uploaded_data = st.file_uploader("📄 Ölçüm Verilerini Yükleyin (CSV formatında)", type="csv")

    if uploaded_data is not None:
        # Veriyi yükleme
        data = pd.read_csv(uploaded_data)
        st.write("📋 Yüklenen Veri")
        st.dataframe(data)

        # Grafik Seçimi
        graph_type = st.selectbox("Grafik Türü Seçin", ["Çizgi Grafiği", "Bar Grafiği", "Dağılım Grafiği"])

        # X ve Y eksenleri seçimi
        x_axis = st.selectbox("X Eksenini Seçin", options=data.columns)
        y_axis = st.selectbox("Y Eksenini Seçin", options=data.columns)

        # Grafik oluşturma
        if st.button("📈 Grafik Oluştur"):
            plt.figure(figsize=(10, 6))
            if graph_type == "Çizgi Grafiği":
                plt.plot(data[x_axis], data[y_axis], marker="o", color="b")
            elif graph_type == "Bar Grafiği":
                plt.bar(data[x_axis], data[y_axis], color="g")
            elif graph_type == "Dağılım Grafiği":
                plt.scatter(data[x_axis], data[y_axis], color="r")

            plt.title(f"{y_axis} vs {x_axis}")
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            plt.grid(True)
            st.pyplot(plt)

# 3. Sohbet
elif tab == "Sohbet":
    st.subheader("💬 Danışma ve Soru-Cevap")
    # Daha önceki mesajları gösterme
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Maksimum mesaja ulaşıldıysa bilgilendirme
    if len(st.session_state.messages) >= st.session_state.max_messages:
        st.info(
            """Dikkat: Bu demo sürümünde maksimum mesaj sınırına ulaşıldı. İlginize teşekkür ederiz!
            Daha fazlasını denemek için Streamlit'in [Bir LLM Sohbet Uygulaması Geliştirin](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)
            rehberine göz atabilirsiniz."""
        )
    else:
        # Kullanıcı giriş alanı
        if prompt := st.chat_input("Sorularınızı yazın (ör. 'Skolyoz için hangi egzersizleri önerirsiniz?')"):
            # Kullanıcı mesajını kaydetme
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Asistan yanıtı
            with st.chat_message("assistant"):
                try:
                    # OpenAI ile sohbet oluşturma
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except:
                    # Yoğunluk durumunda mesaj sınırı belirleme
                    st.session_state.max_messages = len(st.session_state.messages)
                    rate_limit_message = """
                        Üzgünüz! Şu anda hizmet verilemiyor. Lütfen daha sonra tekrar deneyin.
                    """
                    st.session_state.messages.append(
                        {"role": "assistant", "content": rate_limit_message}
                    )
                    st.rerun()
