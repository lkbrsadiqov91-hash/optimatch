import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Tətbiq Konfiqurasiyası
st.set_page_config(
    page_title="OptiMatch — Optimizasiya Və Ədalətli Bölüşdürmə Modeli",
    page_icon="https://raw.githubusercontent.com/lkbrsadiqov91-hash/optimatch/main/icon.png",
    layout="wide"
)

# PWA və Mobil Tam Ekran Dəstəyi
st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="OptiMatch">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="display" content="standalone">
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/lkbrsadiqov91-hash/optimatch/main/icon.png">
        <link rel="manifest" href="data:application/json,{%22name%22:%22OptiMatch%22,%22short_name%22:%22OptiMatch%22,%22start_url%22:%22/%22,%22display%22:%22standalone%22,%22background_color%22:%22%23ffffff%22,%22theme_color%22:%22%23ffffff%22,%22icons%22:[{%22src%22:%22https://raw.githubusercontent.com/lkbrsadiqov91-hash/optimatch/main/icon.png%22,%22sizes%22:%22192x192%22,%22type%22:%22image/png%22}]}">
    </head>
""", unsafe_allow_html=True)

st.title("⚽ OptiMatch — Optimizasiya Və Ədalətli Bölüşdürmə Modeli")
st.markdown("Karabakh State University | Mathematics Education Project")
st.markdown("---")

# Naviqasiya Menyusu (Bütün bölmələr bir yerdə)
tab1, tab2, tab3 = st.tabs([
    "🏆 UEFA İsveçrə Sistemi (Liqa)", 
    "🎓 Universitet Pley-off Turniri", 
    "👥 Ədalətli Qrup Bölgüsü (GPA / Bal Sistemi)"
])

# ==========================================
# TAB 1: UEFA İsveçrə Sistemi və Klub Yorğunluq Analizi
# ==========================================
with tab1:
    st.subheader("📊 Klub Yorğunluğu, Bərpa və Təqvim Optimizasiyası (Sports Science)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        team_name = st.selectbox("Təhlil Ediləcək Komanda:", ["Arsenal", "Real Madrid", "Mançester Siti", "Qarabağ FK", "Sabah FK", "Bavariya Münhen"])
        last_match_date = st.date_input("Son Oynadığı Oyun Tarixi:", datetime.now() - timedelta(days=3), key="cl_start_date")

    with col2:
        injured_players = st.number_input("Zədəli Oyunçu Sayı:", min_value=0, max_value=15, value=2, key="cl_injured")
        fatigue_level = st.slider("Cari Yorğunluq Faizi (%):", min_value=0, max_value=100, value=65, key="cl_fatigue")

    with col3:
        next_opponent = st.selectbox("Növbəti Rəqib:", ["Liverpul", "Barselona", "Çelsi", "Napoli", "Borussiya Dortmund"], key="cl_opp")
        min_recovery_days = st.number_input("Optimal İstirahət Gün Limiti:", min_value=2, max_value=7, value=4, key="cl_rec")

    if st.button("🚀 8 Rəqib Seç Və Liqa Təqvimi Yarat", type="primary", key="cl_btn"):
        today = datetime.now().date()
        days_passed = (today - last_match_date).days
        
        st.markdown("---")
        st.subheader(f"🛡️ {team_name} üçün 8 Rəqibli Təqvim Analizi")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col1:
            st.metric(label="Son Oyundan Keçən Vaxt", value=f"{days_passed} gün")
            if days_passed < min_recovery_days:
                st.error(f"⚠️ Kritik Risk! Komanda hələ tam bərpa olmayıb (Minimum {min_recovery_days} gün lazımdır).")
            else:
                st.success("✅ Komanda fiziki olaraq dincəlib.")
                
        with res_col2:
            adjusted_fatigue = min(100, max(0, fatigue_level - (days_passed * 10) + (injured_players * 3)))
            st.metric(label="Növbəti Oyun Üçün Yorğunluq", value=f"%{adjusted_fatigue}")
            
        with res_col3:
            base_win_chance = 60
            win_chance = max(15, min(95, base_win_chance - (adjusted_fatigue * 0.4) - (injured_players * 5)))
            if days_passed >= min_recovery_days:
                win_chance += 10
                
            st.metric(label=f"{next_opponent} ilə Görüşdə Qələbə Şansı", value=f"%{round(win_chance, 1)}")

        # Simulyasiya olunmuş İsveçrə sistemi təqvimi
        st.markdown("### 📅 İsveçrə Sistemi 8 Rəqibli Təqvim Simulyasiyası:")
        opponents_pool = ["Liverpul", "Barselona", "Çelsi", "Napoli", "Borussiya Dortmund", "Milan", "Inter", "Atletiko Madrid"]
        selected_opponents = random.sample(opponents_pool, 4)
        
        schedule = []
        current_date = last_match_date
        for i, opp in enumerate(selected_opponents, 1):
            rest_days = random.randint(3, 6)
            current_date += timedelta(days=rest_days)
            match_type = "Evdə (Home)" if i % 2 != 0 else "Səfərdə (Away)"
            schedule.append({
                "Oyun": f"Tur {i}",
                "Rəqib": opp,
                "Ev/Səfər": match_type,
                "Təyin Olunan Tarix": current_date.strftime("%Y-%m-%d"),
                "İstirahət Günü": f"{rest_days} gün"
            })
            
        df_schedule = pd.DataFrame(schedule)
        st.dataframe(df_schedule, use_container_width=True)

# ==========================================
# TAB 2: Universitet Pley-off Turniri
# ==========================================
with tab2:
    st.subheader("🎓 Universitet İntellektual və İdman Pley-off Toru")
    num_teams = st.selectbox("Komanda Sayı:", [4, 8, 16], key="playoff_num")
    
    if st.button("Pley-off Cədvəlini Qur", key="playoff_btn"):
        st.success(f"{num_teams} komandalı universitet pley-off mərhələsi uğurla generasiya edildi!")
        if num_teams == 4:
            st.markdown("### 🏆 Yarımfinal və Final")
            st.write("1. Qarabağ Universiteti vs ADA Universiteti")
            st.write("2. BDU vs UNEC")
            st.info("Qaliblər Böyük Finalda qarşılaşacaqlar!")
        elif num_teams == 8:
            st.markdown("### 🏆 1/4 Final, Yarımfinal və Final mərhələləri hazırdır.")

# ==========================================
# TAB 3: Ədalətli Qrup Bölgüsü (GPA / Bal Sistemi)
# ==========================================
with tab3:
    st.subheader("👥 Tələbələrin GPA və Bal Səviyyəsinə Görə Ədalətli Qruplara Bölünməsi")
    
    num_groups = st.number_input("Yaradılacaq Qrup Sayı:", min_value=2, max_value=6, value=4)
    
    students_data = [
        {"Ad": "Əli", "Bal": 95}, {"Ad": "Valide", "Bal": 92}, {"Ad": "Məhəmməd", "Bal": 91}, {"Ad": "Leyla", "Bal": 94},
        {"Ad": "Nigar", "Bal": 85}, {"Ad": "Rauf", "Bal": 78}, {"Ad": "Orxan", "Bal": 82}, {"Ad": "Sevinc", "Bal": 75},
        {"Ad": "Murad", "Bal": 88}, {"Ad": "Aysel", "Bal": 71}, {"Ad": "Elvin", "Bal": 62}, {"Ad": "Həsən", "Bal": 55},
        {"Ad": "Kənan", "Bal": 68}, {"Ad": "Zəhra", "Bal": 58}, {"Ad": "Nicat", "Bal": 45}, {"Ad": "Aytən", "Bal": 48}
    ]
    
    if st.button("Qrupları Ədalətli Böl (GPA Balansı)", key="group_btn"):
        sorted_students = sorted(students_data, key=lambda x: x["Bal"], reverse=True)
        groups = [[] for _ in range(num_groups)]
        
        for i, student in enumerate(sorted_students):
            group_idx = i % num_groups if (i // num_groups) % 2 == 0 else num_groups - 1 - (i % num_groups)
            groups[group_idx].append(student)
            
        g_cols = st.columns(num_groups)
        for idx, group in enumerate(groups):
            with g_cols[idx]:
                st.markdown(f"#### Qrup {idx + 1}")
                avg_score = sum(s["Bal"] for s in group) / len(group)
                st.caption(f"Ortalama Bal: {round(avg_score, 1)}")
                for s in group:
                    st.write(f"- {s['Ad']} ({s['Bal']} bal)")
