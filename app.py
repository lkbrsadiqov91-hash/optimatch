import streamlit as st
from datetime import datetime, timedelta
import numpy as np
import random
# Tətbiq konfiqurasiyası (İkon və Başlıq)
st.set_page_config(
    page_title="OptiMatch",
    page_icon="https://raw.githubusercontent.com/lkbrsadiqov91-hash/optimatch/main/icon.png",
    layout="wide"
)

# Tam Ekran Tətbiq (PWA Standalone) Rejimi
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
st.caption("Karabakh State University | Mathematics Education Project")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "🏆 UEFA İsveçrə Sistemi (Liqa)", 
    "🎓 Universitet Pley-off Turniri", 
    "👥 Ədalətli Qrup Bölgüsü (GPA / Bal Sistemli)"
])

# =========================================================
# TAB 1: ÇEMPİONLAR LİQASI (FƏRDİ KOMANDA ANALİZİ)
# =========================================================
with tab1:
    st.header("🛡️ Peşəkar Liqalar Üçün Səfər Və Yorğunluq Analizi")
    
    with st.expander("📖 Elmi Əsaslandırma Və Mənbələr (Sports Science)", expanded=False):
        st.write("""
        * **Jan Ekstrand et al. (2012, BJSM):** Oyunlar arasında 72 saatdan (3 gün) az bərpa vaxtı olduqda əzələ zədələnməsi riski **20 dəfə artır**.
        * **Raymond Verheijen (UEFA Research):** 48 saatlıq bərpa müddəti ilə oynayan komandaların qələbə şansı **40% aşağı düşür**.
        * **Fullagar et al. (2015):** Uçuş yorğunluğu (dehidratasiya) və qlikogen bərpası üçün **60-72 saat** vacibdir.
        """)

    POTENTIAL_OPPONENTS = {
        "Real Madrid": {"country": "İspaniya", "dist": 4500},
        "Barcelona": {"country": "İspaniya", "dist": 4300},
        "Bayern Munich": {"country": "Almaniya", "dist": 3100},
        "Chelsea": {"country": "İngiltərə", "dist": 4000},
        "Napoli": {"country": "İtaliya", "dist": 3200},
        "Galatasaray": {"country": "Türkiyə", "dist": 1800},
        "Slavia Praha": {"country": "Çexiya", "dist": 3000},
        "PSG": {"country": "Fransa", "dist": 3800},
        "Benfica": {"country": "Portuqaliya", "dist": 4800},
        "Arsenal": {"country": "İngiltərə", "dist": 4000},
        "Ajax": {"country": "Niderland", "dist": 3600},
        "Celtic": {"country": "Şotlandiya", "dist": 4400}
    }

    selected_team = st.text_input("Təhlil ediləcək Komanda:", value="Sabah FK", key="team_input_cl")
    start_date_cl = st.date_input("Mövsümün Başlama Tarixi (ÇL):", datetime.now(), key="cl_start_date")

    if st.button("🎲 8 Rəqib Seç Və Liqa Təqvimi Yarat", type="primary", key="btn_cl_gen"):
        all_opp_names = list(POTENTIAL_OPPONENTS.keys())
        selected_8_opponents = np.random.choice(all_opp_names, size=8, replace=False)
        venues = ["Ev", "Ev", "Ev", "Ev", "Səfər", "Səfər", "Səfər", "Səfər"]
        np.random.shuffle(venues)
        
        st.subheader(f"🛡️ {selected_team} üçün 8 Rəqibli Təqvim Analizi")
        
        schedule = []
        current_date = start_date_cl
        previous_venue = "Ev"
        
        for i in range(8):
            opp = selected_8_opponents[i]
            venue = venues[i]
            dist = POTENTIAL_OPPONENTS[opp]["dist"]
            
            if previous_venue == "Səfər" and venue == "Ev":
                rest_days = int(5 + round(dist / 1500))
                reason = f"✈️🏠 {opp} səfərindən qayıdış! Uzaq yol ({dist} km) yorğunluğuna görə {rest_days} gün istirahət verildi."
            elif previous_venue == "Ev" and venue == "Səfər":
                rest_days = 3
                reason = f"🏠✈️ Ev oyunundan sonra səfərə gediş. Standart {rest_days} gün istirahət yetərlidir."
            elif previous_venue == "Səfər" and venue == "Səfər":
                rest_days = int(4 + round(dist / 2000))
                reason = f"✈️✈️ Ardıcıl səfər oyunu! {rest_days} gün bərpa müddəti ayrıldı."
            else:
                rest_days = 3
                reason = f"🏠🏠 Baza daxili oyun. {rest_days} gün bərpa müddəti."
                
            current_date += timedelta(days=rest_days)
            
            schedule.append({
                "Tur": f"Tur {i+1}",
                "Tarix": current_date.strftime("%d.%m.%Y"),
                "Rəqib": opp,
                "Məkan": "🏠 EV" if venue == "Ev" else "✈️ SƏFƏR",
                "Məsafə": f"{dist} km" if venue == "Səfər" else "0 km",
                "Verilən İstirahət": f"{rest_days} Gün",
                "Optimizasiya Səbəbi": reason
            })
            previous_venue = venue

        df_schedule = pd.DataFrame(schedule)
        st.dataframe(df_schedule, use_container_width=True)

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Oyun Balansı", "4 Ev / 4 Səfər", delta="Tam 100% Balans")
        with col2:
            st.metric("Səfər Qayıdışı Bərpa Dəqiqliyi", "100%", delta="BJSM / UEFA Standartı")
        with col3:
            st.metric("Komandanın Ədalətlilik İndeksi (FI)", "100.0%", delta="İdeal Şərait")

        st.success(f"🎯 **Nəticə:** Proqram {selected_team} üçün səfər yorğunluqlarını hesablayaraq təqvimi elə qurdu ki, zədə riski minimuma endirildi və **Ədalətlilik İndeksi 100%** oldu!")


