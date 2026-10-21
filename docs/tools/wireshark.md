# 🛡️ Tool Profile: Wireshark

> The World's Foremost and Widely-Used Network Protocol and Packet Analyzer.

---

## 📌 Ringkasan Eksekutif

| Parameter | Keterangan |
| :--- | :--- |
| **Kategori Tim** | 🔵 Blue Team / 🟣 Purple Team |
| **Kapabilitas Utama** | `packet-analysis`, `dfir` |
| **Model Arsitektur** | Desktop GUI / CLI (`tshark`) Packet Dissector in C/C++ |
| **Lisensi** | GPL-2.0-or-later |
| **Pemeliharaan (*Maintenance*)** | Sangat Aktif (Wireshark Foundation) |
| **Situs Resmi** | [wireshark.org](https://www.wireshark.org/) |
| **Repositori Resmi** | [github.com/wireshark/wireshark](https://github.com/wireshark/wireshark) |

---

## 🎯 Kapan Menggunakan Wireshark?

### ✅ Skenario Terbaik (Best Use Cases)
1. **Forensik Jaringan Sesi Mikro**: Menganalisis berkas tangkapan (`.pcap` / `.pcapng`) untuk membedah urutan paket byte-per-byte saat investigasi insiden siber.
2. **Follow TCP / TLS Stream**: Merekonstruksi percakapan utuh antara client dan server untuk melihat muatan transaksi HTTP, SMTP, atau payload malware yang tidak terenkripsi.
3. **Troubleshooting Protokol Kustom**: Membedah struktur header protokol proprietary dan decoding ribuan format protokol jaringan.
4. **Ekstraksi Objek Transmisi**: Menyimpan file yang ditransfer melalui HTTP, SMB, atau TFTP langsung dari berkas capture pcap.

### ❌ Kapan JANGAN Menggunakan Wireshark?
- **Pemantauan Gateway Produksi Jangka Panjang**: Menjalankan Wireshark GUI secara terus-menerus pada gateway traffic tinggi berisiko crash kehabisan memori. Gunakan `tcpdump`, `Zeek`, atau `Suricata` untuk capture level jaringan.

---

## 🚀 Perintah Cepat (`tshark` CLI)

```bash
# Menampilkan IP Pengirim dan Penerima dari file PCAP
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e _ws.col.Protocol

# Mengekstrak semua query DNS yang tercatat
tshark -r capture.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name

# Menemukan percobaan login HTTP basic auth
tshark -r capture.pcap -Y "http.authorization" -T fields -e http.authorization
```
