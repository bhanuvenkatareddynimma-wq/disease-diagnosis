import streamlit as st
from datetime import datetime
import time,base64,csv,smtplib,email.utils
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.message import EmailMessage

def send_email_full(receiver_email, patient_name, disease, confidence, medication, pdf_buffer=None):
    sender_email = "d31520052@gmail.com"  
    app_password = "kroiprnprhqltlsg"   
    msg = MIMEMultipart()
    msg['Subject'] = f"Diagnosis Report - {patient_name}"
    msg['From'] = f"Med-Diag <{sender_email}>"
    msg['To'] = receiver_email
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid()
    body = f"Dear {patient_name},\n\nYour diagnosis result is:\n\nDisease: {disease}\nConfidence: {confidence}%\nMedication: {medication}\n\nPlease find the attached report for full details.\n\nStay safe and take care.\n\n- Med-Diag System"
    msg.attach(MIMEText(body, 'plain'))
    if pdf_buffer:
        part = MIMEApplication(pdf_buffer.getvalue(), Name='Diagnosis_Report.pdf')
        part['Content-Disposition'] = 'attachment; filename="Diagnosis_Report.pdf"'
        msg.attach(part)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, app_password)
            server.send_message(msg)
        return True, "Email Sent Successfully"
    except Exception as e:
        return False, str(e)
