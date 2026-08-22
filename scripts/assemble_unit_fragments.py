#!/usr/bin/env python3
"""Assemble reviewed contiguous translation fragments deterministically."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPECS = {
    "O005-LEGA-V101-CH03": {
        "source_lines": 410,
        "problem_count": 23,
        "fragments": [
            "01-main-through-nonlinear.html",
            "02-friction-summary-descriptions.html",
            "03-problems.html",
        ],
        "replacements": [
            (
                "merupakan simpul stabil (jika $latex \\alpha^2 \\gt 4)$ atau spiral stabil (jika $latex \\alpha^2 \\lt 4$).",
                "merupakan simpul stabil (jika $latex \\alpha^2 \\gt 4$), simpul stabil degenerat pada kasus kesamaan di batas 4, atau spiral stabil (jika $latex \\alpha^2 \\lt 4$).",
                1,
            ),
            (
                "simpul stabil degenerat pada kasus kesamaan di batas 4",
                "simpul stabil degenerat pada kasus kritis ketika kuadrat koefisien redaman sama dengan 4",
                1,
            ),
            (
                "manifold tak stabil dari $latex ((2 p + 1) \\pi,0)$ memuat titik-titik tetap stabil $latex (2 p \\pi,0)$ dan $latex ((2 p + 2) \\pi,0)$.",
                "cabang-cabang manifold tak stabil dari $latex ((2 p + 1) \\pi,0)$ mendekati titik-titik tetap stabil $latex (2 p \\pi,0)$ dan $latex ((2 p + 2) \\pi,0)$; kedua titik itu berada dalam penutupan manifold tersebut.",
                1,
            ),
            (
                "$latex A, B \\in \\mathbb{R}$",
                "$latex C, \\phi \\in \\mathbb{R}$",
                1,
            ),
            (
                "$latex (1,-\\sin(\\theta))$",
                "$latex (\\Lambda,-\\sin(\\theta))$",
                1,
            ),
            (
                "ruas kiri Persamaan (<a href=\"#sol_curv\">3.13</a>) bernilai real",
                "ruas kanan Persamaan (<a href=\"#sol_curv\">3.13</a>) bernilai real",
                1,
            ),
            (
                "merupakan titik ekstrem $latex V(x)$",
                "merupakan titik kritis $latex V(x)$",
                1,
            ),
            (
                "Dapat diperiksa bahwa titik minimum $latex V$ bersesuaian dengan <em>pusat</em> dan titik maksimum $latex V$ dengan <em>titik pelana</em> (lihat soal-soal).",
                "Jika titik-titik kritis tersebut nondegenerat, dapat diperiksa bahwa titik minimum $latex V$ bersesuaian dengan <em>pusat</em> dan titik maksimum $latex V$ dengan <em>titik pelana</em> (lihat soal-soal).",
                1,
            ),
            (
                "Lintasan-lintasan ini memiliki garis singgung vertikal pada titik potong tersebut (lihat soal-soal).",
                "Apabila turunan potensial tidak nol di titik potong tersebut, lintasan-lintasan ini memiliki garis singgung vertikal di sana (lihat soal-soal).",
                1,
            ),
            (
                "dapat diduga bahwa lintasan dengan $latex d \\theta / d \\tau \\ne 0$ akan konvergen menuju solusi berenergi $latex E = -1$.",
                "dapat diduga bahwa lintasan generik yang bukan kesetimbangan—sehingga $latex d \\theta / d \\tau \\ne 0$ setidaknya pada sebagian waktu—dan tidak terletak pada manifold stabil titik pelana akan konvergen menuju solusi berenergi $latex E = -1$.",
                1,
            ),
            (
                "sebanding dengan negatif dari kecepatan massa",
                "berlawanan arah dan sebanding dengan kecepatan massa",
                1,
            ),
            (
                "sistem dinamika dua dimensi nonkonservatif",
                "sistem dinamik dua dimensi nonkonservatif",
                1,
            ),
            (
                "disebut <em>Jacobian</em> sistem",
                "disebut <em>matriks Jacobi</em> sistem",
                1,
            ),
            (
                "dengan $latex C, \\phi \\in \\mathbb{R}$, jika $latex A$ dan $latex B$ dinyatakan",
                "dengan $latex A, B \\in \\mathbb{R}$, jika $latex A$ dan $latex B$ dinyatakan",
                1,
            ),
            (
                "$latex \\bar x \\in [x_0,x]$",
                "$latex \\bar x \\in [\\min(x_0,x),\\max(x_0,x)]$",
                1,
            ),
            (
                "Perhatikan persamaan diferensial berikut, $latex \\displaystyle \\frac{d x}{d t} = \\lambda x - \\gamma x^3.$",
                "Perhatikan persamaan diferensial berikut, $latex \\displaystyle \\frac{d x}{d t} = \\lambda x - \\gamma x^3.$ Untuk penskalaan real, perlakukan secara terpisah kasus ketika salah satu parameter nol; jika keduanya tidak nol, besar parameternya dapat diserap, tetapi tandanya tetap menentukan kelas dinamika.",
                1,
            ),
            (
                "untuk “menghilangkan” parameter $latex \\lambda$.",
                "untuk menghilangkan besar parameter $latex \\lambda$ ketika parameter itu tidak nol. Jelaskan pula apa yang terjadi ketika λ = 0 dan besaran diskret apa yang masih tersisa ketika λ ≠ 0.",
                1,
            ),
            (
                "Dapatkah Anda menemukan perubahan variabel yang juga memungkinkan Anda menghilangkan $latex \\gamma$?",
                "Jika γ ≠ 0, dapatkah Anda menemukan perubahan variabel yang juga menghilangkan besar $latex \\gamma$? Jelaskan peran tanda γ dan kasus γ = 0.",
                1,
            ),
            ("[\\hbox{force}]", "[\\hbox{gaya}]", 2),
            ("merujuk ke", "merujuk pada", 1),
            ("dikerahkan", "diberikan", 3),
            ("dalam vektor", "dalam basis vektor", 2),
            ("dalam sudut", "sebagai fungsi sudut", 1),
            ("persamaan(-persamaan)", "persamaan-persamaan", 1),
            ("bernilai real", "bernilai riil", 2),
            ("orde dua", "orde kedua", 5),
            ("keseimbangan", "kesetimbangan", 1),
            ("kerapatan gaya badan", "gaya badan per satuan volume", 1),
            (
                "menyatakan turunan pertama dan kedua vektor posisi $latex \\vec x$ dalam basis vektor $latex \\vec r$ dan $latex \\vec \\theta$, serta dalam turunan-turunan sudut $latex \\theta$",
                "menyatakan turunan pertama dan kedua vektor posisi $latex \\vec x$ dalam bentuk vektor $latex \\vec r$, $latex \\vec \\theta$, dan turunan sudut $latex \\theta$",
                1,
            ),
            ("uraikan ruas kanannya", "uraikan ruas-ruas kanannya", 1),
            ("sistem dinamis", "sistem dinamik", 3),
            ("sistem dinamika", "sistem dinamik", 1),
            ("orde satu", "orde pertama", 3),
            (
                "$latex \\displaystyle \\frac{d^2 x}{d t^2} + \\omega^2 x = \\epsilon \\frac{d x}{d t} (1 - x^2), \\qquad \\epsilon \\ge 0.$",
                "$latex \\displaystyle \\frac{d^2 x}{d t^2} + \\omega^2 x = \\epsilon \\frac{d x}{d t} (1 - x^2), \\qquad \\epsilon \\ge 0, \\qquad \\omega \\gt 0.$",
                1,
            ),
            (
                "$latex \\min(V) \\lt E \\lt \\max(V)$",
                "$latex \\inf V \\lt E \\lt \\sup V$",
                1,
            ),
            ("$latex \\min(V)$", "$latex \\inf V$", 1),
            ("$latex \\max(V)$", "$latex \\sup V$", 1),
            (
                "lintasan horizontal bergelombang di bagian atas dan bawah bingkai. [",
                "lintasan horizontal bergelombang di bagian atas dan bawah bingkai. Catatan: label vertikal pada gambar sumber menggunakan dθ/dt, sedangkan model tak berdimensi dalam teks menggunakan dθ/dτ. [",
                1,
            ),
            (
                '[caption id="attachment_33" align="alignleft" width="300"]',
                '[caption id="attachment_29" align="alignleft" width="300"]',
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Mech_pot1-1-300x218.png",
                "assets/potential-1-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Mech_pot2-1-300x166.png",
                "assets/potential-2-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Mech_pot3-1-300x271.png",
                "assets/potential-3-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Mech_pot4-1-300x160.png",
                "assets/potential-4-source.png",
                1,
            ),
            (
                "assets/phase-portrait-construction-source.png",
                "assets/phase-portrait-construction-id-v3.png",
                1,
            ),
            (
                'alt="Shape of the potential V. Long description below."',
                'alt="Bentuk potensial V. Deskripsi panjang tersedia di bawah."',
                4,
            ),
            ("$x$", "$latex x$", 2),
        ],
    },
    "O005-LEGA-V101-CH04": {
        "source_lines": 185,
        "problem_count": 4,
        "fragments": [
            "01-model-and-equations.html",
            "02-analysis-summary-descriptions.html",
            "03-problems.html",
        ],
        "replacements": [
            (
                "Memberikan alasan bagi pendekatan-pendekatan yang digunakan untuk menyederhanakan persamaan gerak.",
                "Menjelaskan alasan penggunaan aproksimasi untuk menyederhanakan persamaan gerak.",
                1,
            ),
            (
                "batu tipis, pipih (planar), homogen, dan simetris",
                "batu tipis, pipih, homogen, dan simetris",
                1,
            ),
            (
                r"\frac{d \vec V}{d t}",
                r"\frac{\partial \vec V}{\partial t}",
                1,
            ),
            (
                r"\frac{d \omega_y}{d t}",
                r"\frac{d \omega_{-y}}{d t}",
                1,
            ),
            (
                r"\displaystyle I_t \frac{d \omega_p}{d t}",
                r"\displaystyle I_p \frac{d \omega_p}{d t}",
                1,
            ),
            (
                "Rotasi benda tegar batu terhadap pusat massanya diberikan oleh persamaan Euler,",
                "Gerak rotasi batu sebagai benda tegar terhadap pusat massanya diberikan oleh persamaan Euler,",
                1,
            ),
            (
                "Kerangka ortonormal $latex (-\\vec y, \\vec n, \\vec p)$ melekat pada pusat massa batu dan berotasi bersamanya.",
                "Kerangka ortonormal $latex (-\\vec y, \\vec n, \\vec p)$ melekat pada pusat massa batu dan berotasi bersamanya. Dalam penampang pada Gambar 4.1, arah $latex \\vec p$ berimpit dengan arah tangensial $latex \\vec t$.",
                1,
            ),
            (
                r"\begin{array} \displaystyle J_1",
                r"\begin{array}{ll} \displaystyle J_1",
                1,
            ),
            (
                r"$latex \theta(t) = \omega_{-y}(0)\, t.$",
                r"$latex \theta(t) = \theta(0) + \omega_{-y}(0)\, t.$",
                1,
            ),
            (
                r"$latex \theta(t) = \theta(0) + \frac{1}{\delta} \omega_{-y}(0) \sin(\delta t) - \frac{1}{\delta} \omega_p(0) \cos(\delta t)$",
                r"$latex \theta(t) = \theta(0) + \frac{\omega_{-y}(0)}{\delta} \sin(\delta t) + \frac{\omega_p(0)}{\delta} \left[1-\cos(\delta t)\right]$",
                1,
            ),
            (
                "rotasi terhadap sumbu $latex \\vec y$",
                "rotasi terhadap sumbu $latex -\\vec y$",
                1,
            ),
            (
                r"$latex \tau_f = \frac{2 v_z(0)}{g},$",
                r"$latex \tau_f = \frac{2 v_z(0)}{g}, \qquad v_z(0) \gt 0,$",
                1,
            ),
            (
                r"$latex {\mathcal U}(z) = \int_0^z F(s)\, ds,$",
                r"$latex {\mathcal U}(z) = \int_0^z {\mathcal F}(s)\, ds,$",
                1,
            ),
            (
                "Kehilangan energi bertanda $latex \\mathcal W$ sama dengan usaha yang dilakukan oleh gaya gesek air pada batu.",
                "Perubahan energi selama tumbukan, yang dinyatakan dengan $latex \\mathcal W$, sama dengan usaha yang dilakukan oleh gaya gesek air pada batu dan bernilai negatif untuk disipasi.",
                1,
            ),
            (r"$latex \theta = 20^o$", r"$latex \theta = 20^\circ$", 1),
            (r"$latex C_n$", r"$latex C_f$", 1),
            (
                "parameter sudut untuk kemiringan batu ($latex \\theta$), vektor kecepatan ($latex \\vec{v}$), dan sudut tumbukan ($latex \\beta$)",
                "sudut kemiringan batu ($latex \\theta$), vektor kecepatan batu ($latex \\vec{v}$), dan sudut datang ($latex \\beta$)",
                1,
            ),
            (
                "$latex \\alpha$ masing-masing bernilai $latex y,\\,n$, dan $latex p$.",
                "$latex \\alpha$ masing-masing bernilai $latex -y,\\,n$, dan $latex p$.",
                1,
            ),
            (
                "Perhatikan Persamaan (<a href=\"#Stone_New5\">4.11</a>) dan anggap bahwa batu berbentuk persegi.",
                "Perhatikan Persamaan (<a href=\"#Stone_New5\">4.11</a>) dan anggap bahwa batu berbentuk persegi. Ambil $latex t=0$ pada awal tumbukan, dengan kondisi awal $latex z(0)=0$ dan $latex \\dot z(0)=v_z(0)\\lt 0$. Rumus luas terendam pada soal ini berlaku selama perendaman parsial, yaitu $latex -a\\sin(\\theta)\\leq z\\leq 0$.",
                1,
            ),
            (
                "Dinamika sisi batu persegi yang terendam selama fase tumbukan dideskripsikan oleh (lihat Soal 2)",
                "Dinamika sisi batu persegi yang terendam selama fase tumbukan dideskripsikan oleh (lihat Soal 2). Untuk bagian-bagian berikut, abaikan ketebalan $latex h$, tetapkan $latex C \\equiv C_l\\cos(\\theta)-C_f\\sin(\\theta)\\gt 0$, gunakan $latex v_z(0)=-v_x(0)\\tan(\\beta)$, dan asumsikan ruas dalam tanda kurung siku pada hasil akhir positif. Dengan konvensi $latex z\\lt 0$ di bawah permukaan, batu mulai terendam seluruhnya ketika $latex |z|\\geq a\\sin(\\theta)$.",
                1,
            ),
            (
                r"$latex \displaystyle \frac{d^2 \theta}{d t^2} + \frac{J_0 - J_1}{J_1} (\theta - \theta(0)) = \frac{{\mathcal M}_\theta}{J_1},$",
                r"$latex \displaystyle \frac{d^2 \theta}{d t^2} + \nu^2 \left(\theta - \theta(0)\right) = \frac{{\mathcal M}_\theta}{J_1},$",
                1,
            ),
            (
                "dengan $latex {\\mathcal M}_\\theta$ sebagai proyeksi torsi yang dikerahkan air pada batu ke sumbu $latex \\vec y$.",
                "dengan $latex \\nu = ((J_0-J_1)/J_1)\\,\\Omega_0$, sedangkan $latex {\\mathcal M}_\\theta \\equiv N_{-y}$ adalah komponen torsi yang diberikan air pada batu dalam arah peningkatan sudut kemiringan (sumbu $latex -\\vec y$). Bentuk ini mempertahankan kuadrat frekuensi $latex \\nu^2$ pada Persamaan (20) artikel sumber.",
                1,
            ),
        ],
    },
    "O005-LEGA-V101-CH05": {
        "source_lines": 326,
        "problem_count": 17,
        "fragments": [
            "01-first.html",
            "02-age-distribution-through-problem07.html",
            "03-problem08-through-end.html",
        ],
        "replacements": [
            (
                "Nilai $latex 1.025$ juga cukup dekat dengan interval kepercayaan 95% [1.026, 1.029]",
                "Nilai $latex 1.025$ dekat dengan, tetapi sedikit lebih kecil dan berada di luar, interval kepercayaan 95% [1.026, 1.029]",
                1,
            ),
            (
                "yaitu $latex b - d = 0.025$ individu per tahun.",
                r"yaitu $latex b-d=0.025\ \text{tahun}^{-1}$.",
                1,
            ),
            (
                r"Parameter $latex N_\infty$ menyatakan daya dukung lingkungan.",
                r"Parameter $latex N_\infty$ menyatakan daya dukung lingkungan. Simbol $latex \kappa$ di sini berbeda dari pengali tak berdimensi pada Persamaan (5.1): parameter ini berdimensi invers populasi, $latex [\kappa]=[\text{populasi}]^{-1}$. Agar model populasi tetap bermakna, parameter dan rentang keadaan harus dipilih sehingga $latex 1+\kappa\bigl(N_\infty-N(t)\bigr)\geq 0$.",
                1,
            ),
            (
                "yang memiliki laju pertumbuhan yang bergantung pada $latex N$ per-$latex \\Delta t$, yaitu $latex \\Big(1 + \\kappa \\big(N_\\infty - N(t)\\big)\\Big)$.",
                "yang memiliki faktor pengali pertumbuhan yang bergantung pada $latex N$ untuk setiap langkah $latex \\Delta t$, yaitu $latex \\Big(1 + \\kappa \\big(N_\\infty - N(t)\\big)\\Big)$. Laju pertumbuhan fraksional per langkahnya adalah $latex \\kappa\\big(N_\\infty-N(t)\\big)$.",
                1,
            ),
            (
                r"Jika $latex |f^\prime(N_c)| = 1,$ titik $latex N = N_c$ <em>stabil marginal</em>.",
                r"Jika $latex |f^\prime(N_c)| = 1,$ linearisasi tidak menentukan kestabilan titik $latex N = N_c$; titik tersebut <em>nonhiperbolik</em> dan suku nonlinear harus diperiksa.",
                1,
            ),
            (
                "Titik ini stabil untuk $latex a \\lt 1$ dan stabil marginal jika $latex a = 1$.",
                "Titik ini stabil untuk $latex a \\lt 1$. Jika $latex a = 1$, titik tersebut nonhiperbolik: pada ruang keadaan fisik $latex x \\in [0,1]$ ia menarik dari kanan, sedangkan pada garis real ia hanya menarik dari satu sisi.",
                1,
            ),
            ("Mitchell J. Feigenbaurn", "Mitchell J. Feigenbaum", 1),
            (
                "berguna untuk memandang $latex R(t) \\delta t + O(\\delta t^2)$ sebagai peluang pertumbuhan per kapita",
                "berguna untuk memandang $latex R(t) \\delta t + O(\\delta t^2)$ sebagai perubahan bersih per kapita yang diharapkan; besaran ini bukan peluang jika laju bersihnya negatif",
                1,
            ),
            (
                "fungsi terdiferensialkan dari $latex t$",
                "fungsi yang dapat didiferensialkan terhadap $latex t$",
                1,
            ),
            (
                "Dalam bagian selanjutnya catatan ini",
                "Dalam bagian selanjutnya dari catatan ini",
                1,
            ),
            (
                "Solusi Persamaan (<a href=\"#Logistic_cont\">5.5</a>) dengan kondisi awal $latex M(0) = M_0$ adalah $latex M(t) = \\displaystyle \\left[1 + \\frac{1-M_0}{M_0} \\exp(- \\lambda t)\\right]^{-1},$ untuk semua nilai parameter $latex \\lambda$. Ketika $latex t \\rightarrow \\infty$, $latex M \\rightarrow 1$ jika $latex \\lambda &gt; 0$, untuk semua nilai $latex M_0$.",
                "Solusi Persamaan (<a href=\"#Logistic_cont\">5.5</a>) dengan kondisi awal $latex M(0) = M_0$ dan $latex M_0 \\gt 0$ adalah $latex M(t) = \\displaystyle \\left[1 + \\frac{1-M_0}{M_0} \\exp(- \\lambda t)\\right]^{-1},$ untuk semua nilai parameter $latex \\lambda$ pada selang keberadaan solusi. Ketika $latex t \\rightarrow \\infty$, $latex M \\rightarrow 1$ jika $latex \\lambda &gt; 0$ untuk semua nilai positif $latex M_0$. Kasus $latex M_0=0$ merupakan kesetimbangan tersendiri dan solusinya tetap nol.",
                1,
            ),
            ("Titik-titik tetap Persamaan (5.39)", "Titik-titik tetap Persamaan (5.6)", 1),
            (
                "Memang, $latex f(N)$ berubah tanda pada $latex N = N_c$.",
                "Periksalah tanda $latex f(N)$ pada kedua sisi $latex N = N_c$; nol bermultiplikitas genap tidak harus disertai perubahan tanda.",
                1,
            ),
            (
                "Matriks $latex A$ biasanya memiliki entri konstan dan taknegatif. Dalam konteks model dinamika populasi, matriks ini disebut <em>matriks Leslie</em>.",
                r"Matriks $latex A$ memiliki entri konstan dan taknegatif jika laju-lajunya taknegatif serta $latex (d_1+g_1)\Delta t\leq 1$, $latex (d_2+g_2)\Delta t\leq 1$, dan $latex d_3\Delta t\leq 1$. Karena matriks ini memuat retensi pada diagonal dan kelas tahap, bentuknya lebih tepat disebut <em>matriks proyeksi kelas tahap bertipe Lefkovitch</em> daripada matriks Leslie klasik.",
                1,
            ),
            (
                "$latex b_2$ adalah laju per kapita individu dalam kelompok 2 melahirkan",
                "$latex b_2$ adalah laju kelahiran per kapita pada kelompok 2",
                1,
            ),
            (
                "(LPA merupakan singkatan dari Larva, Pupa, Dewasa)",
                "(LPA menyingkat istilah Inggris Larva, Pupa, Adult, yakni larva, pupa, dan dewasa)",
                1,
            ),
            (
                "artikel Jim Cushing <em>et al</em>. tahun 2004",
                "artikel Jim Cushing <em>et al</em>. tahun 1998",
                1,
            ),
            (
                "model kontinu satu dimensi (maupun dua dimensi) memiliki dinamika yang sangat sederhana. Secara khusus, model-model tersebut tidak dapat memperlihatkan kekacauan.",
                "ODE otonom reguler satu dimensi dan aliran otonom planar dua dimensi dengan solusi unik memiliki dinamika yang jauh lebih terbatas. Secara khusus, sistem-sistem tersebut tidak dapat memperlihatkan atraktor kacau.",
                1,
            ),
            (
                "Perkirakan nilai $latex \\kappa$ dari Gambar 5.1, yang menunjukkan jumlah elang ekor-merah di Amerika Serikat sebagai fungsi waktu.",
                "Perkirakan nilai $latex \\kappa$ dari Gambar 5.1 pada selang pencocokan 1950–1995, yang menunjukkan jumlah elang ekor-merah di Amerika Serikat sebagai fungsi waktu.",
                1,
            ),
            (
                "Apakah model diskret lebih cepat atau lebih lambat daripada hampiran kontinunya?</li>",
                "Apakah model diskret lebih cepat atau lebih lambat daripada hampiran kontinunya? Bedakan korespondensi beda-maju dari sampling eksak, dan gunakan korespondensi beda-maju untuk perbandingan cepat atau lambat.</li>",
                1,
            ),
            (
                "Apa yang Anda amati?</li>",
                r"Apa yang Anda amati? Pada nilai kritis $latex a=0$ dan $latex a=4/27$, klasifikasikan titik tetap ganda sebagai nonhiperbolik, bukan memaksanya ke dalam pilihan stabil atau tak stabil.</li>",
                1,
            ),
            (
                "Gunakan metode karakteristik untuk menyelesaikan persamaan diferensial parsial McKendrick yang diturunkan dalam Soal 9.",
                r"Gunakan metode karakteristik untuk menyelesaikan persamaan diferensial parsial McKendrick yang diturunkan dalam Soal 9. Nyatakan solusi dalam bentuk data awal $latex M(a,0)=M_0(a)$ dan syarat batas kelahiran $latex M(0,t)=B(t)$.",
                1,
            ),
            (
                "dengan $latex b$, $latex d_J$, dan $latex d_A$ sebagai parameter positif.",
                r"dengan $latex b\gt 0$, $latex c\gt 0$, dan $latex 0\leq d_J,d_A\leq 1$ sebagai parameter.",
                1,
            ),
            (
                "Impor himpunan data ini ke MATLAB atau EXCEL.",
                "Gunakan salinan lokal terverifikasi dari himpunan data ini dalam buku catatan Python terbuka pendamping.",
                1,
            ),
            (
                "<em>laju kematian per</em> k<em>apita</em>",
                "<em>laju kematian</em> per <em>kapita</em>",
                1,
            ),
            (
                "selama rentang sedikit lebih dari 100 \"Tahun\"",
                "dengan sumbu horizontal berlabel \"Tahun\" yang membentang sedikit lebih dari 100 tahun",
                1,
            ),
            ("garis merah utuh", "garis merah tak terputus", 1),
            ("jalur menuju chaos", "jalur menuju kekacauan", 1),
            ("keadaan chaos", "keadaan kacau", 1),
            ("memperlihatkan chaos", "memperlihatkan kekacauan", 1),
            ("takstabil", "tak stabil", 8),
            ("ketak stabilan", "ketakstabilan", 1),
            ("pemetaan logistik", "peta logistik", 2),
            ("sampling eksak", "pencuplikan eksak", 1),
            (
                r"dengan $latex f^k$ merupakan iterasi $latex k^{\text{th}}$ dari $latex f$.",
                r"dengan $latex f^k$ merupakan iterasi ke-$latex k$ dari $latex f$.",
                1,
            ),
            ("sifat-sifat dinamis model LPA", "sifat-sifat dinamik model LPA", 1),
            (
                "ODE otonom reguler satu dimensi dan aliran otonom planar dua dimensi",
                "persamaan diferensial biasa otonom reguler satu dimensi dan aliran otonom planar dua dimensi",
                1,
            ),
            ("nilai eigennya real", "nilai eigennya riil", 1),
            ("satu nilai eigen real", "satu nilai eigen riil", 1),
            ("entri real", "entri riil", 1),
            ("kondisi awal real", "kondisi awal riil", 1),
            ("<sup>o</sup>", "<sup>°</sup>", 3),
            (
                '[caption id="attachment_41" align="alignleft" width="450"]',
                '[caption id="attachment_41" align="alignleft" width="300"]',
                1,
            ),
            (
                '[caption id="attachment_42" align="alignleft" width="450"]',
                '[caption id="attachment_42" align="alignleft" width="300"]',
                1,
            ),
            (
                '[caption id="attachment_47" align="alignleft" width="450"]<img class="wp-image-43"',
                '[caption id="attachment_43" align="alignleft" width="300"]<img class="wp-image-43"',
                1,
            ),
            (
                '[caption id="attachment_47" align="alignleft" width="287"]<img class="wp-image-44 size-medium"',
                '[caption id="attachment_44" align="alignleft" width="287"]<img class="wp-image-44 size-medium"',
                1,
            ),
            (
                '[caption id="attachment_47" align="alignleft" width="300"]<img class="wp-image-45 size-medium"',
                '[caption id="attachment_45" align="alignleft" width="300"]<img class="wp-image-45 size-medium"',
                1,
            ),
            (
                '[caption id="attachment_47" align="alignleft" width="300"]<img class="size-medium wp-image-46"',
                '[caption id="attachment_46" align="alignleft" width="300"]<img class="size-medium wp-image-46"',
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Redhawk_US_1-105-300x213.png",
                "assets/redhawk-count-id.svg",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Redhawk_US_1-105_rate-300x213.png",
                "assets/redhawk-rate-id.svg",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Redhawk_US_1-105_1stR-300x213.png",
                "assets/redhawk-return-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Iterations-287x300.png",
                "assets/cobweb-iterations-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Logistic1a-300x241.png",
                "assets/logistic-bifurcation-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Logistic2a-300x239.png",
                "assets/logistic-bifurcation-zoom-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Gen_stable-300x220.png",
                "assets/one-dimensional-stability-id.svg",
                1,
            ),
            ('alt="Plot of annual bird count. Long description available." width="450" height="320"', 'alt="Plot jumlah burung tahunan. Deskripsi panjang tersedia." width="300" height="213"', 1),
            ('alt="Plot of the normalized rate of change. Long description available." width="450" height="320"', 'alt="Plot laju perubahan ternormalisasi. Deskripsi panjang tersedia." width="300" height="213"', 1),
            ('alt="First return map of the annual bird count. Long description available." width="450" height="320"', 'alt="Peta balik pertama jumlah burung tahunan. Deskripsi panjang tersedia." width="300" height="213"', 1),
            ('alt="Cobweb plot. Long description available."', 'alt="Diagram jaring laba-laba. Deskripsi panjang tersedia."', 1),
            ('alt="Bifurcation diagram. Long description available."', 'alt="Diagram bifurkasi. Deskripsi panjang tersedia."', 1),
            ('alt="Zoomed-in bifurcation diagram. Long description available."', 'alt="Pembesaran diagram bifurkasi. Deskripsi panjang tersedia."', 1),
            ('alt="Stability diagram of a one-dimensional system. Long description available."', 'alt="Diagram kestabilan sistem satu dimensi. Deskripsi panjang tersedia."', 1),
        ],
    },
    "O005-LEGA-V101-CH06": {
        "source_lines": 182,
        "problem_count": 6,
        "fragments": [
            "01-predator-prey.html",
            "02-competition-exercises.html",
        ],
        "replacements": [],
    },
    "O005-LEGA-V101-CH07": {
        "source_lines": 123,
        "problem_count": 5,
        "fragments": [
            "01-viral-intro.html",
            "02-sir-endemic-summary.html",
            "03-exercises.html",
        ],
        "replacements": [],
    },
    "O005-LEGA-V101-CH08": {
        "source_lines": 216,
        "problem_count": 13,
        "fragments": [
            "01-objectives-mass-action-brusselator.html",
            "02-oregonator-waves-summary-figures.html",
            "03-exercises.html",
        ],
        "replacements": [],
    },
    "O005-LEGA-V101-CH09": {
        "source_lines": 172,
        "problem_count": 7,
        "fragments": [
            "01-objectives-macroscopic-diffusion.html",
            "02-microscopic-diffusion-fisher-kpp.html",
            "03-chemical-waves-summary-exercises.html",
        ],
        "replacements": [],
    },
    "O005-LEGA-V101-CH10": {
        "source_lines": 98,
        "problem_count": 6,
        "fragments": [
            "01-objectives-turing-and-model.html",
            "02-linear-stability-and-selection.html",
            "03-vegetation-summary-descriptions.html",
            "04-exercises.html",
        ],
        "replacements": [],
    },
    "O005-LEGA-V101-CH11": {
        "source_lines": 166,
        "problem_count": 7,
        "fragments": [
            "01-vector-spaces-and-linear-mappings.html",
            "02-matrices.html",
            "03-eigenvalues-and-eigenvectors.html",
            "04-exercises.html",
        ],
        "replacements": [
            (
                "$latex \\mathcal S$ adalah <em>ruang vektor</em> real (atau kompleks) jika dan hanya jika tertutup terhadap penjumlahan dan perkalian dengan skalar. Dengan kata lain,",
                "Himpunan bagian tak kosong $latex \\mathcal S$ dari suatu ruang vektor real (atau kompleks) merupakan <em>ruang vektor</em> jika dan hanya jika tertutup terhadap penjumlahan dan perkalian dengan skalar. Dengan kata lain,",
                1,
            ),
            (r"\text{ (resp. }", r"\text{ (atau }", 1),
            (
                r"\{u_i \in S, i=1 \dots n\}",
                r"\{u_i\in\mathcal S\mid i=1,\dots,n\}",
                1,
            ),
            (
                r"\begin{align*} \forall &amp;\{\alpha_i, i=1, \dots n \} \subset \mathbb{R} \text { (or } \mathbb{C}),\\ &amp;\sum_{i=1}^n \alpha_i\,u_i = 0 \Longrightarrow \alpha_i = 0, \forall i=1, \dots n. \end{align*}",
                r"\begin{align*} &amp;\forall\,\alpha_1,\dots,\alpha_n \in \mathbb{R} \text{ (atau } \mathbb{C}),\\ &amp;\sum_{i=1}^n \alpha_i\,u_i = 0 \Longrightarrow \alpha_i = 0,\ \forall i=1,\dots,n. \end{align*}",
                1,
            ),
            (r"i^{\hbox{th}}", "i", 1),
            (r"j^{\hbox{th}}", "j", 1),
            (
                "<span style=\"text-align: initial;font-size: 1em\">Perhatikan bahwa setelah suatu basis dipilih, setiap </span>ruang vektor berdimensi $latex n$ isomorfik dengan $latex \\mathbb{R}^n$.",
                "<span style=\"text-align: initial;font-size: 1em\">Perhatikan bahwa setelah suatu basis dipilih, setiap </span>ruang vektor real berdimensi $latex n$ isomorfik dengan $latex \\mathbb{R}^n$.",
                1,
            ),
            (r"(A^T_{ij}) = (A_{ji})", r"(A^T)_{ij}=A_{ji}", 1),
            (
                "$latex i$ adalah satu baris dari $latex A$",
                "$latex i$ adalah indeks baris tetap pada $latex A$",
                1,
            ),
            (
                "Persamaan $latex A X = b$ memiliki tepat satu solusi.",
                "Persamaan $latex A x = b$ memiliki tepat satu solusi untuk setiap ruas kanan.",
                1,
            ),
            (
                "Misalkan $latex A$ adalah matriks real berukuran $latex n \\times n$.",
                "Misalkan $latex A$ adalah matriks real berukuran $latex n \\times n$. Untuk nilai eigen tak real, pembahasan dilakukan dalam ruang vektor kompleks yang diperoleh dengan memperluas skalar.",
                1,
            ),
            (
                "merupakan <em>vektor eigen tergeneralisasi</em> dari $latex A$ dengan <em>nilai eigen</em> $latex a$ jika, untuk suatu bilangan bulat positif $latex m \\ne 1$, berlaku",
                "merupakan <em>vektor eigen tergeneralisasi</em> dari $latex A$ dengan <em>nilai eigen</em> $latex a$ jika, untuk suatu bilangan bulat positif $latex m \\ge 1$, vektor tersebut berperingkat tepat m dalam arti bahwa",
                1,
            ),
            (
                r"(A - a I_n) f \ne 0, \qquad (A - a I_n)^m f = 0, \qquad f \ne 0.",
                r"(A - a I_n)^{m-1} f \ne 0, \qquad (A - a I_n)^m f = 0, \qquad f \ne 0.",
                1,
            ),
            (r"\det (A - a I)= 0", r"\det (A - a I_n)= 0", 1),
            (
                "Polinom karakteristik $latex A$ memiliki $latex n$ akar kompleks, yang merupakan nilai-nilai eigen $latex A$.",
                "Polinom karakteristik $latex A$ memiliki $latex n$ akar kompleks jika dihitung dengan multiplisitas aljabarnya; akar-akar tersebut merupakan nilai-nilai eigen $latex A$.",
                1,
            ),
            (
                "Jejak $latex A$ adalah jumlah nilai-nilai eigen $latex A$.",
                "Jejak $latex A$ adalah jumlah nilai-nilai eigen $latex A$, dengan memperhitungkan multiplisitas aljabar.",
                1,
            ),
            (
                "Determinan $latex A$ adalah hasil kali nilai-nilai eigen $latex A$.",
                "Determinan $latex A$ adalah hasil kali nilai-nilai eigen $latex A$, dengan memperhitungkan multiplisitas aljabar.",
                1,
            ),
            (
                "Setelah suatu nilai eigen ditemukan, persamaan (A1.1) perlu diselesaikan untuk memperoleh vektor eigen yang bersesuaian. Vektor eigen semacam itu tidak hanya satu, melainkan membentuk suatu subruang linear. Masing-masing ruang eigen ini merupakan subruang invarian dari transformasi linear $latex \\mathcal T$ yang berkaitan dengan matriks $latex A$. Ruang vektor $latex \\mathcal S$, atau secara ekuivalen $latex \\mathbb{R}^n$, dengan demikian dapat dipandang sebagai jumlah ruang-ruang eigen dari $latex A$, dan dekomposisi ini memberikan gambaran geometris tentang cara $latex \\mathcal T$ bekerja pada $latex \\mathcal S$.",
                "Setelah suatu nilai eigen ditemukan, persamaan (A1.1) perlu diselesaikan untuk memperoleh vektor eigen yang bersesuaian. Himpunan semua solusinya, termasuk vektor nol, membentuk ruang eigen; anggota tak nol ruang ini adalah vektor-vektor eigen. Setiap ruang eigen merupakan subruang invarian dari transformasi linear $latex \\mathcal T$ yang berkaitan dengan matriks $latex A$. Jika matriks tersebut dapat didiagonalkan atas medan skalar yang digunakan, ruang vektor $latex \\mathcal S$, atau $latex \\mathbb{R}^n$ dalam kasus real, merupakan jumlah langsung ruang-ruang eigen $latex A$. Secara umum, dekomposisi memerlukan ruang eigen tergeneralisasi pada kompleksifikasi atau blok invarian real; keduanya memberikan gambaran geometris tentang cara $latex \\mathcal T$ bekerja pada $latex \\mathcal S$.",
                1,
            ),
            (r"\text{where}", r"\text{dengan}", 1),
            (r"\begin{array}{cccc}", r"\begin{array}{c}", 5),
        ],
    },
    "O005-LEGA-V101-CH12": {
        "source_lines": 112,
        "problem_count": 0,
        "fragments": [
            "01-gradient-line-integrals.html",
            "02-curl-stokes-green.html",
            "03-divergence.html",
        ],
        "replacements": [
            (
                "<li>$latex \\vec \\nabla f$ mengarah ke arah pertambahan $latex f$ yang paling cepat.</li>",
                "<li>Pada titik tempat $latex \\vec \\nabla f$ tak nol, arahnya merupakan arah pertambahan $latex f$ yang paling cepat.</li>",
                1,
            ),
            (
                "<li>Laju perubahan $latex f$ ke arah tersebut sama dengan $latex ||\\vec \\nabla f||$.</li>",
                "<li>Laju perubahan maksimum $latex f$ di antara semua arah yang direpresentasikan oleh vektor satuan sama dengan $latex ||\\vec \\nabla f||$.</li>",
                1,
            ),
            (
                "<li>$latex \\vec \\nabla f$ tegak lurus terhadap permukaan aras $latex f$ (yaitu, terhadap permukaan dengan persamaan $latex f=C$ = konstanta).</li>",
                "<li>Pada titik tempat $latex \\vec \\nabla f$ tak nol, gradien tersebut tegak lurus terhadap permukaan aras reguler fungsi $latex f$ (yaitu, terhadap permukaan dengan persamaan $latex f=C$ = konstanta).</li>",
                1,
            ),
            (
                "<li>Ekstremum $latex f$ dengan kendala $latex g(x,y,z)=C$ adalah titik-titik pada kurva dengan persamaan $latex g(x,y,z)=C$ tempat gradien $latex f$ sejajar dengan gradien $latex g.$ Konstanta kesebandingannya disebut <em>pengali Lagrange</em>.</li>",
                "<li>Ekstremum lokal $latex f$ dengan kendala $latex g(x,y,z)=C$ pada titik reguler permukaan $latex g(x,y,z)=C$ harus memenuhi bahwa gradien $latex f$ sejajar dengan gradien $latex g.$ Di sini, titik reguler berarti gradien kendala tidak nol; konstanta kesebandingannya disebut <em>pengali Lagrange</em>.</li>",
                1,
            ),
            (
                r"\left[\frac{1}{2} m \left(\frac{d \vec r}{d t}\right)^2 \right]_{t_0}^{t_1}",
                r"\left[\frac{1}{2} m \left\|\frac{d \vec r}{d t}\right\|^2 \right]_{t_0}^{t_1}",
                1,
            ),
            (
                "yaitu, usaha yang dilakukan oleh $latex \\vec F$ ketika suatu massa titik bergerak di sepanjang lintasan $latex \\mathcal C$ sama dengan selisih energi kinetik massa titik tersebut di antara kedua titik ujung $latex \\mathcal C$.",
                "di mana $latex v$ menyatakan kelajuan; dengan demikian, usaha yang dilakukan oleh $latex \\vec F$ ketika suatu massa titik bergerak di sepanjang lintasan $latex \\mathcal C$ sama dengan selisih energi kinetik massa titik tersebut di antara kedua titik ujung $latex \\mathcal C$.",
                1,
            ),
            (r"V(r)", r"V(\vec r)", 1),
            (
                "<li><span style=\"text-align: initial;font-size: 1em\">Sebaliknya, setiap medan vektor mulus yang didefinisikan pada suatu domain tanpa </span>lubang berkodimensi satu dan yang rotasinya nol di setiap titik merupakan medan gradien (inilah <em>uji rotasi</em>).</li>",
                "<li><span style=\"text-align: initial;font-size: 1em\">Sebaliknya, setiap medan vektor mulus yang didefinisikan pada domain terbuka terhubung sederhana dan </span>memiliki rotasi nol di setiap titik merupakan medan gradien (inilah <em>uji rotasi</em>).</li>",
                1,
            ),
            (
                "<li>Arah $latex \\text{curl}\\vec F$ di suatu titik $latex P$ adalah arah sumbu yang dikelilingi oleh rapat sirkulasi $latex \\vec F$ terbesar.</li>",
                "<li>Jika $latex \\text{curl}\\vec F$ tak nol di titik $latex P$, arahnya adalah arah sumbu dengan rapat sirkulasi $latex \\vec F$ terbesar di sekeliling sumbu tersebut.</li>",
                1,
            ),
            (
                "<li>Magnitudo $latex \\text{curl} \\vec F$ adalah rapat sirkulasi di sekitar arah tersebut.</li>",
                "<li>Nilai maksimum rapat sirkulasi di antara semua arah yang direpresentasikan oleh vektor satuan sama dengan magnitudo $latex \\text{curl} \\vec F$.</li>",
                1,
            ),
            (
                "<li>Jika permukaan $latex S$ adalah grafik suatu fungsi $latex f(x,y)$, maka, jika $latex R$ adalah domain $latex f(x,y)$, kita dapat menuliskan</li>",
                "<li>Jika permukaan $latex S$ adalah grafik suatu fungsi $latex f(x,y)$ dan diorientasikan ke atas, maka, jika $latex R$ adalah domain $latex f(x,y)$, kita dapat menuliskan</li>",
                1,
            ),
            (r"\vec F\left(x,y,z(x,y)\right)", r"\vec F\left(x,y,f(x,y)\right)", 1),
            (
                r"\text{div} \vec F = \displaystyle \lim_{W \rightarrow 0} \frac{\int_S \vec F \cdot d \vec A} {\hbox{volume of }W}.",
                r"\text{div} \vec F(P) = \displaystyle \lim_{\varepsilon \rightarrow 0} \frac{\iint_{\partial B_\varepsilon(P)} \vec F \cdot \vec n\, dS}{\operatorname{vol}(B_\varepsilon(P))}.",
                1,
            ),
            (
                "<li>Divergensi $latex \\vec F$ di suatu titik $latex P$ sama dengan limit, ketika permukaan $latex S$ yang mengelilingi $latex P$ menyusut ke nol, dari fluks $latex \\vec F$ melalui $latex S$ (yang diorientasikan ke luar) dibagi dengan volume daerah $latex W$ yang dibatasi oleh $latex S$. Dengan kata lain,</li>",
                "<li>Divergensi $latex \\vec F$ di titik $latex P$ sama dengan limit fluks per volume ketika permukaan $latex S$ yang mengelilingi $latex P$ menyusut ke titik tersebut: fluks $latex \\vec F$ melalui $latex S$ yang berorientasi ke luar dibagi dengan volume daerah $latex W$ yang dibatasi oleh $latex S$. Dalam rumus berikut, $latex B_\\varepsilon(P)$ adalah bola berpusat di titik itu dengan jari-jari epsilon; $latex \\partial B_\\varepsilon(P)$ adalah permukaannya; dan $latex \\vec n$ adalah vektor normal satuan ke luar. Dengan kata lain,</li>",
                1,
            ),
            (
                "<li>Sebaliknya, setiap medan vektor mulus $latex \\vec F$ yang domainnya tertutup dan tidak memiliki lubang, serta yang divergensinya nol di setiap titik, merupakan <em>medan rotasi</em>; yaitu, terdapat suatu medan vektor $latex \\vec G$ sedemikian sehingga $latex \\vec F = \\text{curl} \\vec G$ (inilah <em>uji divergensi</em>).</li>",
                "<li>Sebaliknya, pada setiap domain terbuka berbentuk bintang, setiap medan vektor mulus $latex \\vec F$ yang divergensinya nol di setiap titik merupakan <em>medan rotasi</em>; yaitu, terdapat suatu medan vektor $latex \\vec G$ sedemikian sehingga $latex \\vec F = \\text{curl} \\vec G$ (inilah <em>uji divergensi</em>).</li>",
                1,
            ),
        ],
    },
    "O005-LEGA-V101-CH13": {
        "source_lines": 581,
        "problem_count": 11,
        "answer_heading_count": 11,
        "fragments": [
            "01-foundations-first-second-order.html",
            "02-higher-order-systems.html",
            "03-phase-plane-problems-answers.html",
        ],
        "replacements": [
            (r"\frac{d^2 y}{d x},", r"\frac{d^2 y}{d x^2},", 1),
            (
                r"\rho(x,y)=f(x).",
                r"\rho(x)=\exp\left(\int f(x)\,dx\right).",
                1,
            ),
            (
                r"\rho(x,y)=f(y).",
                r"\rho(y)=\exp\left(-\int f(y)\,dy\right).",
                1,
            ),
            (
                r"x_1(t)=\alpha_1, x_2(t)=\alpha_2,\dots, x_n(t)=\alpha_n",
                r"x_1(t_0)=\alpha_1, x_2(t_0)=\alpha_2,\dots, x_n(t_0)=\alpha_n",
                1,
            ),
            (
                r"\Re e[\exp(\alpha+i \beta)",
                r"\operatorname{Re}[\exp((\alpha+i\beta)t)",
                1,
            ),
            (
                r"\Im m[\exp(\alpha+i \beta)",
                r"\operatorname{Im}[\exp((\alpha+i\beta)t)",
                1,
            ),
            (r"\Re e(X_p)", r"\operatorname{Re}(X_p)", 1),
            (r"\Im m(X_p)", r"\operatorname{Im}(X_p)", 1),
            (r"F(X)", r"F(Y)", 1),
            (r"\det(A)&gt;0", r"\det(A)\ge 0", 1),
            (
                r"\displaystyle \left\{ \begin{array}{l} x = C_1 \cos(t) e^{2 t} + C_2 \sin(t) e^{2 t} - 2 e^t \\ y = -C_1 \sin(t) e^{2 t} + C_2 \cos(t) e^{2 t} - e^t \end{array} \right. .",
                r"\displaystyle \left\{ \begin{array}{l} x = 2 \cos(t) e^{2 t} + 2 \sin(t) e^{2 t} - 2 e^t \\ y = -2 \sin(t) e^{2 t} + 2 \cos(t) e^{2 t} - e^t \end{array} \right. .",
                1,
            ),
            (r"\text{and}", r"\text{dan}", 2),
            (r"\text{ and }", r"\text{ dan }", 1),
            (r"\text{ constant}", r"\text{ konstan}", 1),
            (r"{\rm and}", r"\text{dan}", 1),
            (r"\text{and }", r"\text{dan }", 1),
            (r"\text{ constants}", r"\text{ konstan}", 1),
            (
                r'Secara bersama-sama, teorema-teorema ini menyiratkan bahwa untuk sistem dinamis yang terdiferensialkan secara kontinu dan berbentuk (<a href="#Eq_13.3">13.3</a>), setiap masalah nilai awal memiliki solusi tunggal. Dengan kata lain, jika $latex f$ dalam (<a href="#Eq_13.3">13.3</a>) terdiferensialkan secara kontinu, lintasan-lintasan dalam ruang fase sistem dinamis (<a href="#Eq_13.3">13.3</a>) tidak dapat saling berpotongan.',
                r'Secara bersama-sama, teorema-teorema ini menyiratkan bahwa untuk sistem dinamis yang terdiferensialkan secara kontinu dan berbentuk (<a href="#Eq_13.3">13.3</a>), setiap masalah nilai awal memiliki solusi tunggal. Karena $latex f$ dalam (<a href="#Eq_13.3">13.3</a>) dapat bergantung secara eksplisit pada variabel bebas, kesimpulan tanpa-perpotongan berlaku dalam ruang keadaan diperluas (x,Y); untuk sistem otonom berbentuk (<a href="#Eq_13.3">13.3</a>), kesimpulan itu berlaku langsung bagi lintasan dalam ruang fase Y.',
                1,
            ),
            (
                r'<li>Jika $latex \displaystyle \frac{1}{N} \left[\frac{\partial M}{\partial y}-\frac{\partial N}{\partial x}\right]$ hanya merupakan fungsi $latex x$, gunakan faktor integrasi $latex \rho(x)=\exp\left(\int f(x)\,dx\right).$</li>',
                r'<li>Jika $latex \displaystyle \frac{1}{N} \left[\frac{\partial M}{\partial y}-\frac{\partial N}{\partial x}\right]$ hanya bergantung pada $latex x$ dan hasilnya dinamai f(x), faktor integrasinya adalah $latex \rho(x)=\exp\left(\int f(x)\,dx\right).$</li>',
                1,
            ),
            (
                r'<li>Jika $latex \displaystyle \frac{1}{M} \left[\frac{\partial M}{\partial y}-\frac{\partial N} {\partial x}\right]$ hanya merupakan fungsi $latex y$, gunakan faktor integrasi $latex \rho(y)=\exp\left(-\int f(y)\,dy\right).$</li>',
                r'<li>Jika $latex \displaystyle \frac{1}{M} \left[\frac{\partial M}{\partial y}-\frac{\partial N} {\partial x}\right]$ hanya bergantung pada $latex y$ dan hasilnya dinamai f(y), faktor integrasinya adalah $latex \rho(y)=\exp\left(-\int f(y)\,dy\right).$</li>',
                1,
            ),
            (
                r'Solusi umum persamaan $latex \displaystyle \frac{d y}{d x}=\frac{y^2 + 2 x y}{x^2}$ adalah $latex \displaystyle y = \frac{C x^2}{1 - C x}$, dengan $latex C$ konstanta sembarang.',
                r'Keluarga solusi persamaan $latex \displaystyle \frac{d y}{d x}=\frac{y^2 + 2 x y}{x^2}$ adalah $latex \displaystyle y = \frac{C x^2}{1 - C x}$, dengan $latex C$ konstanta sembarang. Selain keluarga ini, $latex y=-x$ juga merupakan solusi dan tidak diperoleh untuk nilai parameter C yang berhingga.',
                1,
            ),
            (
                r'Solusi umum persamaan $latex x^2 y^\prime + 2 x y - y^3 = 0, x&gt;0$ adalah $latex \displaystyle y = \pm \sqrt{\frac{5 x}{2 + C x^5}}$.',
                r'Keluarga solusi tak nol persamaan $latex x^2 y^\prime + 2 x y - y^3 = 0, x&gt;0$ adalah $latex \displaystyle y = \pm \sqrt{\frac{5 x}{2 + C x^5}}$. Solusi nol $latex y=0$ juga memenuhi persamaan.',
                1,
            ),
            (
                r'Solusi umum persamaan $latex y^\prime = 1 + x^2 - 2 x y + y^2$ adalah $latex y = x + 1/(C - x)$.',
                r'Keluarga solusi persamaan $latex y^\prime = 1 + x^2 - 2 x y + y^2$ adalah $latex y = x + 1/(C - x)$. Solusi khusus $latex y=x$ juga memenuhi persamaan dan tidak termasuk dalam keluarga untuk nilai parameter C yang berhingga.',
                1,
            ),
            (
                r'dengan $latex C_1$ dan $latex C_2$ konstanta sembarang.',
                r'dengan $latex C_1$ dan $latex C_2$ konstanta sembarang. Selain keluarga tersebut, setiap fungsi konstan $latex y=C$ juga merupakan solusi.',
                1,
            ),
            (
                r'Jika nilai-nilai eigen dari $latex A$ memiliki bagian imajiner tak nol, maka $latex Y=Y_0$ merupakan spiral stabil. Potret fase (<a href="#Eq_13.5">13.5</a>) yang bersesuaian ditunjukkan pada Gambar 13.4.<a id="Fig_13.4"></a>',
                r'Jika nilai-nilai eigen dari $latex A$ merupakan pasangan kompleks konjugat dengan bagian imajiner tak nol dan bagian real negatif, maka $latex Y=Y_0$ merupakan spiral stabil. Jika bagian realnya positif, spiral tersebut tak stabil. Potret fase stabil (<a href="#Eq_13.5">13.5</a>) ditunjukkan pada Gambar 13.4.<a id="Fig_13.4"></a>',
                1,
            ),
            (
                r'[caption id="attachment_483" align="alignleft" width="100"]<img class="wp-image-483" src="assets/phase-center-source.png" alt="Potret fase sebuah pusat (linear). Deskripsi panjang tersedia." width="100" height="125" /> Gambar 13.7 [<a href="#Fig_13.7_Desc"><em>Deskripsi Gambar</em></a>][/caption]<span style="text-align: initial;font-size: 1em">Terakhir, jika semua nilai eigen dari $latex A$ memiliki bagian real nol, maka $latex Y=Y_0$ <em>stabil marginal</em>. Karena kita mengabaikan situasi nongenerik ketika $latex A = 0$, hal ini menyiratkan bahwa $latex A$ memiliki nilai-nilai eigen kompleks konjugat yang imajiner murni, dan titik tetap $latex Y=Y_0$ disebut </span><em style="text-align: initial;font-size: 1em">pusat linear</em><span style="text-align: initial;font-size: 1em">. Dalam hal ini, $latex \det(A) &gt; 0$ tetapi $latex \text{Tr} (A) = 0$. Gambar 13.7 menunjukkan potret fase sistem linear (<a href="#Eq_13.5">13.5</a>) ketika titik asal merupakan pusat (linear). Menentukan apakah titik tetap $latex Y = Y_0$ merupakan pusat nonlinear bagi sistem dinamis (<a href="#Eq_13.4">13.4</a>) memerlukan analisis lebih lanjut.</span>',
                r'[caption id="attachment_483" align="alignleft" width="100"]<img class="wp-image-483" src="assets/phase-center-source.png" alt="Potret fase sebuah pusat (linear). Deskripsi panjang tersedia." width="100" height="125" /> Gambar 13.7 [<a href="#Fig_13.7_Desc"><em>Deskripsi Gambar</em></a>][/caption]<span style="text-align: initial;font-size: 1em">Terakhir, jika nilai-nilai eigen $latex A$ membentuk pasangan konjugat imajiner murni tak nol, maka $latex Y=Y_0$ <em>stabil marginal</em>. Sekadar mensyaratkan semua bagian real nol tidaklah cukup: sekalipun kasus $latex A = 0$ diabaikan, matriks $latex A$ dapat nilpoten tak nol, dengan nilai-nilai eigen nol dan solusi linear yang tumbuh tak terbatas. Untuk pasangan imajiner murni tak nol, titik tetap $latex Y=Y_0$ disebut </span><em style="text-align: initial;font-size: 1em">pusat linear</em><span style="text-align: initial;font-size: 1em">. Dalam hal ini, $latex \det(A) &gt; 0$ tetapi $latex \text{Tr} (A) = 0$. Gambar 13.7 menunjukkan potret fase sistem linear (<a href="#Eq_13.5">13.5</a>) ketika titik asal merupakan pusat (linear). Menentukan apakah titik tetap $latex Y = Y_0$ merupakan pusat nonlinear bagi sistem dinamis (<a href="#Eq_13.4">13.4</a>) memerlukan analisis lebih lanjut.</span>',
                1,
            ),
            (
                r'<p style="text-align: center">$latex \displaystyle \frac{1}{3} \ln\left[(y-1)^2 |y+2|\right] = e^{-x} - x + \frac{1}{3} \ln(20) -1.$</p>',
                r'<p style="text-align: center">$latex \displaystyle \frac{1}{3} \ln\left[(y-1)^2 |y+2|\right] = e^{-x} - x + \frac{1}{3} \ln(20) -1.$ Karena ruas kanan bentuk eksplisit persamaan diferensial kontinu dan Lipschitz lokal terhadap y di sekitar (0,3), dengan penyebut 1+y tidak nol, masalah nilai awal tersebut memiliki solusi lokal tunggal.</p>',
                1,
            ),
            (
                r'Selesaikan $latex \displaystyle x y^{\prime \prime} + y^\prime = 0$.',
                r'Selesaikan $latex \displaystyle x y^{\prime \prime} + y^\prime = 0$ pada suatu interval yang tidak melintasi x=0.',
                1,
            ),
            (
                r'<p style="text-align: center">$latex \displaystyle y = K_1 \ln(|x|) + K_2.$</p>',
                r'<p style="text-align: center">$latex \displaystyle y = K_1 \ln(|x|) + K_2.$ Keluarga ini berlaku secara terpisah pada interval dengan x positif atau x negatif.</p>',
                1,
            ),
            (
                r'<p style="text-align: center">$latex \displaystyle \left\{ \begin{array}{l} x = 2 \cos(t) e^{2 t} + 2 \sin(t) e^{2 t} - 2 e^t \\ y = -2 \sin(t) e^{2 t} + 2 \cos(t) e^{2 t} - e^t \end{array} \right. .$</p>',
                r'<p style="text-align: center">$latex \displaystyle \left\{ \begin{array}{l} x = 2 \cos(t) e^{2 t} + 2 \sin(t) e^{2 t} - 2 e^t \\ y = -2 \sin(t) e^{2 t} + 2 \cos(t) e^{2 t} - e^t \end{array} \right. .$ Kondisi awal memberikan C1=C2=2.</p>',
                1,
            ),
        ],
    },
    "O005-LEGA-V101-CH14": {
        "source_lines": 240,
        "problem_count": 0,
        "fragments": [
            "01-intro-projects-01-06.html",
            "02-projects-07-12.html",
        ],
        "replacements": [],
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assemble(unit_id: str, *, write: bool) -> dict[str, object]:
    spec = SPECS[unit_id]
    unit_root = ROOT / "source" / "id-ID" / unit_id
    fragment_root = unit_root / "fragments"
    paths = [fragment_root / name for name in spec["fragments"]]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing translation fragments: " + ", ".join(missing))

    payloads: list[bytes] = []
    fragment_rows: list[dict[str, object]] = []
    for path in paths:
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            raise RuntimeError(f"UTF-8 BOM is not permitted: {path}")
        data.decode("utf-8")
        if not data.endswith(b"\n"):
            raise RuntimeError(f"Fragment lacks terminal LF: {path}")
        payloads.append(data)
        fragment_rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(data),
                "lines": len(data.splitlines()),
                "sha256": sha256(data),
            }
        )

    payload = b"".join(payloads)
    for old, new, expected_count in spec.get("replacements", []):
        old_bytes = old.encode("utf-8")
        if payload.count(old_bytes) != expected_count:
            raise RuntimeError(
                f"Expected {expected_count} declared correction surface(s): {old!r}"
            )
        payload = payload.replace(old_bytes, new.encode("utf-8"))
    text = payload.decode("utf-8")
    problem_heading = re.compile(
        r"<h3(?P<attrs>[^>]*)>(?P<body>(?:(?!</h3>).)*Soal (?P<number>\d+)(?:(?!</h3>).)*)</h3>"
    )
    matches = list(problem_heading.finditer(text))
    problem_count = int(spec.get("problem_count", 0))
    answer_heading_count = int(spec.get("answer_heading_count", 0))
    expected_numbers = list(range(1, problem_count + 1))
    expected_numbers.extend(range(1, answer_heading_count + 1))
    actual_numbers = [int(match.group("number")) for match in matches]
    if actual_numbers != expected_numbers:
        raise RuntimeError("Translated problem-heading sequence differs")

    match_index = 0

    def add_problem_id(match: re.Match[str]) -> str:
        nonlocal match_index
        number = int(match.group("number"))
        attrs = match.group("attrs")
        if re.search(r"\bid\s*=", attrs):
            raise RuntimeError("Translation fragment already has a problem-heading ID")
        prefix = "P" if match_index < problem_count else "A"
        match_index += 1
        return (
            f'<h3{attrs} id="{unit_id}-{prefix}{number:02d}">'
            f'{match.group("body")}</h3>'
        )

    payload = problem_heading.sub(add_problem_id, text).encode("utf-8")
    source = ROOT / "authority" / "units" / unit_id / "content.raw.en.html"
    if len(source.read_bytes().splitlines()) != spec["source_lines"]:
        raise RuntimeError("Frozen source line census differs")
    if len(payload.splitlines()) != spec["source_lines"]:
        raise RuntimeError("Assembled target line census differs")

    output = unit_root / "content.html"
    if write:
        output.write_bytes(payload)
    elif not output.is_file() or output.read_bytes() != payload:
        raise RuntimeError("Assembled content.html is absent or stale")
    return {
        "unit_id": unit_id,
        "bytes": len(payload),
        "lines": len(payload.splitlines()),
        "sha256": sha256(payload),
        "fragments": fragment_rows,
        "written": write,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", choices=sorted(SPECS), required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    import json

    print(json.dumps(assemble(args.unit, write=args.write), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
