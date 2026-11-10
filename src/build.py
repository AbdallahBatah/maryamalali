#!/usr/bin/env python3
"""Static site builder for macro by maryam: English at the root, Arabic under /ar/."""
import os, json, shutil, html
from PIL import Image

DOMAIN = "https://macrobymaryam.com"   # replace with the real domain before launch
TODAY = "2026-11-10"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public")   # the deployable website

# ---------- images: SEO file names + bilingual alt text ----------
IMGS = {
 'hero-tiger':('plain-tiger-butterfly-macro-uae',"Plain tiger butterfly (Danaus chrysippus) resting on a leafy stem, macro photograph by Emirati photographer Maryam Aalali in the UAE","فراشة النمر على غصن أخضر، صورة ماكرو للمصورة الإماراتية مريم آل علي في دولة الإمارات"),
 'jumper-eyes':('jumping-spider-eyes-macro-uae',"A jumping spider's large front eyes in extreme close-up, macro photography of UAE biodiversity by Maryam Aalali","عيون العنكبوت القافز الأمامية عن قرب شديد، تصوير ماكرو للتنوع البيولوجي في الإمارات بعدسة مريم آل علي"),
 'cuckoo-wasp':('cuckoo-wasp-macro-uae',"Metallic green cuckoo wasp on tree bark, photographed in the UAE by Emirati macro photographer Maryam Aalali","دبور الوقواق بلونه الأخضر المعدني على لحاء شجرة، صوّرته مصورة الماكرو الإماراتية مريم آل علي في الإمارات"),
 'pierrot':('pierrot-butterfly-macro-uae',"Pierrot butterfly with striped wings on a dry seed head, macro documentation of UAE insects by Maryam Aalali","فراشة البييرو بأجنحتها المخططة على نبتة جافة، توثيق ماكرو لحشرات الإمارات بعدسة مريم آل علي"),
 'lacewing':('green-lacewing-macro-uae',"Green lacewing with transparent veined wings, a beneficial insect photographed in the UAE by Maryam Aalali","أسد المنّ الأخضر بأجنحته الشفافة، حشرة نافعة من بيئة الإمارات بعدسة مريم آل علي"),
 'mantis':('conehead-mantis-macro-uae',"Conehead mantis at night with raised forelegs, UAE wildlife macro photograph by Maryam Aalali","فرس النبي المخروطي ليلاً رافعاً قائمتيه الأماميتين، صورة ماكرو للحياة البرية في الإمارات بعدسة مريم آل علي"),
 'chrysalis':('butterfly-chrysalis-macro-uae',"Butterfly chrysalis hanging from a twig, documenting the butterfly life cycle in the UAE, by Maryam Aalali","خادرة فراشة معلقة على غصن، توثيق لدورة حياة الفراشات في الإمارات بعدسة مريم آل علي"),
 'pierid':('pierid-butterfly-macro-uae',"Pierid butterfly with pale green eyes on a grass seed head, macro photograph from the UAE by Maryam Aalali","فراشة صفراء بعيون خضراء فاتحة على سنبلة عشب، صورة ماكرو من الإمارات بعدسة مريم آل علي"),
 'honeybee-feed':('honeybee-feeding-macro-uae',"Honeybee feeding with its tongue extended, close-up macro of bees in the UAE by Maryam Aalali","نحلة عسل تتغذى ولسانها ممدود، صورة ماكرو قريبة للنحل في الإمارات بعدسة مريم آل علي"),
 'jumper-leaf':('jumping-spider-leaf-macro-uae',"Small jumping spider peeking from behind a green stem, macro photograph by Emirati photographer Maryam Aalali","عنكبوت قافز صغير يطل من خلف ساق خضراء، صورة ماكرو للمصورة الإماراتية مريم آل علي"),
 'grasshopper':('grasshopper-macro-uae',"Front view of a grasshopper's face and compound eyes, macro insect photography in the UAE by Maryam Aalali","وجه جندب وعيونه المركبة من الأمام، تصوير ماكرو للحشرات في الإمارات بعدسة مريم آل علي"),
 'sand-wasp':('sand-wasp-macro-uae',"Sand wasp digging its burrow in sand, documenting insect behaviour in the UAE, by Maryam Aalali","دبور الرمل يحفر جحره في الرمال، توثيق لسلوك الحشرات في الإمارات بعدسة مريم آل علي"),
 'moth-fly':('moth-fly-macro-uae',"Moth fly with fringed, feather-like wings seen from above, macro photograph by Maryam Aalali","ذبابة العُث بأجنحتها الريشية من الأعلى، صورة ماكرو بعدسة مريم آل علي"),
 'swallowtail':('swallowtail-wing-scales-macro',"Swallowtail butterfly wing scales in extreme macro, showing colour patterns invisible to the naked eye, by Maryam Aalali","حراشف جناح فراشة ذيل السنونو بتكبير شديد تكشف ألواناً لا تراها العين المجردة، بعدسة مريم آل علي"),
 'lynx-spider':('lynx-spider-macro-uae',"Green lynx spider on dry flowers, spider macro photography from the UAE by Maryam Aalali","عنكبوت الوشق الأخضر على أزهار جافة، تصوير ماكرو للعناكب في الإمارات بعدسة مريم آل علي"),
 'digger-bee':('solitary-bee-macro-uae',"Solitary bee with green eyes resting on a stem, bee macro photograph from the UAE by Maryam Aalali","نحلة انفرادية بعيون خضراء تستريح على ساق نبتة، صورة ماكرو للنحل في الإمارات بعدسة مريم آل علي"),
 'antlion':('antlion-macro-uae',"Antlion with clubbed antennae perched on a stem, macro photograph by Emirati photographer Maryam Aalali","أسد النمل بقرون استشعار معقوفة على ساق نبتة، صورة ماكرو للمصورة الإماراتية مريم آل علي"),
 'honeybee':('honeybee-comb-macro-uae',"Honeybee standing on the honeycomb, from Maryam Aalali's bee documentation series in the UAE","نحلة عسل على أقراص الشمع، من سلسلة توثيق النحل للمصورة مريم آل علي في الإمارات"),
 'blue-wing':('butterfly-wing-scales-macro',"Iridescent blue butterfly wing scales in macro, by Maryam Aalali","حراشف جناح فراشة زرقاء متلألئة بتصوير الماكرو، بعدسة مريم آل علي"),
 'comb':('honeybees-hive-macro-uae',"Two honeybees working on the comb cells, macro photograph from Maryam Aalali's bee series","نحلتان تعملان على خلايا القرص، صورة ماكرو من سلسلة النحل لمريم آل علي"),
 'bts-portrait':('maryam-aalali-emirati-macro-photographer',"Maryam Aalali, Emirati macro photographer, smiling as she checks her camera and flash diffuser in the field","المصورة الإماراتية مريم آل علي تبتسم وهي تراجع الكاميرا وموزّع الفلاش في الميدان"),
 'bts-walk':('maryam-aalali-exploration-trip-uae',"Maryam Aalali talking with a participant during an exploration trip in the UAE countryside","مريم آل علي تتحدث مع إحدى المشاركات خلال رحلة استكشافية في طبيعة الإمارات"),
 'bts-night':('night-exploration-trip-insects-uae',"Night exploration trip in the UAE: Maryam Aalali photographs insects in the grass while participants hold torches","رحلة استكشافية ليلية في الإمارات: مريم آل علي تصوّر الحشرات بين الأعشاب والمشاركون يحملون المصابيح"),
 'bts-prints':('outdoor-macro-photography-exhibition-uae',"Macro prints of a jumping spider displayed on wooden easels at an outdoor exhibition in the UAE","مطبوعات ماكرو لعنكبوت قافز على حوامل خشبية في معرض خارجي في الإمارات"),
 'bts-crouch':('maryam-aalali-macro-fieldwork-uae',"Maryam Aalali crouching at ground level to photograph insects, documenting local UAE biodiversity","مريم آل علي تنحني قرب الأرض لتصوير الحشرات وتوثيق التنوع البيولوجي المحلي في الإمارات"),
 'bts-screen':('macro-photography-session-camera',"Camera screen and flash trigger during a macro photography session in the field","شاشة الكاميرا ومشغّل الفلاش خلال جلسة تصوير ماكرو في الميدان"),
 'bts-field':('maryam-aalali-documenting-uae-biodiversity',"Maryam Aalali walking through tall grass searching for insects to document in the UAE","مريم آل علي تسير بين الأعشاب الطويلة بحثاً عن حشرات لتوثيقها في الإمارات"),
 'bts-group':('exploration-trip-group-uae',"Participants observing shrubs for insects on a guided exploration trip in the UAE","مشاركون يراقبون الشجيرات بحثاً عن الحشرات في رحلة استكشافية بإرشاد في الإمارات"),
 'bts-forest':('woodland-exploration-trip-uae',"Small group on a guided exploration trip through a UAE woodland at dusk","مجموعة صغيرة في رحلة استكشافية بإرشاد عبر غابة في الإمارات عند الغروب"),
 'bts-hat':('nature-observation-exploration-trip',"Participant examining leaves up close during a nature exploration trip","مشارك يتأمل الأوراق عن قرب خلال رحلة استكشافية في الطبيعة"),
 'bts-exhibit':('maryam-aalali-macro-prints-exhibition-uae',"Maryam Aalali with her macro photography prints at an outdoor exhibition in the UAE","مريم آل علي مع مطبوعات صور الماكرو في معرض خارجي في الإمارات"),
 'kids-loupe':('children-nature-trip-magnifiers-uae',"Children using magnifying glasses to explore a desert plant on a children's nature trip in the UAE","أطفال يستكشفون نبتة صحراوية بالعدسات المكبّرة في رحلة أطفال تعليمية في الإمارات"),
}
DIM = {}

def prep_images():
    """Images already live in public/img (full size) and public/img/thumbs. Read their sizes for width/height attributes."""
    for k,(fn,_,_) in IMGS.items():
        DIM[k] = (Image.open(f"{OUT}/img/{fn}.jpg").size, Image.open(f"{OUT}/img/thumbs/{fn}.jpg").size)

# ---------- gallery register ----------
CATS = [('all','All','الكل','',''),
        ('butterflies','Butterflies & moths','الفراشات',"Wings, scales and a chrysalis","أجنحة وحراشف وخادرة"),
        ('bees','Bees & wasps','النحل والدبابير',"Honeybees, solitary bees, wasps","نحل العسل والنحل الانفرادي والدبابير"),
        ('spiders','Spiders','العناكب',"Jumping and lynx spiders","العناكب القافزة وعناكب الوشق"),
        ('other','Other insects','حشرات أخرى',"Mantis, lacewing, antlion and more","فرس النبي وأسد المن وأسد النمل")]
G = [
 ('jumper-eyes','spiders','Jumping spider','عنكبوت قافز','Salticidae',0),
 ('cuckoo-wasp','bees','Cuckoo wasp','دبور الوقواق','Chrysididae',0),
 ('pierrot','butterflies','Pierrot butterfly','فراشة البييرو','Lycaenidae',0),
 ('lacewing','other','Green lacewing','أسد المنّ الأخضر','Chrysopidae',0),
 ('mantis','other','Conehead mantis','فرس النبي المخروطي','Empusidae',0),
 ('chrysalis','butterflies','Chrysalis','خادرة فراشة','Lepidoptera',0),
 ('pierid','butterflies','Pierid butterfly','فراشة صفراء','Pieridae',0),
 ('honeybee-feed','bees','Honeybee feeding','نحلة عسل تتغذى','Apis',1),
 ('jumper-leaf','spiders','Jumping spider','عنكبوت قافز','Salticidae',0),
 ('grasshopper','other','Grasshopper','جندب','Orthoptera',0),
 ('hero-tiger','butterflies','Plain tiger','فراشة النمر','Danaus chrysippus',1),
 ('sand-wasp','bees','Sand wasp','دبور الرمل','Hymenoptera',0),
 ('moth-fly','other','Moth fly','ذبابة العُث','Psychodidae',0),
 ('swallowtail','butterflies','Swallowtail wing scales','حراشف جناح ذيل السنونو','Papilionidae',0),
 ('lynx-spider','spiders','Lynx spider','عنكبوت الوشق','Oxyopidae',0),
 ('digger-bee','bees','Solitary bee at rest','نحلة انفرادية تستريح','Apidae',0),
 ('antlion','other','Antlion','أسد النمل','Myrmeleontidae',0),
 ('honeybee','bees','Honeybee on the comb','نحلة على القرص','Apis',1),
 ('blue-wing','butterflies','Wing scales','حراشف الجناح','Lepidoptera',0),
 ('comb','bees','Honeybees at work','نحل في الخلية','Apis',1),
]

