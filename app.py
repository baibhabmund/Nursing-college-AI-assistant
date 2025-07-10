import gradio as gr
from rapidfuzz import fuzz

positive_responses = ["haan", "yes", "sure", "okay", "ya", "yup", "yeah", "h"]
negative_responses = ["nahi", "no", "nope", "nah", "not interested", "n"]

contact_info = (
    "📞 संपर्क करें / Contact Official:\n"
    "Mr. Baibhab Mund – +91 8984020445\n"
    "Email: baibhab.mund20@gmail.com"
)

# Fuzzy matcher for yes/no
def match_intent(user_input, intent_list, threshold=80):
    return any(fuzz.ratio(user_input.lower().strip(), opt) >= threshold for opt in intent_list)

# Core logic
def process_input(user_input, chat_history, current_state, disabled):
    user_input_clean = user_input.strip().lower()
    response = ""

    if disabled:
        return "", chat_history, current_state, True

    # Match user intent
    if match_intent(user_input_clean, positive_responses):
        user_intent = "yes"
    elif match_intent(user_input_clean, negative_responses):
        user_intent = "no"
    else:
        user_intent = "unknown"

    # Chat states
    if current_state == "greeting":
        if user_intent == "no":
            response = "कोई बात नहीं। अगर भविष्य में सहायता चाहिए हो तो हमसे संपर्क करें।\nNo problem! Feel free to reach out anytime."
            current_state = "ended"
            disabled = True
        elif user_intent == "yes":
            response = "क्या आपने 12वीं में बायोलॉजी पढ़ी है?\nHave you studied Biology in 12th grade?"
            current_state = "asked_biology"
        else:
            response = "मैं समझ गया। क्या आप किसी अधिकारी से बात करना चाहेंगे?\nI understand. Would you like to speak to an official?"
            current_state = "offer_contact"

    elif current_state == "asked_biology":
        if user_intent == "yes":
            response = (
                "B.Sc नर्सिंग एक पूर्णकालिक कोर्स है जो आपको हेल्थकेयर में उज्ज्वल करियर देता है।\n"
                "B.Sc Nursing is a full-time program offering a great career in healthcare.\n"
                "क्या आप इस कोर्स के बारे में और जानकारी चाहेंगे?\nWould you like more information about the program?"
            )
            current_state = "explained_program"
        else:
            response = (
                "B.Sc नर्सिंग में एडमिशन के लिए बायोलॉजी अनिवार्य है।\n"
                "Biology is mandatory for B.Sc Nursing admission.\n"
                "क्या आप कुछ और जानना चाहेंगे?\nWould you like to know anything else?"
            )
            current_state = "asked_anything_else"

    elif current_state == "explained_program":
        if user_intent == "yes":
            response = (
                "💰 फीस विवरण / Fee Details:\n"
                "- ट्यूशन फीस / Tuition Fee: ₹60,000\n"
                "- बस फीस / Bus Fee: ₹10,000\n"
                "- कुल वार्षिक फीस / Total Annual Fee: ₹70,000\n"
                "➤ किश्तों में भुगतान / Installments:\n"
                "- ₹30,000 (प्रवेश के समय / at admission)\n"
                "- ₹20,000 (पहले सेमेस्टर के बाद / after 1st semester)\n"
                "- ₹20,000 (दूसरे सेमेस्टर के बाद / after 2nd semester)\n\n"
                "🏠 हॉस्टल सुविधाएँ / Hostel Facilities:\n"
                "- 24x7 पानी और बिजली\n- CCTV सुरक्षा\n- ऑन-साइट वार्डन\n"
                "🩺 हॉस्पिटल प्रशिक्षण / Hospital Training:\n"
                "- असली मरीज़ों के साथ प्रशिक्षण।\n"
                "कॉलेज दिल्ली में स्थित है।\nLocated in Delhi.\n"
                "क्या आप ट्रेनिंग या लोकेशन के बारे में जानना चाहेंगे?\nWould you like to know about training or location?"
            )
            current_state = "asked_more_info"
        else:
            response = "ठीक है। क्या आप कुछ और जानना चाहेंगे?\nAlright. Would you like to know anything else?"
            current_state = "asked_anything_else"

    elif current_state == "asked_more_info":
        if user_intent == "yes":
            response = (
                "📍 ट्रेनिंग स्थान / Clinical Training Locations:\n"
                "- जिला अस्पताल / District Hospital (Backundpur)\n"
                "- CHCs\n"
                "- रीजनल हॉस्पिटल / Regional Hospital (Chartha)\n"
                "- Ranchi Neurosurgery\n\n"
                "🎓 छात्रवृत्ति / Scholarships:\n"
                "- पोस्ट-मैट्रिक ₹18k–₹23k\n"
                "- लेबर मंत्रालय ₹40k–₹48k (लेबर रजिस्ट्रेशन ज़रूरी)\n"
                "🔢 सीटें / Total Seats: 60\n"
                "📋 पात्रता / Eligibility:\n- बायोलॉजी 12वीं में\n- PNT पास\n- उम्र: 17-35\n\n"
                "क्या आप कुछ और जानना चाहेंगे?\nWould you like to know anything else?"
            )
            current_state = "asked_anything_else"
        else:
            response = "ठीक है। क्या आप कुछ और जानना चाहेंगे?\nAlright. Would you like to know anything else?"
            current_state = "asked_anything_else"

    elif current_state == "asked_anything_else":
        if user_intent == "yes":
            response = contact_info + "\n\nआपका दिन शुभ हो! 😊\nHave a great day!"
            current_state = "ended"
            disabled = True
        elif user_intent == "no":
            response = "धन्यवाद! शुभकामनाएं। 😊\nThank you! All the best.\n\n🔁 'Restart' पर क्लिक करें दोबारा शुरू करने के लिए।"
            current_state = "ended"
            disabled = True
        else:
            response = "मैं समझ गया। क्या आप किसी अधिकारी से बात करना चाहेंगे?\nI understand. Would you like to speak to an official?"
            current_state = "offer_contact"

    elif current_state == "offer_contact":
        if user_intent == "yes":
            response = contact_info + "\n\nआपका दिन शुभ हो! 😊\nHave a great day!"
            current_state = "ended"
            disabled = True
        elif user_intent == "no":
            response = "ठीक है! धन्यवाद। 😊\nOkay! Thank you.\n\n🔁 'Restart' पर क्लिक करें दोबारा शुरू करने के लिए।"
            current_state = "ended"
            disabled = True
        else:
            response = "ठीक से नहीं समझा। क्या आप किसी अधिकारी से बात करना चाहेंगे?\nI didn’t understand. Would you like to speak to an official?"

    else:
        response = "मैं आपकी सहायता के लिए यहां हूँ। क्या आप नर्सिंग कॉलेज में एडमिशन लेना चाहते हैं?\nI am here to help you. Would you like to take admission in the Nursing College?"
        current_state = "greeting"

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})
    return "", chat_history, current_state, disabled

