import re
import random

pairs = {
    "halo" : ["Halo, bagaimana perasaanmu hari ini?", "Hai, bagaimana saya bisa membantumu hari ini?"],

    "saya merasa (.*)": [
        "Mengapa kamu merasa {0}?",
        "Saya turut sedih mendengar bahwa kamu merasa {0}, bisakah kamu ceritakan lebih banyak tentang hal itu?",
        "Sepertinya kamu sedang merasa {0}. Sudah berapa lama kamu merasa seperti ini?",
        "Apa yang menurutmu mungkin menyebabkanmu merasa {0}?",
        "Terima kasih telah berbagi tentang perasaanmu. Saya di sini untuk mendengarkan."
    ],

    "saya (.*)": [
        "Mengapa kamu merasa {0}?",
        "Sudah berapa lama kamu merasa {0}?",
        "Saya di sini untukmu. Bisakah kamu ceritakan lebih lanjut tentang perasaan {0}?",
        "Tidak apa-apa merasa {0}. Kadang-kadang, emosi bisa sangat kuat, dan itu wajar."
    ],

    "saya merasa cemas(.*)": [
        "Maaf mendengar bahwa kamu merasa cemas. Apa yang biasanya membantumu merasa lebih tenang?",
        "Kecemasan bisa sulit. Apakah kamu ingin membicarakan apa yang membuatmu cemas?",
        "Tidak apa-apa merasa cemas. Apakah ada sesuatu yang secara khusus memicu perasaan ini?",
        "Kamu tidak sendirian. Banyak orang mengalami kecemasan. Apakah kamu ingin menjelajahi beberapa teknik menenangkan bersama?"
    ],

    "saya merasa depresi(.*)": [
        "Saya sangat menyesal mendengar kamu merasa seperti ini. Depresi bisa sangat sulit. Apakah kamu ingin berbicara lebih lanjut tentang apa yang ada di pikiranmu?",
        "Ingat, kamu tidak harus menghadapi ini sendirian. Saya di sini untukmu. Apakah kamu ingin berbagi lebih banyak tentang perasaanmu?",
        "Tidak apa-apa untuk tidak merasa baik-baik saja. Apakah ada sesuatu yang khusus yang mengganggumu akhir-akhir ini?",
        "Depresi bisa membuat seseorang merasa terisolasi. Tahu bahwa meminta bantuan adalah langkah berani. Bagaimana saya bisa mendukungmu hari ini?"
    ],
    "saya merasa sedih(.*)": [
    "Saya turut sedih mendengar kamu merasa sedih. Apakah kamu tahu apa yang menyebabkan perasaan ini?",
    "Sedih adalah perasaan yang alami. Apakah kamu ingin berbagi tentang apa yang membuatmu merasa sedih?",
    "Kadang-kadang, perasaan sedih datang tanpa alasan yang jelas. Apakah ada sesuatu yang terjadi baru-baru ini?",
    "Bagaimana saya bisa mendukungmu saat kamu merasa sedih?"
    ],

    "saya sulit berfokus(.*)": [
    "Sulit berfokus bisa menjadi tanda bahwa ada sesuatu yang mengganggu pikiranmu. Apakah kamu tahu apa yang menyebabkan ini?",
    "Apakah ada hal yang terjadi yang membuatmu kesulitan berkonsentrasi?",
    "Kadang-kadang, sulit fokus bisa terjadi karena stres. Apakah kamu ingin berbicara tentang apa yang membuatmu tertekan?",
    "Apakah kamu sudah mencoba teknik tertentu untuk membantu meningkatkan fokus?"
    ],

    
    "saya tidak tahu apa yang saya rasakan(.*)": [
    "Kadang-kadang kita merasa bingung dengan perasaan kita sendiri. Apakah ada sesuatu yang terjadi yang membuatmu merasa seperti ini?",
    "Tidak apa-apa untuk merasa bingung tentang perasaanmu. Bisakah kamu berbagi lebih lanjut?",
    "Mungkin membantu untuk mengekspresikan perasaanmu lebih banyak. Apa yang ada di pikiranmu saat ini?",
    "Saya di sini untuk membantu menjelajahi perasaan ini bersamamu. Apa yang bisa saya lakukan untuk membantumu memahami perasaanmu?"
    ],


    "saya merasa marah(.*)": [
    "Saya mengerti bahwa kamu merasa marah. Apakah kamu ingin berbicara tentang apa yang membuatmu marah?",
    "Marah adalah emosi yang normal, tetapi penting untuk memahami penyebabnya. Apa yang membuatmu merasa seperti ini?",
    "Kadang-kadang, marah bisa sangat membebani. Apakah ada hal spesifik yang memicu kemarahanmu?",
    "Apakah kamu biasanya melakukan sesuatu untuk meredakan kemarahanmu? Bisakah kita berbicara tentang hal itu?"
    ],

    "saya tidak bisa tidur(.*)": [
        "Maaf mendengar bahwa kamu kesulitan tidur. Bisakah kamu ceritakan lebih banyak tentang apa yang ada di pikiranmu?",
        "Kadang-kadang, pikiran bisa membuat kita terjaga di malam hari. Apakah kamu ingin membicarakannya?",
        "Tidak bisa tidur bisa sangat menjengkelkan. Apakah kamu sudah mencoba teknik untuk membantu rileks sebelum tidur?",
        "Tidur penting untuk kesehatan mentalmu. Mari kita eksplorasi beberapa cara yang mungkin bisa membantu kamu tidur lebih baik."
    ],

    "saya merasa stres(.*)": [
        "Sepertinya kamu merasa stres. Apakah kamu ingin membicarakan apa yang menyebabkan stres ini?",
        "Saya di sini untuk mendengarkan jika kamu ingin berbagi apa yang membuatmu stres.",
        "Stres bisa sangat berat. Apakah ada hal-hal tertentu yang terasa sangat menantang bagimu?",
        "Kamu tidak sendirian dalam perasaan ini. Apa yang biasanya membantumu mengelola stres?"
    ],

    "(.*)serangan panik(.*)": [
        "Maaf mendengar bahwa kamu mengalami serangan panik. Tarik napas dalam-dalam, dan ketahuilah bahwa kamu aman.",
        "Serangan panik bisa sangat menakutkan. Apakah kamu ingin beberapa tips tentang teknik grounding?",
        "Tidak apa-apa untuk mengambil langkah perlahan. Apakah kamu ingin membicarakan apa yang sedang terjadi?",
        "Saya di sini untukmu. Apakah ada sesuatu yang biasanya membantu kamu tenang?"
    ],

    "(.*)bantuan(.*)": [
        "Saya di sini untuk membantumu. Apa yang ingin kamu bicarakan hari ini?",
        "Tidak apa-apa untuk meminta bantuan. Bagaimana saya bisa mendukungmu?",
        "Kadang-kadang, kita semua butuh sedikit bantuan. Apa yang kamu rasakan sekarang?",
        "Saya ingin membantu sebaik mungkin. Bisakah kamu berbagi sedikit lebih banyak tentang apa yang ada di pikiranmu?"
    ],

    "(.*)kesepian(.*)": [
        "Maaf kamu merasa kesepian. Ingat, kamu tidak sendirian di sini.",
        "Kesepian bisa sangat sulit. Apakah kamu ingin membicarakan apa yang telah terjadi?",
        "Tidak apa-apa merasa kesepian. Apakah kamu ingin berbagi lebih banyak tentang perasaanmu?",
        "Kamu tidak sendirian dalam perasaan ini. Saya di sini untuk mendengarkan apa pun yang ingin kamu bagikan."
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

    "sejak (.*)": [
        "Sejak {0}? Itu waktu yang cukup lama. Apa yang kamu rasakan selama ini?",
        "Sudah sejak {0}, ya? Bagaimana kamu menghadapi perasaan ini sejauh ini?",
        "Saya paham bahwa kamu telah merasakan ini sejak {0}. Apakah kamu ingin berbicara lebih lanjut tentang hal itu?",
        "Sejak {0}, apakah kamu melihat ada perubahan dalam intensitas perasaanmu?"
    ],

    "beberapa (hari|minggu|bulan|tahun)": [
        "Beberapa {0} bisa menjadi waktu yang lama untuk menghadapi perasaan seperti ini. Apa yang menurutmu membuat hal ini terus berlanjut?",
        "Selama beberapa {0}, apakah kamu menemukan cara untuk mengelola perasaan ini?",
        "Beberapa {0} terdengar cukup lama. Apakah ada perubahan atau pola yang kamu amati selama waktu tersebut?",
        "Apakah ada sesuatu yang terjadi selama beberapa {0} terakhir yang menurutmu berpengaruh pada perasaan ini?"
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
        if match:
            response = random.choice(responses)
            return response.format(*match.groups())
    return "Maaf saya tidak tahu apa yang kamu maksud. Tolong ceritakan lebih banyak."