PROJECTS = [
 ('documentation','Macro documentation of UAE biodiversity','توثيق التنوع البيولوجي في الإمارات',"A growing visual record of local species.","سجل بصري متنامٍ للكائنات المحلية.",'pierid'),
 ('bees','Documenting the beauty of bees','توثيق جمال عالم النحل',"Honeybees and solitary bees, up close.","نحل العسل والنحل الانفرادي عن قرب.",'honeybee-feed'),
 ('trips','Exploration trips','رحلات استكشافية في عالم الماكرو',"Guided day and night walks for small groups.","جولات نهارية وليلية لمجموعات صغيرة.",'bts-forest'),
 ('kids','Children\'s trips & workshops','رحلات وورش تعليمية للأطفال',"Magnifiers, prints and first discoveries.","عدسات مكبّرة ومطبوعات واكتشافات أولى.",'kids-loupe'),
 ('exhibitions','Unseen beauty exhibitions','معارض جمال العالم الصغير',"Prints shown outdoors, where the subjects live.","مطبوعات تُعرض في الطبيعة حيث تعيش الكائنات.",'bts-prints'),
]

# ---------- page metadata ----------
PAGES = ['index','about','gallery','projects','book','faq','contact']
META = {
 'index':  {'en':("Macro by Maryam | Emirati Macro Photographer, UAE","Maryam Aalali is an Emirati macro photographer documenting UAE biodiversity: insects, spiders and bees, plus exploration trips and children's workshops."),
            'ar':("ماكرو باي مريم | مصورة ماكرو إماراتية","مريم آل علي مصورة إماراتية موهوبة توثّق التنوع البيولوجي في الإمارات بعدسة الماكرو: حشرات وعناكب ونحل، مع رحلات استكشافية وورش تعليمية للأطفال.")},
 'about':  {'en':("About Maryam Aalali | Emirati Macro Photographer","Meet Maryam Aalali, a talented Emirati photographer who turned a childhood love of insects into local documentation of UAE biodiversity."),
            'ar':("عن مريم آل علي | مصورة إماراتية موهوبة","تعرّف على مريم آل علي، مصورة إماراتية حوّلت شغف الطفولة بالحشرات إلى توثيق محلي للتنوع البيولوجي في دولة الإمارات بتصوير الماكرو.")},
 'gallery':{'en':("Macro Photography Gallery | UAE Insects & Spiders","Explore macro photographs of UAE insects, spiders, bees and butterflies by Maryam Aalali, each labelled with its common name and scientific family."),
            'ar':("معرض تصوير الماكرو | حشرات وعناكب الإمارات","صور ماكرو لحشرات وعناكب ونحل وفراشات من دولة الإمارات بعدسة مريم آل علي، لكل صورة اسمها الشائع وعائلتها العلمية.")},
 'projects':{'en':("Exploration Trips & Kids Photography Workshops, UAE","Biodiversity documentation, bee photography, exploration trips, children's photography workshops and outdoor macro exhibitions in the UAE."),
            'ar':("رحلات استكشافية وورش تعليمية للتصوير | المشاريع","توثيق التنوع البيولوجي، رحلات استكشافية نهارية وليلية، رحلات أطفال وورش تعليمية للتصوير، ومعارض ماكرو في الهواء الطلق في الإمارات.")},
 'book':   {'en':("Book a Macro Walk or Kids Trip | Calendar, UAE","Check available dates and book a macro exploration trip, night walk or children's trip with Emirati photographer Maryam Aalali in the UAE."),
            'ar':("احجز رحلة استكشافية أو رحلة أطفال | التقويم","اطّلع على المواعيد المتاحة واحجز رحلة ماكرو استكشافية أو جولة ليلية أو رحلة أطفال مع المصورة الإماراتية مريم آل علي في الإمارات.")},
 'faq':    {'en':("FAQ | Macro Trips & Photography Workshops in the UAE","Answers about Maryam Aalali's exploration trips, children's trips, educational photography workshops, macro prints and how to book in the UAE."),
            'ar':("الأسئلة الشائعة | رحلات الأطفال وورش التصوير","إجابات عن الرحلات الاستكشافية ورحلات الأطفال والورش التعليمية للتصوير وشراء المطبوعات والحجز مع المصورة الإماراتية مريم آل علي.")},
 'contact':{'en':("Contact Maryam Aalali | Book a Trip or Workshop","Book an exploration trip, a children's workshop, an exhibition or a print with Emirati macro photographer Maryam Aalali. Email, WhatsApp and Instagram."),
            'ar':("تواصل مع مريم آل علي | احجز رحلة أو ورشة","احجز رحلة استكشافية أو ورشة تعليمية للأطفال أو معرضاً أو مطبوعة مع مصورة الماكرو الإماراتية مريم آل علي عبر البريد أو واتساب أو إنستغرام.")},
}
NAV_NAME = {'index':("Home","الرئيسية"),'about':("About Maryam","عن مريم"),'gallery':("Gallery","المعرض"),
            'projects':("Projects","المشاريع"),'book':("Book a trip","احجز رحلة"),'faq':("FAQ","الأسئلة الشائعة"),'contact':("Contact","تواصل")}

# ---------- FAQ content (shared by page, schema and llms.txt) ----------
FAQ = [
 ("About Maryam and macro photography","عن مريم وتصوير الماكرو",[
  ("Who is Maryam Aalali?","من هي مريم آل علي؟",
   "Maryam Aalali is a talented Emirati macro photographer who documents the biodiversity of the UAE. She photographs insects, spiders and other small creatures in their own habitat, and shares that work through exhibitions, exploration trips and educational workshops.",
   "مريم آل علي مصورة إماراتية موهوبة متخصصة في تصوير الماكرو، توثّق التنوع البيولوجي في دولة الإمارات. تصوّر الحشرات والعناكب والكائنات الصغيرة في بيئتها الطبيعية، وتشارك أعمالها من خلال المعارض والرحلات الاستكشافية والورش التعليمية."),
  ("What is macro photography?","ما هو تصوير الماكرو؟",
   "Macro photography captures very small subjects at life size or larger, so details the eye cannot see become visible: the scales on a butterfly wing, the eyes of a jumping spider, the hairs on a bee.",
   "تصوير الماكرو هو تصوير الأشياء الصغيرة جداً بحجمها الحقيقي أو أكبر، لتظهر تفاصيل لا تراها العين المجردة: حراشف جناح الفراشة، وعيون العنكبوت القافز، وشعيرات النحلة."),
  ("Which insects and creatures does Maryam photograph in the UAE?","ما الحشرات والكائنات التي تصوّرها مريم في الإمارات؟",
   "Her gallery includes butterflies and moths, honeybees and solitary bees, wasps, jumping and lynx spiders, mantises, lacewings, grasshoppers and antlions, all photographed in the UAE.",
   "يضم معرضها الفراشات والعث، ونحل العسل والنحل الانفرادي، والدبابير، والعناكب القافزة وعناكب الوشق، وفرس النبي، وأسد المنّ، والجنادب، وأسد النمل، وجميعها مصوّرة في دولة الإمارات."),
  ("Why does local documentation of biodiversity matter?","لماذا يهم التوثيق المحلي للتنوع البيولوجي؟",
   "Small creatures pollinate plants, recycle nutrients and feed other wildlife, yet they are rarely noticed or recorded. Documenting them locally builds a visual record of UAE nature and helps people value what lives around them.",
   "تلقّح الكائنات الصغيرة النباتات وتعيد تدوير العناصر الغذائية وتشكّل غذاءً لكائنات أخرى، ومع ذلك نادراً ما تُلاحظ أو تُوثّق. التوثيق المحلي يبني سجلاً بصرياً لطبيعة الإمارات ويساعد الناس على تقدير ما يعيش من حولهم."),
 ]),
 ("Trips and workshops","الرحلات والورش",[
  ("What happens on an exploration trip?","ماذا يحدث في الرحلة الاستكشافية؟",
   "Exploration trips are guided walks for small groups. Maryam shows participants how to find, observe and photograph insects and spiders. Day trips focus on habitat and patience; night trips use torches and diffused flash to find species that appear after dark.",
   "الرحلات الاستكشافية جولات بإرشاد لمجموعات صغيرة، تعلّم فيها مريم المشاركين كيف يجدون الحشرات والعناكب ويراقبونها ويصوّرونها. تركّز الرحلات النهارية على البيئة والصبر، وتستعين الرحلات الليلية بالمصابيح والفلاش الموزّع لاكتشاف كائنات لا تظهر إلا بعد حلول الظلام."),
  ("Do you organise trips for children?","هل تنظّمين رحلات للأطفال؟",
   "Yes. Children's trips and workshops introduce young explorers to nature with magnifying glasses, printed macro photographs and simple field observation. Schools and families can book a session through the contact page.",
   "نعم. رحلات الأطفال والورش التعليمية تعرّف المستكشفين الصغار بالطبيعة باستخدام العدسات المكبّرة وصور الماكرو المطبوعة والملاحظة الميدانية البسيطة. يمكن للمدارس والعائلات حجز جلسة عبر صفحة التواصل."),
  ("Do you offer educational photography workshops?","هل تقدّمين ورشاً تعليمية للتصوير؟",
   "Yes. Workshops cover how to observe small subjects, approach them without disturbing them, and photograph them with care. Content is adapted to the group, from children to adults.",
   "نعم. تتناول الورش التعليمية للتصوير كيفية ملاحظة الكائنات الصغيرة والاقتراب منها دون إزعاجها وتصويرها بعناية، ويُكيَّف المحتوى حسب المجموعة، من الأطفال إلى الكبار."),
  ("Do I need a professional camera to join?","هل أحتاج إلى كاميرا احترافية للمشاركة؟",
   "Children's sessions use magnifiers and printed photographs, so no camera is needed. For photography-focused trips, ask about equipment when you book and Maryam will advise.",
   "لا تحتاج جلسات الأطفال إلى كاميرا، إذ تُستخدم العدسات المكبّرة والصور المطبوعة. أما الرحلات المخصصة للتصوير، فاسأل عن المعدات عند الحجز وستقدّم لك مريم النصيحة."),
  ("Where do the trips take place?","أين تُقام الرحلات؟",
   "Trips take place in natural areas in the UAE, from woodland to desert. The meeting point is confirmed for each trip when you book.",
   "تُقام الرحلات في مناطق طبيعية داخل دولة الإمارات، من الغابات إلى الصحراء، ويُؤكَّد مكان اللقاء لكل رحلة عند الحجز."),
 ]),
 ("Prints, exhibitions and booking","المطبوعات والمعارض والحجز",[
  ("Can I buy prints of Maryam's photographs?","هل يمكنني شراء مطبوعات من صور مريم؟",
   "Yes. Select a photograph from the gallery and send an inquiry with its catalogue number, for example No. 01.",
   "نعم. اختر صورة من المعرض وأرسل استفساراً يتضمن رقمها، مثل رقم 01."),
  ("Can Maryam exhibit at our school, venue or event?","هل يمكن لمريم إقامة معرض في مدرستنا أو مكاننا أو فعاليتنا؟",
   "Yes. Her outdoor print displays work well in schools, parks, cultural venues and community events. Share your dates and space in an inquiry.",
   "نعم. تناسب معارضها الخارجية المدارس والحدائق والمراكز الثقافية والفعاليات المجتمعية. شارك التواريخ وطبيعة المكان في استفسارك."),
  ("How do I book a trip or workshop?","كيف أحجز رحلة أو ورشة؟",
   "Open the Book a trip page, choose an available date in the calendar, transfer the fee and upload the receipt with your details. For private groups or schools, use the contact page or WhatsApp +971 52 913 7373.",
   "افتح صفحة احجز رحلة، واختر موعداً متاحاً من التقويم، ثم حوّل الرسوم وارفع الإيصال مع بياناتك. للمجموعات الخاصة والمدارس، استخدم صفحة التواصل أو واتساب ‎+971 52 913 7373‎."),
 ]),
]

