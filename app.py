import math, time
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyArrowPatch

st.set_page_config(page_title="Virtual 8086 Stepper Motor Lab", page_icon="⚙️", layout="wide")
st.markdown('<style>.stApp{background:radial-gradient(circle at 10% 0%,#12324a,#071522 48%,#030a12)} section[data-testid="stSidebar"]{background:#071b2b;border-right:1px solid #087ca7} h1,h2,h3{color:#65d8ff!important} div[data-testid="stMetric"]{background:#071f30;border:1px solid #12658b;padding:10px;border-radius:12px}</style>', unsafe_allow_html=True)
st.title("⚙️ Virtual 8086 Stepper Motor Laboratory")
st.caption("8086 assembly • I/O interfacing • Motor sequencing • Waveform analysis | Software-only simulator")
if "angle" not in st.session_state: st.session_state.angle=0.0
if "logs" not in st.session_state: st.session_state.logs=[]
with st.sidebar:
    st.markdown("## 🧭 LAB NAVIGATION")
    page=st.radio("Module",["Dashboard","Stepper Motor Theory","8086 Hardware Interface","Assembly Programs","Simulation Lab","Waveforms & Signals","Memory & I/O View","Experiment Guide","Quiz / Assessment","Troubleshooting"])
    st.divider(); st.write("**CPU:** 8086 · 16-bit"); st.write("**Mode:** Virtual hardware")
    st.caption("Confirm trainer-specific port maps before physical experiments.")

cw="""; Clockwise reference listing
6000: B0 80     MOV AL, 80H
6002: BA C6 FF  MOV DX, 0FFC6H
6005: EE        OUT DX, AL
6006: B0 88     MOV AL, 88H
6008: BA C4 FF  MOV DX, 0FFC4H
600B: EE        OUT DX, AL
600C: E8 F5 00  CALL DELAY
600F: D0 C8     ROR AL, 1
6011: EB F8     JMP A1
6104: B9 00 20  MOV CX, 2000H
6107: E2 FE     LOOP 6107H
6109: C3        RET"""
ccw=cw.replace("Clockwise","Anticlockwise").replace("ROR AL, 1","ROL AL, 1")

def motor(angle):
    fig,ax=plt.subplots(figsize=(5,4),facecolor="#06111b"); ax.set_facecolor("#06111b")
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.35,1.35); ax.set_ylim(-1.3,1.3)
    ax.add_patch(Circle((0,0),1,fill=False,edgecolor="#6b8799",linewidth=5))
    ax.add_patch(Circle((0,0),.72,fill=False,edgecolor="#254a61",linewidth=2))
    colors=["#00d4ff","#ffe347","#ff4b63","#3c91ff"]
    for i,deg in enumerate([0,90,180,270]):
        ax.add_patch(Wedge((0,0),.96,deg-18,deg+18,width=.22,color=colors[i],alpha=.9))
        ax.text(1.16*math.cos(math.radians(deg)),1.16*math.sin(math.radians(deg)),chr(65+i),color=colors[i],ha="center",va="center",weight="bold")
    t=math.radians(angle); ax.add_patch(Circle((0,0),.12,color="#d8f3ff"))
    ax.add_patch(FancyArrowPatch((0,0),(.65*math.cos(t),.65*math.sin(t)),arrowstyle="-|>",mutation_scale=24,linewidth=4,color="white"))
    ax.text(0,-1.17,f"ROTOR ANGLE {angle%360:.1f}°",color="#64e5ff",ha="center",weight="bold")
    fig.tight_layout(); return fig

