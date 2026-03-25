import streamlit as st
from datetime import datetime
import time,base64,csv,smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

st.set_page_config(page_title="Med-Diag Expert",page_icon="🩺",layout="wide")

def send_email_full(receiver_email, data, best, confidence, pdf_buffer):
    sender_email = "d31520052@gmail.com"
    app_password = "nngizedyzdilvdze"
    receiver_email = receiver_email.strip()
    name = data.get('name') or 'Patient'

    msg = MIMEMultipart()
    msg['Subject'] = f"Diagnosis Report - {name}"
    msg['From'] = f"Med-Diag <{sender_email}>"
    msg['To'] = receiver_email

    body = f"Dear {name},\n\nYour diagnosis: {best.get('name')} (Confidence: {confidence}%).\nRecommended: {best.get('medication')}\n\nPlease see the attached PDF for full details.\n\n- Med-Diag System"
    msg.attach(MIMEText(body, 'plain'))

    if pdf_buffer:
        part = MIMEApplication(pdf_buffer.getvalue(), Name='Report.pdf')
        part['Content-Disposition'] = 'attachment; filename="Report.pdf"'
        msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True, "Email Sent Successfully"
    except Exception as e:
        return False, str(e)




st.markdown("""
<style>
.stApp{background:transparent}
.bg-video{position:fixed;top:0;left:0;width:100%;height:100%;object-fit:cover;z-index:-1;opacity:0.3}
</style>
""",unsafe_allow_html=True)

c1,c2,c3=st.columns([1,0.5,6])
with c1: st.image("logo.png",width=130)
with c3: st.image("name.png",width=1000)


# STYLISH CENTERED NAVIGATION
st.markdown("""
<style>
    /* Center the radio buttons below the branch info */
    .stRadio > div {
        justify-content: center !important;
        gap: 40px;
    }

    /* Increase font size and make it bold */
    .stRadio label {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #000 !important;
    }
    /* Style the radio items for a menu look */
    div[data-testid="stMarkdownContainer"] p {
        margin-bottom: 0px;
    }
    .stRadio div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.4);
        padding: 10px 30px;
        border-radius: 50px;
        border: 1.5px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0;
        width: fit-content;
        margin-top: 5px;
        margin-bottom: 20px;
        margin: 15px auto !important;
        width: fit-content;
    }


    /* Keep the Branch title box styling from the screenshot */
    .branch-box {
        background-color: #fcae3e;
        color: black;
        font-weight: bold;
        padding: 10px 30px;
        border-radius: 10px;
        font-size: 20px;
        text-align: center;
        width: fit-content;
        margin: 5px auto 15px auto;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# BRANCH INFO (New centered box added)
st.markdown('<div class="branch-box">Artificial Intelligence & Data Science</div>', unsafe_allow_html=True)

page = st.radio("", ["Home", "Diagnosis System", "About"], horizontal=True)

if page == "Home":
    st.markdown("<style>.stApp{background:rgba(30,144,255,0.2);backdrop-filter:blur(5px);}</style>",unsafe_allow_html=True)

    # RESTORE ORIGINAL CREDITS BOX
    rc1, rc2 = st.columns([2, 1.2])
    with rc2:
        st.markdown("""
        <div style="font-size:14.5px;line-height:1.4;text-align:left;color:#000;background:rgba(255,255,255,0.6);backdrop-filter:blur(10px);padding:15px;border-radius:12px;border:1.5px solid rgba(255,255,255,0.8);box-shadow:0 6px 20px rgba(0,0,0,0.15);width:fit-content;margin-top: -30px; transform: translateX(35px);">
            <b style="font-size:15px;">Group Members:</b><br>
            • <b>T. Udayasri Durga (25ME5A5409)</b><br>
            • <b>N. Pujitha (24ME1A5481)</b><br>
            • <b>Sk. Ushna (24ME1A54A6)</b><br>
            • <b>N. Bhanu Venkata Reddy (24ME1A5480)</b>
        </div>
        """,unsafe_allow_html=True)

if page != "Home":
    with open("bg_video.mp4","rb") as f:
        v=base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <video autoplay muted loop class="bg-video">
    <source src="data:video/mp4;base64,{v}" type="video/mp4">
    </video>
    """,unsafe_allow_html=True)




