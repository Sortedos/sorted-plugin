FOR NATIVE REVIEW: this Arabic text was written by an assistant and has not been checked by a native speaker.

# Sorted مع المساعد الذكي بتاعك

**Sorted** (https://sortedos.com) بيجمع أرقام الشركة في شاشة واحدة. بيتوصل بأنظمة الشركة (الحسابات زي Odoo، المتجر الإلكتروني، الإعلانات، والتحليلات)، ويقراها كل ساعة، ويحتفظ بالتاريخ، ويوريك فين نظامين مختلفين في نفس الرقم.

المشروع ده (مجموعة ملفات) بيخلي المساعد الذكي يشتغل مع Sorted. وفيه:

- **13 skill**: ملفات تعليمات قصيرة، كل واحد بيعلّم المساعد يعمل شغلانة واحدة كويس مع Sorted، زي مراجعة أداء الشركة، أو قائمة التحصيل، أو الأرقام اللي مش متطابقة، أو توصيل نظام.
- **إضافة Codex** و**إضافة Claude Code**، وكل واحدة بتنزّل الـ skills دي مع الاتصال بـ Sorted.
- **دليل لـ ChatGPT**، لأنه بيتوصل بـ Sorted مباشرة.

## مين اللي يستخدم ده

أصحاب الشركات والفرق اللي بيستخدموا Sorted أو بيجربوه، ومعاهم مساعد ذكي: Codex أو Claude Code أو Claude أو ChatGPT. مش محتاج برمجة. كل طريقة تركيب بتاخد دقايق.

اختار الطريقة على حسب المساعد اللي بتستخدمه. الـ terminal (شاشة الأوامر) هو الشباك اللي بتكتب فيه أوامر (PowerShell على Windows، و Terminal على Mac).

| بتستخدم | محتاج terminal؟ | اتبع |
|---|---|---|
| Codex | آه | التركيب: إضافة Codex |
| Claude Code | آه | التركيب: إضافة Claude Code |
| Claude على الويب أو تطبيق الديسكتوب | لأ | Claude على الويب أو تطبيق الديسكتوب |
| ChatGPT | لأ | التركيب: دليل ChatGPT |

## المساعد يقدر يعمل إيه مع Sorted

- يرد على "الشغل ماشي إزاي؟" من الأرقام الحية، مع وقت كل لقطة.
- يطلع مين عليه فلوس للشركة ويكتب رسايل تذكير مؤدبة.
- يلاقي فين نظامين مختلفين (زي الدفاتر والبنك) ويطلع السجلات اللي ورا الفرق.
- يساعد صاحب الشركة يوصّل Odoo أو Shopify أو Google Ads أو Google Analytics، علشان Sorted يقراهم بنفسه.
- **يبعت أرقام من أنظمة مش بيقراها Sorted بنفسه** (إعلانات Meta، نظام الكاشير، تطبيق التوصيل، أو أي حاجة تانية) عن طريق **feed**: مساحة باسم معين على الداشبورد، صاحب الشركة بيوافق عليها مرة واحدة. فيه 6 skills للموضوع ده، واحدة لكل نظام. Sorted بيقرا Odoo و Shopify و Google Ads و Google Analytics بنفسه، وكل skill من دول بتعرض الطريقة دي الأول؛ الـ feed لما اتصال Sorted مايقدرش يوصل للحساب، أو لرقم Sorted مش بيعرضه.

حاجتين لازم تعرفهم عن الـ feeds:

1. **Sorted مايقدرش يتأكد من الأرقام اللي بتيجي عن طريق feed.** دي الأرقام اللي المساعد قراها. الداشبورد بيكتب عليها إنها "مبعوتة من المساعد بتاعك، مش مقروءة بواسطة Sorted"، وصاحب الشركة هو المسؤول عنها.
2. **الـ feeds بتشتغل بس لما Sorted يفعّلها لشركتك.** لو الأدوات `define_feed` و`feed_numbers` و`list_feeds` و`end_feed` مش موجودة في أدوات Sorted عند المساعد، يبقى مش متفعّلة. اسأل Sorted من رابط التواصل على موقع Sorted.

الأدوات وحدودها وأمثلة: [docs/feed-tools.md](../feed-tools.md) (بالإنجليزي). قايمة الـ 13 skill وكل واحدة بتعمل إيه: في [الصفحة الإنجليزي](../../README.md#the-13-skills).

## التركيب: إضافة Codex

محتاج Codex متسطّب ومسجّل دخول، ومفتاح إضافة Sorted شخصي (بيبدأ بـ `srt_`). Sorted بيديك واحد: اطلبه من رابط التواصل على موقع Sorted. المفتاح بتاعك وبتاع شركتك؛ ماتديهوش لحد.

1. نزّل ملفات المشروع على جهازك: من صفحته على GitHub، دوس على زرار **Code** الأخضر، وبعدين **Download ZIP**، وفُك الضغط عن الملف. بعد كده افتح الـ terminal جوه الفولدر اللي فكّيته: على Windows، دوس كليك يمين جوه الفولدر في File Explorer واختار **Open in Terminal**؛ على Mac، دوس كليك يمين على الفولدر واختار **Services** وبعدين **New Terminal at Folder**.
2. احفظ المفتاح في مكان Codex يقدر يقراه، في متغير البيئة `SORTED_TOKEN` (إعداد باسم معين جهازك بيحتفظ بيه للبرامج).

   على Windows، في PowerShell (اتأكد إن الشباك مكتوب فيه PowerShell، مش Command Prompt)، سطر سطر:

   أ. الزق السطر ده ودوس Enter:

      ```powershell
      $key = Read-Host "Paste your Sorted key" -AsSecureString
      ```

   ب. الزق المفتاح لما يطلبه ودوس Enter. مش هيظهر حاجة على الشاشة وانت بتلزق: ده طبيعي.
   ج. الزق السطر ده ودوس Enter:

      ```powershell
      [Environment]::SetEnvironmentVariable("SORTED_TOKEN", [Net.NetworkCredential]::new("", $key).Password, "User")
      ```

   على Mac، اكتب `touch ~/.zshrc; open -e ~/.zshrc` علشان تفتح ملف بدء تشغيل الـ terminal في TextEdit؛ على Linux، اكتب `nano ~/.bashrc`. ضيف في الآخر سطر جديد: `export SORTED_TOKEN=` وبعده المفتاح بتاعك، من غير مسافات. احفظ الملف واقفله. كتابة المفتاح في الملف، مش في الـ terminal، بتخليه مايتسجّلش في تاريخ الأوامر.
3. ضيف الإضافة لـ Codex:

   ```
   codex plugin marketplace add .
   codex plugin add sorted@sorted
   ```

4. اقفل كل شبابيك Codex، ومعاها تطبيق Codex على الديسكتوب لو مفتوح، علشان Codex يشوف المفتاح الجديد. افتح terminal جديد، اكتب `codex` ودوس Enter، وبعدين اسأل: "Do a quick business review using Sorted." الرد الصح بيذكر أرقام شركتك ووقت قرايتها.

اتجرّب على: Windows 11 مع Codex 0.155.1، يوم 6 أكتوبر 2026 (الإضافة و13 skill اتركّبوا). ما اتجرّبش على: macOS و Linux.

## التركيب: إضافة Claude Code

محتاج Claude Code متسطّب. مفيش مفتاح: Claude Code بيسجّل دخول على Sorted بحسابك.

1. نزّل ملفات المشروع وافتح الـ terminal جوه الفولدر بتاعها، زي الخطوة 1 في جزء Codex اللي فوق.
2. ضيف الإضافة:

   ```
   claude plugin marketplace add ./
   claude plugin install sorted@sorted
   ```

3. شغّل Claude Code، واكتب `/mcp`، واختار **sorted**، وسجّل دخول بحساب Sorted لما المتصفح يفتح.
4. اسأل: "Do a quick business review using Sorted."

اتجرّب على: Windows 11 مع Claude Code 2.1.291 و 2.1.292، يوم 6 أكتوبر 2026 (الإضافة و13 skill ومدخل سيرفر Sorted اتركّبوا؛ خطوة تسجيل الدخول ماجرّبناهاش في الاختبار ده). ما اتجرّبش على: macOS و Linux.

### Claude على الويب أو تطبيق الديسكتوب

من غير terminal ومن غير مفتاح: Claude بيتوصل بـ Sorted مباشرة بحساب Sorted بتاعك.

1. في Claude، افتح **Customize**، وبعدين **Connectors**، ودوس **+ Add**، وبعدين **Add custom connector**. سمّيه Sorted واكتب العنوان `https://sortedos.com/api/mcp`. في باقة Team أو Enterprise، صاحب حساب Claude بتاع الشركة بيضيفه الأول من **Organization settings** ثم **Connectors**، وبعدين كل عضو يلاقيه في **Customize** ثم **Connectors** ويدوس **Connect**. دليل Claude نفسه بيوري كل شاشة: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
2. سجّل دخول بحساب Sorted بتاعك لما Claude يطلب.
3. علشان تستخدم skill، افتح الملف بتاعها من [قايمة الـ skills](../../README.md#the-13-skills)، وانسخ كل النص والزقه كأول رسالة، أو ضيفها كـ skill لو باقة Claude بتاعتك بتسمح بكده.

اتجرّب على: ولا حاجة لسه؛ اتراجعت أسامي القوايم بس على دليل Claude يوم 7 أكتوبر 2026. ما اتجرّبش: توصيل Claude على الويب أو الديسكتوب بـ Sorted.

## التركيب: دليل ChatGPT

ChatGPT بيتوصل بـ Sorted مباشرة كـ app، بتسجيل دخول ومن غير مفتاح. أنهي باقات ChatGPT تقدر تعمل ده، والخطوات، وإزاي تدي ChatGPT الـ skills: [docs/chatgpt-connector.md](../chatgpt-connector.md) (بالإنجليزي).

اتجرّب: الخطوات اتراجعت على صفحات OpenAI نفسها يوم 7 أكتوبر 2026 (OpenAI غيّرت الشاشات دي يوم 1 أكتوبر 2026؛ الدليل بيدي الطريقة الجديدة الأول والشاشات القديمة كبديل)، وسيرفر Sorted رد بأدوات الـ feed الأربعة في اختبار محلي. ما اتجرّبش: workspace حقيقي في ChatGPT بيتوصل بـ Sorted.

## الأمان، بكلام بسيط

- Sorted بيقرا بس من أنظمة الشركة. الـ skills بتقول للمساعد يستخدم صلاحية قراءة بس ومايغيّرش أي حاجة في أنظمة صاحب الشركة.
- صاحب الشركة هو اللي بيتعامل مع كل باسورد ومفتاح. الـ skills بتقول للمساعد مايطلبش مفتاح، ومايكررهوش، ومايحفظهوش، ومايبصّش على مفتاح على الشاشة.
- الـ feed بيتعمل بس بعد ما صاحب الشركة يشوف المعاينة ويقول آه، و`end_feed` بيمسح كل اللي اتبعت.
- الأسماء والتسميات اللي جاية من أنظمة تانية بتتعامل كبيانات، مش كأوامر.
