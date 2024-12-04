import numpy as np

# Yeni Sayfa: Skolyoz Simülasyonu
elif tab == "Skolyoz Simülasyonu":
    st.subheader("👤 Skolyoz Simülasyonu")
    st.write(
        """Bu sayfa, skolyoz etkilerini görselleştiren bir insan infografiği sunar.
        Eğriliklerin insan vücudundaki etkilerini daha iyi anlamak için tasarlanmıştır."""
    )
    
    # Skolyoz açılarını kullanıcının belirlemesi için bir slider
    scoliosis_angle = st.slider("Skolyoz Açısı (derece)", min_value=0, max_value=50, step=5, value=20)
    
    # İnsan vücudu infografiği için bir görselleştirme
    fig, ax = plt.subplots(figsize=(6, 12))
    
    # İnsan vücudu çizimi (basitleştirilmiş şekil)
    spine_x = [0, 0]  # Omurga x-koordinatı
    spine_y = np.linspace(0, 10, 100)  # Omurga y-koordinatı

    # Skolyoz eğriliği simülasyonu
    curvature = scoliosis_angle / 100 * np.sin(2 * np.pi * spine_y / 10)  # Sinüs eğrisi ile eğrilik oluşturma
    ax.plot(spine_x + curvature, spine_y, color="red", label="Skolyoz Eğrisi")

    # Vücudu temsil eden basit şekiller
    ax.plot([-1, 1], [10, 10], color="blue", linewidth=4, label="Omuzlar")
    ax.plot([-0.5, 0.5], [0, 0], color="blue", linewidth=6, label="Kalça")

    # Vücut görünümü için bazı detaylar
    ax.plot([0, 0], [0, 10], color="black", linestyle="--", label="Düz Omurga (Referans)")

    # Görselleştirme ayarları
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 11)
    ax.set_title("Skolyoz Simülasyonu")
    ax.set_xlabel("Omurga Eğriliği (cm)")
    ax.set_ylabel("Vücut Uzunluğu (cm)")
    ax.legend()
    ax.axis("off")  # Eksenleri kaldırma

    # Streamlit'e grafiği ekle
    st.pyplot(fig)
