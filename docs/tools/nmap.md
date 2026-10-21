# 🛡️ Tool Profile: Nmap (Network Mapper)

> The Industry-Standard Open-Source Utility for Network Discovery and Vulnerability Auditing.

---

## 📌 Ringkasan Eksekutif

| Parameter | Keterangan |
| :--- | :--- |
| **Kategori Tim** | 🔴 Red Team / 🔵 Blue Team |
| **Kapabilitas Utama** | `network-discovery`, `penetration-testing` |
| **Model Arsitektur** | Standalone CLI Scanner (Raw Packet Socket Engine in C/C++) |
| **Lisensi** | NPSL (Nmap Public Source License) |
| **Pemeliharaan (*Maintenance*)** | Sangat Aktif (Gordon Lyon / Fyodor) |
| **Situs Resmi** | [nmap.org](https://nmap.org/) |
| **Repositori Resmi** | [github.com/nmap/nmap](https://github.com/nmap/nmap) |

---

## 🎯 Kapan Menggunakan Nmap?

### ✅ Skenario Terbaik (Best Use Cases)
1. **Host Discovery & Asset Inventory**: Memetakan perangkat aktif dalam subnet IP lokal atau enterprise (*ping sweeps, ARP discovery*).
2. **Service & Version Fingerprinting**: Menentukan port mana yang terbuka dan versi aplikasi layanan yang sedang mendengarkan (Apache, SSH, MySQL, RDP).
3. **OS Fingerprinting**: Mengestimasi sistem operasi dan versi kernel berdasarkan respons stack TCP/IP.
4. **Otomasi Audit dengan Nmap Scripting Engine (NSE)**: Menjalankan ratusan skrip Lua untuk mengecek kerentanan CVE (seperti EternalBlue, Log4j, SSL ciphers lemah).

### ❌ Kapan JANGAN Menggunakan Nmap?
- **Massive Internet-Scale Scanning (> /16 subnet)**: Untuk pemindaian seluruh rentang internet, Masscan atau ZMap jauh lebih cepat karena arsitektur stateless-nya (meski Nmap jauh lebih akurat untuk analisis layanan mendalam).

---

## 🚀 Perintah Cepat (Quickstart)

```bash
# Pemindaian Cepat Port Terbuka & Deteksi Versi
nmap -sV -sC -T4 192.168.1.100

# Audit Kelemahan SSL/TLS pada Web Server
nmap --script ssl-enum-ciphers -p 443 192.168.1.100

# Pemindaian Seluruh Port TCP (1 - 65535)
nmap -p- -T4 192.168.1.100 -oA hasil_scan_penuh
```
