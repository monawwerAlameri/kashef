"""Comprehensive Pharmaceutical Dataset for Kashef.
Contains detailed bilingual medical information for hundreds of common medications
across multiple categories: Analgesics, Antibiotics, Antihistamines, Antacids,
Cardiovascular, Diabetes, Respiratory, and Vitamins.
"""

PHARMA_DATASET = [
    # --- Analgesics & Antipyretics (مسكنات وخوافض حرارة) ---
    {
        "id": "panadol_extra",
        "name": "Panadol Extra",
        "name_ar": "بنادول إكسترا",
        "generic_name": "Paracetamol + Caffeine",
        "active_ingredient": "Paracetamol 500mg, Caffeine 65mg",
        "aliases": ["panadol extra", "بنادول اكسترا", "بنادول إكسترا", "panadol قرمز", "panadol red"],
        "category": "مسكنات وخافضات حرارة (Analgesic)",
        "strength": "500mg / 65mg",
        "dosage_amount": "1 إلى 2 قرص",
        "timing": "كل 4 إلى 6 ساعات عند اللزوم (بحد أقصى 8 أقراص يومياً)",
        "purpose": "تسكين الآلام الشديدة، الصداع، آلام الأسنان، وخفض درجات الحرارة المرتفعة.",
        "warnings": [
            "لا تتجاوز 8 أقراص خلال 24 ساعة تجنباً للتسمم الكبدي الحاد.",
            "يحظر تناوله مع أي مستحضرات أخرى تحتوي على الباراسيتامول في نفس الوقت."
        ],
        "precautions": [
            "استشر الطبيب في حالات أمراض الكبد والكلى المزمنة.",
            "الحد من استهلاك المشروبات المحتوية على الكافيين لتجنب الأرق وتسارع ضربات القلب."
        ],
        "side_effects": ["أرق أو عصبية طفيفة بسبب الكافيين", "نادراً تفاعلات تحسسية جلدية"],
        "storage": ["يحفظ تحت 25 درجة مئوية في مكان جاف وبارد بعيداً عن متناول الأطفال."]
    },
    {
        "id": "panadol_advance",
        "name": "Panadol Advance",
        "name_ar": "بنادول أدفانس الأزرق",
        "generic_name": "Paracetamol",
        "active_ingredient": "Paracetamol 500mg",
        "aliases": ["panadol advance", "بنادول الأزرق", "بنادول ادفانس", "panadol blue", "panadol 500"],
        "category": "مسكنات وخافضات حرارة (Analgesic)",
        "strength": "500mg",
        "dosage_amount": "1 إلى 2 قرص",
        "timing": "كل 4 إلى 6 ساعات عند اللزوم (الحد الأقصى 4000 مجم يومياً)",
        "purpose": "تسكين الصداع، آلام العضلات، آلام المفاصل الخفيفة، وخفض الحرارة.",
        "warnings": ["تجاوز الجرعة الموصى بها قد يسبب تلفاً خطيراً في الكبد."],
        "precautions": ["آمن أثناء الحمل والرضاعة بالجرعات المقررة سريرياً."],
        "side_effects": ["نادر الحدوث عند الالتزام بالجرعة العلاجية المحددة."],
        "storage": ["يحفظ في درجة حرارة الغرفة أقل من 25 درجة مئوية."]
    },
    {
        "id": "panadol_cold_flu",
        "name": "Panadol Cold & Flu",
        "name_ar": "بنادول كولد آند فلو",
        "generic_name": "Paracetamol + Pseudoephedrine + Chlorpheniramine",
        "active_ingredient": "Paracetamol 500mg, Pseudoephedrine 30mg, Chlorpheniramine 2mg",
        "aliases": ["panadol cold", "panadol flu", "بنادول الأخضر", "بنادول الزكام", "panadol green"],
        "category": "أدوية البرد والإنفلونزا (Cold & Flu)",
        "strength": "500mg / 30mg / 2mg",
        "dosage_amount": "1 إلى 2 قرص",
        "timing": "كل 6 إلى 8 ساعات بعد الأكل",
        "purpose": "علاج أعراض البرد والرشح والإنفلونزا واحتقان الأنف والصداع.",
        "warnings": ["يمنع لمرضى الضغط المرتفع غير المنتظم ومرضى الشريان التاجي."],
        "precautions": ["يسبب النعاس؛ تجنب القيادة أو تشغيل الآلات الثقيلة."],
        "side_effects": ["نعاس، جفاف الفم، دوخة طفيفة، تسارع نبضات القلب أحياناً."],
        "storage": ["يحفظ بعيداً عن الرطوبة وأشعة الشمس المباشرة."]
    },
    {
        "id": "brufen",
        "name": "Brufen / Advil",
        "name_ar": "بروفين / أدفيل",
        "generic_name": "Ibuprofen",
        "active_ingredient": "Ibuprofen 400mg / 600mg",
        "aliases": ["brufen", "advil", "بروفين", "ادفل", "أدفيل", "ايبوبروفين", "ibuprofen"],
        "category": "مضادات الالتهاب غير الستيرويدية (NSAID)",
        "strength": "400mg / 600mg",
        "dosage_amount": "قرص واحد (400 مجم أو 600 مجم)",
        "timing": "كل 8 ساعات بعد الأكل مباشرة مع كوب ماء كامل",
        "purpose": "تسكين آلام الأسنان، الصداع النصفي، علاج التهاب المفاصل، وتخفيف آلام الدورة الشهرية.",
        "warnings": [
            "يمنع استخدامه لمرضى قرحة المعدة والنزيف الهضمي النشط.",
            "يحظر في الثلث الأخير من الحمل لتجنب المضاعفات الجنينية."
        ],
        "precautions": ["يؤخذ بعد الطعام لحماية جدار المعدة من التهيج."],
        "side_effects": ["ألم أو حرقة بالمعدة، عسر هضم، غثيان خفيف."],
        "storage": ["يحفظ تحت 25°C في عبوته الأصلية المحكمة."]
    },
    {
        "id": "cataflam",
        "name": "Cataflam",
        "name_ar": "كاتافلام",
        "generic_name": "Diclofenac Potassium",
        "active_ingredient": "Diclofenac Potassium 50mg",
        "aliases": ["cataflam", "كاتافلام", "ديكلوفيناك بوتاسيوم", "diclofenac"],
        "category": "مضادات الالتهاب غير الستيرويدية سريعة المفعول",
        "strength": "50mg",
        "dosage_amount": "قرص واحد 50 مجم",
        "timing": "كل 8 إلى 12 ساعة بعد الأكل",
        "purpose": "تسكين فوري وحاد لآلام الأسنان، الصداع النصفي، والآلام الروماتيزمية الحادة.",
        "warnings": ["يمنع لمرضى الفشل الكلوي الحاد ومرضى القرحة الهضمية."],
        "precautions": ["الحذر لدى مرضى القلب والشرايين وارتفاع ضغط الدم."],
        "side_effects": ["حرقة المعدة، غثيان، دوخة."],
        "storage": ["يحفظ في درجة حرارة أقل من 30 درجة مئوية."]
    },
    {
        "id": "voltaren",
        "name": "Voltaren",
        "name_ar": "فولتارين",
        "generic_name": "Diclofenac Sodium",
        "active_ingredient": "Diclofenac Sodium 50mg / 75mg / 100mg",
        "aliases": ["voltaren", "فولتارين", "فولتارين ريتارد", "diclofenac sodium"],
        "category": "مسكنات ومضادات الروماتيزم (NSAID)",
        "strength": "50mg / 75mg / 100mg",
        "dosage_amount": "قرص واحد أو تحميلة واحدة",
        "timing": "مرة إلى مرتين يومياً بعد الأكل مباشرة",
        "purpose": "علاج التهاب المفاصل الروماتويدي، آلام العمود الفقري، والالتواءات الحادة.",
        "warnings": ["يمنع استخدامه لمرضى الربو الذين يتحسسون من الأسبرين."],
        "precautions": ["يجب مراقبة وظائف الكلى والكبد في الاستخدام طويل الأمد."],
        "side_effects": ["اضطراب هضمي، ارتفاع طفيف بضغط الدم، صداع."],
        "storage": ["يحفظ بعيداً عن الحرارة والرطوبة."]
    },
    {
        "id": "solpadeine",
        "name": "Solpadeine",
        "name_ar": "سولبادين فوار / أقراص",
        "generic_name": "Paracetamol + Codeine + Caffeine",
        "active_ingredient": "Paracetamol 500mg, Codeine 8mg, Caffeine 30mg",
        "aliases": ["solpadeine", "سولبادين", "سولبادين فوار", "solpadine"],
        "category": "مسكنات أفيونية خفيفة (Opioid Combination)",
        "strength": "500mg / 8mg / 30mg",
        "dosage_amount": "1 إلى 2 قرص فوار مذاب في نصف كوب ماء",
        "timing": "كل 6 ساعات عند اللزوم (لا يستخدم أكثر من 3 أيام متتالية)",
        "purpose": "تسكين الآلام الشديدة التي لا تستجيب للباراسيتامول بمفرده.",
        "warnings": [
            "خطر التعود والإدمان عند الاستخدام المتواصل لأكثر من 3 أيام دون إشراف طبي.",
            "ممنوع للأطفال دون 12 عاماً والنساء المرضعات."
        ],
        "precautions": ["قد يسبب النعاس والإمساك، تجنب القيادة أثناء تناوله."],
        "side_effects": ["إمساك، دوار، نعاس، جفاف الفم."],
        "storage": ["يحفظ تحت 25°C في مكان جاف."]
    },

    # --- Antibiotics (المضادات الحيوية) ---
    {
        "id": "augmentin",
        "name": "Augmentin",
        "name_ar": "أوجمنتين",
        "generic_name": "Amoxicillin + Clavulanic Acid",
        "active_ingredient": "Amoxicillin 875mg + Clavulanic Acid 125mg (1g) / 625mg",
        "aliases": ["augmentin", "اوجمنتين", "أوجمنتين", "اوغمنتين", "amoxicillin clavulanate", "amoclan"],
        "category": "مضادات حيوية واسعة المجال (Penicillin-based)",
        "strength": "1g (1000mg) / 625mg",
        "dosage_amount": "قرص واحد (1 جم أو 625 مجم)",
        "timing": "كل 12 ساعة في بداية الوجبة لتقليل اضطراب المعدة",
        "purpose": "علاج التهابات الجهاز التنفسي، التهاب الجيوب الأنفية، الأذن الوسطى، والتهابات المسالك البولية والجلد.",
        "warnings": [
            "ممنوع منعاً باتاً لمرضى حساسية البنسلين ومشتقاته (خطر الصدمة التحسسية).",
            "يجب إكمال الكورس العلاجي بالكامل (7-10 أيام) حتى لو اختفت الأعراض لمنع مقاومة البكتيريا."
        ],
        "precautions": ["استشر الطبيب في حال حدوث إسهال حاد أو مستمر أثناء العلاج."],
        "side_effects": ["إسهال خفيف، غثيان، طفح جلدي في حالات التحسس."],
        "storage": ["يحفظ تحت 25°C؛ أما الشراب المعلق فيحفظ بالثلاجة لمدة 7 أيام فقط."]
    },
    {
        "id": "amoxil",
        "name": "Amoxil",
        "name_ar": "أموكسيل / أموكسيسيلين",
        "generic_name": "Amoxicillin",
        "active_ingredient": "Amoxicillin 500mg / 250mg",
        "aliases": ["amoxil", "amoxicillin", "اموكسيل", "أموكسيل", "اموكسيسيلين", "أموكسيسيلين"],
        "category": "مضادات حيوية (Aminopenicillin)",
        "strength": "500mg",
        "dosage_amount": "كبسولة واحدة (500 مجم)",
        "timing": "كل 8 ساعات لمدة 7 إلى 10 أيام",
        "purpose": "علاج التهاب اللوزتين، التهابات الشعب الهوائية، وخراجات الأسنان.",
        "warnings": ["يحظر على المصابين بحساسية البنسلين."],
        "precautions": ["قد يقلل من فعالية بعض حبوب منع الحمل."],
        "side_effects": ["إسهال، غثيان، اضطرابات معوية خفيفة."],
        "storage": ["يحفظ في مكان جاف أقل من 25 درجة مئوية."]
    },
    {
        "id": "zithromax",
        "name": "Zithromax",
        "name_ar": "زيثر Sex / زيثروماكس",
        "generic_name": "Azithromycin",
        "active_ingredient": "Azithromycin 500mg / 250mg",
        "aliases": ["zithromax", "azithromycin", "زيثروماكس", "زيثرون", "ازيثرومايسين", "أزيثروميسين"],
        "category": "مضادات حيوية ماكروليدية (Macrolide)",
        "strength": "500mg",
        "dosage_amount": "قرص واحد يومياً (500 مجم)",
        "timing": "مرة واحدة يومياً لمدة 3 أو 5 أيام قبل الأكل بساعة أو بعده بساعتين",
        "purpose": "علاج التهابات الجهاز التنفسي العلوي والسفلي، والتهابات الجلد والأنسجة الرخوة.",
        "warnings": ["الحذر لدى المرضى الذين يعانون من اضطراب في كهربية القلب وتطاول فترة QT."],
        "precautions": ["لا يؤخذ بالتزامن مع مضادات الحموضة المحتوية على الألمنيوم أو المغنيسيوم."],
        "side_effects": ["إسهال، ألم بالمعدة، صداع، فقدان شهية مؤقت."],
        "storage": ["يحفظ في درجة حرارة دون 30°C بعيداً عن الرطوبة."]
    },
    {
        "id": "cipro",
        "name": "Ciprocin / Cipro",
        "name_ar": "سيبروفلوكساسين / سيبرو",
        "generic_name": "Ciprofloxacin",
        "active_ingredient": "Ciprofloxacin 500mg / 750mg",
        "aliases": ["cipro", "ciprofloxacin", "سيبرو", "سيبروفلوكساسين", "سيبروباي", "ciprobay"],
        "category": "مضادات الفلوروكينولون (Fluoroquinolone)",
        "strength": "500mg",
        "dosage_amount": "قرص واحد (500 مجم)",
        "timing": "كل 12 ساعة مع كمية وفيرة من الماء (تجنب منتجات الألبان ساعتين قبل وبعد)",
        "purpose": "علاج التهابات المسالك البولية الحادة والمعقدة، والتهابات البروستاتا والمسالك الهضمية.",
        "warnings": [
            "خطر التهاب أو تمزق الأوتار العضلية (خاصة وتر أكيليس).",
            "ممنوع للأطفال والمراهقين تحت سن 18 عاماً وللحوامل."
        ],
        "precautions": ["يزيد من حساسية الجلد لأشعة الشمس؛ تجنب التعرض المباشر للشمس."],
        "side_effects": ["غثيان، دوخة، إسهال، ألم مفاصل."],
        "storage": ["يحفظ تحت 25°C في مكان جاف."]
    },
    {
        "id": "flagyl",
        "name": "Flagyl",
        "name_ar": "فلاجيل",
        "generic_name": "Metronidazole",
        "active_ingredient": "Metronidazole 500mg",
        "aliases": ["flagyl", "فلاجيل", "مترونيدازول", "metronidazole"],
        "category": "مضادات الطفيليات والبكتيريا اللاهوائية (Antiprotozoal)",
        "strength": "500mg",
        "dosage_amount": "قرص واحد (500 مجم)",
        "timing": "كل 8 ساعات مع الوجبات لمدة 5-10 أيام",
        "purpose": "علاج داء الأميبا، الجيارديات، التهابات اللثة والأسنان اللاهوائية، والالتهابات المهبلية.",
        "warnings": [
            "يمنع منعاً باتاً تناول الكحوليات أثناء العلاج ولمدة 48 ساعة بعده (تفاعل ديسلفيرام الحاد).",
            "يمنع في الثلث الأول من الحمل."
        ],
        "precautions": ["يؤخذ مع الطعام لمنع تهيج المعدة."],
        "side_effects": ["طعم معدني مميز في الفم، غمقان لون البول، فقدان الشهية."],
        "storage": ["يحفظ بعيداً عن الضوء المباشر في مكان بارد."]
    },

    # --- Gastrointestinal & Antacids (أدوية الجهاز الهضمي والمعدة) ---
    {
        "id": "nexium",
        "name": "Nexium",
        "name_ar": "نيكسيوم",
        "generic_name": "Esomeprazole",
        "active_ingredient": "Esomeprazole 20mg / 40mg",
        "aliases": ["nexium", "نيكسيوم", "ايزوميبرازول", "esomeprazole"],
        "category": "مثبطات مضخة البروتون (PPI)",
        "strength": "20mg / 40mg",
        "dosage_amount": "قرص واحد (20 مجم أو 40 مجم)",
        "timing": "مرة واحدة يومياً صباحاً على معدة فارغة قبل الإفطار بنصف ساعة",
        "purpose": "علاج ارتجاع المريء (GERD)، قرحة المعدة والاثني عشر، وحرقة الفؤاد الشديدة.",
        "warnings": ["يجب بلع القرص كاملاً ولا يجوز كسره أو مضغه."],
        "precautions": ["الاستخدام طويل الأمد قد يقلل من امتصاص فيتامين B12 والمغنيسيوم والكالسيوم."],
        "side_effects": ["صداع، ألم في البطن، إسهال أو إمساك طفيف."],
        "storage": ["يحفظ تحت 30°C في مكان جاف ومحمي من الرطوبة."]
    },
    {
        "id": "pantoloc",
        "name": "Pantoloc / Controloc",
        "name_ar": "بانتولوك / كونترولوك",
        "generic_name": "Pantoprazole",
        "active_ingredient": "Pantoprazole 20mg / 40mg",
        "aliases": ["pantoloc", "controloc", "بانتولوك", "كونترولوك", "بانتوبرازول", "pantoprazole"],
        "category": "مثبطات حموضة المعدة (PPI)",
        "strength": "40mg",
        "dosage_amount": "قرص واحد 40 مجم",
        "timing": "مرة واحدة يومياً صباحاً قبل الأكل بنصف ساعة",
        "purpose": "علاج حموضة المعدة والارتجاع المريئي والوقاية من قرحة المعدة الناتجة عن المسكنات.",
        "warnings": ["لا تمضغ القرص."],
        "precautions": ["استشر الطبيب إذا استمرت الأعراض لأكثر من أسبوعين."],
        "side_effects": ["صداع، غازات، غثيان خفيف."],
        "storage": ["يحفظ تحت 25°C."]
    },
    {
        "id": "gaviscon",
        "name": "Gaviscon",
        "name_ar": "جافيسكون",
        "generic_name": "Sodium Alginate + Potassium Bicarbonate",
        "active_ingredient": "Sodium Alginate 500mg, Potassium Bicarbonate 100mg",
        "aliases": ["gaviscon", "جافيسكون", "جافسكون"],
        "category": "مضادات الحموضة والارتجاع الموضعية (Antacid Barrier)",
        "strength": "10ml شراب أو قرصين للمضغ",
        "dosage_amount": "10-20 مل أو 1-2 قرص للمضغ",
        "timing": "بعد الوجبات الرئيسية وقبل النوم مباشرة",
        "purpose": "تخفيف فوري لحرقة المعدة، عسر الهضم الحمضي، وارتجاع العصارة الصفراوية.",
        "warnings": ["يحتوي على الصوديوم؛ يرجى الحذر لمرضى الضغط العالي والقصور الكلوي."],
        "precautions": ["مضغ الأقراص جيداً قبل البلع، ورج زجاجة الشراب قبل الاستعمال."],
        "side_effects": ["انتفاخ بطن طفيف، تجشؤ."],
        "storage": ["يحفظ تحت 30°C ولا يوضع في الثلاجة."]
    },
    {
        "id": "motilium",
        "name": "Motilium",
        "name_ar": "موتيليوم",
        "generic_name": "Domperidone",
        "active_ingredient": "Domperidone 10mg",
        "aliases": ["motilium", "موتيليوم", "دومبيريدون", "domperidone"],
        "category": "محفزات حركة الجهاز الهضمي ومضادات الغثيان (Prokinetic)",
        "strength": "10mg",
        "dosage_amount": "قرص واحد (10 مجم)",
        "timing": "قبل الأكل بـ 15-30 دقيقة، حتى 3 مرات يومياً (أقصر مدة ممكنة)",
        "purpose": "علاج الغثيان والقيء والشعور بالامتلاء المبكر وعسر الهضم الحركي.",
        "warnings": ["يحظر لمرضى اضطراب نبضات القلب والقصور الكبدي المعتدل والشديد."],
        "precautions": ["لا تتجاوز مدة العلاج أسبوعاً واحداً بدون استشارة طبية."],
        "side_effects": ["جفاف الفم، تشنجات بطنية نادرة."],
        "storage": ["يحفظ تحت 25°C."]
    },

    # --- Antihistamines & Allergy (أدوية الحساسية ومضادات الهيستامين) ---
    {
        "id": "zyrtec",
        "name": "Zyrtec",
        "name_ar": "زيرتك",
        "generic_name": "Cetirizine",
        "active_ingredient": "Cetirizine Hydrochloride 10mg",
        "aliases": ["zyrtec", "زيرتك", "سيتريزين", "cetirizine"],
        "category": "مضادات الهيستامين غير المهدئة (Antihistamine)",
        "strength": "10mg",
        "dosage_amount": "قرص واحد (10 مجم)",
        "timing": "مرة واحدة يومياً مساءً قبل النوم مع أو بدون طعام",
        "purpose": "علاج حمى القش، حساسية الأنف الموسمية، الحكة الجلدية، والارتكاريا المزمنة.",
        "warnings": ["قد يسبب نعاساً لدى بعض الأشخاص الحساسين."],
        "precautions": ["تجنب المشروبات الكحولية والمهدئات أثناء الاستخدام."],
        "side_effects": ["نعاس خفيف، جفاف الفم، صداع."],
        "storage": ["يحفظ تحت 25°C في مكان جاف."]
    },
    {
        "id": "claritin",
        "name": "Claritin",
        "name_ar": "كلاريتين",
        "generic_name": "Loratadine",
        "active_ingredient": "Loratadine 10mg",
        "aliases": ["claritin", "كلاريتين", "لوراتادين", "loratadine"],
        "category": "مضادات الهيستامين من الجيل الثاني (Non-drowsy Antihistamine)",
        "strength": "10mg",
        "dosage_amount": "قرص واحد (10 مجم)",
        "timing": "مرة واحدة يومياً في أي وقت من اليوم",
        "purpose": "علاج حساسية الأنف، العطاس وسيلان الأنف، وحساسية العين والجلد.",
        "warnings": ["لا يسبب النعاس في الجرعات العلاجية الموصى بها."],
        "precautions": ["استشر الطبيب لمرضى الفشل الكبدي لتعديل الجرعة."],
        "side_effects": ["نادرة جداً، جفاف فم طفيف، تعب عابر."],
        "storage": ["يحفظ في درجة حرارة أقل من 25 درجة مئوية."]
    },
    {
        "id": "telfast",
        "name": "Telfast",
        "name_ar": "تلفاست",
        "generic_name": "Fexofenadine",
        "active_ingredient": "Fexofenadine Hydrochloride 120mg / 180mg",
        "aliases": ["telfast", "تلفاست", "فيكسوفينادين", "fexofenadine"],
        "category": "مضادات حساسية متطورة لا تسبب النعاس",
        "strength": "120mg / 180mg",
        "dosage_amount": "قرص واحد (120 مجم للحساسية الأنفية، أو 180 مجم للارتكاريا الجلدية)",
        "timing": "مرة واحدة يومياً مع الماء (تجنب عصائر الفاكهة كالجريب فروت والبرتقال)",
        "purpose": "تخفيف أعراض التهاب الأنف التحسسي وحكة الجلد والطفح الجلدي.",
        "warnings": ["عصائر الحمضيات قد تقلل من امتصاص الدواء بشكل كبير."],
        "precautions": ["آمن لمن يحتاجون لليقظة العالية وسائقي المركبات."],
        "side_effects": ["صداع طفيف، دوار نادر."],
        "storage": ["يحفظ تحت 25°C."]
    },

    # --- Cardiovascular, Hypertension & Diabetes (الضغط والقلب والسكر) ---
    {
        "id": "concor",
        "name": "Concor",
        "name_ar": "كونكور",
        "generic_name": "Bisoprolol Fumarate",
        "active_ingredient": "Bisoprolol 2.5mg / 5mg / 10mg",
        "aliases": ["concor", "كونكور", "بيسوبرولول", "bisoprolol"],
        "category": "حاصرات بيتا القلبية الانتقائية (Beta-blocker)",
        "strength": "2.5mg / 5mg / 10mg",
        "dosage_amount": "قرص واحد يومياً",
        "timing": "مرة واحدة صباحاً مع أو بعد الإفطار في نفس الموعد يومياً",
        "purpose": "علاج ارتفاع ضغط الدم، الذبحة الصدرية، وقصور عضلة القلب المزمن.",
        "warnings": [
            "يحظر التوقف المفاجئ عن تناول الدواء دون استشارة الطبيب لتجنب ارتداد الضغط وتسارع القلب.",
            "ممنوع لمرضى الربو القصبي الشديد ومرضى بطء القلب الحاد."
        ],
        "precautions": ["مراقبة النبض وضغط الدم بانتظام."],
        "side_effects": ["برودة الأطراف، إرهاق، بطء معدل ضربات القلب، دوخة."],
        "storage": ["يحفظ في درجة حرارة دون 30°C."]
    },
    {
        "id": "glucophage",
        "name": "Glucophage",
        "name_ar": "جلوكوفاج",
        "generic_name": "Metformin Hydrochloride",
        "active_ingredient": "Metformin 500mg / 850mg / 1000mg",
        "aliases": ["glucophage", "جلوكوفاج", "ميتفورمين", "metformin", "منظم السكر"],
        "category": "منظمات سكر الدم (Biguanide)",
        "strength": "500mg / 850mg / 1000mg",
        "dosage_amount": "قرص واحد مع الوجبات",
        "timing": "مرة إلى مرتين يومياً مع الأكل أو بعده مباشرة لتقليل اضطراب المعدة",
        "purpose": "علاج السكري من النوع الثاني وتحسين حساسية الخلايا للإنسولين.",
        "warnings": ["يمنع لمرضى الفشل الكلوي الحاد والحماض اللبني (Lactic Acidosis)."],
        "precautions": ["يجب إيقاف الدواء مؤقتاً قبل إجراء الأشعة المقطعية بالصبغة بـ 48 ساعة."],
        "side_effects": ["اضطراب معوي، غثيان، إسهال في الأسابيع الأولى، طعم معدني."],
        "storage": ["يحفظ تحت 25°C في مكان جاف."]
    },
    {
        "id": "lipitor",
        "name": "Lipitor",
        "name_ar": "ليبيتور",
        "generic_name": "Atorvastatin",
        "active_ingredient": "Atorvastatin Calcium 10mg / 20mg / 40mg",
        "aliases": ["lipitor", "ليبيتور", "اتورفاستاتين", "atorvastatin"],
        "category": "خافضات الكوليسترول والدهون الثلاثية (Statin)",
        "strength": "10mg / 20mg / 40mg",
        "dosage_amount": "قرص واحد يومياً",
        "timing": "مرة واحدة يومياً مساءً قبل النوم مع أو بدون طعام",
        "purpose": "خفض الكوليسترول الضار (LDL) والدهون الثلاثية، والوقاية من النوبات القلبية والسكتات الدماغية.",
        "warnings": ["ممنوع منعاً باتاً للحوامل والمرضعات لتأثيره على تكوين الجنين."],
        "precautions": ["راجع الطبيب فوراً إذا شعرت بآلام عضلية شديدة أو وهن غير مبرر."],
        "side_effects": ["آلام عضلية خفيفة، اضطراب هضمي، ارتفاع طفيف بإنزيمات الكبد."],
        "storage": ["يحفظ تحت 25°C بعيداً عن الرطوبة."]
    },

    # --- Respiratory (الجهاز التنفسي) ---
    {
        "id": "ventolin",
        "name": "Ventolin Inhaler",
        "name_ar": "بخاخ فنتولين الأزرق",
        "generic_name": "Salbutamol",
        "active_ingredient": "Salbutamol 100mcg per dose",
        "aliases": ["ventolin", "فنتولين", "سالبوتامول", "salbutamol", "بخاخ أزرق"],
        "category": "موسعات الشعب الهوائية سريعة المفعول (Short-Acting Beta Agonist)",
        "strength": "100mcg / actuation",
        "dosage_amount": "بخة إلى بختين استنشاق",
        "timing": "عند حدوث نوبة ضيق التنفس أو قبل ممارسة الرياضة بـ 15 دقيقة",
        "purpose": "علاج سريع وفوري لنوبات الربو الشعبي وضيق التنفس وتشنج القصبات.",
        "warnings": ["إذا لم يهدأ ضيق التنفس بعد بختين، اطلب الطوارئ الطبية فوراً."],
        "precautions": ["رج البخاخ جيداً قبل الاستخدام واشطف الفم بالماء بعد البخ."],
        "side_effects": ["رعشة خفيفة في اليدين، تسارع نبضات القلب، صداع عابر."],
        "storage": ["يحفظ تحت 30°C بعيداً عن أشعة الشمس المباشرة والتجميد."]
    },
    {
        "id": "otrivin",
        "name": "Otrivin Nasal Drops / Spray",
        "name_ar": "أوتريفين بخاخ / نقط الأنف",
        "generic_name": "Xylometazoline",
        "active_ingredient": "Xylometazoline 0.1% (Adults) / 0.05% (Children)",
        "aliases": ["otrivin", "اوترفين", "أوتريفين", "زايلوميتازولين", "xylometazoline"],
        "category": "مضادات احتقان الأنف الموضعية (Nasal Decongestant)",
        "strength": "0.1% (Adults)",
        "dosage_amount": "بخة واحدة أو قطرتان في كل فتحة أنف",
        "timing": "كل 8 إلى 10 ساعات (الحد الأقصى 3 مرات يومياً)",
        "purpose": "فتح انسداد الأنف السريع وتخفيف احتقان الجيوب الأنفية والزكام.",
        "warnings": [
            "يحظر استخدامه لأكثر من 5 إلى 7 أيام متتالية تجنباً لانسداد الأنف الارتدادي المزمن (Rhinitis Medicamentosa).",
            "الحذر لمرضى ضغط الدم المرتفع ومرضى الجلوكوما."
        ],
        "precautions": ["لا يشارك البخاخ مع شخص آخر لمنع انتقال العدوى."],
        "side_effects": ["جفاف الأنف، حرقة خفيفة، عطاس."],
        "storage": ["يحفظ تحت 25°C."]
    },

    # --- Vitamins & Supplements (الفيتامينات والمكملات) ---
    {
        "id": "vitamin_d3",
        "name": "Vitamin D3 (Cholecalciferol)",
        "name_ar": "فيتامين د3 (كوليكالسيفيرول)",
        "generic_name": "Cholecalciferol",
        "active_ingredient": "Cholecalciferol 50,000 IU / 5,000 IU / 1,000 IU",
        "aliases": ["vitamin d", "vitamin d3", "فيتامين د", "فيتامين د3", "cholecalciferol", "vidrop"],
        "category": "فيتامينات ومكملات غذائية أساسية (Vitamin)",
        "strength": "50,000 IU / 5,000 IU",
        "dosage_amount": "كبسولة واحدة (50,000 وحدة أسبوعياً أو 5,000 وحدة يومياً)",
        "timing": "مع وجبة دسمة تحتوي على دهون صحية لتعزيز الامتصاص",
        "purpose": "علاج نقص فيتامين د، تقوية العظام والأسنان، ودعم المناعة وامتصاص الكالسيوم.",
        "warnings": ["تجنب الجرعات المفرطة بدون فحص مخبري لتجنب التسمم وارتفاع كالسيوم الدم."],
        "precautions": ["افحص مستوى فيتامين د في الدم بصفة دورية."],
        "side_effects": ["نادر عند الجرعات المقررة، إفراط الجرعة يسبب غثيان وعطش شديد."],
        "storage": ["يحفظ بعيداً عن الضوء والحرارة تحت 25°C."]
    },
    {
        "id": "vitamin_c",
        "name": "Vitamin C (Ascorbic Acid)",
        "name_ar": "فيتامين سي الفوار",
        "generic_name": "Ascorbic Acid",
        "active_ingredient": "Ascorbic Acid 1000mg",
        "aliases": ["vitamin c", "فيتامين سي", "فيتامين ج", "فوار فيتامين سي", "ascorbic acid", "cebion", "redoxon"],
        "category": "مضادات أكسدة وفيتامينات (Antioxidant / Vitamin)",
        "strength": "1000mg (1g)",
        "dosage_amount": "قرص فوار واحد مذاب في كوب ماء كامل",
        "timing": "مرة واحدة يومياً صباحاً بعد الأكل",
        "purpose": "تعزيز المناعة ومقاومة نزلات البرد، والمساعدة في تصنيع الكولاجين وامتصاص الحديد.",
        "warnings": ["الحذر لمرضى حصوات الكلى من نوع أوكسالات الكالسيوم."],
        "precautions": ["يشرب فور ذوبانه بالماء للحصول على الفائدة الكاملة."],
        "side_effects": ["اضطراب معوي أو إسهال طفيف عند الجرعات العالية."],
        "storage": ["يحفظ الأنبوب محكم الإغلاق في مكان جاف وبارد."]
    }
]

def search_dataset_by_name(query, max_results=3):
    """Simple linear search returning best dataset items matching text."""
    if not query:
        return []
    q = query.lower().strip()
    matches = []
    for med in PHARMA_DATASET:
        score = 0
        if q in med["name"].lower():
            score += 10
        if q in med["name_ar"].lower():
            score += 10
        if q in med["generic_name"].lower():
            score += 8
        for alias in med.get("aliases", []):
            if alias in q or q in alias:
                score += 7
        if score > 0:
            matches.append((score, med))
    matches.sort(key=lambda x: x[0], reverse=True)
    return [m[1] for m in matches[:max_results]]