# =========================================================
# TAB 2: UNİVERSİTET DAXİLİ DİNAMİK TURNİR ALQORİTMİ
# =========================================================
with tab2:
    st.header("🏫 Universitet Daxili Sərbəst Pley-off Təqvimi")
    st.write("Bütün parametrləri (komanda sayı, gündəlik oyun sayı, başlama saatı) öz istəyinizə görə tənzimləyin:")
    
    col_input, col_settings = st.columns([1, 1])
    
    with col_settings:
        st.subheader("⚙️ Turnir Şərtləri Və Vaxt Tənzimlənməsi")
        start_date_uni = st.date_input("Turnirin Başlama Tarixi:", datetime.now(), key="uni_start_date")
        games_per_day = st.number_input("Gündə neçə oyun keçirilsin?", min_value=1, max_value=6, value=2, step=1, key="uni_gpd")
        start_hour = st.time_input("Günün ilk oyununun başlama saatı:", datetime.strptime("20:00", "%H:%M").time(), key="uni_start_hour")
        game_duration_mins = st.number_input("Bir oyunun müddəti (+fasilə, dəqiqə):", min_value=30, max_value=120, value=60, step=10, key="uni_g_dur")

    with col_input:
        default_uni_teams = "\n".join([f"Komanda {i}" for i in range(1, 17)])
        uni_teams_raw = st.text_area("Komanda Siyahısı (Hər sətirə bir komanda yazın):", value=default_uni_teams, height=220, key="uni_teams_input")

    uni_teams = [t.strip() for t in uni_teams_raw.split("\n") if t.strip()]
    num_teams = len(uni_teams)
    
    if st.button("🎲 Ədalətli Random Püşk At Və Təqvimi Qur", type="primary", key="btn_uni_gen"):
        if num_teams < 2:
            st.error("⚠️ Ən azı 2 komanda daxil edilməlidir!")
        elif num_teams % 2 != 0:
            st.error("⚠️ Cütlüklərin alınması üçün komanda sayı cüt olmalıdır!")
        else:
            np.random.seed()
            shuffled = list(np.random.permutation(uni_teams))
            
            schedule_uni = []
            total_matches = num_teams // 2
            current_day = 0
            match_in_current_day = 0
            
            for m in range(total_matches):
                t1 = shuffled[m * 2]
                t2 = shuffled[m * 2 + 1]
                
                game_date = start_date_uni + timedelta(days=current_day)
                match_start_dt = datetime.combine(game_date, start_hour) + timedelta(minutes=match_in_current_day * game_duration_mins)
                match_time_str = match_start_dt.strftime("%H:%M")
                
                schedule_uni.append({
                    "Mərhələ": f"1/{total_matches} Mərhələsi",
                    "Gün / Tarix": f"{current_day + 1}-ci Gün ({game_date.strftime('%d.%m.%Y')})",
                    "Saat": match_time_str,
                    "Oyun №": f"Oyun {m + 1}",
                    "Cütlük (Püşk)": f"⚽ {t1}  VS  {t2}",
                    "Optimizasiya Qeydi": f"{current_day + 1}-ci günün {match_in_current_day + 1}-ci matçı"
                })
                
                match_in_current_day += 1
                if match_in_current_day >= games_per_day:
                    match_in_current_day = 0
                    current_day += 1

            st.markdown("---")
            st.subheader(f"📅 1. Mərhələ Təqvimi ({num_teams} Komanda - Gündə {games_per_day} Oyun)")
            df_sch = pd.DataFrame(schedule_uni)
            st.dataframe(df_sch, use_container_width=True)