# ---------- helpers ----------
def T(L, en, ar): return en if L=='en' else ar
def esc(s): return html.escape(s, quote=True)
def href(L, page, frm='same'):
    return f"{page}.html"
def url(L, page):
    p = '' if page=='index' else f"{page}.html"
    return f"{DOMAIN}/{'ar/' if L=='ar' else ''}{p}"
def img(k, A): return f"{A}img/{IMGS[k][0]}.jpg"
def th(k, A): return f"{A}img/thumbs/{IMGS[k][0]}.jpg"
def alt(k, L): return esc(IMGS[k][1] if L=='en' else IMGS[k][2])
def tag_img(k, L, A, thumb=True, cls='', lazy=True, extra=''):
    (fw,fh),(tw,tht) = DIM[k]
    w,h = (tw,tht) if thumb else (fw,fh)
    src = th(k,A) if thumb else img(k,A)
    c = f' class="{cls}"' if cls else ''
    ld = ' loading="lazy" decoding="async"' if lazy else ''
    return f'<img{c} src="{src}" width="{w}" height="{h}" alt="{alt(k,L)}"{ld}{extra}>'

def label(L, i):
    k,c,en,ar,tx,it = G[i]; no=f"{i+1:02d}"
    return (f'<span class="no">{T(L,"No. ","رقم ")}{no}</span><span class="nm">{T(L,en,ar)}</span>'
            f'<span class="tx{" it" if it else ""}">{tx}</span>')

CHEV = '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>'

def header(L, page, A):
    other = ('ar/' if L=='en' else '../') + ('index' if page=='index' else page) + '.html'
    cur = lambda p: ' aria-current="page"' if p==page else ''
    gcount = {c[0]: sum(1 for g in G if g[1]==c[0]) for c in CATS}
    mm_about = f'''
      <div class="mm" id="mm-about"><div class="wrap mm-in">
        <div class="mm-intro"><p class="eyebrow">{T(L,"About Maryam","عن مريم")}</p><p class="mm-lede">{T(L,"An Emirati macro photographer documenting UAE biodiversity.","مصورة ماكرو إماراتية توثّق التنوع البيولوجي في الإمارات.")}</p><a class="tlink" href="about.html">{T(L,"Meet Maryam","تعرّف على مريم")} <span class="arrow">→</span></a></div>
        <ul class="mm-links">
          <li><a href="about.html#story"><b>{T(L,"My story","قصتي")}</b><small>{T(L,"From a garden curiosity to local documentation","من فضول في حديقة البيت إلى التوثيق المحلي")}</small></a></li>
          <li><a href="about.html#practice"><b>{T(L,"What I do","ما أقوم به")}</b><small>{T(L,"Documentation, trips, workshops, exhibitions","توثيق ورحلات وورش ومعارض")}</small></a></li>
          <li><a href="about.html#lens"><b>{T(L,"Behind the lens","خلف العدسة")}</b><small>{T(L,"Fieldwork from first light to after dark","العمل الميداني من أول ضوء حتى ما بعد الظلام")}</small></a></li>
          <li><a href="faq.html"><b>{T(L,"Questions","أسئلة شائعة")}</b><small>{T(L,"Macro photography, trips and booking","تصوير الماكرو والرحلات والحجز")}</small></a></li>
        </ul>
        <a class="mm-feat" href="about.html">{tag_img('bts-portrait',L,A)}<span class="label"><span class="nm">{T(L,"Maryam Aalali in the field","مريم آل علي في الميدان")}</span></span></a>
      </div></div>'''
    cats = ''.join(f'<li><a href="gallery.html#{c[0]}"><b>{T(L,c[1],c[2])}<sup>{gcount[c[0]]}</sup></b><small>{T(L,c[3],c[4])}</small></a></li>' for c in CATS[1:])
    mm_gal = f'''
      <div class="mm" id="mm-gallery"><div class="wrap mm-in">
        <div class="mm-intro"><p class="eyebrow">{T(L,"Gallery","المعرض")}</p><p class="mm-lede">{T(L,f"{len(G)} macro photographs of UAE insects and spiders.",f"{len(G)} صورة ماكرو لحشرات وعناكب الإمارات.")}</p><a class="tlink" href="gallery.html">{T(L,"View all","عرض الكل")} <span class="arrow">→</span></a></div>
        <ul class="mm-links">{cats}</ul>
        <a class="mm-feat" href="gallery.html#spiders">{tag_img('jumper-eyes',L,A)}<span class="label">{label(L,0)}</span></a>
      </div></div>'''
    projs = ''.join(f'<li><a href="projects.html#{p[0]}"><b>{T(L,p[1],p[2])}</b><small>{T(L,p[3],p[4])}</small></a></li>' for p in PROJECTS)
    mm_proj = f'''
      <div class="mm" id="mm-projects"><div class="wrap mm-in">
        <div class="mm-intro"><p class="eyebrow">{T(L,"Projects","المشاريع")}</p><p class="mm-lede">{T(L,"Exploration trips, children's workshops and exhibitions across the UAE.","رحلات استكشافية وورش للأطفال ومعارض في أنحاء الإمارات.")}</p><a class="tlink" href="book.html">{T(L,"See available dates","المواعيد المتاحة")} <span class="arrow">→</span></a></div>
        <ul class="mm-links">{projs}</ul>
        <a class="mm-feat" href="projects.html#trips">{tag_img('bts-night',L,A)}<span class="label"><span class="nm">{T(L,"Night exploration trip","رحلة استكشافية ليلية")}</span></span></a>
      </div></div>'''
    def mmli(p, panel):
        return (f'<li class="has-mm"><a href="{p}.html"{cur(p)}>{T(L,*NAV_NAME[p])}</a>'
                f'<button class="mm-t" type="button" aria-expanded="false" aria-controls="mm-{p}" aria-label="{T(L,"Show "+NAV_NAME[p][0]+" menu","إظهار قائمة "+NAV_NAME[p][1])}">{CHEV}</button>{panel}</li>')
    return f'''<header class="bar">
  <div class="wrap bar-in">
    <a class="brand" href="index.html" aria-label="{T(L,"macro by maryam, home","ماكرو باي مريم، الصفحة الرئيسية")}"><span class="mark" aria-hidden="true"></span><span class="word">macro by maryam</span></a>
    <nav class="nav" id="nav" aria-label="{T(L,"Main","القائمة الرئيسية")}">
      <ul class="menu">
        <li><a href="index.html"{cur('index')}>{T(L,*NAV_NAME['index'])}</a></li>
        {mmli('about',mm_about)}
        {mmli('gallery',mm_gal)}
        {mmli('projects',mm_proj)}
        <li><a href="faq.html"{cur('faq')}>{T(L,*NAV_NAME['faq'])}</a></li>
        <li><a href="contact.html"{cur('contact')}>{T(L,*NAV_NAME['contact'])}</a></li>
        <li class="cta-li"><a class="nav-cta" href="book.html"{cur('book')}>{T(L,*NAV_NAME['book'])}</a></li>
      </ul>
    </nav>
    <a class="lang" href="{other}" hreflang="{T(L,'ar','en')}" lang="{T(L,'ar','en')}">{T(L,"عربي","English")}</a>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="nav">{T(L,"Menu","القائمة")}</button>
  </div>
</header>'''

def footer(L, page, A):
    other = ('ar/' if L=='en' else '../') + page + '.html'
    pages = ''.join(f'<li><a href="{p}.html">{T(L,*NAV_NAME[p])}</a></li>' for p in PAGES)
    projs = ''.join(f'<li><a href="projects.html#{p[0]}">{T(L,p[1],p[2])}</a></li>' for p in PROJECTS)
    cats = ''.join(f'<li><a href="gallery.html#{c[0]}">{T(L,c[1],c[2])}</a></li>' for c in CATS[1:])
    return f'''<footer>
  <div class="wrap">
    <div class="fgrid">
      <div class="fbrand">
        <span class="mark" aria-hidden="true"></span>
        <p style="font:400 1.1rem/1 var(--f-mark)">macro by maryam</p>
        <p class="tag">{T(L,"small details. extraordinary worlds.","تفاصيل صغيرة، عالم استثنائي.")}</p>
        <p class="d">{T(L,"Maryam Aalali is an Emirati macro photographer documenting insects, spiders and the biodiversity of the UAE, with exploration trips, children's trips and educational photography workshops.","مريم آل علي مصورة ماكرو إماراتية توثّق الحشرات والعناكب والتنوع البيولوجي في دولة الإمارات، وتقدّم رحلات استكشافية ورحلات للأطفال وورشاً تعليمية للتصوير.")}</p>
      </div>
      <nav class="fcol" aria-label="{T(L,"Site pages","صفحات الموقع")}"><p class="fh">{T(L,"Pages","الصفحات")}</p><ul>{pages}<li><a href="{other}" hreflang="{T(L,'ar','en')}" lang="{T(L,'ar','en')}">{T(L,"النسخة العربية","English version")}</a></li></ul></nav>
      <nav class="fcol" aria-label="{T(L,"Projects","المشاريع")}"><p class="fh">{T(L,"Projects","المشاريع")}</p><ul>{projs}</ul></nav>
      <nav class="fcol" aria-label="{T(L,"Gallery","المعرض")}"><p class="fh">{T(L,"Gallery","المعرض")}</p><ul>{cats}</ul></nav>
      <div class="fcol"><p class="fh">{T(L,"Contact","تواصل")}</p><ul>
        <li><a class="ltr" href="mailto:maryamaalali@live.com">maryamaalali@live.com</a></li>
        <li><a class="ltr" href="https://wa.me/971529137373" target="_blank" rel="noopener">+971 52 913 7373</a></li>
        <li><a class="ltr" href="https://www.instagram.com/macrobymaryam/" target="_blank" rel="noopener">@macrobymaryam</a></li>
        <li>{T(L,"United Arab Emirates","دولة الإمارات العربية المتحدة")}</li></ul></div>
    </div>
    <div class="fine">
      <span>© 2026 Maryam Aalali · {T(L,"All photographs protected","جميع الصور محفوظة الحقوق")}</span>
      <span><a href="{A}sitemap.xml">{T(L,"Sitemap","خريطة الموقع")}</a> · <a href="{A}admin.html" rel="nofollow">{T(L,"Admin","الإدارة")}</a> · {T(L,"Brand identity by Ola Allouz","الهوية البصرية: علا علّوز")}</span>
    </div>
  </div>
</footer>'''

LIGHTBOX = lambda L: f'''<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="{T(L,"Photograph viewer","عارض الصور")}">
  <div class="lb-top"><span id="lbCount"></span><button class="lb-x" id="lbClose" type="button">{T(L,"Close ✕","إغلاق ✕")}</button></div>
  <div class="lb-stage" id="lbStage"><img id="lbImg" alt="">
    <button class="lb-nav lb-prev" id="lbPrev" type="button" aria-label="{T(L,"Previous photograph","الصورة السابقة")}"><span>←</span></button>
    <button class="lb-nav lb-next" id="lbNext" type="button" aria-label="{T(L,"Next photograph","الصورة التالية")}"><span>→</span></button></div>
  <div class="label" id="lbLabel"></div>
</div>'''

def crumbs(L, page):
    return (f'<nav aria-label="{T(L,"Breadcrumb","مسار التنقل")}"><ol class="crumbs"><li><a href="index.html">{T(L,*NAV_NAME["index"])}</a></li>'
            f'<li aria-current="page">{T(L,*NAV_NAME[page])}</li></ol></nav>')

def work_fig(L, A, i, cls, big):
    k=G[i][0]; (fw,fh),_=DIM[k]
    return (f'<figure class="work {cls}" style="--ar:{fw}/{fh}"><button class="lb-open" type="button" data-full="{img(k,A)}" aria-label="{T(L,"View photograph: ","عرض الصورة: ")}{T(L,G[i][2],G[i][3])}">'
            f'{tag_img(k,L,A,thumb=not big)}</button><figcaption class="label">{label(L,i)}</figcaption></figure>')

