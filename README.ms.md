# Tcl untuk VLSI · Daripada Sintaks Asas hingga Penskripan DRV

<p align="center">
  <a href="README.md">English</a> · 
  <a href="README.zh.md">简体中文</a> · 
  <b>Bahasa Melayu</b> · 
  <a href="README.fr.md">Français</a>
</p>

[![Lesen: CC BY 4.0](https://img.shields.io/badge/Lesen-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub](https://img.shields.io/badge/GitHub-SJTU--YONGFU--RESEARCH--GRP%2Ftcl--language-181717?logo=github)](https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language)
[![Taman Permainan Kod](https://img.shields.io/badge/Playground-Sifar--Pemasangan-17776b?logo=javascript&logoColor=white)](https://sjtu-yongfu-research-grp.github.io/tcl-language/playground/)
[![DRV-Lite](https://img.shields.io/badge/DRV--Lite-Sifar--Lesen_Sim_SusunAtur-0f4f46)](docs/DRVLITE_HELP.md)
[![Makmal STA](https://img.shields.io/badge/Makmal_STA-Margin_Slack-b96b28)](docs/TIMING_ANALYZER_LAB.md)
[![Pelbagai Bahasa](https://img.shields.io/badge/i18n-EN%20%7C%20ZH%20%7C%20MS%20%7C%20FR-blue)](https://sjtu-yongfu-research-grp.github.io/tcl-language/ms/)

Platform pendidikan dan latihan amali **Penskripan Tcl untuk VLSI** yang mesra pemula, merangkumi sintaks Tcl moden, struktur data, pengaturcaraan berorientasikan objek (TclOO), serta aplikasi penskripan industri dalam susun atur IC, analisis pelanggaran peraturan reka bentuk (DRV), dan analisis pemasaan statik (STA).

---

## 🌟 Ciri-Ciri Utama & Alat Interaktif (Core Features)

Menggabungkan amalan pengajaran sumber terbuka daripada Shanghai Jiao Tong University dengan alat praktikal dan reka bentuk interaktif:

1. **⚡ Taman Permainan Kod Web Interaktif (Interactive Web Playground)**:
   - Sifar pemasangan persekitaran tempatan, 100% dilaksanakan dalam pelayar web tanpa bergantung pada pelayan luaran.
   - Dilengkapi templat pratetap: model penggantian Welch, expr selamat berkurung, senarai, kamus, penguraian STA, dan penskripan susun atur DRV-Lite.
   - [👉 Buka Taman Permainan Kod Web Sekarang](https://sjtu-yongfu-research-grp.github.io/tcl-language/playground/)

2. **📐 DRV-Lite: Simulator Susun Atur Tulin Tcl & Visualiser Dalam Talian**:
   - Sifar lesen komersial EDA diperlukan! Model objek `layout` tulin Tcl untuk memanipulasi poligon, pin, lapisan, dan koordinat susun atur mikron.
   - Dilengkapi [📐 Visualiser Susun Atur VLSI Interaktif](https://sjtu-yongfu-research-grp.github.io/tcl-language/help/layout_viewer/), menyokong zum, sorot, serta pelaksanaan perintah Tcl gaya CalibreDRV (`create`, `delete`, `bbox`, `iterator count`, `shift`, `scale`, dll.).

3. **⚡ Analisis Pemasaan Statik (STA) & Penjaga Pintu Tapeout**:
   - Menghurai laporan pemasaan sebenar (`data/sample_timing.rpt`), mengira Worst Negative Slack (WNS) dan Total Negative Slack (TNS).
   - Dilengkapi [⚡ Penjaga Masa STA Interaktif](https://sjtu-yongfu-research-grp.github.io/tcl-language/help/timing_calculator/) untuk melaraskan tempoh jam, kelewatan logik gabungan, dan ketidakpastian jam secara dinamik bagi menentukan kelulusan pita keluar (tapeout).

4. **🎯 18 Latihan Data Kejuruteraan (54 Tugas Bertingkat) & Skema Jawapan**:
   - Merangkumi penggantian pembolehubah, pengisihan senarai, kamus bersarang, padanan regex, penghuraian fail, penukaran CSV/JSON, hingga pengagregatan medan berbilang.
   - Menggunakan set data kejuruteraan sebenar: `data/chip_runs.csv`, `data/top10_servers.tsv`, `data/wafers.csv`, `data/weather_beijing.json`, dll.
   - Templat latihan (`exercises/`) dan jawapan rujukan lengkap (`solutions/`).

5. **🏆 6 Projek Capstone Kejuruteraan Data (Projek A–F)**:
   - **Projek A**: Statistik log akses Nginx/Apache & penapisan amaran
   - **Projek B**: Pengagregatan hasil ujian wafer & pengelasan kecacatan
   - **Projek C**: Penjanaan laporan metrik komit repositori Git
   - **Projek D**: Penyelarasan aliran jualan dan inventori berbilang jadual
   - **Projek E**: Saluran pembersihan & penukaran format data JSON/CSV
   - **Projek F**: Penghuraian laporan teks EDA & analisis pelanggaran susun atur DRV
   - Dilengkapi set kes ujian penegasan (`case-1.tcl` hingga `case-4.tcl`).

6. **🧠 Model Mental 3-Langkah Tcl**:
   - Mengikuti model `Pengelompokan (Grouping)` $\to$ `Penggantian (Substitution)` $\to$ `Seruan (Invocation)` untuk memahami perbezaan antara kurungan kerinting `{}` dan tanda petikan `""`, serta amalan selamat `expr {$a + $b}`.

7. **🎯 Cabaran Kuiz & Papan Pendahulu Awam**:
   - 4 modul penilaian dengan pensijilan digital yang boleh disahkan dan paparan papan juara komuniti secara langsung.

---

## 📚 Pelan Kurikulum 40 Pelajaran (Curriculum Roadmap)

- **M10: Sintaks Teras Tcl (Pelajaran 01–10)**: Perintah asas, pembolehubah, kawalan aliran, prosedur `proc`, senarai, dan model mental penilaian tiga langkah.
- **M20: Kelancaran Pengaturcaraan & Perekat Alat (Pelajaran 11–20)**: Kamus `dict`, I/O fail, ungkapan nalar (regex), ruang nama `namespace`, dan pengaturcaraan berorientasikan objek `TclOO`.
- **M30: Teras Susun Atur Calibre (Pelajaran 21–30)**: Simulator susun atur tulin Tcl DRV-Lite, penciptaan lapisan, poligon geometri, dan interaksi perintah CalibreDRV.
- **M40: Katalog Susun Atur & Sign-Off Industri (Pelajaran 31–40)**: Analisis pemasaan STA, pengekstrakan DEF/LEF, pengauditan pelanggaran DRV, dan automasi pembaikan ECO.

---

## 🚀 Panduan Mula Pantas (Quick Start)

### 1. Keperluan Persekitaran
- **Pelajaran 1–20**: Pasang [`tclsh`](https://www.tcl.tk/) dalam terminal tempatan (Tcl 8.5/8.6/9.0).
- **Pelajaran 21–40**: `calibredrv` komersial **atau** simulator tulin Tcl **DRV-Lite** (kemunduran automatik disokong sepenuhnya).

### 2. Klon Repositori & Perintah Biasa

```bash
git clone https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language.git
cd tcl-language

# Sahkan persekitaran tempatan & status DRV-Lite
make check-env

# Jalankan 6 ujian unit simulator susun atur DRV-Lite
make drvlite-test

# Jalankan makmal analisis pemasaan statik STA
make timing-demo

# Jalankan contoh skrip Pelajaran 1
make week1-01

# Jalankan skrip susun atur Pelajaran 21 (simulasi DRV-Lite)
make week21-01

# Jalankan skema jawapan latihan & projek capstone
tclsh solutions/01/01.tcl
(cd capstone/A && tclsh solution.tcl)
```

### 3. Bina Laman Dokumentasi Tempatan

```bash
make site-install    # Pasang kebergantungan Python & MkDocs
make site            # Jana dokumentasi statik & laman pelbagai bahasa
make site-serve      # Pratonton tempatan di http://127.0.0.1:8000
```

---

## 📁 Struktur Repositori (Repository Layout)

```text
tcl-language/
├── PLAN.md                 # Sukatan pelajaran 40 minggu & pelan kemajuan
├── Makefile                # Pelari kursus, skrip ujian unit & pembina laman
├── data/                   # Set data industri sebenar (wafer, log pelayan, STA)
├── exercises/              # 18 templat permulaan latihan amali (54 tugas)
├── solutions/              # 18 skema jawapan rujukan piawai
├── capstone/               # 6 projek kejuruteraan data (A–F bersama kes ujian)
├── homework/               # Set soalan latihan kerja rumah & pengesah
├── quiz/                   # Bank soalan kuiz & cabaran pensijilan
├── lessons/                # 40 pelajaran dwibahasa & 100+ skrip contoh boleh laksana
├── examples/               # Contoh industri seperti timing_report_analyzer.tcl
├── docs/                   # Dokumen panduan TCL_HELP.md, DRVLITE_HELP.md
├── tools/
│   ├── drvlite/            # Simulator susun atur Calibre DESIGNrev tulin Tcl
│   └── ...                 # Alat analisis sintaks & perintah
└── website/                # Fail sumber tapak MkDocs & dokumentasi i18n
```

---

## 👥 Penghargaan Penyumbang (Contributors)

Penghargaan khusus kepada pasukan penyelidik, pengajar, dan pelajar (mengikut susunan abjad ID GitHub):

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/yongfu-li">
        <img src="https://avatars.githubusercontent.com/u/10367890?v=4" width="80" height="80" alt="yongfu-li"/><br/>
        <sub><b>Li Yongfu</b></sub><br/>
        <sub>@yongfu-li</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Capeur">
        <img src="https://avatars.githubusercontent.com/u/197603203?v=4" width="80" height="80" alt="Capeur"/><br/>
        <sub><b>David MUY</b></sub><br/>
        <sub>@Capeur</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/FanqinZeng">
        <img src="https://avatars.githubusercontent.com/u/151010024?v=4" width="80" height="80" alt="FanqinZeng"/><br/>
        <sub><b>FanQin Zeng</b></sub><br/>
        <sub>@FanqinZeng (WASM & Exercises)</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/GateUltra">
        <img src="https://avatars.githubusercontent.com/u/138369042?v=4" width="80" height="80" alt="GateUltra"/><br/>
        <sub><b>GateUltra</b></sub><br/>
        <sub>@GateUltra (Homeworks)</sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/muranfei">
        <img src="https://avatars.githubusercontent.com/u/31174606?v=4" width="80" height="80" alt="muranfei"/><br/>
        <sub><b>muranfei</b></sub><br/>
        <sub>@muranfei</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/stephQ-lab">
        <img src="https://avatars.githubusercontent.com/u/186373504?v=4" width="80" height="80" alt="stephQ-lab"/><br/>
        <sub><b>stephQ-lab</b></sub><br/>
        <sub>@stephQ-lab</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Su3037">
        <img src="https://avatars.githubusercontent.com/u/154591477?v=4" width="80" height="80" alt="Su3037"/><br/>
        <sub><b>Supan</b></sub><br/>
        <sub>@Su3037</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/thy031">
        <img src="https://avatars.githubusercontent.com/u/188567228?v=4" width="80" height="80" alt="thy031"/><br/>
        <sub><b>thy031</b></sub><br/>
        <sub>@thy031 (Quizzes)</sub>
      </a>
    </td>
  </tr>
</table>

Lihat [`CONTRIBUTORS.md`](CONTRIBUTORS.md) dan [Direktori Penyumbang](https://sjtu-yongfu-research-grp.github.io/tcl-language/ms/contributors/) dalam talian.

---

## 📜 Lesen (License)

- Kandungan kurikulum dan dokumentasi dilesenkan di bawah [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- Kod sumber skrip dan alat simulasi dilesenkan di bawah [Lesen MIT](LICENSE).
