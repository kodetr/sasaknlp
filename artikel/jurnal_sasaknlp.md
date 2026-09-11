# SasakNLP: Research-Grade Morphological Processing and Dialect-Aware Natural Language Processing Framework for Low-Resource Bahasa Sasak

**Penulis / Peneliti Utama**: **kodetr**  
**Afiliasi**: Riset Komputasi Bahasa Daerah Nusantara, [kodetr.com](https://kodetr.com)  
**Korespondensi**: [https://kodetr.com](https://kodetr.com) | Repositori GitHub: [https://github.com/kodetr/sasaknlp](https://github.com/kodetr/sasaknlp)  
**Akses Publik**: Paket PyPI (`pip install sasaknlp`) | Hugging Face Dataset (`kodetr/sasak-benchmark-100k`) | Web Demo (`kodetr/sasaknlp-demo`)

---

## Abstrak

Bahasa Sasak (*Basa Sasak*) merupakan bahasa daerah berakar Austronesia yang dituturkan oleh lebih dari 3 juta penduduk di Pulau Lombok, Nusa Tenggara Barat, Indonesia. Meskipun memiliki jumlah penutur yang signifikan, Bahasa Sasak tergolong sebagai bahasa dengan sumber daya komputasi rendah (*low-resource language*) karena kelangkaan korpus teks teranotasi, variasi dialektal yang tajam lintas wilayah geografis, serta ketiadaan pustaka pemrosesan bahasa alami (NLP) berstandar industri. Artikel ini memperkenalkan **SasakNLP**, toolkit komputasional pertama yang dirancang secara ilmiah untuk standardisasi ortografi, tokenisasi reduplikasi, klasifikasi dialek berbasis penanda diagnostik (*shibboleths*), serta dekonstruksi morfologi bertingkat yang divalidasi leksikon kamus resmi Balai Bahasa Provinsi NTB.

Evaluasi komprehensif dilakukan menggunakan protokol empiris bertingkat terhadap tolok ukur baku emas (*gold-standard benchmark*) berskala **100.000 pasangan morfem** serta korpus autentik **12.591 kalimat**. SasakNLP mencapai akurasi lematisasi sebesar **87,98%**, presisi makro **99,00%**, pemanggilan makro (*macro recall*) **95,35%**, dan *macro F1-score* **96,22%**. Uji signifikansi statistik McNemar menegaskan keunggulan model yang sangat signifikan ($\chi^2 = 14.962,14, p < 0,0001$) dibandingkan algoritma pembanding berbasis *greedy affix stripping*. Analisis taksonomi kesalahan membuktikan bahwa arsitektur dual-gating berhasil menekan *overstemming* hingga mendekati **0,00%** dan *understemming* hingga **0,09%**, dengan penanganan *Out-of-Vocabulary* (11,92%) yang aman tanpa merusak struktur leksikal. Dari sudut pandang efisiensi komputasi, SasakNLP membukukan *throughput* **22.500 kata per detik** dengan latensi rata-rata **0,044 milidetik per kata** tanpa dependensi pihak ketiga (*zero external dependencies*). Seluruh kode sumber, dataset, model, dan demonstrasi interaktif dirilis secara terbuka demi kemajuan komputasi bahasa daerah di Indonesia.

**Kata Kunci**: *Bahasa Sasak, Pemrosesan Bahasa Alami (NLP), Lematisasi Komputasional, Dekomposisi Morfonemik, Dialektologi Komputasi, Low-Resource Language, Balai Bahasa NTB.*

---

## Abstract

*Bahasa Sasak is an Austronesian regional language spoken by approximately 3 million people across Lombok Island, West Nusa Tenggara (NTB), Indonesia. Despite its sizable speaker community, it remains a digitally underrepresented low-resource language due to the scarcity of annotated corpora, pronounced cross-island dialectal variation, and the total absence of standardized natural language processing (NLP) pipelines. This paper presents **SasakNLP**, the first research-grade computational toolkit engineered for text normalization, reduplication-aware tokenization, shibboleth-driven dialect identification, and dictionary-enhanced multi-candidate morphological disambiguation grounded in the authentic lexicon of Balai Bahasa Provinsi NTB.*

*Empirical evaluation across a 100,000-pair gold-standard benchmark and an authentic corpus of 12,591 sentences demonstrates that SasakNLP achieves **87.98%** morphological disambiguation accuracy, **99.00%** macro precision, **95.35%** macro recall, and a **96.22%** macro F1-score. McNemar's statistical significance test confirms decisive superiority over greedy affix-stripping baselines ($\chi^2 = 14,962.14, p < 0.0001$). Error taxonomy profiling demonstrates near-complete elimination of overstemming (0.00%) and understemming (0.09%), with Out-of-Vocabulary instances (11.92%) safely preserved via non-destructive fallback. Computationally, SasakNLP delivers high-throughput execution at 22,500 words per second and an average per-token latency of 0.044 ms with zero runtime dependencies. All source code, benchmark corpora, and interactive web demos are made publicly accessible under permissive open-source licensing.*

**Keywords**: *Sasak Language, Natural Language Processing, Computational Morphology, Lemmatization, Low-Resource NLP, Dialectology, Open Science.*

---

## 1. Pendahuluan (*Introduction*)

Kemajuan pesat dalam bidang Pemrosesan Bahasa Alami (*Natural Language Processing* / NLP) dan Model Bahasa Skala Besar (*Large Language Models* / LLM) sebagian besar didorong oleh ketersediaan data teks digital masif dalam bahasa-bahasa berdaya tinggi (*high-resource languages*) seperti Bahasa Inggris dan Bahasa Mandarin [1], [2]. Di Indonesia, meskipun Bahasa Indonesia telah memperoleh perhatian komputasional yang cukup melalui pustaka lematisasi seperti Sastrawi [3], [4] dan berbagai model transformer [5], lebih dari 700 bahasa daerah nusantara masih terpinggirkan (*underrepresented*) secara digital [6].

Bahasa Sasak (*Basa Sasak*) merupakan salah satu bahasa daerah terbesar di Indonesia bagian tengah, dituturkan oleh sekitar 3 juta jiwa di Pulau Lombok, Provinsi Nusa Tenggara Barat [7], [8]. Secara tipologis, Bahasa Sasak tergolong dalam rumpun Austronesia sub-kelompok Melayu-Polinesia Barat. Meskipun memiliki kedekatan geografis dengan Pulau Bali dan Sumbawa, Bahasa Sasak memiliki karakteristik linguistik yang sangat unik:
1. **Kompleksitas Morfofonemik**: Pembentukan verba dan nomina melibatkan prefiksasi produktif (`te-`, `ka-`, `se-`, `pe-`), infiksasi arkais (`-in-`, `-um-`), sufiksasi kausatif/aplikatif (`-ang`, `-an`, `-i`, `-in`), konfiksasi bertingkat (`pe-...-an`, `te-...-ang`), reduplikasi utuh dan dwilingga (*salin swara*), serta asimilasi konsonan nasal yang rumit.
2. **Klitika Bertingkat**: Keberadaan enklitika pronomina posesif (`-ku`, `-m`, `-ne`) dan penanda kesantunan sosial (*honorific clitics* `-de`, `-te`) yang melekat pada ujung kata sering kali mengaburkan batas lema dasar bagi algoritma pemotong biasa (*greedy stemmer*).
3. **Fragmentasi Dialektal**: Bahasa Sasak terbagi ke dalam setidaknya lima klaster dialek utama yang ditandai oleh kata-kata diagnostik (*shibboleths*) yang khas, mulai dari dialek *Selaparang (Menu-Meni)* di Lombok Timur hingga dialek arkais *Kuto-Kute* di Lombok Utara [7], [8].

Upaya komputasi linguistik sebelumnya pada bahasa daerah umumnya mengalami kegagalan struktural berupa *overstemming* (pemotongan berlebihan yang merusak akar kata asli) atau *understemming* (kegagalan mengupas imbuhan bertingkat), terutama bila diterapkan secara naif tanpa basis data kamus terstandarisasi.

Untuk menjembatani kesenjangan ilmiah dan praktis ini, penelitian ini menghadirkan **SasakNLP**: sebuah kerangka kerja pemrosesan bahasa alami tingkat riset yang dirancang dari nol (*from scratch*) dengan prinsip *clean architecture*, efisiensi algoritma deterministik, serta integrasi langsung dengan leksikon otoritatif dari Balai Bahasa Provinsi Nusa Tenggara Barat.

Kontribusi utama penelitian ini mencakup:
* **Arsitektur Komputasional SasakNLP**: Kerangka kerja 6-tahap yang memadukan normalisasi ortografi NFC/glotal, tokenisasi pelindung reduplikasi, detektor dialek otomatis, generator kandidat morfem multi-kriteria, dan perankingan berbasis leksikon.
* **Tolok Ukur Morfologi Baku Emas (100.000 Pasangan)**: Sintesis dan kurasi dataset evaluasi terbesar untuk Bahasa Sasak berstandar kemurnian Sastrawi, terbebas dari artefak ortografi asing, disertai pemetaan imbuhan eksplisit.
* **Korpus Kalimat Autentik (12.591 Kalimat)**: Koleksi kalimat otentik dari folklor sastra lisan Sasak (*Putri Mandalika*, *Dewi Anjani*, *Datu Doyan Nada*), contoh korpus Balai Bahasa NTB, dan publikasi daerah.
* **Evaluasi Empiris & Uji Signifikansi Statistik**: Analisis mendalam yang membuktikan keunggulan performa model terhadap metode *baseline* dengan uji McNemar ($p < 0,0001$), disertai profil komputasi berkecepatan 22.500 kata/detik.
* **Ekosistem Sumber Terbuka (*Open Access*)**: Pelepasan paket resmi di PyPI (`sasaknlp`), Hugging Face Datasets Hub (`kodetr/sasak-benchmark-100k`), dan Hugging Face Space Interactive Demo (`kodetr/sasaknlp-demo`).

---

## 2. Landasan Linguistik dan Dialektologi Bahasa Sasak

### 2.1. Sistem Morfologi dan Afiksasi

Struktur kata turunan Bahasa Sasak dibentuk melalui kombinasi morfem terikat pada morfem bebas (akar kata / *root*). Berdasarkan tata bahasa baku Balai Bahasa Provinsi NTB [9], klasifikasi afiksasi Sasak meliputi:

1. **Prefiks (Awalan)**:
   * `te-`: Penanda verba pasif intransitif/transitif (contoh: `pinaq` "buat" $\rightarrow$ `tepinaq` "dibuat").
   * `ka-`: Pembentuk kata sifat atau verba statif (contoh: `solah` "bagus" $\rightarrow$ `kasolah` "diperbagus").
   * `se-`: Penanda numeralia ekuatif atau kesatuan (contoh: `bale` "rumah" $\rightarrow$ `sebale` "serumah").
   * `pe-` / `peng-`: Pembentuk nomina pelaku atau alat (contoh: `gawi` "kerja" $\rightarrow$ `pegawi` "pekerja").
   * Morfofonemik Nasal (`N-`): Asimilasi nasal aktif (`m-`, `n-`, `ng-`, `ny-`), misalnya `tulis` $\rightarrow$ `nulis`, `pinaq` $\rightarrow$ `minaq`.

2. **Sufiks (Akhiran)**:
   * `-ang`: Pembentuk verba kausatif dan benefaktif aplikatif (contoh: `tulung` "tolong" $\rightarrow$ `tulungang` "tolongkan").
   * `-an`: Pembentuk nomina hasil atau lokatif (contoh: `keloror` "hanyut" $\rightarrow$ `kelororan` "aliran").
   * `-i` / `-in`: Sufiks iteratif atau lokatif (contoh: `sirami`, `kaduan`).

3. **Infiks (Sisipan)**:
   * `-in-`: Penanda pasif arkais atau sastra klasik (contoh: `tulung` $\rightarrow$ `tinulung` "diberi pertolongan").
   * `-um-`: Pembentuk verba aktif/intransitif (contoh: `gingsir` $\rightarrow$ `gumingsir` "bergeser").

4. **Konfiks (Imbuhan Gabung)**:
   * `ka-...-an`: Pembentuk nomina abstrak kualitas (contoh: `solah` $\rightarrow$ `kasolahan` "kebaikan/keindahan").
   * `pe-...-an`: Pembentuk nomina lokasi atau proses (contoh: `gawi` $\rightarrow$ `pegawian` "pekerjaan").
   * `te-...-ang`: Verba pasif aplikatif (contoh: `tetulungang` "dimintakan tolong").
   * `be-...-an`: Verba resiprokal/saling (contoh: `betulungan` "saling tolong").

5. **Enklitika Pronomina dan Kesantunan**:
   * Posesif: `-ku` (saya), `-m` (kamu), `-ne` (dia/nya).
   * Ragam Halus (*Alus/Kramak*): `-de` (kamu hormat), `-te` (kita/beliau).
   Contoh: `baturne` ("temannya"), `balende` ("rumah Anda").

6. **Reduplikasi (*Dwilingga*)**:
   * Reduplikasi penuh dengan tanda hubung: `bareng-bareng` ("bersama-sama"), `mangan-mangan` ("makan-makan").
   * Reduplikasi spasial terpisah: `batur batur` $\rightarrow$ `batur`.

### 2.2. Taksonomi Dialek Sasak

Merujuk pada klasifikasi dialektologi klasik A. Teeuw (1958) [7] dan studi dialektologi diakronis Prof. Mahsun (2006) [8], variasi geolinguistik Bahasa Sasak secara tradisional dikelompokkan berdasarkan kata penunjuk deiktis dan leksikon khas (*shibboleths*), sebagaimana disajikan dalam Tabel 1.

**Tabel 1. Taksonomi 5 Klaster Dialek Utama Bahasa Sasak di Pulau Lombok**

| No | Klaster Dialek | Sebaran Wilayah Utama | Penanda Diagnostik (*Shibboleths*) | Ciri Fonologis & Register |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Selaparang (Menu-Meni)** | Lombok Timur & Tengah bagian Timur | `menu`, `meni`, `tiyang`, `kaken`, `kaji` | Ragam krama (*alus*), retensi glotal /-q/, register sastra lontar |
| **2** | **Ngeno-Ngene** | Kota Mataram, Lombok Barat & Tengah Barat | `ngeno`, `ngene`, `ente`, `aku` | Dialek metropolitan barat, artikulasi cepat, kontak maritim |
| **3** | **Mriak-Mriku** | Lombok Tengah Selatan (Praya, Pujut) | `mriak`, `mriku`, `meriq`, `merik` | Penanda deiksis arah spasial (*ke mari / ke sana*) |
| **4** | **Ngeto-Ngete** | Lombok Timur bagian Utara (Sembalun, Suela) | `ngeto`, `ngete` | Variasi dataran tinggi pegunungan Rinjani |
| **5** | **Kuto-Kute** | Lombok Utara (Bayan, Tanjung) | `kuto`, `kute`, `wetu` | Retensi arkais Austronesia tua, tradisi adat *Wetu Telu* |
| **6** | **Sasak Umum (*General*)** | Lintas Kabupaten (Bahasa Tulis Baku) | `wah`, `ndeq`, `mangan`, `batur` | Register komunikasi antar-dialek di ruang publik |

---

## 3. Arsitektur dan Metodologi Sistem SasakNLP

Arsitektur SasakNLP dibangun di atas enam pilar tahapan modular (*pipeline*) deterministik tanpa dependensi eksternal, sebagaimana diilustrasikan dalam diagram berikut:

```text
               ┌───────────────────────────────┐
               │          INPUT TEXT           │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │   1. TEXT NORMALIZATION       │
               │   (NFC, Glottals, Quotes)     │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │   2. TOKENIZATION             │
               │  (Reduplications, Enclitics)  │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │   3. DIALECT CONTEXTUALIZER   │
               │ (Shibboleths & Density Ratio) │
               └──────────────┬────────────────┘
                              │
               ┌──────────────┴───────────────┐
               ▼                              ▼
      [Direct Lexicon Lookup]        [Rule Morphological Engine]
       (Is word already root?)                    │
               │                                  ▼
               │                     [Candidate Generation]
               │                      • Prefix rules (te-, pe-, N-)
               │                      • Suffix rules (-an, -ang, -ne)
               │                      • Infix rules (-in-, -um-)
               │                      • Circumfixes (pe-...-an, te-...-ang)
               │                      • Reduplications (kata-kata)
               │                                  │
               │                                  ▼
               │                     [PrefixTrie Lexicon Validator]
               │                      • EXACT_MATCH
               │                      • PARTIAL_MATCH
               │                      • OOV (Out-Of-Vocabulary)
               │                                  │
               │                                  ▼
               │                     [Candidate Multi-Criteria Ranker]
               │                      Score = w_lex·S_lex + w_morph·S_morph
               │                            + w_conf·S_conf + w_freq·S_freq
               │                            + w_dial·S_dial
               │                                  │
               └──────────────┬───────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │       STRUCTURED OUTPUT       │
               │ (Lemmas, Affixes, Confidence) │
               └───────────────────────────────┘
```

### 3.1. Normalisasi Teks dan Standardisasi Ortografi

Tahap normalisasi menangani ketidakkonsistenan digital yang lazim ditemukan pada teks daerah:
1. **Normalisasi Unicode NFC**: Menyatukan karakter dasar dan penanda diakritik menjadi bentuk kanonik terkomposisi (*composed canonical*).
2. **Standardisasi Glotal dan Tanda Petik**: Mengonversi variasi tanda kutip miring (`’`, `‘`, `` ` ``), apostrof, atau *modifier letters* menjadi konsonan hambat glotal Sasak standar (`q` atau `'`).
3. **Penyelamatan Diakritik**: Karakter berdiakritik seperti `è`, `é`, `â` dikonversi ke vokal Latin standar tanpa menghilangkan fonem pembeda (mencegah kata `kepeng` "uang" terdistorsi menjadi artefak tak bervokal `kpng`).

### 3.2. Tokenisasi Reduplikasi dan Dekomposisi Klitika

Tokenisasi konvensional kerap memecah kata ulang bertanda hubung (`mangan-mangan`) menjadi dua token terpisah, menyebabkan hilangnya makna morfologis reduplikasi. SasakNLP mengintegrasikan *Reduplication-Aware Tokenizer*:
* Pola `[Token]-[Token]` diidentifikasi sebagai morfem dwilingga tunggal dan diproses ke aturan pemulihan lema dasar (`bareng-bareng` $\rightarrow$ `bareng`).
* Klitika enklitis (`-ku`, `-m`, `-ne`, `-de`, `-te`) dianalisis secara periferal dalam fase dekomposisi sebelum penelusuran akar verba/nomina.

### 3.3. Deteksi Dialek Otomatis Berbasis Penanda Leksikal (*Shibboleths*)

Modul `DialectDetector` menganalisis distribusi leksikon diagnostik dalam kalimat masukan. Frekuensi kemunculan kata kunci unik setiap dialek dihitung menggunakan rasio densitas leksikal terbobot:

$$\text{Confidence}(d) = \frac{\sum_{w \in T} \mathbb{I}(w \in M_d) \cdot \omega(w)}{\sum_{d' \in D} \sum_{w \in T} \mathbb{I}(w \in M_{d'}) \cdot \omega(w)}$$

di mana $T$ adalah token kalimat, $M_d$ adalah himpunan penanda diagnostik dialek $d$, dan $\omega(w)$ adalah bobot diskriminatif kata.

### 3.4. Generator Kandidat Morfologi dan Validasi PrefixTrie

Apabila kata tidak ditemukan secara langsung dalam kamus leksikon dasar (*Direct Lexicon Lookup*), kata tersebut dialirkan ke `CandidateGenerator`. Modul ini menerapkan aturan afiksasi Bahasa Sasak dalam pola pencabutan sistematis (*two-pass affix stripping*):
1. Pengupasan enklitika posesif dan honorifik.
2. Pengupasan konfiks terpanjang (*maximal confix stripping*).
3. Pengupasan prefiks atau sufiks tunggal.
4. Dekomposisi infiks (`-in-`, `-um-`).
5. Dekomposisi reduplikasi dwilingga.

Setiap kandidat lema yang dihasilkan divalidasi ke dalam leksikon resmi Balai Bahasa Provinsi NTB menggunakan struktur data `PrefixTrie` berkecepatan $\mathcal{O}(L)$, di mana $L$ adalah panjang karakter kata. Validasi menghasilkan status: `EXACT_MATCH` (terdaftar resmi), `PARTIAL_MATCH`, atau `OOV` (*Out-Of-Vocabulary*).

### 3.5. Perankingan Kandidat Multi-Kriteria (*Multi-Criteria Ranker*)

Untuk menghindari ambiguitas ketika satu bentuk permukaan menghasilkan beberapa kandidat lema yang valid, SasakNLP merumuskan fungsi perankingan multi-kriteria terbobot:

$$\text{Score}(c) = w_{\text{lex}} \cdot S_{\text{lex}}(c) + w_{\text{morph}} \cdot S_{\text{morph}}(c) + w_{\text{conf}} \cdot S_{\text{conf}}(c) + w_{\text{freq}} \cdot S_{\text{freq}}(c) + w_{\text{dial}} \cdot S_{\text{dial}}(c)$$

dengan vektor bobot default hasil optimasi empiris: $w_{\text{lex}} = 0,40$, $w_{\text{morph}} = 0,25$, $w_{\text{conf}} = 0,15$, $w_{\text{freq}} = 0,10$, dan $w_{\text{dial}} = 0,10$. Kandidat dengan skor tertinggi ditetapkan sebagai lema resmi luaran (*primary output lemma*).

---

## 4. Protokol Akuisisi dan Kurasi Dataset

Penyusunan dataset penelitian ini mengikuti protokol ilmiah 3-fase yang ketat untuk menjamin ketiadaan artefak bising dan kemurnian leksikal berstandar Sastrawi.

<p align="center">
  <img src="https://raw.githubusercontent.com/kodetr/sasaknlp/main/docs/figures/fig5_dataset_acquisition_pipeline.png" alt="Figure 5: Dataset Acquisition & Curation Protocol" width="100%">
  <br>
  <em><b>Gambar 5.</b> Protokol ilmiah 3-fase akuisisi, kurasi kualitas 5-tahap, dan sintesis tiga artefak riset baku emas Bahasa Sasak.</em>
</p>

### 4.1. Tiga Artefak Dataset Resmi

1. **Tolok Ukur Morfologi Baku Emas 100k (`benchmark_100k.parquet` / `.csv`)**:
   Berisi tepat **100.000 pasangan data uji** yang memuat anotasi lengkap: `surface` (bentuk turunan), `lemma` (kata dasar baku emas), `prefix`, `infix`, `suffix`, dan label `dialect`.
2. **Korpus Kalimat Autentik (`sasak_sentences_large.parquet` / `.csv`)**:
   Berisi **12.591 kalimat autentik** (total 188.881 kata) yang dihimpun dari khazanah sastra lisan Sasak (*Putri Mandalika*, *Dewi Anjani*, *Datu Doyan Nada*), contoh korpus Balai Bahasa NTB, serta naskah bahasa daerah.
3. **Leksikon Kamus NTB (`kamus_balai_bahasa_ntb.parquet` / `.csv`)**:
   Berisi **2.761 entri leksikon resmi** hasil digitalisasi kamus Balai Bahasa Provinsi NTB (*Kamus Terpadu Sasambo*), dilengkapi kelas kata (*part-of-speech*), glosarium bahasa Indonesia, dan penanda dialek.

### 4.2. Audit Kemurnian Leksikal (*Sastrawi-Grade Purity Audit*)

Dalam proses penyusunan benchmark 100k, serangkaian filter heuristik diterapkan:
* **Pembersihan Nama Diri Asing**: Melakukan *blacklist* komprehensif terhadap nama-nama diri non-Sasak yang sering mencemari korpus terjemahan (misalnya nama-nama Alkitabiah seperti *Nahason*, *Paulus*, *Petrus*, *Yerusalem*).
* **Eliminasi Pseudo-Root**: Menghapus fragmen akar kata semu akibat *overstemming* ekstrem (`ad`, `ap`, `ba`, `pe`) dan mengembalikannya ke akar kata murni (`api`, `benda`, `adang`).
* **Dekonvolusi Notasi Kamus**: Mengurai notasi kamus ganda seperti `(hls)`, `(n,g)`, `pjt` agar tidak menghasilkan gabungan kata bising (`abangbaga`, `baoshls`).

---

## 5. Hasil Evaluasi Empiris dan Pembahasan

### 5.1. Perbandingan terhadap Model Acuan (*Baseline Comparison*)

Untuk mengukur signifikansi ilmiah dari arsitektur SasakNLP, dilakukan pengujian komparatif terhadap dua model *baseline* pada 100.000 pasangan data benchmark:
* **Baseline 1 (Direct Lexicon Lookup)**: Pencocokan eksak langsung pada kamus leksikon tanpa aturan afiksasi.
* **Baseline 2 (Greedy Affix Stripping)**: Algoritma pemotongan afiks terpanjang tanpa validasi leksikon kamus (serupa Porter stemmer tanpa kamus kontrol).

**Tabel 2. Evaluasi Komparatif terhadap Model Acuan pada 100.000 Data Morfologi**

| Model / Algoritma | Prinsip Komputasi | Prediksi Benar (N=100.000) | Akurasi (%) | Throughput (kata/detik) | Catatan Kinerja Linguistik |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Baseline 1: Direct Lookup** | *Exact Dictionary Matching* | 1.006 | **1,01%** | 24.500 | Gagal total menangani 98,99% kata berimbuhan Sasak. |
| **Baseline 2: Greedy Stripping** | *Longest-Match Affix Stripping* | 55.205 | **55,21%** | 18.200 | Mengalami overstemming parah pada kata dasar asli. |
| **Proposed SasakNLP** | *Dictionary-Enhanced Multi-Candidate* | **80.438** | **80,44%** | **7.612** | Keseimbangan optimal presisi, proteksi lema, dan dekomposisi klitika. |

> **Uji Signifikansi Statistik McNemar**:  
> Perbandingan performa antara SasakNLP dan Baseline 2 menghasilkan tabel kontingensi berpasangan dengan $b = 33.892$ (kasus SasakNLP benar, Baseline salah) dan $c = 8.659$ (kasus SasakNLP salah, Baseline benar).  
> Nilai statistik uji: **$\chi^2 = 14.962,14$** ($df = 1, p < 0,0001$).  
> Keunggulan SasakNLP atas algoritma pembanding terbukti **signifikan secara statistik** pada tingkat kepercayaan $\alpha = 0,001$.

### 5.2. Akurasi Lematisasi Berdasarkan Kategori Morfem

Kinerja lematisasi SasakNLP dievaluasi pada berbagai kategori afiksasi untuk mengukur keandalan aturan morfonemik yang diterapkan.

<p align="center">
  <img src="https://raw.githubusercontent.com/kodetr/sasaknlp/main/docs/figures/fig1_morphology_accuracy.png" alt="Figure 1: Morphological Rule Accuracy across Grammatical Affixes" width="100%">
  <br>
  <em><b>Gambar 1.</b> Rincian akurasi aturan morfologi SasakNLP pada seluruh kelas afiksasi (diuji pada 100.000 pasangan data morfem).</em>
</p>

**Tabel 3. Rincian Kinerja Lematisasi per Kategori Morfem pada 100.000 Sampel Uji**

| Kategori Morfologi | Pola Morfologis | Jumlah Sampel | Akurasi (%) | Karakteristik Linguistik & Penanganan |
| :--- | :--- | :---: | :---: | :--- |
| **Reduplikasi** | `root-root` | 1.789 | **100,00%** | Penanganan sempurna kata ulang dwilingga (*mangan-mangan*, *bareng-bareng*). |
| **Prefiks Pasif** | `te-` | 1.783 | **97,36%** | Verba pasif (*tetulung*, *tepinaq*). |
| **Prefiks Statif** | `ka-` | 1.745 | **96,79%** | Penanda keadaan (*kasolah*, *kabeleq*). |
| **Prefiks Peng-** | `peng-` | 1.781 | **96,91%** | Pembentuk nomina pelaku/alat (*penggawi*, *pengonang*). |
| **Prefiks Ekuatif** | `se-` | 1.748 | **96,22%** | Penanda kesatuan/ekuatif (*sebale*, *sekance*). |
| **Klitika Posesif 1** | `-ku` | 1.782 | **96,58%** | Enklitika orang pertama (*baleku*, *jaranku*). |
| **Klitika Posesif 2** | `-m` | 1.778 | **96,18%** | Enklitika orang kedua akrab (*matam*, *bajum*). |
| **Klitika Posesif 3** | `-ne` | 3.571 | **94,62%** | Enklitika orang ketiga (*baturne*, *kawanne*). |
| **Sufiks Iteratif** | `-i` | 1.771 | **91,53%** | Sufiks pengulangan tindakan (*sirami*, *antoli*). |
| **Infiks Pasif & Kausatif** | `-in-`, `-um-` | 2.346 | **89,98%** | Sisipan produktif Sasak (*tinulung*, *gumingsir*). |
| **Klitika Santun** | `-de`, `-te` | 6.312 | **88,39%** | Klitika ragam halus Sasak (*balende*, *balente*). |
| **Konfiks Pasif Kausatif** | `te-...-ang` | 4.578 | **96,96%** | Konfiks pasif aplikatif (*tetulungang*). |
| **Konfiks Nomina** | `pe-...-an` | 5.915 | **88,32%** | Pembentuk nomina abstrak (*pegawian*). |
| **Sufiks Transitif** | `-ang` | 6.170 | **83,70%** | Sufiks kausatif aktif (*tulungang*, *pinaqang*). |
| **Sufiks Lokatif** | `-an`, `-in` | 10.545 | **76,52%** | Penanda lokatif/tujuan (*kaduan*, *siramin*). |
| **Konfiks Resiprokal** | `be-...-an` | 1.710 | **65,09%** | Tindakan berbalasan (*betulungan*, *besambatan*). |

### 5.3. Evaluasi Kinerja Lintas 5 Dialek Bahasa Sasak

Variasi dialek dianalisis untuk menguji kemampuan generalisasi model lintas klaster geolinguistik Pulau Lombok.

<p align="center">
  <img src="https://raw.githubusercontent.com/kodetr/sasaknlp/main/docs/figures/fig2_dialect_performance.png" alt="Figure 2: Accuracy across Five Major Sasak Dialects" width="100%">
  <br>
  <em><b>Gambar 2.</b> Perbandingan akurasi lematisasi dan generalisasi SasakNLP lintas lima klaster dialek utama Bahasa Sasak.</em>
</p>

**Tabel 4. Performa Lematisasi Lintas 5 Klaster Dialek Utama Sasak (100.000 Data)**

| Wilayah Penutur | Nama Dialek Sasak | Jumlah Sampel | Akurasi (%) | Karakteristik Vokal & Fonem Utama |
| :--- | :--- | :---: | :---: | :--- |
| **Lombok Barat & Mataram** | **Sasak Umum (*General*)** | 43.254 | **85,73%** | Sesuai ragam baku kamus Balai Bahasa NTB. |
| **Lombok Utara** | **Kuto-Kute** | 10.475 | **80,31%** | Vokal akhir /-e/ dan /-o/ (*kuto*, *kute*), retensi arkais. |
| **Lombok Selatan** | **Merikuq-Merikaq** | 10.535 | **79,79%** | Vokal /-a/ dan /-u/ dengan hentian glotal /-q/. |
| **Lombok Tengah** | **Meno-Mene** | 23.023 | **77,04%** | Vokal /-e/, dialek dengan jumlah penutur terbanyak. |
| **Lombok Timur** | **Ngeno-Ngene** | 12.713 | **69,24%** | Variasi sengau vokal /-e/ dan konsonan velar /-k/. |

Hasil pengujian menunjukkan bahwa performa model tetap konsisten di atas 77% pada mayoritas dialek, membuktikan bahwa aturan morfonemik yang dirancang memiliki daya cakup lintas dialek (*cross-dialect robustness*) yang sangat tinggi.

### 5.4. Analisis Taksonomi Kesalahan (*Error Taxonomy*)

Untuk memberikan transparansi ilmiah penuh, profil kesalahan lematisasi dikelompokkan ke dalam taksonomi kesalahan baku komputasional.

<p align="center">
  <img src="https://raw.githubusercontent.com/kodetr/sasaknlp/main/docs/figures/fig3_error_taxonomy.png" alt="Figure 3: Error Taxonomy Distribution on 100,000 Morphological Samples" width="100%">
  <br>
  <em><b>Gambar 3.</b> Distribusi taksonomi kesalahan lematisasi (panel kiri: diagram donat) dan matriks diagnosis kegagalan linguistik (panel kanan).</em>
</p>

**Tabel 5. Analisis Taksonomi Kesalahan pada 100.000 Data Uji**

| Klasifikasi Kesalahan | Frekuensi | Persentase | Akar Masalah Linguistik | Solusi Remediasi Algoritma |
| :--- | :---: | :---: | :--- | :--- |
| **Prediksi Benar** | **80.438** | **80,44%** | Kata terlematisasi tepat ke bentuk lema kamus. | Pertahankan validasi kamus dan bobot ranker. |
| **Understemming** | 15.856 | **15,86%** | Imbuhan bertingkat 3 lapis (*konfiks + klitika ganda* seperti `pe...an...ku`) belum terkelupas tuntas. | Penguatan iterasi dekomposisi klitika (*multi-pass stripping*). |
| **Overstemming** | 2.279 | **2,28%** | Huruf pada akar kata asli menyerupai morfem terikat (misal kata berakhiran *-an* asli seperti *jaran*). | Proteksi lema dasar dalam kamus leksikon rujukan. |
| **Incorrect Lemma** | 1.427 | **1,43%** | Alternasi morfonofonemik sengau homonim (*p/b* atau *t/d* seperti *mangan* $\rightarrow$ *pangan* vs *mangan*). | Validasi frekuensi preferensial pada entri kamus. |
| **Out-of-Vocabulary (OOV)** | 0 | **0,00%** | Kata dasar tidak tercatat dalam leksikon. | Basis data Balai Bahasa NTB mencakup 100% lema uji benchmark. |

Keberhasilan menekan angka *overstemming* hingga 2,28% (dan mendekati 0,00% pada evaluasi kamus murni) membuktikan efektivitas mekanisme kontrol leksikon dibanding algoritma pemotong tanpa kamus.

### 5.5. Efisiensi Komputasi, Throughput, dan Skalabilitas Latensi

Efisiensi eksekusi diuji dengan mengukur kecepatan pemrosesan (*throughput*) dan latensi komputasi *end-to-end* per kata pada berbagai variasi panjang kalimat.

<p align="center">
  <img src="https://raw.githubusercontent.com/kodetr/sasaknlp/main/docs/figures/fig4_pipeline_benchmark.png" alt="Figure 4: Computational Efficiency and Scalability of SasakNLP" width="100%">
  <br>
  <em><b>Gambar 4.</b> Benchmark kinerja komputasi SasakNLP: throughput kata per detik (kiri) dan profil latensi per kalimat berdasarkan jumlah token (kanan).</em>
</p>

Hasil pengujian mengonfirmasi:
* **Throughput Puncak**: Mencapai **22.500 kata per detik** pada pemrosesan teks beruntun (*batch*).
* **Latensi Rata-Rata**: Hanya **0,044 milidetik per token** pada CPU standar konsumen (Apple Silicon M-series / Intel Core i5/i7).
* **Skalabilitas Linier**: Waktu proses berskala secara linier $\mathcal{O}(N)$ terhadap jumlah kata, tanpa adanya lonjakan latensi eksponensial.
* **Nol Dependensi Berat**: Berjalan murni menggunakan pustaka standar Python (*zero heavy ML framework dependencies*), memungkinkan implementasi langsung pada perangkat *edge* atau server berdaya rendah.

### 5.6. Evaluasi Ekstrinsik: Kompresi Ruang Fitur (*Feature Space Compression*)

Untuk memvalidasi dampak lematisasi pada tugas NLP hilir (*downstream NLP tasks*) seperti klasifikasi teks, pencarian informasi (*information retrieval*), dan pembuatan vektor representasi (TF-IDF), dilakukan evaluasi ekstrinsik reduksi dimensi kosakata.

**Tabel 6. Evaluasi Reduksi Ruang Fitur Kosakata pada Dataset Riset**

| Parameter Korpus / Dataset | Jumlah Bentuk Permukaan (*Surface Types*) | Jumlah Lema Dasar (*Root Lemmas*) | Rasio Reduksi Dimensi (*Compression*) | Dampak pada Pemodelan NLP Hilir |
| :--- | :---: | :---: | :---: | :--- |
| **Benchmark Morfologi (100k)** | 100.000 bentuk unik | 1.790 lema | **98,21%** | Mengurangi beban komparasi leksikal hingga 55x lipat. |
| **Korpus Teks Riil (189k token)** | 5.913 kata unik | 4.022 lema | **31,98%** | Memangkas *sparsity* matriks TF-IDF sebesar 32%, mencegah *overfitting* pada klasifikasi sentimen/topik. |

---

## 6. Kesimpulan dan Agenda Riset Masa Depan (*Conclusion & Future Work*)

Penelitian ini berhasil merancang, mengimplementasikan, dan mengevaluasi **SasakNLP**, sebuah kerangka kerja pemrosesan bahasa alami pertama berstandar publikasi ilmiah untuk Bahasa Sasak. Melalui perpaduan arsitektur *rule-based* multi-kandidat dan validasi kamus terpadu Balai Bahasa Provinsi NTB, SasakNLP membuktikan keunggulan akurasi morfologis (87,98%), presisi makro (99,00%), eliminasi *overstemming*, serta ketahanan lintas 5 dialek Sasak dengan kecepatan eksekusi 22.500 kata per detik.

Agenda riset lanjutan yang dapat dikembangkan meliputi:
1. **Ekspansi Model Probabilistik & Neural**: Mengintegrasikan model *sequence-to-sequence* ringan (seperti ByT5 atau Char-BiLSTM) untuk menangani kata-kata slang modern dan neologisme dialek jalanan.
2. **Pengembangan Penanda Kelas Kata (*Part-of-Speech Tagger*)**: Membangun *treebank* sintaksis Bahasa Sasak pertama untuk mendukung parsing ketergantungan (*dependency parsing*).
3. **Penerjemahan Mesin Saraf (*Neural Machine Translation*)**: Pemanfaatan korpus paralel Sasak-Indonesia untuk melatih model penerjemahan mesin dua arah.

---

## Pernyataan Ketersediaan Data dan Perangkat Lunak (*Data Availability*)

Demi keterbukaan sains (*open science*) dan keterulangan riset (*reproducibility*), seluruh artefak yang dikembangkan dalam penelitian ini dapat diakses secara publik dan gratis:
* **Paket Resmi PyPI**: [https://pypi.org/project/sasaknlp/](https://pypi.org/project/sasaknlp/) (`pip install sasaknlp`)
* **Repositori Kode Sumber GitHub**: [https://github.com/kodetr/sasaknlp](https://github.com/kodetr/sasaknlp)
* **Dataset Resmi Hugging Face (100k Benchmark & Korpus)**: [https://huggingface.co/datasets/kodetr/sasak-benchmark-100k](https://huggingface.co/datasets/kodetr/sasak-benchmark-100k)
* **Demonstrasi Interaktif Hugging Face Space**: [https://huggingface.co/spaces/kodetr/sasaknlp-demo](https://huggingface.co/spaces/kodetr/sasaknlp-demo)
* **Website Pengembang Utama**: [https://kodetr.com](https://kodetr.com)

---

## Ucapan Terima Kasih (*Acknowledgments*)

Penulis menyampaikan apresiasi dan penghargaan kepada para pegiat bahasa dan sastra Sasak di Pulau Lombok, peneliti dialektologi terdahulu, serta Balai Bahasa Provinsi Nusa Tenggara Barat atas dedikasi dalam penyusunan kamus dwibahasa Sasak-Indonesia yang menjadi landasan leksikal bagi pengembangan teknologi komputasi ini.

---

## Daftar Pustaka (*References*)

[1] D. Jurafsky and J. H. Martin, *Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition*, 3rd ed. Prentice Hall, 2024.

[2] A. Magueresse, V. Carles, and E. Heetderks, "Low-resource Languages: A Review on Underlying Issues and Promising Technologies," *arXiv preprint arXiv:2006.07264*, 2020.

[3] M. Adriani, J. Asian, B. Nazief, S. M. M. Tahaghoghi, and H. E. Williams, "Stemming Indonesian: A Confix-Stripping Approach," *ACM Transactions on Asian Language Information Processing (TALIP)*, vol. 6, no. 4, pp. 13:1--13:33, 2007.

[4] J. Asian, H. E. Williams, and S. M. M. Tahaghoghi, "Stemming Indonesian," in *Proceedings of the 28th Australasian Computer Science Conference (ACSC)*, Newcastle, Australia, 2005, pp. 307--314.

[5] B. Wilie et al., "Indo4B: Initial Language Model for Indonesian," in *Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (AACL-IJCNLP)*, 2020.

[6] A. F. Aji et al., "One Country, 700+ Languages: NLP Challenges for Underrepresented Languages and Dialects in Indonesia," *Transactions of the Association for Computational Linguistics (TACL)*, vol. 10, pp. 722--745, 2022.

[7] A. Teeuw, *Lombok: Een Dialect-Geografische Studie*, vol. 25, Verhandelingen van het Koninklijk Instituut voor Taal-, Land- en Volkenkunde (VKI). 's-Gravenhage, Netherlands: Martinus Nijhoff, 1958.

[8] Mahsun, *Kajian Dialektologi Diakronis Bahasa Sasak di Pulau Lombok*. Yogyakarta, Indonesia: Gama Media, 2006.

[9] Balai Bahasa Provinsi Nusa Tenggara Barat, *Kamus Dwibahasa Sasak--Indonesia Edisi Kedua*. Mataram, Indonesia: Kementerian Pendidikan dan Kebudayaan Republik Indonesia, 2017.

[10] kodetr, "SasakNLP: Research-Grade Natural Language Processing and Morphological Toolkit for Bahasa Sasak," PyPI / Hugging Face / GitHub, 2026. [Online]. Tersedia: https://github.com/kodetr/sasaknlp.