# ---------- pages ----------
def p_index(L, A):
    gi = {g[0]:i for i,g in enumerate(G)}
    works = ''.join(work_fig(L,A,gi[k],c,b) for k,c,b in [('jumper-eyes','w-a r1',1),('cuckoo-wasp','w-b r1',0),('mantis','w-c r2',1),('lacewing','w-d r2',0),('chrysalis','w-e r2',0)])
    rows = ''.join(f'<a class="row" href="projects.html#{p[0]}"><h3>{T(L,p[1],p[2])}</h3><p>{T(L,p[3],p[4])}</p>{tag_img(p[5],L,A,cls="thumb")}</a>' for p in PROJECTS)
    faqs = [FAQ[1][2][1], FAQ[1][2][2], FAQ[1][2][0]]
    teaser = ''.join(f'<a href="faq.html"><span>{T(L,q[0],q[1])}</span><span class="arrow">→</span></a>' for q in faqs)
    (hw,hh),_ = DIM['hero-tiger']
    return f'''
<div class="hero">
  <div class="hero-media" id="stage">
    <img id="heroImg" src="{img('hero-tiger',A)}" width="{hw}" height="{hh}" alt="{alt('hero-tiger',L)}" fetchpriority="high">
    <div class="hero-shade"></div>
    <div class="lens" id="lens" aria-hidden="true">
      <svg viewBox="0 0 230 230" fill="none" stroke="rgba(246,243,237,.55)" stroke-width="1"><line x1="70" y1="160" x2="160" y2="160"/><line x1="70" y1="152" x2="70" y2="160"/><line x1="79" y1="156" x2="79" y2="160"/><line x1="88" y1="156" x2="88" y2="160"/><line x1="97" y1="156" x2="97" y2="160"/><line x1="106" y1="156" x2="106" y2="160"/><line x1="115" y1="150" x2="115" y2="160"/><line x1="124" y1="156" x2="124" y2="160"/><line x1="133" y1="156" x2="133" y2="160"/><line x1="142" y1="156" x2="142" y2="160"/><line x1="151" y1="156" x2="151" y2="160"/><line x1="160" y1="152" x2="160" y2="160"/><line x1="115" y1="103" x2="115" y2="127"/><line x1="103" y1="115" x2="127" y2="115"/></svg>
      <b>×2.5</b>
    </div>
    <p class="hint"><i></i>{T(L,"Loupe ×2.5 · move across the wing","عدسة مكبّرة ×2.5 · مرّر فوق الجناح")}</p>
  </div>
  <div class="hero-copy"><div class="wrap"><div class="inner">
    <h1><span class="kicker">{T(L,"Emirati macro photographer · UAE biodiversity","مصورة ماكرو إماراتية · التنوع البيولوجي في الإمارات")}</span>{T(L,"See what<br><em>I</em> see.","ما لا تراه<br>العيون")}</h1>
    <p class="sub">{T(L,"I photograph the insects, spiders and small lives of the UAE, close enough to see what the eye usually misses.","أوثّق الحشرات والعناكب والكائنات الصغيرة في دولة الإمارات، عن قرب يكشف ما يفوت العين عادةً.")}</p>
    <div class="ctas">
      <a class="btn solid" href="gallery.html">{T(L,"View the gallery","استعرض المعرض")} <span class="arrow">→</span></a>
      <a class="btn" href="book.html">{T(L,"Book a trip","احجز رحلة")}</a>
    </div>
  </div></div></div>
</div>

<section class="band paper">
  <div class="wrap intro-grid">
    <div style="display:grid;gap:1.6rem;min-width:0">
      <p class="eyebrow">Maryam Aalali · <span lang="ar">مريم آل علي</span></p>
      <h2 class="statement">{T(L,"Every small creature has a role in our ecosystem, and <em>a story worth preserving.</em>","كل مخلوق، مهما كان صغيراً، يحمل قيمة ودوراً في <em>توازن بيئتنا.</em>")}</h2>
    </div>
    <div class="intro-aside">
      <p>{T(L,"I'm an Emirati photographer documenting the biodiversity of the UAE. Through macro photography I explore tiny worlds and hidden details that often go unnoticed, and share them through exhibitions, exploration trips and educational workshops.","مصوّرة إماراتية تهتم بتوثيق التنوع البيولوجي في دولتنا. أقترب من العالم الصغير بعدسة الماكرو، وأبحث عن التفاصيل التي لا تُرى بالعين المجردة، وأشاركها عبر المعارض والرحلات الاستكشافية والورش التعليمية.")}</p>
      <a class="tlink" href="about.html#story">{T(L,"Read my story","اقرأ قصتي")} <span class="arrow">→</span></a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head">
      <div class="titles">
        <p class="eyebrow">{T(L,"Macro documentation of UAE biodiversity","توثيق التنوع البيولوجي في الإمارات")}</p>
        <h2>{T(L,"Selected works","أعمال مختارة")}</h2>
      </div>
      <a class="tlink" href="gallery.html">{T(L,f"Full gallery · {len(G)} photographs",f"المعرض الكامل · {len(G)} صورة")} <span class="arrow">→</span></a>
    </div>
    <div class="works">{works}</div>
  </div>
</section>

<section class="band surface">
  <div class="wrap">
    <div class="head">
      <div class="titles">
        <p class="eyebrow">{T(L,"In the field","في الميدان")}</p>
        <h2>{T(L,"Projects","المشاريع")}</h2>
      </div>
      <p class="muted" style="max-width:28em">{T(L,"Local documentation, exploration trips, children's trips, educational photography workshops and outdoor exhibitions.","توثيق محلي، رحلات استكشافية، رحلات أطفال، ورش تعليمية للتصوير ومعارض في الهواء الطلق.")}</p>
    </div>
    <div class="rows">{rows}</div>
  </div>
</section>

<section class="night">
  {tag_img('bts-night',L,A,thumb=False)}
  <div class="cap"><div class="wrap"><p>{T(L,"The work happens close to the ground, from first light until long after dark.","يبدأ العمل قريباً من الأرض، من أول ضوء حتى ما بعد حلول الظلام بوقت طويل.")}</p></div></div>
</section>

<section class="band paper">
  <div class="wrap cta-grid" style="align-items:start">
    <div style="display:grid;gap:1.4rem;min-width:0">
      <p class="eyebrow">{T(L,"Questions","أسئلة شائعة")}</p>
      <h2 style="font-size:var(--s-h2)">{T(L,"Planning a trip or a workshop?","تخطّط لرحلة أو ورشة؟")}</h2>
      <a class="tlink" href="faq.html">{T(L,"All questions","جميع الأسئلة")} <span class="arrow">→</span></a>
    </div>
    <div class="faq-teaser">{teaser}</div>
  </div>
</section>

<section class="band">
  <div class="wrap cta-grid">
    <div style="display:grid;gap:1.4rem;min-width:0">
      <p class="eyebrow">{T(L,"Work with Maryam","تعاون معي")}</p>
      <h2>{T(L,"Prints, exhibitions, field trips and workshops.","مطبوعات، معارض، رحلات استكشافية وورش عمل.")}</h2>
    </div>
    <div style="display:grid;gap:1.4rem;justify-items:start;min-width:0">
      <p class="muted">{T(L,"For schools, museums, nature organisations and brands looking for a closer view of UAE nature.","للمدارس والمتاحف والجهات المعنية بالطبيعة والعلامات التجارية الباحثة عن نظرة أقرب إلى طبيعة الإمارات.")}</p>
      <p class="mailbig">maryamaalali@live.com</p>
      <a class="btn" href="contact.html">{T(L,"Start an inquiry","أرسل استفسارك")} <span class="arrow">→</span></a>
    </div>
  </div>
</section>'''

def p_about(L, A):
    strip = ''.join(tag_img(k,L,A) for k in ['bts-crouch','bts-screen','bts-hat','bts-exhibit'])
    practice = [
      ('projects.html#documentation',"Documentation","التوثيق","Photographing UAE species in their own habitat to build a visual record of local biodiversity.","تصوير الكائنات في بيئتها الطبيعية لبناء سجل بصري للتنوع البيولوجي المحلي."),
      ('projects.html#trips',"Exploration trips","الرحلات الاستكشافية","Guided day and night walks into the macro world for small groups.","جولات نهارية وليلية بإرشاد لمجموعات صغيرة في عالم الماكرو."),
      ('projects.html#kids',"Children's trips & workshops","رحلات وورش الأطفال","Educational sessions that turn curiosity into care for nature.","جلسات تعليمية تحوّل الفضول إلى اهتمام بالطبيعة."),
      ('projects.html#exhibitions',"Exhibitions & prints","المعارض والمطبوعات","Fine prints and outdoor displays of the unseen details of UAE nature.","مطبوعات فنية ومعارض خارجية تكشف تفاصيل الطبيعة الإماراتية الخفية."),
    ]
    pr = ''.join(f'<a href="{h}"><h3>{T(L,a,b)}</h3><p>{T(L,c,d)}</p></a>' for h,a,b,c,d in practice)
    return f'''
<section class="band paper" style="padding-top:clamp(2.5rem,5vw,4rem)">
  <div class="wrap" style="display:grid;gap:clamp(2rem,4vw,3.5rem)">
    {crumbs(L,'about')}
    <div class="about-top">
      <figure>
        {tag_img('bts-portrait',L,A,thumb=False,lazy=False)}
        <figcaption class="figcap">{T(L,"In the field, checking the frame","في الميدان، أراجع اللقطة")}</figcaption>
      </figure>
      <div class="who">
        <div class="namepair">
          <h1><span class="kicker" style="color:var(--sage)">{T(L,"About · Emirati macro photographer","عن مريم · مصورة ماكرو إماراتية")}</span>{T(L,"Maryam Aalali","مريم آل علي")}</h1>
          <span class="other" lang="{T(L,'ar','en')}">{T(L,"مريم آل علي","Maryam Aalali")}</span>
        </div>
        <p class="lead">{T(L,"An Emirati dedicated to documenting the biodiversity of the UAE. Through my lens, I explore the tiny worlds and hidden details that often go unnoticed.","مصوّرة إماراتية تهتم بتوثيق التنوع البيولوجي في دولتنا. أقترب من العالم الصغير بعدستي، وأبحث عن التفاصيل التي لا تُرى بالعين المجردة.")}</p>
        <p class="muted">{T(L,"I believe every small creature has a role in our ecosystem and a story worth preserving. My work aims to highlight the beauty of our local nature and share it with others.","أؤمن أن كل مخلوق مهما كان صغيراً يحمل قيمة ودوراً في توازن بيئتنا. ما أقوم بتوثيقه هو محاولة لحفظ جمال الطبيعة في الإمارات ومشاركته مع الآخرين.")}</p>
      </div>
    </div>
  </div>
</section>

<section class="band" id="story">
  <div class="wrap story">
    <div class="imgs">{tag_img('bts-field',L,A,thumb=False)}</div>
    <div class="txt">
      <p class="eyebrow">{T(L,"My story","قصتي")}</p>
      <h2>{T(L,"A garden curiosity that became local documentation.","فضول بدأ في حديقة البيت وأصبح توثيقاً محلياً.")}</h2>
      <p>{T(L,"I grew up watching insects in our home gardens, a small curiosity that grew into a deep passion. Today, as an Emirati documenting biodiversity, I find myself returning to the tiny world I loved as a child.","كبرت وأنا أراقب الحشرات في حديقة البيت… فضول بسيط تحوّل مع الوقت إلى شغف عميق. واليوم، كإماراتية تهتم بتوثيق التنوع البيولوجي، أعود للعالم الصغير الذي أحببته منذ الطفولة.")}</p>
      <p>{T(L,"With every image, I learn something new about our rich environment and the life hidden within it.","ألتقط ما لا تراه العيون، وأتعلّم مع كل صورة شيئاً جديداً عن بيئتنا في دولة الإمارات.")}</p>
      <p class="pull">{T(L,"My macro journey is a journey of calm, reflection, and a desire to preserve the beauty of nature in my country.","رحلتي مع الماكرو هي رحلة هدوء وتأمل… وتوثيق جمال الطبيعة في دولتنا.")}</p>
    </div>
  </div>
</section>

<section class="band paper" id="practice">
  <div class="wrap">
    <div class="head"><div class="titles">
      <p class="eyebrow">{T(L,"What I do","ما أقوم به")}</p>
      <h2>{T(L,"There's lots of magic in the tiny world.","اكتشف جمال العالم الصغير.")}</h2>
    </div></div>
    <div class="practice">{pr}</div>
  </div>
</section>

<section class="band" id="lens">
  <div class="wrap">
    <div class="head"><div class="titles">
      <p class="eyebrow">{T(L,"Behind the lens","خلف العدسة")}</p>
      <h2>{T(L,"Fieldwork in the UAE","العمل الميداني في الإمارات")}</h2>
    </div></div>
    <div class="strip">{strip}</div>
  </div>
</section>'''

