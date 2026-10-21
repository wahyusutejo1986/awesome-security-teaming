# 🧭 Decision Matrix, Architectures & Cost Analysis

> Panduan strategis pemilihan alat (*tooling selection*), analisis topologi arsitektur, skenario penggunaan nyata (*use-cases*), dan estimasi biaya operasional (*Total Cost of Ownership - TCO*).

---

## 🎯 1. Head-to-Head Decision Matrix

Memilih alat keamanan yang tepat memerlukan pemahaman mendalam tentang **tujuan utama**, **lingkup lingkungan**, dan **kemampuan tim operasional**. Berikut adalah komparasi head-to-head untuk use-case yang paling sering dipertimbangkan:

### 🌐 A. Analisis Trafik & Pemantauan Jaringan

```
[Trafik Jaringan / SPAN Port / TAP]
        ├──> Suricata  (Inline IPS / Signature IDS)  ──> Alerting & Drop Packet
        ├──> Zeek      (Metadata Extraction Engine)  ──> Structured Protocol Logs (DNS, SSL, HTTP)
        └──> Wireshark (Deep Packet Inspection GUI) ──> Manual Forensic PCAP Drilldown
```

| Tool | Skenario Terbaik (*When to Use*) | Kapan *JANGAN* Digunakan | Kompleksitas Setup |
| :--- | :--- | :--- | :--- |
| **Suricata** | Saat Anda memerlukan **Network IDS/IPS** real-time berbasis tanda tangan (*signatures/rules*) untuk mendeteksi exploit dan memblokir traffic berbahaya secara inline. | Bukan untuk analisis transaksional protokol mendalam atau rekayasa log jangka panjang. | Sedang |
| **Zeek** | Saat Anda memerlukan **visibilitas metadata jaringan terstruktur** (menjawab: siapa bicara dengan siapa, sertifikat apa yang dipakai, domain apa yang di-resolve) tanpa alert kebisingan (*noise*). | Bukan untuk memblokir paket secara inline atau pemindaian malware biner instan. | Sedang - Tinggi (butuh scripting Zeek) |
| **Wireshark** | Investigasi forensik mendalam oleh operator pada satu sesi koneksi atau berkas tangkapan (`.pcap`) tertentu. | **JANGAN PERNAH** jalankan Wireshark secara continuous di gateway produksi dengan live high-speed traffic (risiko stabilitas memori). | Rendah (Desktop GUI) |

---

### ⚔️ B. Validasi Deteksi & Adversary Emulation

```
[Pengujian Keamanan Ofensif / Purple Teaming]
        ├──> Atomic Red Team (Unit Testing)        ──> Uji 1 Teknik MITRE ATT&CK Spesifik
        ├──> MITRE Caldera   (Autonomous Campaign) ──> Simulasi Serangan Rantai Penuh Otomatis
        └──> VECTR           (Exercise Management) ──> Dashboard Kolaborasi Red-Blue & Pelaporan
```

| Tool | Skenario Terbaik (*When to Use*) | Kapan *JANGAN* Digunakan | Kebutuhan Infrastruktur |
| :--- | :--- | :--- | :--- |
| **Atomic Red Team** | **Unit testing deteksi**: Memverifikasi apakah alert SIEM/EDR memicu teknik ATT&CK tertentu (misal: `T1059.001 PowerShell`) dalam hitungan detik. | Bukan untuk simulasi *lateral movement* multi-host yang adaptif dan terkoordinasi secara otonom. | Sangat Minimal (skrip PowerShell/Bash lokal) |
| **MITRE Caldera** | **Adversary emulation end-to-end**: Menguji postur pertahanan dengan agen otomatis yang menjalankan profil musuh (*adversary profile*) dari initial access hingga exfiltration. | Bukan untuk pengujian ad-hoc cepat pada satu mesin tanpa kebutuhan server orchestrator. | Sedang (Server Caldera + C2 Agent) |
| **VECTR** | **Manajemen latihan Purple Team**: Melacak skor deteksi, gap analysis, dan mengukur peningkatan kapabilitas Blue Team dari waktu ke waktu. | VECTR tidak mengeksekusi serangan sendiri; ia adalah platform pelacakan dan metrik. | Sedang (Docker / Web App) |

