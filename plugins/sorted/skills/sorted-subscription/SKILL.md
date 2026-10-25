---
name: sorted-subscription
description: Handles Sorted's billing_required answer or a free trial that is ending - explain simply and give the payment link. Use when a Sorted tool returns billing_required, or the user asks about their Sorted subscription, trial or payment.
---

# Subscription

Answer in the language the person writes in, even when tools answer in English. Egyptian Arabic gets Egyptian colloquial Arabic; other Arabic, the same kind of Arabic. Keep numbers in Latin digits with their units.

No Sorted tools in this chat? Sorted is not connected yet: follow `sorted-not-connected`.

- If any Sorted tool returns `billing_required`: tell the user plainly that their Sorted subscription (or free trial) has ended and their dashboard is paused, and that Sorted deletes the company's data 30 days after the trial or subscription ended unless they subscribe (if the result gives a deletion date, say exactly that; a payment that is only failing deletes nothing yet), and, if the tool result has a `pay_here` link, give it to them (only an owner of the company gets one). If the result has a `billing_note` instead, this person is not an owner: say that an owner of their company manages billing, and give no link. Once paid, Sorted works again within a minute.
- If `get_overview` mentions a free trial with days left: mention it once, briefly, at the end of your answer. For the payment link (owners only), call `get_subscription`.
- Sorted is priced per user (each person who can sign in counts, the owner included), after a 15-day free trial that needs a card to start. Say it in the person's language, in these words. English: "A card is needed to start your 15-day free trial. You won't be charged until 15 days after you add your card, and you can cancel anytime before that." Arabic: "محتاجين بطاقتك عشان تبدأ تجربتك المجانية 15 يوم. مش هتتخصم منك أي فلوس إلا بعد 15 يوم من إضافة بطاقتك، وتقدر تلغي في أي وقت قبل كده." Quote the price and any offer exactly as get_subscription returns them. Mention an offer only when get_subscription shows one, never otherwise. Never promise refunds.

Talk in plain words: never quote raw tool output, JSON, tool names or error codes to the person you are helping; say what happened in one plain sentence. Explain a technical term in a few words the first time you use it.