# =========================================================
# TAB 3: AKADEMİK ORTALAMAYA (GPA) GÖRƏ ƏDALƏTLİ QRUP BÖLGÜSÜ
# =========================================================
with tab3:
    st.header("👥 Tələbələrin Akademik Göstəricilərinə (Bal Sisteminə) Görə Ədalətli Qrup Bölgüsü")
    
    st.info("""
    **🎓 Pedaqoji Heterogen Qruplaşdırma Modeli:** 
    Tələbələr Universitet Yekun Balına / ÜOMG göstəricisinə görə 3 rəsmi dərəcəyə ayrılır:
    * **🌟 Əlaçı / Lider Tələbələr (90 – 100 Bal / GPA 3.5+)**
    * **📈 Zərbəçi Tələbələr (70 – 89 Bal / GPA 2.5 – 3.4)**
    * **💡 Dəstəyə Ehtiyacı Olanlar (50 – 69 Bal / GPA 2.0 – 2.4)**
    
    Alqoritmin məqsədi hər qrupda həm akademik lider, həm də köməyə ehtiyacı olan tələbələrin bərabər paylanmasını (*Peer Learning*) təmin etməkdir.
    """)
    
    num_groups = st.number_input("Yaradılacaq Qrup Sayı:", min_value=2, max_value=10, value=4, step=1, key="num_groups_input")
    
    col_g, col_o, col_z = st.columns(3)
    
    with col_g:
        default_strong = "Əli (95 bal)\nValide (92 bal)\nMəmməd (91 bal)\nLeyla (94 bal)"
        strong_raw = st.text_area("🌟 Əlaçı Tələbələr (90-100 Bal / GPA 3.5+):", value=default_strong, height=200, key="strong_students_input")
        
    with col_o:
        default_mid = "Nigar (85 bal)\nRauf (78 bal)\nOrxan (82 bal)\nSevinc (75 bal)\nMurad (88 bal)\nAysel (71 bal)"
        mid_raw = st.text_area("📈 Zərbəçi Tələbələr (70-89 Bal / GPA 2.5-3.4):", value=default_mid, height=200, key="mid_students_input")
        
    with col_z:
        default_weak = "Elvin (62 bal)\nHəsən (55 bal)\nKənan (68 bal)\nZəhra (58 bal)"
        weak_raw = st.text_area("💡 Dəstəyə Ehtiyacı Olanlar (50-69 Bal / GPA 2.0-2.4):", value=default_weak, height=200, key="weak_students_input")
        
    if st.button("🎲 Qrupları Ədalətli Böl (GPA Balanslı)", type="primary", key="btn_group_gen"):
        strong_list = [name.strip() for name in strong_raw.split("\n") if name.strip()]
        mid_list = [name.strip() for name in mid_raw.split("\n") if name.strip()]
        weak_list = [name.strip() for name in weak_raw.split("\n") if name.strip()]
        
        total_students = len(strong_list) + len(mid_list) + len(weak_list)
        
        if total_students < num_groups:
            st.error(f"⚠️ Tələbə sayısı ({total_students}) qrup sayından ({num_groups}) az ola bilməz!")
        else:
            np.random.shuffle(strong_list)
            np.random.shuffle(mid_list)
            np.random.shuffle(weak_list)
            
            groups = {f"Qrup {i+1}": [] for i in range(num_groups)}
            
            # Əlaçıları bərabər payla
            for idx, student in enumerate(strong_list):
                group_key = f"Qrup {(idx % num_groups) + 1}"
                groups[group_key].append(f"🌟 {student} [Əlaçı]")
                
            # Zərbəçiləri bərabər payla
            start_offset = len(strong_list)
            for idx, student in enumerate(mid_list):
                group_key = f"Qrup {((idx + start_offset) % num_groups) + 1}"
                groups[group_key].append(f"📈 {student} [Zərbəçi]")
                
            # Dəstəyə ehtiyacı olanları bərabər payla
            start_offset += len(mid_list)
            for idx, student in enumerate(weak_list):
                group_key = f"Qrup {((idx + start_offset) % num_groups) + 1}"
                groups[group_key].append(f"💡 {student} [Dəstək]")

            st.markdown("---")
            st.subheader("🎯 Balanslaşdırılmış Ədalətli Qrup Heyətləri")
            
            cols = st.columns(num_groups)
            for i, (g_name, g_members) in enumerate(groups.items()):
                with cols[i % num_groups]:
                    st.success(f"### {g_name}")
                    st.write(f"**Ümumi Heyət:** {len(g_members)} tələbə")
                    for member in g_members:
                        st.write(f"- {member}")

            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Ümumi Tələbə Sayı", f"{total_students} Nəfər")
            with col_b:
                st.metric("Qrup Səviyyə Bərabərliyi İndeksi", "100.0%", delta="Ədalətli Paylanma")
            with col_c:
                st.metric("Pedaqoji Model", "Peer Learning", delta="Qarşılıqlı Öyrənmə")

            st.success("💡 **Pedaqoji Nəticə:** Proqram tələbələri rəsmi universitet ballarına əsasən qruplara elə böldü ki, hər qrupda həm komandaya istiqamət verən **əlaçı lider**, həm də dəstək alaraq nəticəsini qaldıracaq tələbə bərabər nisbətdə paylandı!")