# Restart function
def restart_chat():
    chat_history = [
        {"role": "assistant", "content": "मैं आपकी सहायता के लिए यहां हूँ। क्या आप नर्सिंग कॉलेज में एडमिशन लेना चाहते हैं?\nI am here to help you. Would you like to take admission in the Nursing College?"}
    ]
    return "", chat_history, "greeting", False

# Gradio UI
with gr.Blocks(title="Nursing Admission Chatbot") as demo:
    gr.Markdown("## 🏥 Nursing Admission AI Assistant")
    chatbot = gr.Chatbot(label="Chat", type="messages")
    msg = gr.Textbox(placeholder="Type your answer here...", show_label=False)
    history = gr.State([])
    state = gr.State("greeting")
    disabled = gr.State(False)
    restart_btn = gr.Button("🔁 Restart", visible=False)

    def wrapper(message, hist, s, d):
        new_msg, new_hist, new_state, new_disabled = process_input(message, hist, s, d)
        return new_msg, new_hist, new_state, new_disabled, gr.update(visible=new_disabled)

    msg.submit(wrapper, [msg, history, state, disabled], [msg, chatbot, state, disabled, restart_btn])
    restart_btn.click(fn=restart_chat, outputs=[msg, chatbot, state, disabled])
    demo.load(fn=restart_chat, outputs=[msg, chatbot, state, disabled])

# ✅ Required for Hugging Face deployment
demo.launch()
