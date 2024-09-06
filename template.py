import re
import random

pairs = {
    ## Greeting Template

    "(halo|hallo|hello)": [
        "Halo, bagaimana perasaanmu hari ini?",
        "Hai, bagaimana saya bisa membantumu hari ini?",
        "Halo, ada yang ingin kamu ceritakan hari ini?",
        "Hai, apa yang bisa saya bantu untukmu hari ini?"
    ],

    "hai": [
        "Hai! Apa kabar? Ada yang bisa saya bantu?",
        "Halo! Bagaimana hari kamu sejauh ini?",
        "Hai, apa yang ada di pikiranmu hari ini?",
        "Hai, apakah ada hal yang ingin kamu diskusikan?"
    ],

    "(saya|aku|gue) (ingin|mau) (cerita|curhat)": [
        "Ingin bercerita tentang sesuatu? Saya siap mendengarkan.",
        "Ada cerita atau perasaan yang ingin kamu bagikan? Saya di sini untuk mendengarkan.",
        "Jika kamu ingin bercerita atau berbagi, saya siap untuk mendengarkan.",
        "Silakan ceritakan apa yang kamu rasakan atau alami. Saya di sini untuk mendengar."
    ],

    "selamat pagi": [
        "Selamat pagi! Bagaimana hari kamu dimulai?",
        "Selamat pagi! Apa yang bisa saya bantu hari ini?",
        "Selamat pagi! Ada yang ingin kamu bicarakan?",
        "Selamat pagi! Bagaimana perasaanmu pagi ini?"
    ],

    "selamat siang": [
        "Selamat siang! Apa kabar siang ini?",
        "Selamat siang! Ada yang bisa saya bantu?",
        "Selamat siang! Bagaimana perasaanmu hari ini?",
        "Selamat siang! Apa yang ada di pikiranmu siang ini?"
    ],

    "selamat sore": [
        "Selamat sore! Bagaimana soremu sejauh ini?",
        "Selamat sore! Ada yang ingin kamu ceritakan?",
        "Selamat sore! Apa yang bisa saya bantu sore ini?",
        "Selamat sore! Bagaimana perasaanmu hari ini?"
    ],

    "selamat malam": [
        "Selamat malam! Bagaimana harimu hari ini?",
        "Selamat malam! Ada yang bisa saya bantu malam ini?",
        "Selamat malam! Apa yang ingin kamu diskusikan sebelum tidur?",
        "Selamat malam! Bagaimana perasaanmu malam ini?"
    ],

    "apa kabar": [
        "Apa kabar? Ada yang ingin kamu bicarakan?",
        "Bagaimana kabarmu hari ini? Apakah ada yang ingin kamu ceritakan?",
        "Apa kabar? Ada hal yang ingin kamu diskusikan?",
        "Bagaimana hari-harimu belakangan ini?"
    ],


    ## Main Template

    "(.*)(cemas)(.*)": [
        "Maaf mendengar bahwa kamu merasa cemas. Apa yang biasanya membantumu merasa lebih tenang?",
        "Kecemasan bisa sulit. Apakah kamu ingin membicarakan apa yang membuatmu cemas?",
        "Tidak apa-apa merasa cemas. Apakah ada sesuatu yang secara khusus memicu perasaan ini?",
        "Kamu tidak sendirian. Banyak orang mengalami kecemasan. Apakah kamu ingin menjelajahi beberapa teknik menenangkan bersama?"
    ],

    "(.*)(khawatir)(.*)": [
        "Saya paham bahwa kamu merasa khawatir. Apa yang biasanya membuatmu merasa lebih baik?",
        "Khawatir bisa membebani. Apakah ada hal tertentu yang membuatmu merasa khawatir?",
        "Tidak apa-apa merasa khawatir. Apakah kamu ingin berbicara tentang apa yang membuatmu khawatir?",
        "Kamu tidak sendirian dalam perasaan ini. Bagaimana saya bisa membantu mengatasi kekhawatiranmu?"
    ],

    "(.*)(takut)(.*)": [
        "Maaf mendengar bahwa kamu merasa takut. Apakah ada sesuatu yang bisa kita lakukan untuk mengatasi rasa takutmu?",
        "Rasa takut bisa sangat menakutkan. Apakah kamu ingin berbagi lebih banyak tentang apa yang membuatmu takut?",
        "Tidak apa-apa merasa takut. Apakah ada hal-hal khusus yang memicu rasa takut ini?",
        "Kamu tidak sendirian dalam perasaan ini. Apa yang biasanya membantu kamu merasa lebih aman?"
    ],

    "(.*)depresi(.*)": [
        "Saya sangat menyesal mendengar kamu merasa seperti ini. Depresi bisa sangat sulit. Apakah kamu ingin berbicara lebih lanjut tentang apa yang ada di pikiranmu?",
        "Ingat, kamu tidak harus menghadapi ini sendirian. Saya di sini untukmu. Apakah kamu ingin berbagi lebih banyak tentang perasaanmu?",
        "Tidak apa-apa untuk tidak merasa baik-baik saja. Apakah ada sesuatu yang khusus yang mengganggumu akhir-akhir ini?",
        "Depresi bisa membuat seseorang merasa terisolasi. Tahu bahwa meminta bantuan adalah langkah berani. Bagaimana saya bisa mendukungmu hari ini?"
    ],

    "(.*)sedih(.*)": [
        "Saya turut sedih mendengar kamu merasa sedih. Apakah kamu tahu apa yang menyebabkan perasaan ini?",
        "Sedih adalah perasaan yang alami. Apakah kamu ingin berbagi tentang apa yang membuatmu merasa sedih?",
        "Kadang-kadang, perasaan sedih datang tanpa alasan yang jelas. Apakah ada sesuatu yang terjadi baru-baru ini?",
        "Bagaimana saya bisa mendukungmu saat kamu merasa sedih?"
    ],

    "(.*)marah(.*)": [
        "Saya mengerti bahwa kamu merasa marah. Apakah kamu ingin berbicara tentang apa yang membuatmu marah?",
        "Marah adalah emosi yang normal, tetapi penting untuk memahami penyebabnya. Apa yang membuatmu merasa seperti ini?",
        "Kadang-kadang, marah bisa sangat membebani. Apakah ada hal spesifik yang memicu kemarahanmu?",
        "Apakah kamu biasanya melakukan sesuatu untuk meredakan kemarahanmu? Bisakah kita berbicara tentang hal itu?"
    ],

    "(.*)kesepian(.*)": [
        "Maaf kamu merasa kesepian. Ingat, kamu tidak sendirian di sini.",
        "Kesepian bisa sangat sulit. Apakah kamu ingin membicarakan apa yang telah terjadi?",
        "Tidak apa-apa merasa kesepian. Apakah kamu ingin berbagi lebih banyak tentang perasaanmu?",
        "Kamu tidak sendirian dalam perasaan ini. Saya di sini untuk mendengarkan apa pun yang ingin kamu bagikan."
    ],

    "(.*)tertekan(.*)": [
        "Saya minta maaf mendengar kamu merasa tertekan. Apa yang menurutmu menyebabkan perasaan ini?",
        "Tertekan bisa menjadi pengalaman yang sangat berat. Apakah kamu ingin membicarakan lebih lanjut?",
        "Perasaan tertekan bisa menguras energi. Adakah hal-hal yang membuatmu merasa lebih baik saat seperti ini?",
        "Kamu tidak sendirian dalam perasaan ini. Apakah ada hal khusus yang ingin kamu diskusikan?"
    ],

    "(.*)(kecewa|tidak puas|ketidakpuasan)(.*)": [
        "Kecewa adalah perasaan yang sulit. Apakah kamu ingin berbagi apa yang membuatmu merasa seperti itu?",
        "Saya mengerti perasaan kecewa bisa menyakitkan. Bagaimana biasanya kamu menghadapi perasaan ini?",
        "Tidak apa-apa merasa kecewa. Apakah ada hal yang bisa aku bantu untuk membuatmu merasa lebih baik?",
        "Kecewa bisa datang dari berbagai hal. Apakah kamu ingin menjelaskan lebih lanjut tentang apa yang terjadi?"
    ],

    "(.*)bingung(.*)": [
        "Rasa bingung bisa membuat kita merasa tidak pasti. Apakah ada sesuatu yang spesifik yang membuatmu merasa bingung?",
        "Bingung adalah reaksi yang wajar ketika menghadapi situasi yang kompleks. Bagaimana aku bisa membantu menjelaskan atau memahami perasaanmu?",
        "Kadang-kadang, berbicara tentang apa yang membuatmu bingung bisa membantu. Apa yang ada di pikiranmu saat ini?",
        "Apa yang bisa aku lakukan untuk membantu kamu merasa lebih jelas tentang situasi ini?"
    ],

    "(.*)harapan(.*)": [
        "Harapan adalah sesuatu yang penting. Apakah ada harapan khusus yang ingin kamu bicarakan?",
        "Memiliki harapan dapat memberikan dorongan. Apakah ada hal yang kamu harapkan untuk terjadi?",
        "Saya ingin mendengar lebih banyak tentang harapanmu. Apa yang membuatmu merasa berharap?",
        "Harapan bisa menjadi sumber kekuatan. Bagaimana aku bisa mendukung harapanmu saat ini?"
    ],

    "(.*)rasa(.*)kosong(.*)": [
        "Rasa kosong bisa sangat mengganggu. Apakah kamu tahu apa yang mungkin menyebabkan perasaan ini?",
        "Kadang-kadang, rasa kosong bisa berasal dari banyak hal. Apakah ada sesuatu yang membuatmu merasa tidak puas?",
        "Apakah kamu sudah mencoba cara tertentu untuk mengisi rasa kosong ini? Bagaimana perasaanmu setelahnya?",
        "Rasa kosong bisa membuat kita merasa terasing. Apa yang biasanya membantu kamu merasa lebih lengkap?"
    ],

    "(.*)memori(.*)": [
        "Memori seringkali bisa memengaruhi perasaan kita. Apakah ada kenangan tertentu yang memengaruhi perasaanmu?",
        "Kenangan bisa sangat kuat. Apakah ada memori yang datang kembali dan mempengaruhi bagaimana kamu merasa?",
        "Kadang-kadang, memori yang sulit dapat mempengaruhi kita. Apakah ada memori tertentu yang ingin kamu bicarakan?",
        "Bagaimana kamu biasanya menghadapi memori yang mengganggu atau menyakitkan?"
    ],

    "(.*)keluarga(.*)": [
        "Keluarga sering memainkan peran besar dalam hidup kita. Apakah ada sesuatu tentang keluargamu yang ingin kamu bicarakan?",
        "Hubungan keluarga bisa sangat mempengaruhi perasaan kita. Apakah kamu ingin berbagi tentang hubunganmu dengan keluargamu?",
        "Kadang-kadang, masalah keluarga bisa menjadi beban. Apakah ada hal khusus yang ingin kamu diskusikan tentang keluargamu?",
        "Keluarga bisa menjadi sumber dukungan atau konflik. Bagaimana hubungan keluargamu saat ini?"
    ],

    "(.*)pertemanan(.*)": [
        "Pertemanan bisa memberikan dukungan besar. Apakah ada sesuatu yang terjadi dengan teman-temanmu yang ingin kamu ceritakan?",
        "Hubungan pertemanan juga penting untuk kesejahteraan kita. Apakah kamu merasa ada masalah atau hal baik yang ingin kamu diskusikan?",
        "Kadang-kadang, pertemanan bisa menjadi tantangan. Apakah ada hal tertentu yang membuatmu merasa tidak nyaman dengan temanmu?",
        "Bagaimana hubungan dengan teman-temanmu? Apakah ada yang ingin kamu bagikan tentang pertemananmu?"
    ],


    "(.*)kehilangan(.*)": [
        "Kehilangan bisa sangat menyakitkan. Apakah kamu ingin berbicara lebih lanjut tentang apa yang kamu rasakan?",
        "Kehilangan seseorang atau sesuatu bisa sangat berat. Apakah ada cara yang bisa aku bantu untuk kamu menghadapi perasaan ini?",
        "Mengatasi kehilangan memerlukan waktu. Apakah ada sesuatu yang bisa aku lakukan untuk membantu kamu selama proses ini?",
        "Bagaimana kamu biasanya mengatasi rasa kehilangan? Apakah ada hal yang bisa membuat proses ini lebih mudah bagimu?"
    ],

    "(.*)keberhasilan(.*)": [
        "Keberhasilan adalah sesuatu yang patut dirayakan. Apakah ada pencapaian khusus yang ingin kamu bicarakan?",
        "Merayakan keberhasilan bisa memberikan rasa puas. Apa yang kamu rasakan setelah mencapai sesuatu yang penting bagimu?",
        "Keberhasilan seringkali datang dari kerja keras. Apakah ada hal yang ingin kamu bagikan tentang perjalanan menuju keberhasilan ini?",
        "Bagaimana kamu merayakan keberhasilanmu? Apakah ada hal yang bisa aku lakukan untuk merayakan denganmu?"
    ],

    "(.*)(kebahagiaan|bahagia)(.*)": [
        "Bagus mendengar bahwa kamu merasa bahagia! Apa yang membuatmu merasa seperti itu?",
        "Kebahagiaan adalah perasaan yang sangat positif. Apa yang terjadi dalam hidupmu saat ini?",
        "Senang mendengar kabar baik. Apakah ada sesuatu yang spesial yang ingin kamu bagikan?",
        "Kebahagiaan adalah hal yang luar biasa. Bagaimana kamu merasakannya hari ini?"
    ],

    "(.*)(kesulitan|tantangan)(.*)": [
        "Tantangan bisa sangat sulit. Apa yang saat ini menjadi tantangan bagimu?",
        "Kadang-kadang, menghadapi kesulitan bisa membuat kita merasa kewalahan. Apakah ada hal yang bisa kita diskusikan?",
        "Bagaimana kamu biasanya mengatasi tantangan? Apakah ada hal spesifik yang membuatmu merasa kesulitan?",
        "Kesulitan adalah bagian dari hidup. Apa yang biasanya membantu kamu menghadapinya?"
    ],

    "(.*)(stres|stress)(.*)": [
        "Sepertinya kamu merasa stres. Apakah kamu ingin membicarakan apa yang menyebabkan stres ini?",
        "Saya di sini untuk mendengarkan jika kamu ingin berbagi apa yang membuatmu stres.",
        "Stres bisa sangat berat. Apakah ada hal-hal tertentu yang terasa sangat menantang bagimu?",
        "Kamu tidak sendirian dalam perasaan ini. Apa yang biasanya membantumu mengelola stres?"
    ],

    "(.*)(hubungan|teman)(.*)": [
        "Hubungan dengan orang lain sangat penting. Apakah ada sesuatu yang ingin kamu bagikan tentang hubunganmu?",
        "Bagaimana hubunganmu dengan teman-teman saat ini? Apakah ada sesuatu yang ingin kamu diskusikan?",
        "Teman dan hubungan sosial memainkan peran besar dalam hidup kita. Apakah ada hal spesifik yang membuatmu merasa seperti ini?",
        "Apa yang bisa kita bahas tentang hubunganmu? Saya di sini untuk mendengarkan."
    ],

     "(.*)hibur(.*)": [
        "Saya di sini untukmu. Apakah kamu ingin mendengar sesuatu yang menenangkan?",
        "Tentu, saya akan melakukan yang terbaik untuk menghiburmu. Apa yang biasanya membuatmu merasa lebih baik?",
        "Tidak apa-apa untuk merasa sedih, tapi kamu juga berhak merasa nyaman. Apa yang bisa saya lakukan untuk menghiburmu?",
        "Kadang-kadang, berbicara tentang perasaan bisa membantu. Apakah ada sesuatu yang ingin kamu ceritakan lebih lanjut?",
        "Saya di sini, kamu tidak sendirian. Mungkin berbicara tentang hal yang membuatmu tersenyum bisa membantu. Apa yang biasanya membuatmu bahagia?"
    ],

    "(.*)hiburkan(.*)": [
        "Tentu, saya akan mencoba membantu. Apa yang kamu butuhkan saat ini?",
        "Saya di sini untuk mendukungmu. Apa yang biasanya membantu membuatmu merasa lebih baik?",
        "Mungkin mendengar kata-kata yang menenangkan bisa membantu. Ingat, kamu berharga dan tidak sendirian.",
        "Bernafas dalam-dalam dan mari kita bicarakan hal-hal yang membuatmu merasa lebih baik. Apa yang kamu pikir bisa menghiburmu?"
    ],

    "(.*)sedih(.*)hibur(.*)": [
        "Saya turut sedih mendengarnya. Mari kita coba membuatmu merasa lebih baik. Apa yang biasanya membantumu merasa lebih tenang?",
        "Tidak apa-apa merasa sedih. Saya di sini untuk mendengarkan dan menghiburmu. Apa yang bisa saya lakukan untuk membantu?",
        "Kadang-kadang, ketika kita merasa sedih, hanya perlu seseorang untuk mendengarkan. Saya ada di sini, kamu ingin bercerita lebih lanjut?",
        "Kesedihan bisa terasa berat. Bagaimana jika kita bicarakan hal-hal yang bisa membantumu merasa lebih baik?"
    ],

    "(.*)(sulit|susah|tidak bisa)(.*)(berfokus|fokus)(.*)": [
        "Sulit berfokus bisa menjadi tanda bahwa ada sesuatu yang mengganggu pikiranmu. Apakah kamu tahu apa yang menyebabkan ini?",
        "Apakah ada hal yang terjadi yang membuatmu kesulitan berkonsentrasi?",
        "Kadang-kadang, sulit fokus bisa terjadi karena stres. Apakah kamu ingin berbicara tentang apa yang membuatmu tertekan?",
        "Apakah kamu sudah mencoba teknik tertentu untuk membantu meningkatkan fokus?"
    ],

    "(.*)(saya|aku|gue)(.*)(tidak tahu|gatau|bingung|tidak tau)(.*)(rasakan|rasa)(.*)": [
        "Kadang-kadang kita merasa bingung dengan perasaan kita sendiri. Apakah ada sesuatu yang terjadi yang membuatmu merasa seperti ini?",
        "Tidak apa-apa untuk merasa bingung tentang perasaanmu. Bisakah kamu berbagi lebih lanjut?",
        "Mungkin membantu untuk mengekspresikan perasaanmu lebih banyak. Apa yang ada di pikiranmu saat ini?",
        "Saya di sini untuk membantu menjelajahi perasaan ini bersamamu. Apa yang bisa saya lakukan untuk membantumu memahami perasaanmu?"
    ],

    "(.*)(tanggung jawab|beban)(.*)": [
        "Tanggung jawab bisa menjadi beban. Apa yang saat ini menjadi tanggung jawab utama kamu?",
        "Kadang-kadang, beban tanggung jawab bisa terasa berat. Apakah ada hal yang ingin kamu diskusikan?",
        "Bagaimana cara kamu mengelola tanggung jawabmu? Apakah ada sesuatu yang membuatmu merasa tertekan?",
        "Tanggung jawab adalah bagian dari hidup. Apakah ada cara tertentu yang kamu gunakan untuk merasa lebih baik menghadapinya?"
    ],
 
    "(.*)(tidak bisa|sulit|ga bisa|)(.*)tidur(.*)": [
        "Maaf mendengar bahwa kamu kesulitan tidur. Bisakah kamu ceritakan lebih banyak tentang apa yang ada di pikiranmu?",
        "Kadang-kadang, pikiran bisa membuat kita terjaga di malam hari. Apakah kamu ingin membicarakannya?",
        "Tidak bisa tidur bisa sangat menjengkelkan. Apakah kamu sudah mencoba teknik untuk membantu rileks sebelum tidur?",
        "Tidur penting untuk kesehatan mentalmu. Mari kita eksplorasi beberapa cara yang mungkin bisa membantu kamu tidur lebih baik."
    ],

    "(.*)(serangan panik|panik)(.*)": [
        "Maaf mendengar bahwa kamu mengalami serangan panik. Tarik napas dalam-dalam, dan ketahuilah bahwa kamu aman.",
        "Serangan panik bisa sangat menakutkan. Apakah kamu ingin beberapa tips tentang teknik grounding?",
        "Tidak apa-apa untuk mengambil langkah perlahan. Apakah kamu ingin membicarakan apa yang sedang terjadi?",
        "Saya di sini untukmu. Apakah ada sesuatu yang biasanya membantu kamu tenang?"
    ],

    "(.*)(self-harm|menyakiti diri sendiri)(.*)": [
        "Saya sangat prihatin mendengar bahwa kamu merasa ingin menyakiti diri sendiri. Apakah ada sesuatu yang bisa kita bicarakan yang mungkin membantu kamu merasa lebih baik?",
        "Self-harm adalah masalah serius, dan kamu tidak sendirian. Apakah ada hal tertentu yang memicu perasaan ini?",
        "Penting untuk berbicara tentang perasaan ini dengan seseorang yang bisa memberikan dukungan lebih lanjut. Apakah kamu ingin berbicara lebih banyak tentang apa yang kamu rasakan?",
        "Saya di sini untuk mendengarkan. Jika kamu merasa tertekan, mungkin ada cara lain yang bisa membantu. Apakah ada hal yang bisa kita lakukan bersama untuk mengatasi perasaan ini?"
    ],

    "(.*)(bunuh diri|mengakhiri hidup)(.*)": [
        "Saya sangat prihatin mendengar bahwa kamu merasa seperti ini. Ini adalah perasaan yang sangat berat. Apakah ada seseorang yang bisa kamu hubungi untuk mendapatkan bantuan lebih lanjut?",
        "Bunuh diri adalah hal yang sangat serius, dan penting untuk berbicara dengan seorang profesional tentang perasaan ini. Apakah ada cara saya bisa membantumu menghubungi seseorang yang bisa memberikan dukungan?",
        "Kamu tidak sendirian dalam perasaan ini. Ada bantuan tersedia, dan penting untuk mencari dukungan dari orang-orang terdekat atau profesional.",
        "Jika kamu merasa tertekan atau berpikir tentang bunuh diri, bicarakanlah dengan seseorang yang bisa mendukungmu, seperti teman, keluarga, atau seorang profesional. Saya di sini untuk mendengarkan jika kamu ingin berbagi lebih banyak."
    ],

    "(.*)(ingin mati|rasa ingin bunuh diri)(.*)": [
        "Saya sangat menyesal mendengar bahwa kamu merasa seperti ini. Ini adalah perasaan yang sangat berat. Apakah kamu sudah berbicara dengan seseorang tentang perasaan ini?",
        "Perasaan ingin mati adalah sinyal bahwa kamu membutuhkan dukungan tambahan. Apakah ada cara yang bisa saya bantu untuk menghubungkanmu dengan sumber dukungan yang tepat?",
        "Jika kamu merasa tidak dapat mengatasi perasaan ini sendirian, penting untuk mencari bantuan dari profesional. Apakah kamu ingin berbicara lebih lanjut tentang perasaan ini?",
        "Kamu berharga, dan ada orang yang peduli denganmu. Mencari bantuan adalah langkah yang penting. Apakah kamu ingin mendiskusikan perasaan ini lebih lanjut atau mencari cara untuk mendapatkan dukungan?"
    ],

    "(.*)(kesulitan|kesusahan)(.*)mental health(.*)": [
        "Kesulitan dalam kesehatan mental bisa sangat berat. Apakah ada sesuatu yang secara khusus mempengaruhi kesehatan mentalmu saat ini?",
        "Kadang-kadang, berbicara tentang kesulitan yang kamu hadapi bisa membantu. Apa yang bisa kita lakukan untuk membantumu merasa lebih baik?",
        "Menangani masalah kesehatan mental bisa sangat menantang. Apakah kamu sudah mencari dukungan dari seorang profesional atau seseorang yang kamu percayai?",
        "Jika kamu merasa kesulitan dengan kesehatan mentalmu, penting untuk mencari dukungan. Mari kita bicarakan apa yang mungkin bisa membantu atau siapa yang bisa memberikan dukungan."
    ],

    "(.*)perlu(.*)bantuan profesional(.*)": [
        "Mencari bantuan profesional bisa menjadi langkah yang sangat positif. Apakah kamu sudah mempertimbangkan untuk berbicara dengan seorang terapis atau konselor?",
        "Bantuan profesional bisa memberikan dukungan yang kamu butuhkan. Apakah ada cara saya bisa membantumu menemukan sumber dukungan atau informasi lebih lanjut?",
        "Kadang-kadang, berbicara dengan seorang profesional bisa membantu mengatasi perasaan sulit. Apakah kamu ingin informasi tentang cara menghubungi bantuan profesional?",
        "Saya bisa membantu dengan informasi tentang mencari bantuan profesional. Apakah ada hal spesifik yang kamu butuhkan bantuan dalam mencarinya?"
    ],

    "(.*)komunikasi(.*)": [
        "Komunikasi yang baik sangat penting. Apakah ada masalah komunikasi yang sedang kamu hadapi?",
        "Bagaimana cara kamu biasanya berkomunikasi dengan orang lain? Apakah ada hal yang ingin kamu ubah?",
        "Komunikasi bisa menjadi tantangan dalam hubungan. Apakah ada sesuatu yang mengganggu cara kamu berkomunikasi?",
        "Apakah kamu merasa bahwa komunikasimu dengan orang lain berjalan dengan baik saat ini?"
    ],
    
    "(.*)bantuan(.*)": [
        "Saya di sini untuk membantumu. Apa yang ingin kamu bicarakan hari ini?",
        "Tidak apa-apa untuk meminta bantuan. Bagaimana saya bisa mendukungmu?",
        "Kadang-kadang, kita semua butuh sedikit bantuan. Apa yang kamu rasakan sekarang?",
        "Saya ingin membantu sebaik mungkin. Bisakah kamu berbagi sedikit lebih banyak tentang apa yang ada di pikiranmu?"
    ],

    "(.*)dukungan(.*)": [
        "Dukungan sangat penting saat menghadapi masa sulit. Apakah ada jenis dukungan khusus yang kamu butuhkan saat ini?",
        "Kadang-kadang, kita semua membutuhkan dukungan ekstra. Bagaimana saya bisa memberikan dukungan yang kamu butuhkan?",
        "Apakah ada seseorang dalam hidupmu yang biasanya memberikan dukungan? Bagaimana jika kamu merasa dukungan itu kurang?",
        "Mencari dukungan adalah langkah yang positif. Apakah kamu ingin berbicara lebih lanjut tentang bagaimana kamu bisa mendapatkan dukungan yang kamu butuhkan?"
    ],

    ## General Template

    "(saya|aku|gue)(.*)merasa(.*)": [
        "Mengapa kamu merasa {2}?",
        "Saya turut sedih mendengar bahwa kamu merasa {2}, bisakah kamu ceritakan lebih banyak tentang hal itu?",
        "Sepertinya kamu sedang merasa {2}. Sudah berapa lama kamu merasa seperti ini?",
        "Apa yang menurutmu mungkin menyebabkanmu merasa {2}?",
        "Terima kasih telah berbagi tentang perasaanmu. Saya di sini untuk mendengarkan."
    ],

    "(saya|aku|gue) (.*)": [
        "Mengapa kamu merasa {1}?",
        "Sudah berapa lama kamu merasa {1}?",
        "Saya di sini untukmu. Bisakah kamu ceritakan lebih lanjut tentang perasaan {1}?",
        "Tidak apa-apa merasa {1}. Kadang-kadang, emosi bisa sangat kuat, dan itu wajar."
    ],

    ## Support or Bridging Template

    "(.*)saat ini(.*)": [
        "Bagaimana perasaanmu saat ini dibandingkan dengan sebelumnya?",
        "Apa yang sedang terjadi saat ini yang mungkin mempengaruhi perasaanmu?",
        "Saat ini, apakah ada hal yang khusus mempengaruhi bagaimana kamu merasa?",
        "Apa yang sedang kamu rasakan saat ini? Apakah ada hal tertentu yang mempengaruhi perasaanmu?"
    ],

    "(.*)sejak (.*)": [
        "Sejak {1}? Itu waktu yang cukup lama. Apa yang kamu rasakan selama ini?",
        "Sudah sejak {1}, ya? Bagaimana kamu menghadapi perasaan ini sejauh ini?",
        "Saya paham bahwa kamu telah merasakan ini sejak {1}. Apakah kamu ingin berbicara lebih lanjut tentang hal itu?",
        "Sejak {1}, apakah kamu melihat ada perubahan dalam intensitas perasaanmu?"
    ],

    "(.*)mempengaruhi(.*)": [
        "Apa yang mempengaruhi perasaanmu saat ini? Apakah ada hal khusus yang membuat perasaanmu berubah?",
        "Kadang-kadang, faktor eksternal mempengaruhi bagaimana kita merasa. Apakah ada hal yang mempengaruhi perasaanmu?",
        "Apa yang menurutmu mempengaruhi perasaanmu? Apakah ada faktor tertentu yang berkontribusi?",
        "Memahami apa yang mempengaruhi perasaanmu bisa membantu. Apakah ada hal tertentu yang mungkin mempengaruhi perasaanmu?"
    ],

    "(.*)(hari|minggu|bulan) ini(.*)": [
        "Selama {0} {1} ini, bagaimana perasaanmu? Apakah ada hal yang mempengaruhi perasaanmu?",
        "Hari ini, minggu ini, atau bulan ini, apakah ada sesuatu yang spesifik mempengaruhi bagaimana kamu merasa?",
        "Apa yang terjadi dalam {0} {1} ini yang mungkin mempengaruhi perasaanmu?",
        "Selama {0} {1}ini, bagaimana cara kamu mengatasi perasaanmu? Apakah ada hal baru yang terjadi?"
    ],

    "(.*)baru (saja|terakhir)(.*)": [
        "Kamu baru saja mengalami ini? Bisa jadi perasaan ini masih sangat segar. Apa yang terjadi baru-baru ini?",
        "Baru saja mengalami sesuatu bisa terasa sangat intens. Apakah ada sesuatu yang spesifik yang mempengaruhi perasaanmu saat ini?",
        "Karena ini baru saja terjadi, mungkin kamu merasa lebih terpengaruh. Apa yang kamu butuhkan saat ini?",
        "Apa yang terjadi baru-baru ini yang mungkin mempengaruhi bagaimana kamu merasa sekarang?"
    ],

    "(.*)dalam (waktu|periode) (ini|terakhir)(.*)": [
        "Dalam periode waktu ini, apa yang mungkin mempengaruhi perasaanmu?",
        "Apakah ada sesuatu dalam waktu ini yang menurutmu berkontribusi pada bagaimana kamu merasa?",
        "Bagaimana kamu menghadapi perasaan ini selama periode terakhir?",
        "Apa yang telah berubah dalam waktu ini yang mungkin mempengaruhi perasaanmu?"
    ],

    "(.*)masa lalu(.*)": [
        "Mungkin ada hal dari masa lalu yang mempengaruhi perasaanmu saat ini. Apakah kamu ingin berbicara tentang itu?",
        "Masa lalu sering mempengaruhi perasaan kita saat ini. Apakah ada pengalaman masa lalu yang mungkin relevan?",
        "Mengatasi perasaan bisa sulit jika ada hal dari masa lalu yang masih mempengaruhi. Apa yang bisa kita bicarakan dari masa lalu?",
        "Apakah ada sesuatu dari masa lalu yang menurutmu berpengaruh pada perasaanmu saat ini?"
    ],

    "(.*)(selama|selama ini)(.*)": [
        "Selama {1}, apakah ada hal-hal yang membantumu mengatasi perasaan ini?",
        "Selama waktu ini, apakah kamu menemukan cara baru untuk menghadapi perasaanmu?",
        "Apa yang sudah terjadi selama {1} yang mungkin mempengaruhi perasaanmu?",
        "Bagaimana kamu mengatasi perasaanmu selama {1} waktu ini?"
    ],

    "(.*)terakhir kali (.*)": [
        "Terakhir kali kamu merasa seperti ini, apa yang membantu atau tidak membantu?",
        "Apakah ada sesuatu yang berbeda atau mirip dengan bagaimana kamu merasa terakhir kali?",
        "Bagaimana kamu mengatasi perasaan ini terakhir kali? Apakah ada hal yang bisa kita coba lagi?",
        "Apakah ada strategi yang berhasil sebelumnya yang bisa kita coba lagi sekarang?"
    ],

    "(.*)(sebelumnya|dulu)(.*)": [
        "Bagaimana kamu merasa sebelumnya tentang hal ini? Apakah ada perubahan dalam perasaanmu?",
        "Dulu, bagaimana kamu mengatasi perasaan ini? Apakah ada sesuatu yang bisa kita gunakan dari pengalaman itu?",
        "Apa yang berbeda sekarang dibandingkan dengan bagaimana kamu merasa sebelumnya?",
        "Dulu, apakah ada cara yang berhasil untuk mengatasi perasaan ini? Mungkin kita bisa mencoba pendekatan yang sama."
    ],

    "(.*)belakangan ini(.*)": [
        "Belakangan ini, apa yang paling mempengaruhi perasaanmu?",
        "Apakah ada sesuatu yang terjadi belakangan ini yang mungkin berhubungan dengan bagaimana kamu merasa sekarang?",
        "Bagaimana belakangan ini berbeda dari waktu-waktu sebelumnya dalam hal perasaanmu?",
        "Apa yang membuat belakangan ini terasa lebih menantang atau berbeda?"
    ],

    "(.*)saat ini(.*)": [
        "Saat ini, apa yang paling membuatmu merasa seperti ini?",
        "Bagaimana kamu merasa saat ini dibandingkan dengan waktu-waktu sebelumnya?",
        "Saat ini, adakah sesuatu yang khusus yang mempengaruhi perasaanmu?",
        "Apa yang bisa kita lakukan saat ini untuk membantu kamu merasa lebih baik?"
    ],

    "(.*)terakhir kali(.*)": [
        "Terakhir kali kamu menghadapi perasaan seperti ini, apa yang kamu lakukan?",
        "Bagaimana pengalaman terakhir kali membantu atau tidak membantu?",
        "Terakhir kali, apakah ada strategi yang berhasil untukmu? Mungkin bisa kita coba lagi.",
        "Apa yang bisa kita pelajari dari pengalaman terakhir kali untuk mengatasi perasaan ini?"
    ],

    "(.*)sejak terakhir kali(.*)": [
        "Sejak terakhir kali, apakah ada perubahan dalam perasaanmu?",
        "Bagaimana perasaanmu berkembang sejak terakhir kali kita berbicara?",
        "Apakah ada perbedaan signifikan antara bagaimana kamu merasa sekarang dan terakhir kali?",
        "Apa yang telah terjadi sejak terakhir kali yang mungkin mempengaruhi perasaanmu?"
    ],

    "(.*)waktu itu(.*)": [
        "Waktu itu, apa yang membantu kamu mengatasi perasaanmu?",
        "Apa yang berbeda dari waktu itu hingga sekarang? Bagaimana hal ini mempengaruhi perasaanmu?",
        "Waktu itu, apa yang menurutmu efektif dalam mengatasi perasaanmu?",
        "Bagaimana perasaanmu berubah sejak waktu itu? Apakah ada hal baru yang mempengaruhi perasaanmu?"
    ],

    "(.*)belum lama ini(.*)": [
        "Belum lama ini, apakah ada kejadian yang mungkin mempengaruhi perasaanmu?",
        "Apa yang terjadi belum lama ini yang mungkin membuat perasaanmu lebih intens?",
        "Belum lama ini, adakah sesuatu yang membuat perasaanmu lebih sulit atau berbeda?",
        "Bagaimana perasaanmu berkembang sejak kejadian belum lama ini?"
    ],

    "(.*)setelah (.*)": [
        "Setelah {1}, bagaimana perasaanmu?",
        "Apa yang berubah setelah {1} yang mungkin mempengaruhi perasaanmu?",
        "Sejak {1}, adakah hal yang menjadi lebih baik atau lebih buruk?",
        "Setelah {1}, apa yang kamu lakukan untuk mengatasi perasaan ini?"
    ],

    "(.*)tidak(.*)": [
        "Tidak apa-apa untuk mengatakan tidak. Bisakah kamu ceritakan lebih banyak mengapa kamu merasa seperti ini?",
        "Tidak masalah. Apakah ada hal lain yang ingin kamu diskusikan?",
        "Saya mengerti. Apakah kamu ingin berbicara tentang hal lain?",
        "Tidak apa-apa. Bagaimana saya bisa membantu lebih lanjut?"
    ],

    "sudah (.*)": [
        "Terima kasih telah berbagi. Bagaimana perasaanmu selama waktu tersebut?",
        "Sepertinya ini sudah berlangsung cukup lama. Apakah ada sesuatu yang membantumu merasa lebih baik selama ini?",
        "Saya mendengar bahwa kamu telah merasakan ini sejak {0}. Apakah perasaan itu berubah seiring waktu, atau tetap sama?",
        "Apakah kamu merasa ada pola atau peristiwa tertentu yang memengaruhi bagaimana perasaanmu selama {0}?"
    ],

    ## Default Template

    "": [
        "Tolong ceritakan lebih banyak.",
        "Bisakah kamu memperjelas itu?",
        "Saya mengerti.",
        "Apakah kamu masih di sana?"
    ]
}

def match_response(input):
    for pattern, responses in pairs.items():
        match = re.match(pattern, input.lower())
        print(match)
        if match:
            response = random.choice(responses)
            return response.format(*match.groups())
    return "Maaf saya tidak tahu apa yang kamu maksud. Tolong ceritakan lebih banyak."