def p_gallery(L, A):
    counts = {c[0]: (len(G) if c[0]=='all' else sum(1 for g in G if g[1]==c[0])) for c in CATS}
    fl = ''.join(f'<button type="button" data-f="{c[0]}" aria-pressed="{"true" if c[0]=="all" else "false"}">{T(L,c[1],c[2])}<sup>{counts[c[0]]}</sup></button>' for c in CATS)
    items = ''.join(
        f'<figure class="g-item" data-cat="{g[1]}"><button class="lb-open" type="button" data-full="{img(g[0],A)}" aria-label="{T(L,"View photograph: ","عرض الصورة: ")}{T(L,g[2],g[3])}">{tag_img(g[0],L,A)}</button><figcaption class="label">{label(L,i)}</figcaption></figure>'
        for i,g in enumerate(G))
    return f'''
<div class="wrap">
  <div class="phead">
    {crumbs(L,'gallery')}
    <h1><span class="kicker">{T(L,"Macro documentation of UAE biodiversity","توثيق التنوع البيولوجي في الإمارات")}</span>{T(L,"Macro photography gallery","معرض تصوير الماكرو")}</h1>
    <p class="lead muted">{T(L,"Insects, spiders, bees and butterflies photographed in the UAE. Each photograph is labelled the way a specimen would be: a catalogue number, a common name and the scientific group it belongs to.","حشرات وعناكب ونحل وفراشات مصوّرة في دولة الإمارات. كل صورة موسومة كما تُوسم العيّنات: رقم، واسم شائع، والمجموعة العلمية التي ينتمي إليها الكائن.")}</p>
  </div>
  <div class="filters" id="filters" role="group" aria-label="{T(L,"Filter photographs","تصفية الصور")}">{fl}</div>
  <div class="masonry" id="masonry">{items}</div>
  <p class="seo-intro" style="padding-block:1rem 4rem">{T(L,"This gallery is part of Maryam Aalali's ongoing local documentation of biodiversity in the United Arab Emirates. To buy a print, quote the catalogue number in your inquiry.","هذا المعرض جزء من التوثيق المحلي المستمر الذي تقوم به مريم آل علي للتنوع البيولوجي في دولة الإمارات العربية المتحدة. لشراء مطبوعة، اذكر رقم الصورة في استفسارك.")} <a href="contact.html" style="color:var(--sand)">{T(L,"Send an inquiry","أرسل استفساراً")}</a></p>
</div>'''

def p_projects(L, A):
    def fmt(*pairs): return '<div class="fmt">'+''.join(f'<span>{T(L,a,b)}</span>' for a,b in pairs)+'</div>'
    def col(ks, two=False):
        cls = ['c1','c2','c3'] if not two else ['c2','c3']
        return f'<div class="collage{" two" if two else ""}">' + ''.join(tag_img(k,L,A,thumb=(c!='c1' and not two),cls=c) for k,c in zip(ks,cls)) + '</div>'
    arts = [
     ('documentation',False,("Photographic series","سلسلة تصوير"),PROJECTS[0],
      ("A growing photographic record of the insects, spiders and other small creatures that live across the UAE, from garden plants to desert scrub. Each image shows a species in its own habitat, at a scale the eye usually misses. This local documentation turns the country's biodiversity into a visual archive anyone can explore.",
       "سجل فوتوغرافي متنامٍ للحشرات والعناكب والكائنات الصغيرة التي تعيش في أنحاء الإمارات، من نباتات الحدائق إلى شجيرات الصحراء. كل صورة تُظهر الكائن في بيئته الطبيعية، وبمقياس لا تلحظه العين عادةً. هذا التوثيق المحلي يحوّل التنوع البيولوجي في الدولة إلى أرشيف بصري متاح للجميع."),
      fmt(("Field photography","تصوير ميداني"),("Species records","سجلات الكائنات")), col(['mantis','pierid','lynx-spider']),
      f'<a class="tlink" href="gallery.html">{T(L,"See the gallery","شاهد المعرض")} <span class="arrow">→</span></a>'),
     ('bees',True,("Photographic series","سلسلة تصوير"),PROJECTS[1],
      ("A close study of bees: honeybees at work on the comb and feeding, and solitary bees resting on a stem. The series shows the hairs, eyes, tongues and wings that make bees such capable pollinators.",
       "دراسة قريبة لعالم النحل: نحل العسل يعمل على الأقراص ويتغذى، ونحل انفرادي يستريح على ساق نبتة. تكشف السلسلة الشعيرات والعيون والألسنة والأجنحة التي تجعل النحل ملقّحاً بهذه البراعة."),
      fmt(("Honeybees","نحل العسل"),("Solitary bees","النحل الانفرادي")), col(['digger-bee','honeybee-feed','honeybee']),
      f'<a class="tlink" href="gallery.html#bees">{T(L,"Bees & wasps in the gallery","النحل والدبابير في المعرض")} <span class="arrow">→</span></a>'),
     ('trips',False,("Guided experiences","تجارب بإرشاد"),PROJECTS[2],
      ("Small-group exploration trips where participants learn to find, observe and photograph tiny life. Day trips focus on habitat and patience; night trips use torches and diffused flash to meet the species that only appear after dark.",
       "رحلات استكشافية لمجموعات صغيرة يتعلّم فيها المشاركون كيف يجدون الكائنات الصغيرة ويراقبونها ويصوّرونها. تركّز الرحلات النهارية على البيئة والصبر، وتستعين الرحلات الليلية بالمصابيح والفلاش الموزّع للتعرّف على كائنات لا تظهر إلا بعد حلول الظلام."),
      fmt(("Day trips","رحلات نهارية"),("Night trips","رحلات ليلية"),("Small groups","مجموعات صغيرة")), col(['bts-forest','bts-walk','bts-group']),
      f'<a class="tlink" href="book.html">{T(L,"See dates and book","المواعيد والحجز")} <span class="arrow">→</span></a>'),
     ('kids',True,("Education","تعليم"),PROJECTS[3],
      ("Children's trips and educational workshops that introduce young explorers to the small world around them, with magnifying glasses, printed macro photographs and simple field observation. Older groups move on to the basics of photographing insects with care. The aim is curiosity, and respect for the creatures we usually overlook.",
       "رحلات أطفال وورش تعليمية تعرّف المستكشفين الصغار بالعالم الصغير من حولهم، باستخدام العدسات المكبّرة وصور الماكرو المطبوعة والملاحظة الميدانية البسيطة، وتنتقل المجموعات الأكبر سناً إلى أساسيات تصوير الحشرات بعناية. الهدف هو إثارة الفضول، وغرس الاحترام لكائنات نمرّ بها عادةً دون أن نراها."),
      fmt(("Schools","المدارس"),("Families","العائلات"),("Photography basics","أساسيات التصوير")), col(['kids-loupe','bts-crouch'],two=True),
      f'<a class="tlink" href="book.html">{T(L,"Book a children\'s trip","احجز رحلة للأطفال")} <span class="arrow">→</span></a>'),
     ('exhibitions',False,("Exhibitions","معارض"),PROJECTS[4],
      ("Macro prints displayed outdoors, in the same landscapes where the subjects were found. Visitors see the detail up close, then start looking for it in the plants around them.",
       "صور ماكرو مطبوعة تُعرض في الهواء الطلق، في البيئات نفسها التي وُجدت فيها الكائنات. يرى الزائر التفاصيل عن قرب، ثم يبدأ بالبحث عنها في النباتات من حوله."),
      fmt(("Outdoor displays","عرض خارجي"),("Fine prints","مطبوعات فنية")), col(['bts-prints','bts-exhibit','blue-wing']),
      f'<a class="tlink" href="contact.html">{T(L,"Plan an exhibition","خطّط لمعرض")} <span class="arrow">→</span></a>'),
    ]
    out = ''
    for pid,flip,eb,P,body,fm,cl,link in arts:
        out += f'''
  <article class="proj{" flip" if flip else ""}" id="{pid}">
    <div class="txt">
      <p class="eyebrow">{T(L,*eb)}</p>
      <h2>{T(L,P[1],P[2])}</h2>
      <p>{T(L,*body)}</p>
      {fm}
      {link}
    </div>
    {cl}
  </article>'''
    return f'''
<div class="wrap">
  <div class="phead">
    {crumbs(L,'projects')}
    <h1><span class="kicker">{T(L,"Exploration trips · children's trips · photography workshops","رحلات استكشافية · رحلات أطفال · ورش تعليمية للتصوير")}</span>{T(L,"Looking closer, together.","نقترب أكثر، معاً.")}</h1>
    <p class="lead muted">{T(L,"Alongside my own documentation of UAE biodiversity, I take people into the field and bring the small world to schools, communities and public spaces.","إلى جانب توثيق التنوع البيولوجي في الإمارات، أصطحب الناس إلى الميدان، وأنقل العالم الصغير إلى المدارس والمجتمعات والأماكن العامة.")}</p>
  </div>
  {out}
  <div class="proj" style="display:block">
    <div class="proj-cta">
      <p class="eyebrow">{T(L,"Bring it to you","نصل إليكم")}</p>
      <h2>{T(L,"Planning a trip, workshop or exhibition for your school, community or organisation?","تخطّطون لرحلة أو ورشة أو معرض لمدرستكم أو مجتمعكم أو مؤسستكم؟")}</h2>
      <div style="display:flex;flex-wrap:wrap;gap:.8rem"><a class="btn solid" href="book.html">{T(L,"Book a trip","احجز رحلة")} <span class="arrow">→</span></a><a class="btn" href="contact.html">{T(L,"Get in touch","تواصلوا معي")}</a><a class="btn" href="faq.html">{T(L,"Read the FAQ","اقرأ الأسئلة الشائعة")}</a></div>
    </div>
  </div>
</div>'''

def p_faq(L, A):
    groups = ''
    for gen,gar,qs in FAQ:
        items = ''.join(f'<details><summary>{esc(T(L,q[0],q[1]))}</summary><div class="ans"><p>{esc(T(L,q[2],q[3]))}</p></div></details>' for q in qs)
        groups += f'<section class="faq-group"><h2>{T(L,gen,gar)}</h2><div class="faq-list">{items}</div></section>'
    return f'''
<div class="wrap faq">
  <div class="phead">
    {crumbs(L,'faq')}
    <h1><span class="kicker">{T(L,"Macro photography · trips · workshops","تصوير الماكرو · الرحلات · الورش")}</span>{T(L,"Frequently asked questions","الأسئلة الشائعة")}</h1>
    <p class="lead muted">{T(L,"Everything about Maryam's work, exploration trips, children's trips and educational photography workshops in the UAE. Can't find your answer?","كل ما تريد معرفته عن أعمال مريم والرحلات الاستكشافية ورحلات الأطفال والورش التعليمية للتصوير في الإمارات. لم تجد إجابتك؟")} <a href="contact.html" style="color:var(--sand)">{T(L,"Ask Maryam directly.","اسأل مريم مباشرة.")}</a></p>
  </div>
  <div id="faqGroups">{groups}</div>
  <div class="proj" style="display:block"><div class="proj-cta">
    <h2>{T(L,"Ready to book a trip or a workshop?","جاهز لحجز رحلة أو ورشة؟")}</h2>
    <div style="display:flex;flex-wrap:wrap;gap:.8rem"><a class="btn solid" href="book.html">{T(L,"See available dates","المواعيد المتاحة")} <span class="arrow">→</span></a><a class="btn" href="contact.html">{T(L,"Contact Maryam","تواصل مع مريم")}</a></div>
  </div></div>
</div>'''

