import streamlit as st
from groq import Groq
import os
import random

# १. API Key आणि क्लायंट सेटअप
# हा की तुझा Groq मधील पर्सनल की आहे
GROQ_API_KEY = "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" 
client = Groq(api_key=GROQ_API_KEY)

# २. वेब पेज कॉन्फिगरेशन
st.set_page_config(page_title="Rokade AI Hub", page_icon="⚡", layout="wide")

# ३. साइडबार मेनू - रितेश रोकडे यांचा ब्रँड
with st.sidebar:
    st.title("⚙️ Rokade AI Menu")
    tool_choice = st.radio("टूल निवडा:", [
        "🤖 AI चॅट (Expert)", 
        "📝 1000+ Question Bank",
        "🖼️ Electrical Symbols", 
        "🔢 Ohm's Law & Color Code", 
        "⚡ Motor Current Calc", 
        "💡 Project Ideas"
    ])
    st.divider()
    st.write("Founder: **Ritesh Rokade**") #
    st.write("Target: 10,000 Students 🚀") #

# ४. मुख्य स्क्रीनवर ब्रँडिंग
if os.path.exists("logo.png"):
    st.image("logo.png", width=100)
else:
    st.title("⚡ Rokade AI Hub")

# --- फिचर्सचे लॉजिक ---

# १. AI चॅट (Expert) - Groq Llama 3 मॉडेल वापरून
if tool_choice == "🤖 AI चॅट (Expert)":
    st.subheader("Rokade AI Expert मार्गदर्शन")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("तुमचा इलेक्ट्रिकल किंवा कोडींगचा प्रश्न विचारा...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "तू 'Rokade ITI Expert' आहेस. तुझे निर्माते Ritesh Rokade आहेत. तू मराठीत उत्तरे देतोस."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile"
            )
            res_text = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            with st.chat_message("assistant"):
                st.markdown(res_text)
        except Exception as e:
            st.error(f"Error: {e}")

# २. १०००+ प्रश्नपेढी (ITI Exam Special)
elif tool_choice == "📝 1000+ Question Bank":
    st.subheader("इलेक्ट्रिकल प्रश्नपेढी")
    # इथे तू तुझे १००० प्रश्न ॲड करू शकतोस
    questions = [
        {"q": "Current कशात मोजतात?", "o": ["Volt", "Ampere", "Ohm"], "a": "Ampere"},
        {"q": "Transformer कशावर काम करतो?", "o": ["AC", "DC", "दोन्ही"], "a": "AC"},
        {"q": "Resistance चे एकक काय आहे?", "o": ["Watt", "Ohm", "Farad"], "a": "Ohm"},
        {"q": "मानवी शरीराचा अंदाजे रोध किती असतो?", "o": ["100 Ohm", "1000 Ohm", "50 Ohm"], "a": "1000 Ohm"},
        {"q": "MCB म्हणजे काय?", "o": ["Circuit Board", "Miniature Circuit Breaker", "Control Board"], "a": "Miniature Circuit Breaker"}
    ]
    q = random.choice(questions)
    st.write(f"**प्रश्न:** {q['q']}")
    ans = st.radio("उत्तर निवडा:", q['o'])
    if st.button("Check Answer"):
        if ans == q['a']: st.success("बरोबर उत्तर! ✅")
        else: st.error(f"चुकीचे उत्तर. योग्य उत्तर: {q['a']}")

# ३. इलेक्ट्रिकल सिम्बॉल्स
elif tool_choice == "🖼️ Electrical Symbols":
    st.subheader("महत्त्वाचे इलेक्ट्रिकल सिम्बॉल्स")
    col1, col2 = st.columns(2)
    with col1:
        st.write("🔋 **Battery**: व्होल्टेज सोर्स")
        st.write("💡 **Lamp**: लोड/प्रकाश")
        st.write("⏚ **Ground**: अर्थिंग सुरक्षा")
    with col2:
        st.write("〰️ **Resistor**: रोध")
        st.write("🔌 **Plug**: कनेक्शन")
        st.write("➰ **Inductor**: कॉइल्स")
    

# ४. कॅल्क्युलेटर विभाग
elif tool_choice == "🔢 Ohm's Law & Color Code":
    tab1, tab2 = st.tabs(["Ohm's Law", "Resistor Color Code"])
    with tab1:
        v_calc = st.selectbox("काय शोधायचे?", ["V", "I", "R"])
        val1 = st.number_input("पहिली व्हॅल्यू", value=1.0)
        val2 = st.number_input("दुसरी व्हॅल्यू", value=1.0)
        if st.button("Calculate Ohm"):
            if v_calc == "V": st.success(f"V = {val1 * val2} V")
            elif v_calc == "I": st.success(f"I = {val1 / val2} A")
            else: st.success(f"R = {val1 / val2} Ω")
    with tab2:
        colors = {"Black":0, "Brown":1, "Red":2, "Orange":3, "Yellow":4, "Green":5, "Blue":6, "Violet":7, "Grey":8, "White":9}
        b1 = st.selectbox("Band 1", list(colors.keys()))
        b2 = st.selectbox("Band 2", list(colors.keys()))
        mul = st.selectbox("Multiplier", list(colors.keys()))
        if st.button("Calculate Resistance"):
            res_val = (colors[b1]*10 + colors[b2]) * (10**colors[mul])
            st.success(f"Resistance: {res_val} Ω")

# ५. मोटार करंट कॅल्क्युलेटर
elif tool_choice == "⚡ Motor Current Calc":
    st.subheader("Motor Full Load Current")
    hp = st.number_input("Motor HP", value=1.0)
    phase = st.selectbox("Phase", ["Single Phase", "Three Phase"])
    if st.button("Calculate Amps"):
        watts = hp * 746
        if phase == "Single Phase": amps = watts / 230
        else: amps = watts / (1.732 * 415 * 0.8)
        st.success(f"अंदाजे करंट: {amps:.2f} Amps")

# ६. प्रोजेक्ट आयडियाज (Arduino आणि इलेक्ट्रिकल)
elif tool_choice == "💡 Project Ideas":
    st.subheader("DIY प्रोजेक्ट आयडियाज")
    st.markdown("""
    - **Automatic Street Light**: LDR वापरून.
    - **Smart Switch**: मोबाईलवरून फॅन कंट्रोल करणे.
    - **Water Level Indicator**: टाकी भरल्यास अलार्म वाजवणे.
    """)