st.set_page_config(page_title="Med-Diag Expert",page_icon="🩺",layout="wide")
st.markdown("""<style>.stApp{background:transparent}.bg-video{position:fixed;top:0;left:0;width:100%;height:100%;object-fit:cover;z-index:-1;opacity:0.3}</style>""",unsafe_allow_html=True)
page=st.radio("",["Home","Diagnosis System","About"],horizontal=True)
if page!="Home":
    with open("bg_video.mp4","rb") as f:
        v=base64.b64encode(f.read()).decode()
    st.markdown(f"""<video autoplay muted loop class="bg-video"><source src="data:video/mp4;base64,{v}" type="video/mp4"></video>""",unsafe_allow_html=True)

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
    st.markdown("<style>.stApp{background:rgba(30,144,255,0.2);backdrop-filter:blur(5px);}</style>",unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,0.5,6])
    with c1: st.image("logo.png",width=130)
    with c3: st.image("name.png",width=1000)
    st.markdown("""<div style="background-color:#FFC107;color:white;font-size:20px;font-weight:bold;padding:8px;border-radius:6px;text-align:center;width:350px;margin:auto;margin-top:15px;">Artificial Intelligence & Data Science</div>""",unsafe_allow_html=True)
    st.markdown("""<div style="font-size:18px;line-height:1.8;text-align:right;margin-top:15px;"><b>Group Members</b><br>T. Udayasri Durga – 25ME5A5409<br>N. Pujitha – 24ME1A5481<br>Sk. Ushna – 24ME1A54A6<br>N. Bhanu Venkata Reddy – 24ME1A5480</div>""",unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    st.markdown("""<style>.title{font-size:60px;font-weight:bold;text-align:center;background:linear-gradient(90deg,#00f2ff,#ffffff,#00f2ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}.subtitle{text-align:center;font-size:22px;color:white;margin-bottom:30px;}.box{background:rgba(30,144,255,0.25);padding:25px;border-radius:12px;margin-top:20px;color:white;font-size:18px;line-height:1.7;}.metric-box{background:rgba(30,144,255,0.45);padding:20px;border-radius:12px;color:white;text-align:center;font-weight:600;font-size:18px;}</style>""",unsafe_allow_html=True)
    st.markdown('<style>.moving-title{font-size:60px;font-weight:bold;text-align:center;background:linear-gradient(90deg,#00f2ff,#ffffff,#00f2ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:moveGlow 3s infinite alternate;}@keyframes moveGlow{0%{letter-spacing:2px;transform:translateY(0px);}100%{letter-spacing:6px;transform:translateY(-4px);}}</style><div class="moving-title">Med-Diag Expert System</div>', unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>AI-Powered Clinical Decision Support for Faster Diagnosis</div>",unsafe_allow_html=True)
    st.markdown("<div class='box'>Med-Diag Expert System helps healthcare professionals quickly assess patient symptoms and suggest possible conditions. Instead of manually checking symptom lists, this system provides a smart, reliable diagnosis with recommended actions for patient care.</div>",unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:white;margin-top:30px;'>How This System Works</h3>",unsafe_allow_html=True)
    steps=["Enter patient details manually or upload a file with symptoms.","System analyzes the symptoms and matches them with known diseases.","Calculates confidence and evaluates risk levels for each condition.","Generates a detailed report with recommended actions for patient care."]
    for col,txt in zip(st.columns(4),steps):
        with col: st.markdown(f"<div class='metric-box'>{txt}</div>",unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='box'>This tool allows doctors and medical staff to make faster, informed decisions. It improves patient care by highlighting high-risk conditions and providing actionable advice efficiently.</div>",unsafe_allow_html=True)
# ---------------- DIAGNOSIS ----------------
elif page=="Diagnosis System":
    st.title("Diagnosis System")
    st.subheader("Upload Patient File")
    file=st.file_uploader("Upload (.txt or .csv)",type=["txt","csv"])
    data={"name":"","age":0,"gender":"","blood":"","chief":"","symptoms":[],"history":[]}
    receiver_email = ""
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
                    elif k.strip() in ["Email", "email", "EMAIL"]:receiver_email = v.strip()
                    elif k=="Chief Complaint":data["chief"]=v.strip()
                    elif k=="Symptoms":data["symptoms"]=[i.strip() for i in v.split(",")]
                    elif k=="Medical History":data["history"]=[i.strip() for i in v.split(",")]
        else:
            for r in csv.DictReader(lines):
                data["name"]=r.get("Name","")
                data["age"]=int(r.get("Age",0) or 0)
                data["gender"]=r.get("Gender","")
                data["blood"]=r.get("Blood Group","")
                receiver_email = r.get("Email", "").strip()
                data["chief"]=r.get("Chief Complaint","")
                data["symptoms"]=[i.strip() for i in r.get("Symptoms","").split(",") if i.strip()]
                data["history"]=[i.strip() for i in r.get("Medical History","").split(",") if i.strip()]        
        run_diagnosis = st.button("Run AI Diagnosis")

    else:
        st.subheader("Manual Entry")
        with st.form("patient_form", clear_on_submit=False):
            c1,c2,c3,c4=st.columns(4)
            with c1:data["name"]=st.text_input("Patient Name")
            with c2:data["age"]=st.number_input("Age",1,120,value=1)
            with c3:data["gender"]=st.selectbox("Gender",["Choose option","Male","Female","Other"])
            with c4:data["blood"]=st.selectbox("Blood Group",["Choose option","A+","A-","B+","B-","O+","O-","AB+","AB-"])
            c5,c6=st.columns(2)
            with c5:
                receiver_email = st.text_input("Patient Email")  
            with c6:
                data["chief"]=st.text_input("Chief Complaint / Main Problem")
            c7,c8=st.columns(2)
            with c7:
                data["symptoms"]=st.multiselect("Select Symptoms",all_symptoms)
            with c8:
                data["history"]=st.multiselect(
                    "Medical History",
                    ["None","Diabetes","Hypertension","Asthma","Heart Disease","Kidney Disease","Allergies"]
                )
            run_diagnosis = st.form_submit_button("Run AI Diagnosis")

    if run_diagnosis:
        if not data["name"] or not data["symptoms"] or not data["gender"] or not data["blood"]:
            st.error("Please fill all required patient details")
        else:
            with st.spinner("AI analyzing symptoms..."):
                time.sleep(2)
                best=None
                m=0
                for d in knowledge_base:
                    match=len(set(data["symptoms"])&set(d["symptoms"]))
                    if match>m: m,best=match,d

            confidence=int((m/len(best["symptoms"]))*100)
            st.success("Diagnosis Completed")
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
            meds=[m.strip() for m in best["medication"].split(",")]
            actions=[
                best["advice"],
                best.get("food","Avoid unhealthy food; take balanced diet."),
                "Follow your doctor’s instructions and seek immediate help if symptoms worsen."
            ]

            col1,col2=st.columns(2)
            with col1:
                st.subheader("Recommended Medication")
                for m in meds:
                    st.write("•",m)
            with col2:
                st.subheader("Recommended Action")
                for a in actions:
                    st.write("•",a)
            buffer=BytesIO()
            styles=getSampleStyleSheet()
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
            b64=base64.b64encode(buffer.getvalue()).decode()       
            if receiver_email:
                success, msg = send_email_full(
                    receiver_email=receiver_email,
                    patient_name=data["name"],
                    disease=best["name"],
                    confidence=confidence,
                    medication=best["medication"],
                    pdf_buffer=buffer
                )
                if success:
                    st.success("Email sent successfully!")
                else:
                    st.error(f"Email failed: {msg}")
            st.markdown(f"""<div style="background:#00bcd4;padding:8px 15px;width:260px;border-radius:6px;text-align:center;margin-top:15px;"><a href="data:application/pdf;base64,{b64}" download="Diagnosis_Report.pdf" style="color:white;text-decoration:none;font-weight:bold;">Download Report</a></div>""",unsafe_allow_html=True)
# ---------------- ABOUT ----------------
else:
    st.markdown("<u><h3 style='text-align:center;'>Technologies Used</h3></u>",unsafe_allow_html=True)
    st.markdown("""
<h4>Rule-Based Expert System:</h4>The diagnosis engine is designed using predefined medical rules where diseases are associated with symptoms and medical advice. The system evaluates these rules to determine possible conditions.</br>
<h4>Forward Chaining Inference:</h4>The system begins with patient symptoms and moves forward through the knowledge base to infer the most relevant disease based on matching rules.</br>
<h4>Priority-Based Disease Evaluation:</h4>Each disease in the knowledge base is assigned a priority level so that serious and high-risk conditions can be identified earlier than low-risk illnesses.</br>
<h4>Symptom Matching (Unification):</h4>Patient symptoms are compared with disease symptom sets stored in the knowledge base. The system calculates the best match and determines the most probable condition.</br>
<h4>Streamlit Framework:</h4>Streamlit is used to build the interactive web interface for entering patient data, running the diagnosis system, and displaying results.</br>
<h4>Python Programming:</h4>Python is the core programming language used to implement the expert system logic, rule matching, and overall system functionality.</br>
<h4>CSV and TXT File Processing:</h4>The system allows uploading patient records in CSV or TXT format. These files are parsed to automatically extract patient details and symptoms.</br>
<h4>ReportLab PDF Generation:</h4>ReportLab library is used to generate downloadable diagnosis reports in PDF format for documentation and patient records.</br>
<h4>SMTP Email Integration:</h4>SMTP protocol is used to automatically send the generated patient reports directly to the patient’s email for quick and easy access.</br>                
""",unsafe_allow_html=True)
    st.markdown("### Developed By")
    names = ["T. Udayasri Durga – 25ME5A5409","N. Pujitha – 24ME1A5481","Sk. Ushna – 24ME1A54A6","N. Bhanu Venkata Reddy – 24ME1A5480"]
    for i in range(0, len(names), 2):
        cols = st.columns(2)
        for col, name in zip(cols, names[i:i+2]):
            with col:
                st.markdown(f"<div style='background:rgba(30,144,255,0.45);padding:10px;border-radius:8px;text-align:center;color:white;font-weight:600;font-size:16px;margin:10px 10px;'>{name}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Med-Diag Expert System © 2026")