def p_contact(L, A):
    topics = [("Print purchase","شراء مطبوعة"),("Exhibition","معرض"),("Exploration trip","رحلة استكشافية"),("Children's trip or workshop","رحلة أو ورشة للأطفال"),("Photography workshop","ورشة تعليمية للتصوير"),("Commission","تكليف بالتصوير"),("Media","إعلام")]
    chips = ''.join(f'<label><input type="radio" name="topic" id="t-{i}" value="{esc(T(L,a,b))}"{" checked" if i==0 else ""}><span>{T(L,a,b)}</span></label>' for i,(a,b) in enumerate(topics))
    cp = T(L,"Copy","نسخ")
    return f'''
<div class="wrap contact">
  <div style="min-width:0">
    {crumbs(L,'contact')}
    <h1 style="margin-top:2rem"><span class="kicker">{T(L,"Book a trip, workshop, exhibition or print","احجز رحلة أو ورشة أو معرضاً أو مطبوعة")}</span>{T(L,"Let's look closer, together.","لنقترب أكثر، معاً.")}</h1>
    <p class="lead muted" style="margin-top:1.5rem">{T(L,"Prints, exhibitions, exploration trips, children's trips, educational photography workshops, commissions and media requests.","المطبوعات، المعارض، الرحلات الاستكشافية، رحلات الأطفال، الورش التعليمية للتصوير، التكليفات وطلبات الإعلام.")}</p>
    <dl class="details">
      <div class="detail"><dt>{T(L,"Email","البريد")}</dt><dd><a class="v" href="mailto:maryamaalali@live.com">maryamaalali@live.com</a><button class="copy" type="button" data-copy="maryamaalali@live.com">{cp}</button></dd></div>
      <div class="detail"><dt>{T(L,"Phone · WhatsApp","الهاتف · واتساب")}</dt><dd><a class="v" href="https://wa.me/971529137373" target="_blank" rel="noopener">+971 52 913 7373</a><button class="copy" type="button" data-copy="+971529137373">{cp}</button></dd></div>
      <div class="detail"><dt>{T(L,"Instagram","إنستغرام")}</dt><dd><a class="v" href="https://www.instagram.com/macrobymaryam/" target="_blank" rel="noopener">@macrobymaryam</a></dd></div>
      <div class="detail"><dt>{T(L,"Based in","المقر")}</dt><dd><span>{T(L,"United Arab Emirates","دولة الإمارات العربية المتحدة")}</span></dd></div>
    </dl>
  </div>
  <form class="inq" id="inq" novalidate>
    <h2>{T(L,"Send an inquiry","أرسل استفساراً")}</h2>
    <div class="two">
      <div class="field"><label for="f-name">{T(L,"Your name","الاسم")}</label><input id="f-name" name="name" type="text" autocomplete="name" placeholder="{T(L,"Full name","الاسم الكامل")}"></div>
      <div class="field"><label for="f-email">{T(L,"Email","البريد الإلكتروني")}</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@example.com"></div>
    </div>
    <fieldset class="field"><legend>{T(L,"What is it about?","موضوع الرسالة")}</legend><div class="chips">{chips}</div></fieldset>
    <div class="field"><label for="f-msg">{T(L,"Message","الرسالة")}</label><textarea id="f-msg" name="message" placeholder="{T(L,"Dates, location, group size, ages, or the photograph number you're interested in.","التواريخ، الموقع، عدد المشاركين وأعمارهم، أو رقم الصورة التي تهمّك.")}"></textarea></div>
    <p class="err" id="err" hidden></p>
    <div><button class="btn solid" type="submit">{T(L,"Prepare message","تجهيز الرسالة")} <span class="arrow">→</span></button></div>
    <div class="ready" id="ready" hidden>
      <p>{T(L,"Your message is ready. Copy it, or open it in your email app, and send it to maryamaalali@live.com.","رسالتك جاهزة. انسخها أو افتحها في تطبيق البريد، وأرسلها إلى maryamaalali@live.com.")}</p>
      <pre id="readyTxt"></pre>
      <div class="acts"><button class="btn" type="button" id="copyMsg">{T(L,"Copy message","نسخ الرسالة")}</button><a class="btn" id="mailMsg" href="mailto:maryamaalali@live.com">{T(L,"Open in email","فتح في البريد")}</a></div>
    </div>
  </form>
</div>'''


def p_book(L, A):
    dows = [T(L,a,b) for a,b in [("Mon","ن"),("Tue","ث"),("Wed","ر"),("Thu","خ"),("Fri","ج"),("Sat","س"),("Sun","ح")]]
    yn = lambda name, yes_id: (f'<div class="radios"><label><input type="radio" name="{name}" id="{yes_id}" value="yes"><span>{T(L,"Yes","نعم")}</span></label>'
                               f'<label><input type="radio" name="{name}" id="{yes_id}-no" value="no"><span>{T(L,"No","لا")}</span></label></div>')
    return f"""
<div class="wrap">
  <div class="phead">
    {crumbs(L,'book')}
    <h1><span class="kicker">{T(L,"Exploration trips · night walks · children's trips · UAE","رحلات استكشافية · جولات ليلية · رحلات أطفال · الإمارات")}</span>{T(L,"Book a trip","احجز رحلتك")}</h1>
    <p class="lead muted">{T(L,"Choose a date in the calendar, pay by bank transfer and upload your receipt. Maryam confirms every registration once the transfer is checked.","اختر موعداً من التقويم، وادفع بالتحويل البنكي، ثم ارفع الإيصال. تؤكد مريم كل تسجيل بعد التحقق من التحويل.")}</p>
  </div>
  <p class="demo-note" id="demoNote" hidden></p>
  <section class="bk" aria-label="{T(L,"Availability calendar","تقويم المواعيد المتاحة")}">
    <div class="cal" id="cal">
      <div class="cal-head"><h2 id="calTitle" aria-live="polite"></h2>
        <div class="cal-nav"><button type="button" id="calPrev" aria-label="{T(L,"Previous month","الشهر السابق")}"><span>←</span></button><button type="button" id="calNext" aria-label="{T(L,"Next month","الشهر التالي")}"><span>→</span></button></div></div>
      <div class="cal-dow">{''.join(f'<span>{d}</span>' for d in dows)}</div>
      <div class="cal-grid" id="calGrid"></div>
      <div class="cal-legend"><span><i></i>{T(L,"Seats available","مقاعد متاحة")}</span><span class="lf"><i></i>{T(L,"Fully booked","مكتملة")}</span></div>
    </div>
    <div style="min-width:0">
      <div class="slots-head"><p class="eyebrow" id="slotsHead"></p><button type="button" class="tlink" id="slotsAll" hidden>{T(L,"Show the whole month","عرض الشهر كاملاً")}</button></div>
      <div id="slots" aria-live="polite"></div>
    </div>
  </section>

  <section class="book-wrap" id="bookWrap" hidden>
    <div class="bf">
      <aside class="bf-trip">
        <p class="eyebrow">{T(L,"Your trip","رحلتك")}</p>
        <h2 id="bfTitle"></h2>
        <div class="bf-meta" id="bfMeta"></div>
        <div id="bfIntro"></div>
        <ul id="bfIncludes"></ul>
        <button type="button" class="tlink" id="bfChange" style="justify-self:start">{T(L,"Choose another date","اختر موعداً آخر")}</button>
      </aside>
      <div style="min-width:0">
      <form id="bookForm" novalidate>
        <ol class="steps">
          <li class="step"><div class="step-h"><h3>{T(L,"Participants","المشاركون")}</h3></div>
            <div class="counters">
              <div class="counter"><label for="f-adults">{T(L,"Adults","البالغون")}<small>{T(L,"18 and over","18 سنة فأكثر")}</small></label>
                <div class="stepper"><button type="button" id="adultsDec" aria-label="{T(L,"Fewer adults","تقليل البالغين")}">−</button><output id="adultsOut" aria-live="polite">1</output><button type="button" id="adultsInc" aria-label="{T(L,"More adults","زيادة البالغين")}">+</button></div>
                <input type="hidden" id="f-adults" name="adults" value="1"></div>
              <div class="counter"><label for="f-children">{T(L,"Children","الأطفال")}<small>{T(L,"Under 18","أقل من 18 سنة")}</small></label>
                <div class="stepper"><button type="button" id="childrenDec" aria-label="{T(L,"Fewer children","تقليل الأطفال")}">−</button><output id="childrenOut" aria-live="polite">0</output><button type="button" id="childrenInc" aria-label="{T(L,"More children","زيادة الأطفال")}">+</button></div>
                <input type="hidden" id="f-children" name="children" value="0"></div>
            </div>
            <p class="privacy">{T(L,"Add the name of each participant. For every child, add their name, age and a parent's mobile number.","أضف اسم كل مشارك. ولكل طفل أضف اسمه وعمره ورقم جوال ولي الأمر.")}</p>
            <div id="people"></div>
          </li>
          <li class="step"><div class="step-h"><h3>{T(L,"Your contact details","بيانات التواصل")}</h3></div>
            <div class="field"><label for="f-name">{T(L,"Name","الاسم")} *</label><input id="f-name" name="contact_name" type="text" autocomplete="name"></div>
            <div class="two">
              <div class="field"><label for="f-mobile">{T(L,"Mobile number","رقم الجوال")} *</label><input id="f-mobile" name="mobile" type="tel" dir="ltr" autocomplete="tel" placeholder="+971 5x xxx xxxx"></div>
              <div class="field"><label for="f-email">{T(L,"Email","البريد الإلكتروني")} *</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@example.com"></div>
            </div>
          </li>
          <li class="step"><div class="step-h"><h3>{T(L,"Health and consent","الصحة والموافقات")}</h3></div>
            <fieldset class="field"><legend class="qlabel">{T(L,"Do you or any of the participants have any allergies?","هل لديك أو لدى أي من المشاركين حساسية؟")} *</legend>{yn('allergies','f-allergy')}</fieldset>
            <div class="field" id="allergyBox" hidden><label for="f-allergy-details">{T(L,"If yes, please specify","إذا كانت الإجابة نعم، يرجى التوضيح")} *</label><textarea id="f-allergy-details" name="allergy_details" rows="2"></textarea></div>
            <fieldset class="field"><legend class="qlabel">{T(L,"I agree to appear in photos or videos shared on @macrobymaryam social media.","أوافق على الظهور في الصور أو الفيديوهات المنشورة على حسابات ‎@macrobymaryam‎.")} *</legend>{yn('photo','f-photo')}</fieldset>
            <label class="agree"><input type="checkbox" id="f-rules" name="rules"><span id="bfRules"></span></label>
          </li>
          <li class="step"><div class="step-h"><h3>{T(L,"Pay by bank transfer","الدفع بالتحويل البنكي")}</h3></div>
            <div class="totalbox"><span>{T(L,"Total to transfer","المبلغ المطلوب تحويله")}</span><b id="bfTotal">0 AED</b><span id="bfCalc" style="flex-basis:100%"></span></div>
            <dl class="bank" id="bank"></dl>
          </li>
          <li class="step"><div class="step-h"><h3>{T(L,"Upload payment receipt","رفع إيصال الدفع")}</h3></div>
            <div class="drop"><b>{T(L,"Choose the receipt file","اختر ملف الإيصال")} *</b><small>{T(L,"Image or PDF, up to 10 MB","صورة أو PDF بحجم أقصاه 10 ميغابايت")}</small>
              <input id="f-receipt" name="receipt" type="file" accept="image/*,application/pdf" aria-label="{T(L,"Upload payment receipt","رفع إيصال الدفع")}"><span id="receiptName"></span></div>
          </li>
        </ol>
        <p class="err" id="bfErr" hidden role="alert"></p>
        <div style="display:grid;gap:1rem;justify-items:start;padding-top:1rem">
          <button class="btn solid" type="submit" id="bfSubmit">{T(L,"Submit registration","إرسال التسجيل")} <span class="arrow">→</span></button>
          <p class="privacy">{T(L,"Your details and receipt are used only to manage this booking and are visible only to Maryam.","تُستخدم بياناتك وإيصالك لإدارة هذا الحجز فقط، ولا يطّلع عليها سوى مريم.")}</p>
        </div>
      </form>
      <div class="done" id="done" hidden tabindex="-1">
        <p class="eyebrow">{T(L,"Registration received","تم استلام التسجيل")}</p>
        <h2>{T(L,"Thank you. See you in the field.","شكراً لك. نلتقي في الميدان.")}</h2>
        <p>{T(L,"Your reference","رقم المرجع")}: <span class="ref" id="doneRef"></span></p>
        <p class="muted" id="doneSum"></p>
        <p>{T(L,"Maryam will confirm your place by WhatsApp or email once the transfer is checked.","ستؤكد مريم مكانك عبر واتساب أو البريد الإلكتروني بعد التحقق من التحويل.")}</p>
        <button class="btn" type="button" id="doneAgain">{T(L,"Book another trip","احجز رحلة أخرى")}</button>
      </div>
      </div>
    </div>
  </section>
</div>"""

