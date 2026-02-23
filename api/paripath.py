from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import datetime

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # 1. Parse date from request args (e.g. ?date=2026-02-23)
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        
        # Default to today if date not provided
        date_str = query.get('date', [datetime.date.today().strftime('%Y-%m-%d')])[0]
        
        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            y = date_obj.year
            m = date_obj.month
            d = date_obj.day
            day_of_week = date_obj.weekday() # 0 = Monday, 6 = Sunday
        except ValueError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid date format, use YYYY-MM-DD")
            return

        # 2. Reference Data
        monthNamesMr = ["जानेवारी", "फेब्रुवारी", "मार्च", "एप्रिल", "मे", "जून", "जुलै", "ऑगस्ट", "सप्टेंबर", "ऑक्टोबर", "नोव्हेंबर", "डिसेंबर"]
        # In Python weekday() -> 0=Mon, ... 6=Sun. Aligning to the array:
        dayNamesMr = ["सोमवार", "मंगळवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
        marathiDigits = {"0":"०", "1":"१", "2":"२", "3":"३", "4":"४", "5":"५", "6":"६", "7":"७", "8":"८", "9":"९"}

        def to_marathi(num):
            return ''.join([marathiDigits.get(c, c) for c in str(num)])

        suvicharList = [
            '"शिक्षण हे जगाला बदलण्यासाठी वापरता येणारे सर्वात शक्तिशाली शस्त्र आहे." - नेल्सन मंडेला',
            '"प्रयत्नांती परमेश्वर." - तुकाराम महाराज',
            '"वेळ कोणासाठीही थांबत नाही, वेळेचा सदुपयोग करा." - अज्ञात',
            '"नम्रता हाच खरा दागिना आहे." - अज्ञात',
            '"ज्ञान हेच खरे सामर्थ्य आहे." - फ्रान्सिस बेकन',
            '"चुका करणे ही प्रगतीची पहिली पायरी आहे." - अज्ञात',
            '"माणुसकी हीच सर्वश्रेष्ठ संपत्ती आहे." - अज्ञात',
            '"वाचाल तर वाचाल." - डॉ. बाबासाहेब आंबेडकर',
            '"उठा, जागे व्हा आणि ध्येय प्राप्त होईपर्यंत थांबू नका." - स्वामी विवेकानंद',
            '"स्वप्ने ती नव्हेत जी झोपेत पडतात, स्वप्ने ती आहेत जी झोपू देत नाहीत." - डॉ. ए. पी. जे. अब्दुल कलाम'
        ]

        mhanList = [
            { "m": "अति शहाणा त्याचा बैल रिकामा.", "a": "स्वतःला खूप हुशार समजणाऱ्या माणसाचे काम वेळेवर होत नाही किंवा बिघडते." },
            { "m": "उथळ पाण्याला खळखळाट फार.", "a": "ज्या माणसाच्या अंगी गुण कमी असतात, तो खूप बडेजाव मारतो." },
            { "m": "पाचामुखी परमेश्वर.", "a": "अनेक लोक जे बोलतात ते खरे मानावे." },
            { "m": "थेंबे थेंबे तळे साचे.", "a": "थोडी थोडी साठवण केल्यास मोठी साठवण होते." },
            { "m": "कामापुरता मामा.", "a": "फक्त आपले काम काढून घेण्यापुरते गोड बोलणारा माणूस." },
            { "m": "इकडे आड, तिकडे विहीर.", "a": "दोन्ही बाजूंनी संकट येणे." },
            { "m": "अंथरूण पाहून पाय पसरावे.", "a": "आपली परिस्थिती पाहून खर्च करावा." }
        ]

        englishWords = [
            { "e": "Curiosity", "m": "जिज्ञासा", "s1": "Children have a lot of curiosity about nature.", "s2": "(मुलांना निसर्गाबद्दल खूप जिज्ञासा असते.)" },
            { "e": "Honesty", "m": "प्रामाणिकपणा", "s1": "Honesty is the best policy.", "s2": "(प्रामाणिकपणा हे सर्वोत्कृष्ट धोरण आहे.)" },
            { "e": "Patience", "m": "संयम", "s1": "Patience is a key to success.", "s2": "(संयम ही यशाची गुरुकिल्ली आहे.)" },
            { "e": "Respect", "m": "आदर", "s1": "We should respect our elders.", "s2": "(आपण आपल्या थोरामोठ्यांचा आदर केला पाहिजे.)" },
            { "e": "Knowledge", "m": "ज्ञान", "s1": "Knowledge is power.", "s2": "(ज्ञान हीच शक्ती आहे.)" },
            { "e": "Brave", "m": "शूरवीर", "s1": "Shivaji Maharaj was a brave leader.", "s2": "(शिवाजी महाराज एक शूरवीर नेते होते.)" },
            { "e": "Nature", "m": "निसर्ग", "s1": "We must protect our nature.", "s2": "(आपण निसर्गाचे रक्षण केले पाहिजे.)" }
        ]

        kodeList = [
            { "q": "एक वस्तू जी वर जाते पण खाली कधीच येत नाही?", "a": "वय (Age)" },
            { "q": "दोन भाऊ शेजारी, भेट नाही संसारी", "a": "डोळे (Eyes)" },
            { "q": "पाण्यात जन्मतो, पाण्यातच मरतो, पण पाणी पाहिलं की घाबरतो", "a": "मीठ (Salt)" },
            { "q": "तीन अक्षरांचे माझे नाव, उलटे वाचले तरी तेच नाव", "a": "नयन / कनक" },
            { "q": "अशी कोणती गोष्ट आहे जी आपण डोळे बंद करूनच पाहू शकतो?", "a": "स्वप्न (Dream)" },
            { "q": "काळ्या रंगाची असते, पण प्रकाश दिसताच गायब होते?", "a": "सावली (Shadow)" },
            { "q": "हात नाहीत, पाय नाहीत पण तरीही ती चालते?", "a": "घड्याळ (Clock)" }
        ]

        vinodList = [
            "<p><strong>शिक्षक:</strong> बंड्या, तुला सर्वात जास्त कोणता महिना आवडतो?</p><p><strong>बंड्या:</strong> सर, मला 'मे' महिना खूप आवडतो.</p><p><strong>शिक्षक:</strong> का रे?</p><p><strong>बंड्या:</strong> कारण त्या महिन्यात शाळेला सुट्टी असते!</p>",
            "<p><strong>मुलगा:</strong> आई, मी आज एक मोठा पराक्रम केला!</p><p><strong>आई:</strong> काय रे?</p><p><strong>मुलगा:</strong> मी आज शाळेत गेलोच नाही!</p><p><strong>आई:</strong> थांबा, बाबांना येऊ दे!</p>",
            "<p><strong>गुरुजी:</strong> गंपू, 'कळस' या शब्दाचा अर्थ काय?</p><p><strong>गंपू:</strong> सर, सकाळी उठल्यावर जो येतो तो 'कळस'!</p>",
            "<p><strong>शिक्षक:</strong> गण्या, पृथ्वी गोल आहे हे कशावरून सिद्ध होते?</p><p><strong>गण्या:</strong> सर, काल मी घरातून पळालो होतो, फिरून पुन्हा तिथेच आलो!</p>",
            "<p><strong>बाबा:</strong> पिंट्या, तुझा रिझल्ट काय आला?</p><p><strong>पिंट्या:</strong> मास्तरचा मुलगा नापास झाला.</p><p><strong>बाबा:</strong> अरे पण तुझा काय?</p><p><strong>पिंट्या:</strong> डॉक्टरचा पण नापास. आणि तुमचा मुलगा काय इंजिनियर आहे का? तो पण नापास!</p>"
        ]

        gkList = [
            "<ol class='list-decimal pl-5 space-y-1 font-medium'><li>महाराष्ट्राची राजधानी कोणती? <span class='text-red-600'>(मुंबई)</span></li><li>भारताचे सध्याचे पंतप्रधान कोण? <span class='text-red-600'>(श्री. नरेंद्र मोदी)</span></li><li>सूर्यमालेतील सर्वात मोठा ग्रह कोणता? <span class='text-red-600'>(गुरू)</span></li><li>'जन गण मन' राष्ट्रगीत कोणी लिहिले? <span class='text-red-600'>(रवींद्रनाथ टागोर)</span></li><li>एका वर्षात किती आठवडे असतात? <span class='text-red-600'>(५२)</span></li></ol>",
            "<ol class='list-decimal pl-5 space-y-1 font-medium'><li>भारताचा राष्ट्रीय प्राणी कोणता? <span class='text-red-600'>(वाघ)</span></li><li>शिवाजी महाराजांचा जन्म कोठे झाला? <span class='text-red-600'>(शिवनेरी)</span></li><li>भारताचे संविधान कोणी लिहिले? <span class='text-red-600'>(डॉ. बी. आर. आंबेडकर)</span></li><li>जगातील सर्वात उंच शिखर कोणते? <span class='text-red-600'>(माउंट एव्हरेस्ट)</span></li><li>पाण्याचे रासायनिक सूत्र काय आहे? <span class='text-red-600'>(H2O)</span></li></ol>",
            "<ol class='list-decimal pl-5 space-y-1 font-medium'><li>महाराष्ट्रातील सर्वात लांब नदी कोणती? <span class='text-red-600'>(गोदावरी)</span></li><li>मानवी शरीरातील सर्वात मोठे हाड कोणते? <span class='text-red-600'>(मांडीचे - फिमर)</span></li><li>भारताचा स्वातंत्र्यदिन कधी असतो? <span class='text-red-600'>(१५ ऑगस्ट)</span></li><li>सूर्योदय कोणत्या दिशेला होतो? <span class='text-red-600'>(पूर्व)</span></li><li>इंग्रजी मुळाक्षरे किती आहेत? <span class='text-red-600'>(२६)</span></li></ol>"
        ]

        bodhkathaList = [
            "<p><strong>कथा शीर्षक :</strong> तहानलेला कावळा</p><p class='mt-1'><strong>कथा :</strong> एका कावळ्याला खूप तहान लागली होती. त्याला एका माठात थोडेसे पाणी दिसले, पण त्याची चोच पाण्यापर्यंत पोहोचत नव्हती. त्याने आजूबाजूचे खडे गोळा करून माठात टाकले. पाणी वर आले आणि त्याने पाणी पिऊन तहान भागवली.</p><p class='mt-2 text-green-800 font-bold bg-green-100 inline-block px-3 py-1 rounded'>बोध : संकटकाळी बुद्धीचा वापर करावा.</p>",
            "<p><strong>कथा शीर्षक :</strong> ससा आणि कासव</p><p class='mt-1'><strong>कथा :</strong> ससा आणि कासवाची शर्यत लागते. ससा वेगाने पळून झाडाखाली झोपतो. कासव मात्र हळूहळू पण न थांबता चालत राहते आणि शर्यत जिंकते.</p><p class='mt-2 text-green-800 font-bold bg-green-100 inline-block px-3 py-1 rounded'>बोध : सातत्य आणि जिद्द असेल तर नक्की यश मिळते.</p>",
            "<p><strong>कथा शीर्षक :</strong> प्रामाणिक लाकूडतोड्या</p><p class='mt-1'><strong>कथा :</strong> एका लाकूडतोड्याची कुऱ्हाड नदीत पडते. देव त्याला सोन्याची व चांदीची कुऱ्हाड दाखवतात, पण तो आपली लोखंडाची कुऱ्हाडच मागतो. त्याच्या प्रामाणिकपणावर खूश होऊन देव त्याला सर्व कुऱ्हाडी बक्षीस देतात.</p><p class='mt-2 text-green-800 font-bold bg-green-100 inline-block px-3 py-1 rounded'>बोध : प्रामाणिकपणाचे फळ नेहमी चांगले मिळते.</p>"
        ]

        dinvisheshData = {
            "1-3": "<li><strong>३ जानेवारी:</strong> क्रांतिज्योती सावित्रीबाई फुले जयंती.</li><li><strong>३ जानेवारी:</strong> बालिका दिन.</li>",
            "1-12": "<li><strong>१२ जानेवारी:</strong> राजमाता जिजाऊ जयंती.</li><li><strong>१२ जानेवारी:</strong> स्वामी विवेकानंद जयंती (राष्ट्रीय युवक दिन).</li>",
            "1-26": "<li><strong>२६ जानेवारी:</strong> भारतीय प्रजासत्ताक दिन.</li>",
            "2-19": "<li><strong>१९ फेब्रुवारी:</strong> छत्रपती शिवाजी महाराज जयंती.</li>",
            "2-23": "<li><strong>२३ फेब्रुवारी:</strong> संत गाडगे बाबा महाराज जयंती.</li><li><strong>१९४७:</strong> 'आंतरराष्ट्रीय मानकीकरण संघटना' (ISO) ची स्थापना.</li>",
            "2-27": "<li><strong>२७ फेब्रुवारी:</strong> मराठी भाषा गौरव दिन (कुसुमाग्रज जयंती).</li>",
            "2-28": "<li><strong>२८ फेब्रुवारी:</strong> राष्ट्रीय विज्ञान दिन.</li>",
            "4-11": "<li><strong>११ एप्रिल:</strong> महात्मा ज्योतिराव फुले जयंती.</li>",
            "4-14": "<li><strong>१४ एप्रिल:</strong> भारतरत्न डॉ. बाबासाहेब आंबेडकर जयंती.</li>",
            "5-1": "<li><strong>१ मे:</strong> महाराष्ट्र दिन.</li><li><strong>१ मे:</strong> कामगार दिन.</li>",
            "6-5": "<li><strong>५ जून:</strong> जागतिक पर्यावरण दिन.</li>",
            "8-1": "<li><strong>१ ऑगस्ट:</strong> लोकमान्य टिळक पुण्यतिथी.</li><li><strong>१ ऑगस्ट:</strong> अण्णाभाऊ साठे जयंती.</li>",
            "8-15": "<li><strong>१५ ऑगस्ट:</strong> भारतीय स्वातंत्र्य दिन.</li>",
            "9-5": "<li><strong>५ सप्टेंबर:</strong> शिक्षक दिन (डॉ. सर्वपल्ली राधाकृष्णन जयंती).</li>",
            "10-2": "<li><strong>२ ऑक्टोबर:</strong> महात्मा गांधी जयंती.</li><li><strong>२ ऑक्टोबर:</strong> लाल बहादूर शास्त्री जयंती.</li>",
            "10-15": "<li><strong>१५ ऑक्टोबर:</strong> वाचन प्रेरणा दिन (डॉ. ए. पी. जे. अब्दुल कलाम जयंती).</li>",
            "11-14": "<li><strong>१४ नोव्हेंबर:</strong> बाल दिन (पंडित नेहरू जयंती).</li>",
            "12-6": "<li><strong>६ डिसेंबर:</strong> महापरिनिर्वाण दिन.</li>"
        }

        # 3. Deterministic Seed Generation
        # Seed ensures that the same date always gets the same quotes/jokes
        seed = d + (m - 1) + (y % 100)
        
        # 4. Process Data
        formatted_date = f"{to_marathi(d)} {monthNamesMr[m - 1]} {to_marathi(y)}"
        formatted_day = dayNamesMr[day_of_week]
        
        din_key = f"{m}-{d}"
        dinvishesh = dinvisheshData.get(din_key, "<li>आजचा कोणताही महत्त्वाचा दिनविशेष नाही. (येथे क्लिक करून माहिती भरा)</li>")
        
        # Format Suvichar
        raw_suvichar = suvicharList[seed % len(suvicharList)]
        suv_parts = raw_suvichar.split(' - ')
        suvichar = {
            "quote": suv_parts[0],
            "author": f"- {suv_parts[1]}" if len(suv_parts) > 1 else ""
        }
        
        response_data = {
            "dateStr": formatted_date,
            "dayStr": formatted_day,
            "suvichar": suvichar,
            "mhan": mhanList[seed % len(mhanList)],
            "english": englishWords[seed % len(englishWords)],
            "kode": kodeList[seed % len(kodeList)],
            "vinod": vinodList[seed % len(vinodList)],
            "gk": gkList[seed % len(gkList)],
            "bodhkatha": bodhkathaList[seed % len(bodhkathaList)],
            "dinvishesh": f"<ul class='list-disc pl-5 space-y-1 text-gray-800'>{dinvishesh}</ul>"
        }

        # 5. Send JSON Response
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        # Enable CORS for local testing if needed
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
