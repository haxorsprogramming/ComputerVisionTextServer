<h1 align="center">Aplikasi Text Recognition (Server)</h1>

<p align="justify">Ini adalah aplikasi client sederhana dari implementasi project <a href="https://github.com/haxorsprogramming/ComputerVisionTextServer">Computer Vision Text Recognition Project</a>, dimana server tersebut dapat digunakan untuk mengola proses recognition pada file gambar, yang dapat membaca/analisa tulisan/font yang ada pada gambar. Dapat digunakan untuk berbagai keperluan, identifikasi KTP, SIM, Kartu Pengenal, Hasil Ujian, Dll. Aplikasi ini menggunakan object storage sebagai media penyimpanan, untuk itu harap persiapkan object storage (S3 compatible) untuk dapat menjalankan sistem ini.
</p>

<br/>
<strong>Fitur</strong>
<li>Capture foto melalui webcam</li>
<li>Upload foto</li>
<li>Hasil analisa yang ditampilkan berupa array</li>
<br/>

<strong>Instalasi</strong>

- Pastikan sudah melakukan instalasi django
- Lakukan instalasi dependency yang diperlukan 
<code>pip install --upgrade azure-cognitiveservices-vision-computervision</code>
<code>pip install pillow</code>
<code>pip install boto3</code>
<code>pip install django-base-url</code>
<code>pip install django-cors-header</code>

- Setting database di file settings.py
- Jalankan server <code>python manage.py runserver</code>
- Server akan berjalan di port 8000 secara default, jika ingin mengganti port dapat menjalankan perintah <code>python manage.py runserver 0.0.0.0:'port'</code>, endpoint ini nanti dibutuhkan untuk aplikasi <a href="https://github.com/haxorsprogramming/TextRecognitionClient">client</a> agar terhubung
- Silahkan hubungkan dengan aplikasi <a href="https://github.com/haxorsprogramming/TextRecognitionClient">client</a> agar dapat menggunakan server ini


Jika terdapat kendala dapat membuat issue di repo ini atau email ke alditha.forum@gmail.com, kami bersedia melakukan setup dengan biaya seikhlasnya ... 