BUILDERS = {'book':p_book, 'index':p_index,'about':p_about,'gallery':p_gallery,'projects':p_projects,'faq':p_faq,'contact':p_contact}
PAGE_IMAGES = {'index':['hero-tiger','jumper-eyes','cuckoo-wasp','mantis','lacewing','chrysalis','bts-night'],
               'about':['bts-portrait','bts-field','bts-crouch','bts-screen','bts-hat','bts-exhibit'],
               'gallery':[g[0] for g in G],
               'projects':['mantis','pierid','lynx-spider','digger-bee','honeybee-feed','honeybee','bts-forest','bts-walk','bts-group','kids-loupe','bts-crouch','bts-prints','bts-exhibit','blue-wing'],
               'faq':['bts-walk'],'contact':['bts-portrait'],'book':['bts-forest','bts-night']}
OG_IMG = {'book':'bts-forest','index':'hero-tiger','about':'bts-portrait','gallery':'jumper-eyes','projects':'bts-night','faq':'bts-walk','contact':'bts-prints'}

# ---------- structured data ----------
def jsonld(L, page):
    title, desc = META[page][L]
    u = url(L,page)
    person = {"@type":"Person","@id":f"{DOMAIN}/#maryam","name":"Maryam Aalali","alternateName":"مريم آل علي",
              "jobTitle":T(L,"Macro photographer","مصورة ماكرو"),"nationality":{"@type":"Country","name":"United Arab Emirates"},
              "description":T(L,"Emirati macro photographer documenting the biodiversity of the UAE.","مصورة إماراتية توثّق التنوع البيولوجي في دولة الإمارات بتصوير الماكرو."),
              "knowsAbout":["Macro photography","Insects","Spiders","Bees","Biodiversity of the United Arab Emirates","Nature documentation","تصوير الماكرو","الحشرات","التنوع البيولوجي"],
              "image":f"{DOMAIN}/img/{IMGS['bts-portrait'][0]}.jpg","url":f"{DOMAIN}/","email":"mailto:maryamaalali@live.com","telephone":"+971529137373",
              "sameAs":["https://www.instagram.com/macrobymaryam/"],"workLocation":{"@type":"Country","name":"United Arab Emirates"}}
    website = {"@type":"WebSite","@id":f"{DOMAIN}/#website","url":f"{DOMAIN}/","name":"Macro by Maryam","alternateName":"ماكرو باي مريم","inLanguage":["en","ar"],"publisher":{"@id":f"{DOMAIN}/#maryam"}}
    ptype = {'index':'WebPage','about':'AboutPage','gallery':'ImageGallery','projects':'CollectionPage','faq':'FAQPage','contact':'ContactPage','book':'WebPage'}[page]
    wp = {"@type":ptype,"@id":u+"#webpage","url":u,"name":title,"description":desc,"inLanguage":L,"isPartOf":{"@id":f"{DOMAIN}/#website"},
          "about":{"@id":f"{DOMAIN}/#maryam"},"primaryImageOfPage":{"@type":"ImageObject","url":f"{DOMAIN}/img/{IMGS[OG_IMG[page]][0]}.jpg"}}
    graph = [person, website, wp]
    if page!='index':
        graph.append({"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":T(L,*NAV_NAME['index']),"item":url(L,'index')},
            {"@type":"ListItem","position":2,"name":T(L,*NAV_NAME[page]),"item":u}]})
    if page=='gallery':
        wp["image"] = [{"@type":"ImageObject","contentUrl":f"{DOMAIN}/img/{IMGS[g[0]][0]}.jpg","name":T(L,g[2],g[3])+f" ({g[4]})",
                        "caption":IMGS[g[0]][1 if L=='en' else 2],"creator":{"@id":f"{DOMAIN}/#maryam"},"copyrightHolder":{"@id":f"{DOMAIN}/#maryam"},
                        "creditText":"Maryam Aalali","contentLocation":{"@type":"Country","name":"United Arab Emirates"}} for g in G]
    if page=='projects':
        services=[("Exploration trips","رحلات استكشافية","Guided day and night macro exploration trips for small groups in the UAE.","رحلات استكشافية نهارية وليلية بإرشاد لمجموعات صغيرة في الإمارات."),
                  ("Children's trips and educational workshops","رحلات أطفال وورش تعليمية","Nature trips and educational photography workshops for children.","رحلات في الطبيعة وورش تعليمية للتصوير للأطفال."),
                  ("Macro photography exhibitions","معارض تصوير الماكرو","Outdoor exhibitions of macro prints of UAE biodiversity.","معارض خارجية لمطبوعات ماكرو للتنوع البيولوجي في الإمارات."),
                  ("Macro photography prints","مطبوعات تصوير الماكرو","Fine prints of UAE insects and spiders.","مطبوعات فنية لحشرات وعناكب الإمارات.")]
        for a,b,c,d in services:
            graph.append({"@type":"Service","name":T(L,a,b),"description":T(L,c,d),"provider":{"@id":f"{DOMAIN}/#maryam"},"areaServed":{"@type":"Country","name":"United Arab Emirates"}})
    if page=='faq':
        wp["mainEntity"] = [{"@type":"Question","name":T(L,q[0],q[1]),"acceptedAnswer":{"@type":"Answer","text":T(L,q[2],q[3])}} for _,_,qs in FAQ for q in qs]
    return json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False, separators=(',',':'))

FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=IBM+Plex+Mono:wght@400&family=Lato:wght@300;400;700&family=Noto+Kufi+Arabic:wght@300;400;500&family=Noto+Naskh+Arabic:wght@400;500&display=swap"

def head(L, page, A):
    title, desc = META[page][L]
    og = OG_IMG[page]
    pre = f'\n<link rel="preload" as="image" href="{img("hero-tiger",A)}" fetchpriority="high">' if page=='index' else ''
    return f'''<title>{esc(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Maryam Aalali">
<meta name="theme-color" content="#161615">
<link rel="canonical" href="{url(L,page)}">
<link rel="alternate" hreflang="en" href="{url('en',page)}">
<link rel="alternate" hreflang="ar" href="{url('ar',page)}">
<link rel="alternate" hreflang="x-default" href="{url('en',page)}">
<meta property="og:type" content="{'profile' if page=='about' else 'website'}">
<meta property="og:site_name" content="Macro by Maryam">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url(L,page)}">
<meta property="og:image" content="{DOMAIN}/img/{IMGS[og][0]}.jpg">
<meta property="og:image:alt" content="{alt(og,L)}">
<meta property="og:locale" content="{T(L,'en_AE','ar_AE')}">
<meta property="og:locale:alternate" content="{T(L,'ar_AE','en_AE')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{DOMAIN}/img/{IMGS[og][0]}.jpg">
<link rel="icon" type="image/png" href="{A}favicon.png">
<link rel="apple-touch-icon" href="{A}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{A}assets/site.css">{pre}
<script type="application/ld+json">{jsonld(L,page)}</script>'''

SUPA = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js"
def scripts(page, A):
    s = ''
    if page in ('book','faq','gallery','contact'):
        s += f'<script src="{A}assets/config.js"></script>\n<script src="{SUPA}"></script>\n<script src="{A}assets/data.js"></script>\n'
    s += f'<script src="{A}assets/site.js" defer></script>'
    if page == 'book': s += f'\n<script src="{A}assets/book.js" defer></script>'
    return s

def page_html(L, page, full=True):
    A = '' if L=='en' else '../'
    body = (header(L,page,A) + f'\n<main id="main">{BUILDERS[page](L,A)}\n</main>\n' + footer(L,page,A) + '\n' + LIGHTBOX(L) + '\n' + scripts(page, A))
    if not full:   # artifact entry page: the host supplies doctype/html/head/body
        return head(L,page,A) + '\n' + body
    return (f'<!doctype html>\n<html lang="{L}" dir="{T(L,"ltr","rtl")}">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head(L,page,A)}\n</head>\n<body>\n{body}\n</body>\n</html>\n')


# ---------- admin page ----------
def admin_html():
    seed = {"faqs":[{"group_en":g[0],"group_ar":g[1],"q_en":q[0],"q_ar":q[1],"a_en":q[2],"a_ar":q[3],"sort":i,"published":True}
                    for i,(g,q) in enumerate((g,q) for g in FAQ for q in g[2])],
            "gallery":[{"image_url":f"img/{IMGS[k][0]}.jpg","thumb_url":f"img/thumbs/{IMGS[k][0]}.jpg","name_en":en,"name_ar":ar,"taxon":tx,"taxon_italic":bool(it),
                        "category":c,"alt_en":IMGS[k][1],"alt_ar":IMGS[k][2],"sort":i,"published":True} for i,(k,c,en,ar,tx,it) in enumerate(G)]}
    return f"""<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Admin · macro by maryam</title>
<meta name="robots" content="noindex, nofollow">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/admin.css">
</head>
<body class="admin">
<div class="a-login" id="login">
  <div class="card">
    <span class="mark" aria-hidden="true"></span>
    <div><p class="eyebrow">macro by maryam</p><h1>Admin</h1></div>
    <div id="loginLive">
      <form id="loginForm" class="aform" novalidate>
        <div class="field"><label for="l-email">Email</label><input id="l-email" name="email" type="email" autocomplete="username" required></div>
        <div class="field"><label for="l-pass">Password</label><input id="l-pass" name="password" type="password" autocomplete="current-password" required></div>
        <p class="err" id="lErr" hidden role="alert"></p>
        <button class="btn solid" type="submit">Sign in</button>
      </form>
    </div>
    <div id="loginDemo" hidden style="display:grid;gap:1rem">
      <p class="muted">The database is not connected yet, so the admin opens in preview mode with example trips and bookings. Changes stay in this browser.</p>
      <button class="btn solid" type="button" id="enterDemo">Open the admin preview</button>
    </div>
    <a class="tlink" href="index.html" style="justify-self:start">Back to the website</a>
  </div>
</div>

<div id="app" hidden>
  <header class="a-top"><div class="wrap a-top-in">
    <a class="brand" href="#overview"><span class="mark" aria-hidden="true"></span><span class="word">macro by maryam · admin</span></a>
    <span class="pill" id="modeBadge"></span>
    <a class="vs" href="index.html" target="_blank" rel="noopener">View website</a>
    <button class="lang" type="button" id="signOut">Sign out</button>
  </div></header>
  <div class="demo-bar" id="demoBar" hidden><span>Preview mode: everything works, but changes are saved in this browser only. Connect Supabase to take real bookings.</span><button type="button" id="resetDemo">Reset preview data</button></div>
  <div class="a-shell">
    <nav class="a-nav" aria-label="Admin sections">
      <span class="sep">Bookings</span>
      <a href="#overview">Overview</a>
      <a href="#calendar">Calendar &amp; trips</a>
      <a href="#bookings">Bookings <span id="pendingBadge" aria-label="pending bookings"></span></a>
      <span class="sep">Website content</span>
      <a href="#payment">Payment details</a>
      <a href="#contact">Contact details</a>
      <a href="#faq">FAQ</a>
      <a href="#gallery">Gallery</a>
    </nav>
    <main class="a-main">
      <section class="a-sec" data-view="overview">
        <div class="a-head"><div><h1>Overview</h1><p>Bookings waiting for payment checks, and how full the next trips are.</p></div></div>
        <div class="tiles" id="ovTiles"></div>
        <div class="two-col">
          <div><h2>Next trips</h2><div id="ovTrips"></div></div>
          <div><h2>Latest bookings</h2><div class="tbl-wrap" id="ovBookings"></div></div>
        </div>
      </section>
      <section class="a-sec" data-view="calendar" hidden>
        <div class="a-head"><div><h1>Calendar &amp; trips</h1><p>Add, edit, hide or duplicate trips. Visible trips appear on the booking calendar straight away.</p></div><button class="btn solid" type="button" id="acNew">New trip</button></div>
        <div class="ac-head"><h2 id="acTitle"></h2><div class="cal-nav"><button type="button" id="acPrev" aria-label="Previous month"><span>←</span></button><button type="button" id="acNext" aria-label="Next month"><span>→</span></button></div></div>
        <div class="ac-grid" id="acGrid"></div>
        <h2>Trips this month</h2>
        <div class="tbl-wrap" id="acList"></div>
      </section>
      <section class="a-sec" data-view="bookings" hidden>
        <div class="a-head"><div><h1>Bookings</h1><p>Open a booking to check the receipt, confirm payment, or cancel. Cancelled bookings free their seats.</p></div><button class="btn" type="button" id="bkExport">Export CSV</button></div>
        <div class="toolbar">
          <select id="bkTrip" aria-label="Trip"></select>
          <div class="seg" id="bkStatus" role="group" aria-label="Status"><button type="button" data-s="all">All</button><button type="button" data-s="pending">Pending</button><button type="button" data-s="confirmed">Confirmed</button><button type="button" data-s="cancelled">Cancelled</button></div>
          <input type="search" id="bkSearch" placeholder="Search name, mobile or ref" aria-label="Search bookings">
        </div>
        <p class="roster" id="bkRoster" hidden></p>
        <div class="tbl-wrap" id="bkTable"></div>
      </section>
      <section class="a-sec" data-view="payment" hidden>
        <div class="a-head"><div><h1>Payment details</h1><p>Shown on the booking form with copy buttons. Check every digit before saving.</p></div></div>
        <div id="payForm"></div>
        <h2>Booking form message</h2>
        <div id="noteForm"></div>
      </section>
      <section class="a-sec" data-view="contact" hidden>
        <div class="a-head"><div><h1>Contact details</h1><p>Used on the contact page and in the footer.</p></div></div>
        <div id="contactForm"></div>
      </section>
      <section class="a-sec" data-view="faq" hidden>
        <div class="a-head"><div><h1>FAQ</h1><p>Questions and answers in English and Arabic. Order here is the order on the website.</p></div><button class="btn solid" type="button" id="faqNew">New question</button></div>
        <div id="faqList"></div>
      </section>
      <section class="a-sec" data-view="gallery" hidden>
        <div class="a-head"><div><h1>Gallery</h1><p>Upload, label and order photographs. Photos are resized automatically; alt text helps them appear in image search.</p></div><button class="btn solid" type="button" id="galNew">Upload photograph</button></div>
        <div class="ggrid" id="galGrid"></div>
      </section>
    </main>
  </div>
</div>
<div class="drawer" id="drawer" hidden><div class="drawer-in" role="dialog" aria-modal="true" aria-label="Editor"><button id="drawerClose" type="button">Close ✕</button><div id="drawerBody"></div></div></div>
<p class="toast" id="toast" hidden role="status"></p>
<script src="assets/config.js"></script>
<script src="{SUPA}"></script>
<script>window.MBM_SEED={json.dumps(seed, ensure_ascii=False)};</script>
<script src="assets/data.js"></script>
<script src="assets/admin.js"></script>
</body>
</html>
"""