knowledge_base=[
{"name":"Dengue","symptoms":["Fever","Headache","Body Pain","Vomiting","Joint Pain"],
 "advice":"Immediate medical attention required. Monitor platelet count.",
 "medication":"Paracetamol, ORS, IV Fluids","risk":"High",
 "food":"Avoid oily and spicy food; take papaya leaf juice, coconut water, and light diet."},

{"name":"Pneumonia","symptoms":["Fever","Cough","Breathing Difficulty","Chest Pain"],
 "advice":"Chest X-ray required. Seek hospital care.",
 "medication":"Azithromycin, Amoxicillin","risk":"High",
 "food":"Avoid cold and heavy foods; take warm soups, ginger tea, and soft foods."},

{"name":"Malaria","symptoms":["Fever","Chills","Sweating","Headache"],
 "advice":"Blood test recommended. Take antimalarial medication.",
 "medication":"Artemisinin Combination Therapy (ACT), Chloroquine","risk":"High",
 "food":"Avoid oily and junk food; take high-protein diet, fruits, and plenty of fluids."},

{"name":"Typhoid","symptoms":["Fever","Stomach Pain","Headache","Weakness"],
 "advice":"Consult doctor. Maintain hygiene and hydration.",
 "medication":"Ciprofloxacin, Azithromycin","risk":"Medium",
 "food":"Avoid spicy and raw foods; take boiled food, khichdi, and fruits."},

{"name":"Food Poisoning","symptoms":["Stomach Pain","Vomiting","Diarrhea","Nausea"],
 "advice":"Drink ORS. Seek medical care if dehydration occurs.",
 "medication":"ORS, Ondansetron","risk":"Medium",
 "food":"Avoid spicy and solid food; take ORS, banana, rice, and curd."},

{"name":"Migraine","symptoms":["Headache","Nausea","Sensitivity to Light"],
 "advice":"Rest in dark room. Avoid stress.",
 "medication":"Sumatriptan, Ibuprofen","risk":"Low",
 "food":"Avoid caffeine and processed foods; take magnesium-rich foods and stay hydrated."},

{"name":"Gastritis","symptoms":["Stomach Pain","Nausea","Bloating"],
 "advice":"Avoid spicy food. Take antacids.",
 "medication":"Omeprazole, Antacids","risk":"Low",
 "food":"Avoid spicy and acidic food; take bland diet, milk, and soft foods."},

{"name":"Flu","symptoms":["Fever","Cough","Cold","Sneezing"],
 "advice":"Rest and hydration advised.",
 "medication":"Oseltamivir, Paracetamol","risk":"Low",
 "food":"Avoid cold drinks and ice cream; take warm fluids, soups, and herbal tea."},

{"name":"Common Cold","symptoms":["Sneezing","Runny Nose","Sore Throat","Cough"],
 "advice":"Rest and stay hydrated.",
 "medication":"Paracetamol, Cetirizine","risk":"Low",
 "food":"Avoid cold items like ice cream; take warm water, soups, and vitamin C fruits."},

{"name":"Hypertension","symptoms":["Headache","Dizziness","Fatigue"],
 "advice":"Monitor BP and consult doctor.",
 "medication":"Amlodipine, Losartan","risk":"Medium",
 "food":"Avoid salty and fried food; take low-sodium diet, fruits, and vegetables."}
]

all_symptoms=sorted({s for d in knowledge_base for s in d["symptoms"]})

