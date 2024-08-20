# BlinkPDF Patching Rule

## 1. Objective

Tujuan dari patching rule ini adalah untuk melindungi sistem dari serangan pencurian flag pada aplikasi. Patching dapat dilakukan dengan cara apapun selagi masih memenuhi peraturan pada poin 2-3 dan memperhatikan poin 4.

## 2. Allowed Patching Techniques

- **Modifikasi parameter, script, dan fungsi pada algorithm** untuk memperbaiki kerentanan pada algoritma.

## 3. Prohibited Patching Techniques

- **Penggantian atau modifikasi flow algorithm** untuk mengubah cara kerja algoritma sehingga fungsi aplikasi menjadi berubah.
- **Penyembunyian atau penggantian flag** untuk membuat flag palsu atau salah.
- **Penggunaan firewall** untuk memfilter dan membatasi lalu lintas jaringan yang mencurigakan.

## 4. Main Point

Proses patching dibebaskan dengan syarat:

- flow aplikasi masih berjalan sebagaimana mestinya
- flow algoritma masih berjalan sebagaimana mestinya (tidak mengubah algoritma yang digunakan)
- perhatikan command pada source code untuk mengetahui tempat yang dilarang untuk dilakukan modifikasi