def waves(n):
    fig,ax=plt.subplots(figsize=(7,3),facecolor="#06111b"); ax.set_facecolor("#06111b")
    x=list(range(n+1)); colors=["#00e676","#ffe347","#ff4b63","#3c91ff"]
    for p in range(4): ax.step(x,[((i+p)//2)%2+p*1.2 for i in x],where="post",color=colors[p],linewidth=2,label=f"Phase {chr(65+p)}")
    ax.set_xlabel("Step index",color="white"); ax.tick_params(colors="#b8cdd9"); ax.grid(alpha=.15)
    for s in ax.spines.values(): s.set_color("#36576b")
    ax.legend(ncol=4,fontsize=8,facecolor="#0a2030",labelcolor="white"); fig.tight_layout(); return fig

if page=="Dashboard":
    st.markdown("### 🚀 Laboratory overview")
    cols=st.columns(4)
    for col,(a,b) in zip(cols,[("8086 CPU","16-bit"),("Interface","I/O mapped"),("Motor","4 phase"),("Simulation","Virtual")]): col.metric(a,b)
    left,right=st.columns([1.1,1])
    with left: st.markdown("### 🔩 Virtual motor"); st.pyplot(motor(st.session_state.angle),use_container_width=True)
    with right:
        st.markdown("### Explore the lab")
        st.markdown("- **Learn:** motor theory\n- **Code:** compare ROR and ROL\n- **Simulate:** direction, angle, count and speed\n- **Analyze:** phase waveforms\n- **Inspect:** memory and I/O ports")
        st.markdown("### Execution log"); st.code("\n".join(st.session_state.logs[-8:]) or "Ready — no runs yet.")
elif page=="Stepper Motor Theory":
    st.markdown("## 📘 Stepper motor theory")
    st.write("A stepper motor converts electrical pulses into discrete angular movement. Sequentially energizing stator windings creates a rotating magnetic field.")
    a,b=st.columns(2)
    a.markdown("### Components\n- **Stator:** stationary coils\n- **Rotor:** rotating shaft\n- **Driver:** switches coil current\n- **Step angle:** movement per step")
    b.markdown("### Key equations"); st.latex(r"\text{Angular movement}=\text{Steps}\times\text{Step angle}"); st.latex(r"\text{RPM}=\frac{\text{Steps per second}\times60}{\text{Steps per revolution}}")
    st.warning("Actual step angle and phase order depend on the motor and driver.")
elif page=="8086 Hardware Interface":
    st.markdown("## 🔌 Hardware block diagram")
    st.code("8086 TRAINER KIT  →  I/O INTERFACE  →  MOTOR DRIVER  →  STEPPER MOTOR\n                                      ↑\n                                MOTOR POWER SUPPLY")
    st.dataframe([{"Item":"26-core FRC","Connection":"Trainer CN4 to interface"},{"Item":"Sample ports","Connection":"0FFC6H and 0FFC4H — verify manual"},{"Item":"Power","Connection":"Check polarity and module labels"},{"Item":"Motor","Connection":"Match phase labels to interface"}],use_container_width=True,hide_index=True)
    st.error("Never connect motor coils directly to 8086 I/O pins. Use a suitable driver module.")
elif page=="Assembly Programs":
    st.markdown("## 💻 8086 assembly reference")
    t1,t2,t3=st.tabs(["Clockwise","Anticlockwise","Instruction guide"])
    t1.code(cw,language="asm"); t2.code(ccw,language="asm")
    with t3: st.dataframe([{"Instruction":"OUT DX, AL","Meaning":"Write AL to I/O port addressed by DX"},{"Instruction":"ROR / ROL","Meaning":"Rotate bits right / left"},{"Instruction":"CALL / RET","Meaning":"Call and return from delay routine"},{"Instruction":"LOOP","Meaning":"Decrement CX and loop while nonzero"},{"Instruction":"JMP","Meaning":"Unconditional jump"}],use_container_width=True,hide_index=True)
    st.caption("Reference only: the supplied listing is trainer-specific and loops continuously.")
elif page=="Simulation Lab":
    st.markdown("## 🎛️ Simulation control room")
    with st.form("run"):
        a,b,c=st.columns(3); direction=a.selectbox("Direction",["Clockwise (CW)","Anticlockwise (CCW)"]); step_angle=b.selectbox("Step angle",[1.8,7.5,15.0,45.0,90.0],index=1); count=c.number_input("Number of steps",1,200,24)
        delay=st.slider("Delay per step (ms)",0,120,5,5); go=st.form_submit_button("▶ Execute simulation",type="primary",use_container_width=True)
    if go:
        sign=1 if direction.startswith("Clockwise") else -1; prog=st.progress(0); status=st.empty(); slot=st.empty()
        for i in range(int(count)):
            st.session_state.angle=(st.session_state.angle+sign*step_angle)%360
            status.write(f"Step {i+1}/{count} · rotor angle {st.session_state.angle:.1f}°"); slot.pyplot(motor(st.session_state.angle),use_container_width=True); prog.progress((i+1)/int(count))
            if delay: time.sleep(delay/1000)
        st.session_state.logs.append(f"{time.strftime('%H:%M:%S')} | {direction} | {count} steps × {step_angle:g}° | final {st.session_state.angle:.1f}°"); st.success("Simulation complete — final angle recorded.")
    st.metric("Current rotor angle",f"{st.session_state.angle:.1f}°"); st.pyplot(motor(st.session_state.angle),use_container_width=True)
    if st.button("↺ Reset rotor"): st.session_state.angle=0; st.rerun()
elif page=="Waveforms & Signals":
    st.markdown("## 📈 Phase waveform explorer"); n=st.slider("Steps to display",8,64,24,4); st.pyplot(waves(n),use_container_width=True)
    st.caption("Illustrative digital phase states only. Real patterns depend on motor, interface and drive method.")
elif page=="Memory & I/O View":
    st.markdown("## 🧮 Memory and I/O inspector")
    st.dataframe([{"Address":"6000H","Bytes":"B0 80","Instruction":"MOV AL,80H"},{"Address":"6002H","Bytes":"BA C6 FF","Instruction":"MOV DX,0FFC6H"},{"Address":"6005H","Bytes":"EE","Instruction":"OUT DX,AL"},{"Address":"6006H","Bytes":"B0 88","Instruction":"MOV AL,88H"},{"Address":"6008H","Bytes":"BA C4 FF","Instruction":"MOV DX,0FFC4H"},{"Address":"600BH","Bytes":"EE","Instruction":"OUT DX,AL"},{"Address":"6104H","Bytes":"B9 00 20","Instruction":"MOV CX,2000H"}],use_container_width=True,hide_index=True)
    port=st.selectbox("Sample I/O port",["0FFC6H","0FFC4H"]); val=st.selectbox("Example output byte",["80H","88H","44H","66H","22H","33H","11H","99H"]); st.code(f"MOV DX, {port}\nMOV AL, {val}\nOUT DX, AL",language="asm")
    st.caption("Explanatory only — no physical port writes occur.")
elif page=="Experiment Guide":
    st.markdown("## 🧪 Experiment guide")
    st.markdown("**Aim:** Study 8086 stepper motor interfacing and simulate both directions.")
    st.markdown("**Procedure**\n1. Review port addresses and interface wiring.\n2. Select direction, angle and number of steps.\n3. Execute simulation.\n4. Observe rotor angle and waveform.\n5. Compare movement with steps × angle (modulo 360°).")
    st.dataframe([{"Trial":"1","Direction":"CW","Angle":"7.5°","Steps":24,"Movement":"180°"},{"Trial":"2","Direction":"CCW","Angle":"7.5°","Steps":24,"Movement":"180°"},{"Trial":"3","Direction":"CW","Angle":"15°","Steps":12,"Movement":"180°"}],use_container_width=True,hide_index=True)
elif page=="Quiz / Assessment":
    st.markdown("## 🧠 Quick knowledge check")
    qs=[("Which instruction writes AL to port DX?",["MOV","OUT","LOOP","RET"],"OUT"),("What does ROL do?",["Rotate bits left","Rotate bits right","Stop motor"],"Rotate bits left"),("Angular movement equals?",["Steps × step angle","Port × delay","CPU clock only"],"Steps × step angle"),("Can motor coils connect directly to CPU pins?",["Yes","No"],"No")]
    ans=[]
    for i,(q,opts,correct) in enumerate(qs): ans.append(st.radio(f"{i+1}. {q}",opts,key=f"q{i}"))
    if st.button("Check answers",type="primary"):
        score=sum(x==q[2] for x,q in zip(ans,qs)); st.metric("Score",f"{score}/{len(qs)}")
        if score==len(qs): st.success("Excellent — all correct.")
        else: st.info("Review Theory and Assembly Programs, then retry.")
elif page=="Troubleshooting":
    st.markdown("## 🛠️ Troubleshooting")
    for title,desc in [("Motor does not rotate","Check supply polarity, driver enable, connector alignment and phase sequence."),("Motor vibrates only","Check coil pairs, phase order, load and supply capability."),("Direction reversed","Verify phase sequence and ROL/ROR operation."),("Missed steps","Reduce speed and check load and driver."),("I/O writes ineffective","Confirm trainer I/O decoding and port addresses.")]:
        with st.expander(title): st.write(desc)
    st.warning("Power down before changing physical wiring. Follow the trainer and driver manuals.")
st.divider(); st.caption("Virtual 8086 Stepper Motor Laboratory · Educational simulator · No physical hardware control")