# ---------------- HOME ----------------
if page=="Home":
    st.markdown("<br><br>", unsafe_allow_html=True)



    st.markdown("""
<style>
.title{font-size:60px;font-weight:bold;text-align:center;background:linear-gradient(90deg,#000000,#333333,#000000);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.subtitle{text-align:center;font-size:22px;color:black;margin-bottom:30px;font-weight:600;}
.box{background:rgba(30,144,255,0.25);padding:25px;border-radius:12px;margin-top:20px;color:black;font-size:18px;line-height:1.7;font-weight:600;}
.metric-box{background:rgba(30,144,255,0.45);padding:20px;border-radius:12px;color:black;text-align:center;font-weight:700;font-size:18px;}
</style>
""",unsafe_allow_html=True)

    st.markdown("""
<style>
.moving-title{
font-size:60px;
font-weight:bold;
text-align:center;
background:linear-gradient(90deg,#000000,#333333,#000000);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
animation:moveGlow 3s infinite alternate;
}

@keyframes moveGlow{
0%{letter-spacing:2px;transform:translateY(0px);}
100%{letter-spacing:6px;transform:translateY(-4px);}
}
</style>

<div class="moving-title">Med-Diag Expert System</div>
""",unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>AI-Powered Clinical Decision Support for Faster Diagnosis</div>",unsafe_allow_html=True)

    st.markdown("<div class='box'>Med-Diag Expert System helps healthcare professionals quickly assess patient symptoms and suggest possible conditions. Instead of manually checking symptom lists, this system provides a smart, reliable diagnosis with recommended actions for patient care.</div>",unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;color:black;margin-top:30px;font-weight:bold;'>How This System Works</h3>",unsafe_allow_html=True)

    steps=[
    "Enter patient details manually or upload a file with symptoms.",
    "System analyzes the symptoms and matches them with known diseases.",
    "Calculates confidence and evaluates risk levels for each condition.",
    "Generates a detailed report with recommended actions for patient care."
    ]

    for col,txt in zip(st.columns(4),steps):
        with col: st.markdown(f"<div class='metric-box'>{txt}</div>",unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='box'>This tool allows doctors and medical staff to make faster, informed decisions. It improves patient care by highlighting high-risk conditions and providing actionable advice efficiently.</div>",unsafe_allow_html=True)

# ---------------- DIAGNOSIS ----------------
elif page=="Diagnosis System":
    st.title("Diagnosis System")
    st.subheader("Upload Patient File")
    file=st.file_uploader("Upload (.txt or .csv)",type=["txt","csv"])
    data={"name":"","age":0,"gender":"","blood":"","email":"","chief":"","symptoms":[],"history":[]}
    if file:
        lines=file.read().decode().splitlines()
        if file.name.endswith(".txt"):
            for l in lines:
                if ":" in l:
                    k,v=l.split(":",1)
                    if k=="Name":data["name"]=v.strip()
                    elif k=="Age":data["age"]=int(v.strip())
                    elif k=="Gender":data["gender"]=v.strip()
                    elif k=="Blood Group":data["blood"]=v.strip()
                    elif k.strip() in ["Email", "email", "EMAIL"]:data["email"]=v.strip()
                    elif k.strip() in ["Chief Complaint", "chief"]:data["chief"]=v.strip()

                    elif k=="Symptoms":data["symptoms"]=[i.strip() for i in v.split(",")]
                    elif k=="Medical History":data["history"]=[i.strip() for i in v.split(",")]
        else:
            for r in csv.DictReader(lines):
                data["name"]=r.get("Name","")
                data["age"]=int(r.get("Age",0) or 0)
                data["gender"]=r.get("Gender","")
                data["blood"]=r.get("Blood Group", r.get("blood", ""))
                # Case-insensitive email extraction for CSV
                data["email"] = r.get("Email") or r.get("email") or r.get("EMAIL") or ""
                data["chief"]=r.get("Chief Complaint", r.get("chief", ""))

                data["symptoms"]=[i.strip() for i in r.get("Symptoms","").split(",") if i.strip()]
                data["history"]=[i.strip() for i in r.get("Medical History","").split(",") if i.strip()]
        
        if data["email"]:
            st.info(f"📍 Detected Patient Email: **{data['email']}**")
        else:
            st.warning("⚠️ No email detected in the file. You can enter one below or in the manual form.")
            data["email"] = st.text_input("Enter Email for Report", key="file_manual_email")

        run_diagnosis = st.button("Run AI Diagnosis", key="file_diag_btn")

    else:
        st.subheader("Manual Entry")
        with st.form("patient_form", clear_on_submit=False):
            c1,c2,c3=st.columns(3)
            with c1:data["name"]=st.text_input("Patient Name")
            with c2:data["age"]=st.number_input("Age",1,120,value=1)
            with c3:data["gender"]=st.selectbox("Gender",["Choose option","Male","Female","Other"])
            c4,c5,c6=st.columns(3)
            with c4:data["blood"]=st.selectbox("Blood Group",["Choose option","A+","A-","B+","B-","O+","O-","AB+","AB-"])
            # Added a unique key to the email input to ensure it's not cross-cached
            with c5:data["email"]=st.text_input("Patient Email", key="live_patient_email")
            with c6:data["chief"]=st.text_input("Chief Complaint / Main Problem")
            data["symptoms"]=st.multiselect("Select Symptoms",all_symptoms)
            data["history"]=st.multiselect("Medical History",["None","Diabetes","Hypertension","Asthma","Heart Disease","Kidney Disease","Allergies"])
            run_diagnosis = st.form_submit_button("Run AI Diagnosis")
    if run_diagnosis:
        st.session_state.diagnosis_active = True
        st.session_state.email_sent_for_this_diag = False # Reset for new diagnosis
        # Create a copy to cache for the display, but we'll always use the live data for mailing
        st.session_state.diag_cache_data = data.copy()


    if st.session_state.get("diagnosis_active", False):
        # We display using the cached diagnosis but allow the email field to remain live
        cached_data = st.session_state.get("diag_cache_data", data)
        if not cached_data["name"] or not cached_data["symptoms"] or not cached_data["gender"] or not cached_data["blood"]:
            st.error("Please fill all required patient details")
            st.session_state.diagnosis_active = False
        else:
            data = cached_data # Use cached data for the display logic below
            with st.spinner("AI analyzing symptoms..."):

                time.sleep(2)
                best=None
                m=0
                for d in knowledge_base:
                    match=len(set(data["symptoms"])&set(d["symptoms"]))
                    if match>m: m,best=match,d
            confidence=int((m/len(best["symptoms"]))*100)
            st.success("Diagnosis Completed")

            # --- PDF GENERATION (REQUIRED FOR BOTH DISPLAY AND EMAIL) ---
            buffer=BytesIO()
            styles=getSampleStyleSheet()
            meds=[m.strip() for m in best["medication"].split(",")]
            actions=[
                best["advice"],
                best.get("food","Avoid unhealthy food; take balanced diet."),
                "Follow your doctor’s instructions and seek immediate help if symptoms worsen."
            ]
            flow=[
                Paragraph("<b>Medical Diagnosis Report</b>",styles["Title"]),
                Spacer(1,20),
                Paragraph(f"Patient: {data['name']}",styles["Normal"]),
                Paragraph(f"Age: {data['age']}",styles["Normal"]),
                Paragraph(f"Gender: {data['gender']}",styles["Normal"]),
                Paragraph(f"Blood Group: {data['blood']}",styles["Normal"]),
                Paragraph(f"Chief Complaint: {data['chief']}",styles["Normal"]),
                Spacer(1,10),
                Paragraph(f"Predicted Condition: {best['name']}",styles["Heading3"]),
                Paragraph(f"Confidence Level: {confidence}%",styles["Normal"]),
                Spacer(1,10),
                Paragraph("Recommended Medication:",styles["Heading3"])
            ]
            for m in meds:
                flow.append(Paragraph(f"• {m}",styles["Normal"]))
            flow.append(Spacer(1,10))
            flow.append(Paragraph("Recommended Action:",styles["Heading3"]))
            for a in actions:
                flow.append(Paragraph(f"• {a}",styles["Normal"]))
            flow.append(Spacer(1,20))
            flow.append(Paragraph(f"Report Generated on : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",styles["Normal"]))
            SimpleDocTemplate(buffer,pagesize=A4).build(flow)

            # AUTOMATIC EMAIL SENDING WITH PDF ATTACHMENT
            target_email = st.session_state.get("live_patient_email", "").strip() or \
                           st.session_state.get("file_manual_email", "").strip() or \
                           data.get("email", "").strip()
            
            if target_email and not st.session_state.get("email_sent_for_this_diag", False):
                with st.spinner(f"Automatically sending PDF report to {target_email}..."):
                    success, msg_response = send_email_full(target_email, data, best, confidence, buffer)
                    if success:
                        st.session_state.email_sent_for_this_diag = True # Mark as sent
                        st.info(f"📧 PDF Report successfully sent to {target_email}")
                    else:
                        st.warning(f"⚠️ Auto-send failed: {msg_response}")
            elif st.session_state.get("email_sent_for_this_diag", False):
                st.success(f"✅ Report already sent to {target_email}")


            st.subheader("Diagnosis Report")


            st.write("Patient:",data["name"])
            st.write("Age:",data["age"])
            st.write("Gender:",data["gender"])
            st.write("Blood Group:",data["blood"])
            st.write("Chief Complaint:",data["chief"])
            st.success("Predicted Condition: "+best["name"])
            st.progress(confidence/100)
            st.write("Confidence Level:",confidence,"%")
            {"High":st.error,"Medium":st.warning,"Low":st.info}[best["risk"]](f"{best['risk']} Risk Condition")
            col1,col2=st.columns(2)
            with col1:
                st.subheader("Recommended Medication")
                for m in meds:
                    st.write("•",m)
            with col2:
                st.subheader("Recommended Action")
                for a in actions:
                    st.write("•",a)
            b64=base64.b64encode(buffer.getvalue()).decode()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
<div style="background:#00bcd4;padding:8px 15px;width:100%;border-radius:6px;text-align:center;margin-top:2px;">
<a href="data:application/pdf;base64,{b64}" download="Diagnosis_Report.pdf" style="color:white;text-decoration:none;font-weight:bold;">Download Report</a>
</div>
""",unsafe_allow_html=True)


# ---------------- ABOUT ----------------
else:

    st.markdown("<u><h3 style='text-align:center; color:#000;'>Technologies Used</h3></u>",unsafe_allow_html=True)

    st.markdown("""
<h4>Rule-Based Expert System:</h4><span style='color:#333;'>The diagnosis engine is designed using predefined medical rules where diseases are associated with symptoms and medical advice. The system evaluates these rules to determine possible conditions.</span></br>
<h4>Forward Chaining Inference:</h4><span style='color:#333;'>The system begins with patient symptoms and moves forward through the knowledge base to infer the most relevant disease based on matching rules.</span></br>
<h4>Priority-Based Disease Evaluation:</h4><span style='color:#333;'>Each disease in the knowledge base is assigned a priority level so that serious and high-risk conditions can be identified earlier than low-risk illnesses.</span></br>
<h4>Symptom Matching (Unification):</h4><span style='color:#333;'>Patient symptoms are compared with disease symptom sets stored in the knowledge base. The system calculates the best match and determines the most probable condition.</span></br>
<h4>Streamlit Framework:</h4><span style='color:#333;'>Streamlit is used to build the interactive web interface for entering patient data, running the diagnosis system, and displaying results.</span></br>
<h4>Python Programming:</h4><span style='color:#333;'>Python is the core programming language used to implement the expert system logic, rule matching, and overall system functionality.</span></br>
<h4>CSV and TXT File Processing:</h4><span style='color:#333;'>The system allows uploading patient records in CSV or TXT format. These files are parsed to automatically extract patient details and symptoms.</span></br>
<h4>ReportLab PDF Generation:</h4><span style='color:#333;'>ReportLab library is used to generate downloadable diagnosis reports in PDF format for documentation and patient records.</span></br>
<h4>SMTP Email Integration:</h4><span style='color:#333;'>SMTP protocol is used to automatically send the generated patient reports directly to the patient’s email for quick and easy access.</span></br>

""",unsafe_allow_html=True)

    st.markdown("### Developed By")

    # Member list updated to include N. Bhanu
    # Member list updated to include N. Bhanu Venkata Reddy
    members = [
        "T. Udayasri Durga<br>25ME5A5409",
        "N. Pujitha<br>24ME1A5481",
        "Sk. Ushna<br>24ME1A54A6",
        "N. Bhanu Venkata Reddy<br>24ME1A5480"
    ]


    # Smaller stylish grid for 4 members (2x2)
    row1_cols = st.columns(2)
    row2_cols = st.columns(2)
    
    for idx, member in enumerate(members):
        target_col = row1_cols[idx] if idx < 2 else row2_cols[idx-2]
        with target_col:
            st.markdown(f"""
                <div style='background:linear-gradient(135deg, #00c6ff, #0072ff); 
                            padding:12px; border-radius:12px; text-align:center; 
                            color:white; font-weight:700; font-size:15px; 
                            box-shadow: 0 4px 10px rgba(0,0,0,0.15); 
                            margin-bottom:15px; border: 1px solid rgba(255,255,255,0.1);'>
                    {member}
                </div>
            """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)


    st.caption("Med-Diag Expert System © 2026")