def sql_str(v):
    if v is None: return 'null'
    if isinstance(v, bool): return 'true' if v else 'false'
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, (list, tuple)): return 'array[' + ','.join(sql_str(x) for x in v) + ']::text[]'
    if isinstance(v, dict): return sql_str(json.dumps(v, ensure_ascii=False)) + '::jsonb'
    return "'" + str(v).replace("'", "''") + "'"

def seed_sql():
    out = ["-- macro by maryam · starter content. Run after schema.sql. Safe to run once.", "begin;"]
    out.append("insert into public.settings(key,value) values")
    out.append(",\n".join([
      f"  ('bank', {sql_str({'bank_name':'ADIB','account_holder':'MARYAM AL ALI','account_number':'23906783','iban':'AE380500000000023906783','swift':'ABDIAEADXXX','currency':'AED'})})",
      f"  ('contact', {sql_str({'email':'maryamaalali@live.com','phone':'+971529137373','instagram':'macrobymaryam'})})",
      f"  ('booking_note', {sql_str({'en':'Please complete the registration by filling in the details below and uploading the payment confirmation.','ar':'يرجى إكمال التسجيل بتعبئة البيانات أدناه ورفع إثبات الدفع.'})})"])
      + "\non conflict (key) do nothing;")
    i = 0
    for gen, gar, qs in FAQ:
        for q in qs:
            out.append(f"insert into public.faqs(group_en,group_ar,q_en,q_ar,a_en,a_ar,sort) values ({sql_str(gen)},{sql_str(gar)},{sql_str(q[0])},{sql_str(q[1])},{sql_str(q[2])},{sql_str(q[3])},{i});")
            i += 1
    for i,(k,c,en,ar,tx,it) in enumerate(G):
        out.append(f"insert into public.gallery(image_url,thumb_url,name_en,name_ar,taxon,taxon_italic,category,alt_en,alt_ar,sort) values ("
                   f"{sql_str('img/'+IMGS[k][0]+'.jpg')},{sql_str('img/thumbs/'+IMGS[k][0]+'.jpg')},{sql_str(en)},{sql_str(ar)},{sql_str(tx)},{sql_str(bool(it))},{sql_str(c)},{sql_str(IMGS[k][1])},{sql_str(IMGS[k][2])},{i});")
    inc_en = ["Macro photos for learning & discussion before the walk","Interactive exploration challenge during the walk","Drinks & snacks","Headlamps","Full trip guidance experience"]
    inc_ar = ["صور ماكرو للتعلّم والنقاش قبل الجولة","تحدٍّ استكشافي تفاعلي خلال الجولة","مشروبات ووجبات خفيفة","مصابيح رأس","تجربة إرشاد كاملة طوال الرحلة"]
    out.append("-- Template trip (hidden). In the admin calendar, open it, set a new date, tick 'Visible' and save, or use 'Duplicate to this date'.")
    out.append("insert into public.trips(kind,title_en,title_ar,trip_date,start_time,end_time,location_en,location_ar,price_aed,capacity,includes_en,includes_ar,rules_en,rules_ar,published) values ("
               + ",".join(sql_str(v) for v in ['macro_walk','Macro Walk','جولة ماكرو','2026-04-04','09:00',None,'Mushrif Park, Dubai','حديقة مشرف، دبي',150,15,inc_en,inc_ar,
                 "I commit to respecting nature, keeping the area clean and following Mushrif Park rules, and I understand that each participant is responsible for their own safety during the walk.",
                 "ألتزم باحترام الطبيعة والحفاظ على نظافة المكان واتباع أنظمة حديقة مشرف، وأدرك أن كل مشارك مسؤول عن سلامته الشخصية خلال الجولة.", False]) + ");")
    out.append("commit;")
    return "\n".join(out) + "\n"

CONFIG_JS = """// Supabase connection. Fill both values to switch the booking calendar and admin panel from preview to live.
// Find them in Supabase → Project Settings → API ("Project URL" and the "anon public" key). The anon key is safe to publish.
window.MBM_CONFIG = {
  supabaseUrl: "",
  supabaseAnonKey: ""
};
"""

# ---------- sitemap, robots, llms ----------
def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    pri = {'index':'1.0','gallery':'0.9','projects':'0.9','book':'0.9','about':'0.8','faq':'0.7','contact':'0.7'}
    for L in ('en','ar'):
        for p in PAGES:
            out.append('  <url>')
            out.append(f'    <loc>{url(L,p)}</loc>')
            out.append(f'    <lastmod>{TODAY}</lastmod>')
            out.append(f'    <changefreq>{"weekly" if p=="gallery" else "monthly"}</changefreq>')
            out.append(f'    <priority>{pri[p]}</priority>')
            for l2 in ('en','ar'):
                out.append(f'    <xhtml:link rel="alternate" hreflang="{l2}" href="{url(l2,p)}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url("en",p)}"/>')
            for k in PAGE_IMAGES[p]:
                out.append(f'    <image:image><image:loc>{DOMAIN}/img/{IMGS[k][0]}.jpg</image:loc></image:image>')
            out.append('  </url>')
    out.append('</urlset>')
    return '\n'.join(out)+'\n'

def robots():
    return f"""# macro by maryam
User-agent: *
Allow: /
Disallow: /admin.html

Sitemap: {DOMAIN}/sitemap.xml
"""

def llms():
    pg = lambda L: '\n'.join(f"- [{T(L,*NAV_NAME[p])}]({url(L,p)}): {META[p][L][1]}" for p in PAGES)
    faq = '\n'.join(f"- **{q[0]}** {q[2]}" for _,_,qs in FAQ for q in qs)
    faq_ar = '\n'.join(f"- **{q[1]}** {q[3]}" for _,_,qs in FAQ for q in qs)
    species = ', '.join(sorted({f"{g[2]} ({g[4]})" for g in G}))
    return f"""# Macro by Maryam

> Maryam Aalali (مريم آل علي) is an Emirati macro photographer who documents the biodiversity of the United Arab Emirates: insects, spiders, bees and other small creatures photographed in their own habitat. She also runs exploration trips (day and night), children's trips, educational photography workshops and outdoor exhibitions of macro prints in the UAE.

The site is bilingual. English pages are at the root; Arabic pages are under /ar/. All photographs are © Maryam Aalali and may not be reused without permission.

## Key facts

- Name: Maryam Aalali (Arabic: مريم آل علي)
- Brand: macro by maryam (ماكرو باي مريم)
- Role: Emirati macro photographer documenting UAE biodiversity
- Based in: United Arab Emirates
- Services: macro photography prints, outdoor exhibitions, guided exploration trips, children's trips and educational workshops, photography workshops, commissions, media
- Booking: available dates, prices and seats are on the Book a trip page; registration requires a bank transfer and receipt upload
- Contact: maryamaalali@live.com · +971 52 913 7373 (phone and WhatsApp) · Instagram @macrobymaryam
- Subjects in the gallery: {species}

## Pages (English)

{pg('en')}

## الصفحات (العربية)

{pg('ar')}

## FAQ

{faq}

## الأسئلة الشائعة

{faq_ar}

## Optional

- [Sitemap]({DOMAIN}/sitemap.xml)
- [Instagram](https://www.instagram.com/macrobymaryam/)
"""

def build():
    os.makedirs(f"{OUT}/ar", exist_ok=True); os.makedirs(f"{OUT}/assets", exist_ok=True)
    prep_images()
    open(f"{OUT}/assets/site.css","w").write(open(f"{HERE}/base.css").read()+open(f"{HERE}/extra.css").read()+open(f"{HERE}/book.css").read())
    for f in ('site.js','data.js','book.js','admin.js','admin.css'): shutil.copy(f"{HERE}/{f}", f"{OUT}/assets/{f}")
    open(f"{OUT}/assets/config.js","w").write(CONFIG_JS)
    open(f"{OUT}/admin.html","w").write(admin_html())
    SB = os.path.join(HERE, "..", "supabase"); os.makedirs(SB, exist_ok=True)
    shutil.copy(f"{HERE}/supabase/schema.sql", f"{SB}/schema.sql")
    open(f"{SB}/seed.sql","w").write(seed_sql())
    for f in ('favicon.png','apple-touch-icon.png'): shutil.copy(f"{HERE}/{f}", f"{OUT}/{f}")
    for L in ('en','ar'):
        for p in PAGES:
            path = f"{OUT}/{'ar/' if L=='ar' else ''}{p}.html"
            open(path,'w').write(page_html(L,p))
    open(f"{OUT}/sitemap.xml",'w').write(sitemap())
    open(f"{OUT}/robots.txt",'w').write(robots())
    open(f"{OUT}/llms.txt",'w').write(llms())
    for p in PAGES:
        for L in ('en','ar'):
            t,d = META[p][L]; print(f"{L} {p:9s} title {len(t):3d}  desc {len(d):3d}")

if __name__=='__main__':
    build()