---

### 🕹️ C. Command & Control (C2) Frameworks

| Tool | Karakteristik Utama | Skenario Terbaik | Trade-offs & Gotchas |
| :--- | :--- | :--- | :--- |
| **Sliver** (Bishop Fox) | Ditulis dalam Go, mendukung mTLS, WireGuard, HTTP(S), dan DNS tunneling. | Asesmen Red Team enterprise multi-operator; kuat untuk pivot jaringan dan cross-platform (Windows, Linux, macOS). | Ukuran payload biner Go relatif besar (~10MB); membutuhkan obfuscation tambahan terhadap EDR modern. |
| **Havoc** | C2 modern dengan payload C/ASM (*Demon agent*), mendukung sleep obfuscation dan indirect syscalls. | Simulasi penyerang tingkat lanjut pada lingkungan Windows modern yang dijaga EDR ketat. | Fokus dominan Windows; kurva belajar tinggi untuk kustomisasi loader. |
| **Mythic** | Arsitektur modular berbasis Docker microservices dengan berbagai pilihan agen (Apfell, Apollo, Poseidon). | Operasi Red Team kolaboratif skala besar dengan tim terdistribusi yang membutuhkan berbagai jenis agen khusus. | Footprint server cukup berat karena menjalankan banyak kontainer Docker. |

---

### 🛡️ D. Deteksi Endpoint & SIEM

| Tool | Model Arsitektur | Kekuatan Utama | Keterbatasan Utama |
| :--- | :--- | :--- | :--- |
| **Wazuh** | Agent-Server terpadu (FIM, Vulnerability Detection, Log Analysis, Active Response). | Solusi *all-in-one* kepatuhan (PCI-DSS, CIS) dan pemantauan endpoint yang langsung siap pakai. | Rule engine berbasis XML; manajemen skala sangat besar (>10.000 agen) memerlukan tuning cluster OpenSearch. |
| **Sigma** | Format spesifikasi aturan deteksi generik (YAML) independen dari vendor SIEM. | Menulis logika deteksi sekali, lalu mengonversinya ke query Splunk, Elasticsearch, Sentinel, atau QRadar. | Sigma adalah bahasa/standar aturan, bukan mesin SIEM penampung data. |
| **Velociraptor** | Live Endpoint Query & Forensics berbasis VQL (Velociraptor Query Language). | Respons insiden kilat (DFIR): menanyakan status ribuan endpoint secara instan (memory dump, process hunting). | Bukan SIEM analitik jangka panjang; difokuskan untuk triage dan investigasi berkecepatan tinggi. |

---

## 🏗️ 2. Tipologi Arsitektur Alat

```
MODEL 1: STANDALONE CLI / OPERATOR TOOL
[ Operator Laptop ] ──(Direct Scan/Analyze)──> [ Target Host / PCAP ]
Contoh: Nmap, Wireshark, Metasploit (Console)

MODEL 2: DISTRIBUTED AGENT-SERVER TOPOLOGY
[ Endpoint A (Agent) ] ──┐
[ Endpoint B (Agent) ] ──┼──(Encrypted TLS)──> [ Master Server / SIEM Engine ] ──> [ Web Dashboard ]
[ Endpoint C (Agent) ] ──┘
Contoh: Wazuh, Velociraptor, Caldera

MODEL 3: C2 MULTI-TIER REDIRECTOR TOPOLOGY
[ Target Machine ] ──> [ Cloud Redirector (Nginx/CDN) ] ──> [ Team Server C2 ] ──> [ Red Team Operators ]
Contoh: Sliver, Havoc, Mythic

MODEL 4: GRAPH-BASED COLLECTOR TOPOLOGY
[ Ingestor (SharpHound/BloodHound.py) ] ──(Active Directory LDAP/RPC)──> [ JSON Data ]
                                                                             │
                                                                             ▼
                                                             [ Neo4j Graph DB + Web UI ]
Contoh: BloodHound
```

---

## 💰 3. Analisis Biaya Nyata (Total Cost of Ownership - TCO)

Meskipun perangkat lunak berlisensi open source (*FOSS*) gratis untuk diunduh, biaya operasional sebenarnya ditentukan oleh **infrastruktur, komputasi, dan pemeliharaan**:

### Matriks Estimasi Resource & Biaya

| Kategori Tool | Kebutuhan Minimum Hardware (Server) | Estimasi Storage Log / Bulan | Model Lisensi | Biaya Tersembunyi (*Hidden Costs*) |
| :--- | :--- | :--- | :--- | :--- |
| **Suricata / Zeek** | 8-16 vCPU, 16-32 GB RAM (Network Interface Card dengan DPDK / AF_PACKET) | 100 GB - 2 TB (tergantung volume traffic) | Open Source (GPL / BSD) | Biaya penyimpanan storage traffic (*cold storage*) dan kartu jaringan dedicated (*capture card*). |
| **Wazuh Cluster** | 4-8 vCPU, 16 GB RAM (Server + Indexer) | 50 GB - 500 GB per 100 endpoints | Open Source (GPLv2 / Apache 2.0) | Beban IOPS disk SSD untuk indexing log OpenSearch/Elasticsearch secara intensif. |
| **Sliver / Havoc C2** | 2-4 vCPU, 4-8 GB RAM (VPS Cloud) | < 10 GB | Open Source (GPLv3 / Apache 2.0) | Biaya sewa VPS cloud domain, SSL certificates, dan domain categorization reputation. |
| **BloodHound** | 4 vCPU, 8-16 GB RAM (Neo4j JVM memory) | < 20 GB (Database Graph) | Open Source (MIT) | Konsumsi RAM server saat memproses graph analysis untuk domain besar (>50.000 objek AD). |
| **Atomic Red Team** | Workstation operator lokal (tanpa server) | Nihil (eksekusi lokal) | Open Source (MIT) | Waktu operator dalam mereview false positives dan merestorasi status sistem pasca-uji. |

---

## 🏢 4. Rekomendasi Setup Berdasarkan Kematangan Organisasi

### 🔰 Tingkat 1: Tim Kecil / Startup / Solo Practitioner (Lean Stack)
- **Fokus**: Menemukan kerentanan dasar dan visibilitas endpoint minimum tanpa beban operasional server yang berat.
- **Rekomendasi**:
  - *Network & Discovery*: **Nmap** (Port scanning) + **Wireshark** (PCAP triage).
  - *Endpoint & Auditing*: **Atomic Red Team** (Pengujian manual via PowerShell).
  - *Host Visibility*: **Velociraptor** (Standalone mode untuk triage darurat).
  - **Biaya Infrastruktur**: ~$0 - $20 / bulan.

### 🛡️ Tingkat 2: Perusahaan Menengah (Active Blue / Purple Team)
- **Fokus**: Sentralisasi deteksi, compliance otomatis, dan pengujian berkala terhadap baseline pertahanan.
- **Rekomendasi**:
  - *Defensive*: **Wazuh** (Agent-Server untuk seluruh server dan endpoint kantor) + **Suricata** (IDS di perimeter gateway).
  - *Testing & Validation*: **Atomic Red Team** diintegrasikan dengan CI/CD + **MITRE ATT&CK Navigator** untuk pemetaan coverage.
  - *Audit*: **BloodHound** secara rutin untuk mengaudit jalur eskalasi hak istimewa Active Directory.
  - **Biaya Infrastruktur**: ~$100 - $300 / bulan (Server VM + SSD Storage).

### 🏛️ Tingkat 3: Enterprise / Mature Security Operations
- **Fokus**: Simulasi musuh otomatis (*adversary emulation*), pemantauan metadata skala besar, dan metrik evolusi keamanan kolaboratif.
- **Rekomendasi**:
  - *Defensive*: **Zeek + Suricata** (Hybrid network monitoring) + Distributed SIEM dengan **Sigma Rules**.
  - *Offensive / Adversary Emulation*: **Sliver** atau **Havoc** (C2 multi-tier dengan redirector) + **MITRE Caldera**.
  - *Continuous Purple Teaming*: **VECTR** untuk mengukur MTTD (*Mean Time to Detect*) dan MTTR (*Mean Time to Respond*).
  - **Biaya Infrastruktur**: ~$500 - $2.000+ / bulan (Cluster terdistribusi berdaya tampung tinggi).
