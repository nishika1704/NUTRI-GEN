import streamlit as st
import google.generativeai as genai
import base64
import os 
from ai_diet_page import generate_diet

st.set_page_config(
    page_title="NutriGen",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "page" not in st.session_state:
    st.session_state.page = 1
if "user_input" not in st.session_state:
    st.session_state.user_input =  {"name": "","age":20, "height":170, "weight":70,"sex":"Male","dietary_preferences":"None","budget":"Student Pocket / Frugal","medical_history":[]}


apikey = st.secrets.get("GEMINI_API_KEY", None)
if apikey:
    genai.configure(api_key=apikey)


def load_bg_base64(relative_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir,"assets", relative_path)
    try:
        with open(full_path,"rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return ""
    

current_bg_flie = "homepage.jpg" if st.session_state.page == 1 else \
                  "metrics.jpg" if st.session_state.page ==2 else \
                  "description.jpg" if st.session_state.page ==3 else \
                  "workout plan page.jpg" if st.session_state.page ==4 else "diet page.jpg"
b64_string = load_bg_base64(current_bg_flie)
bg_rule = f'url("data:image/jpg;base64,{b64_string}")'


st.markdown(f"""
<style>
    /* Global App Setup */
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-image: linear-gradient(rgba(10, 12, 22, 0.85), rgba(10, 12, 22, 0.92)), {bg_rule} !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}
    
    
   div.stButton > button, div.stButton > button:hover, div.stButton > button:focus, div.stButton > button:active {{
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        padding: 14px 30px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.8) !important;
        width: 100% !important;
        transition: transform 0.1s ease-in-out, box-shadow 0.1s ease-in-out !important;
    }}

    div.stButton > button:hover {{
        transform: translateY(-2px);
        background: linear-gradient(135deg,#0f172a 0%, #14532d 100%) !important;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.35) !important;
    }}

    /* PREMIUM DYNAMIC GLOW TYPOGRAPHY */
    .brand-title {{
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        text-align: center !important;
        color: #F8FAFC !important;
        text-shadow: 0px 0px 25px rgba(255, 255, 255, 0.08) !important;
        margin: 0px 0px 5px 0px !important;
        padding: 0px !important;
    }}
    
    .brand-catchy-sub {{
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        color:#F8FAFC  !important;
        margin-bottom: 5px !important;
    }}

    .brand-sub {{
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        text-align: center !important;
        color: #CBD5E1 !important;
        letter-spacing: 1px !important;
        margin-bottom: 25px !important;
    }}

    
</style>
""", unsafe_allow_html=True)


def switchpage(target_page):
    st.session_state.page = target_page
    st.rerun()

def compute_metrics():
    weight = st.session_state.user_input["weight"]
    height = st.session_state.user_input["height"] / 100.0
    age = st.session_state.user_input["age"]
    sex = st.session_state.user_input["sex"]

    bmi = weight / (height ** 2)

    if sex == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * st.session_state.user_input["height"]) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * st.session_state.user_input["height"]) - (4.330 * age)

    target_calories = bmr * 1.2
    return bmi, bmr, target_calories


def beginner_workout_plan(goal):

    plans = {

        "General Fitness": [
            ["Day 1", "Full Body Strength",
             "Bodyweight Squats, Incline Push-ups, Glute Bridge, Dumbbell Row",
             "3 x 12", "60 sec"],

            ["Day 2", "Cardio + Core",
             "Brisk Walk, Bird Dog, Plank",
             "3 x 30 sec", "45 sec"],

            ["Day 3", "Upper Body",
             "Shoulder Press, Chest Press, Bicep Curl",
             "3 x 12", "60 sec"],

            ["Day 4", "Mobility & Recovery",
             "Stretching, Yoga Flow, Foam Rolling",
             "20-30 min", "-"],

            ["Day 5", "Lower Body",
             "Step Ups, Romanian Deadlift, Calf Raises",
             "3 x 12", "60 sec"],

            ["Day 6", "Full Body Circuit",
             "Squats, Push-ups, Rows, Shoulder Press",
             "3 Rounds", "90 sec"],

            ["Day 7", "Recovery",
             "Walking + Stretching",
             "30 min", "-"]
        ],


        "Fat Loss": [

            ["Day 1","HIIT + Full Body",
             "Jumping Jacks, Squats, Push-ups",
             "3 Rounds","45 sec"],

            ["Day 2","Cardio",
             "Brisk Walk / Cycling",
             "40 min","-"],

            ["Day 3","Upper Body",
             "Chest Press, Shoulder Press, Rows",
             "3 x 15","60 sec"],

            ["Day 4","Recovery",
             "Yoga + Mobility",
             "30 min","-"],

            ["Day 5","Lower Body",
             "Squats, Lunges, Glute Bridge",
             "3 x 15","60 sec"],

            ["Day 6","Full Body Circuit",
             "Burpees, Mountain Climbers, Pushups",
             "4 Rounds","60 sec"],

            ["Day 7","Recovery Walk",
             "Walking + Stretching",
             "30 min","-"]
        ],


        "Muscle Gain":[

            ["Day 1","Chest + Triceps",
             "Bench Press, Incline Press, Tricep Pushdown",
             "4 x 10","90 sec"],

            ["Day 2","Back + Biceps",
             "Lat Pulldown, Rows, Bicep Curl",
             "4 x 10","90 sec"],

            ["Day 3","Legs",
             "Squats, Leg Press, Ham Curl",
             "4 x 12","90 sec"],

            ["Day 4","Recovery",
             "Stretching",
             "20 min","-"],

            ["Day 5","Shoulders",
             "Shoulder Press, Lateral Raise",
             "4 x 10","90 sec"],

            ["Day 6","Full Body",
             "Compound Exercises",
             "3 Rounds","90 sec"],

            ["Day 7","Recovery",
             "Walking",
             "30 min","-"]

        ]

    }

    return plans[goal]



def generate_workout(level):
    model= genai.GenerativeModel("gemini-2.5-flash")
    workout_prompt= f"""
    you are an experienced certified strength &onditioning coach, biometric expert.
    your task is to create a personalized, practical,easy to follow 7 days workout plan based on thier fitness level , body metrics, health profile and lifestyle>
    // user profile
    -Name: {st.session_state.user_input['name']}
    - Age/Sex: {st.session_state.user_input['age']} years old, {st.session_state.user_input['sex']}
    - Current Weight: {st.session_state.user_input['weight']} kg | Height: {st.session_state.user_input['height']} cm
    - Program Duration Block: Full sequence for exactly 7 consecutive days.
    -Critical Medical Restrictions: {st.session_state.user_input['medical_history']}
    
    

    // your responsibilities
    1. analyze complete user profile internally. Do not explain your reasoning.
    2. fitness level :{level}, create the workout according to the selected fitness level only.
       -Workout Structure:

       • If Fitness Level = Intermediate:
         Use muscle-group split training with moderate intensity.

       • If Fitness Level = Advanced:
         Use advanced split routines with compound lifts, accessory work and progressive overload.
    3.decide primary goal internally and directly generate the workout plan. Do not explain why you selected the goal.
      - fat loss
      - muscle gain
      -maintenance
      -general fitness
    4. personalize workout intensity, sets,reps, exercise selection and recovery accordingly.
    5. if {st.session_state.user_input['medical_history']} are present modify the plan with safer alternaives. 
    6. important : the entire plan should besafe, realistic and sustainable.

    //OUTPUT STRUCTURE REQUIREMENTS:
    
    1. Present the full daily routine timeline layout using a perfectly structured Markdown Table with these precise column segments:
    | Day  | Focus | Exercise | Sets x Reps  | Rest  |
    2. Provide only 4 'Injury Prevention & Recovery Tips'bullet points  at the bottom.

    very important
    1. keep the response between 300-550 words.
    2. use simple language.
    3.the workout schedule should take most of the response.
    4.max 5 exercises per day
    5.each exercise should be written on a new line , avoid long paragraphs, do not explain exercises, no scientific concepts
    6.use onlu markdown.
    7.do not use HTML tags specially no <br> tags.
    8. the user is opening this page to immediately start working out not to read an article, prioritize work out plan , 90% response should be the plan and only 10% for recovery tips """

    response = model.generate_content(workout_prompt)
    return response.text



if st.session_state.page == 1:
    col1,col2=st.columns([6,7])
    with col1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<h1 class="brand-name">NUTRI<span style="color:#22C55E;">GEN.</span> </h1>', unsafe_allow_html=True)
        st.markdown("""
        <I>YOUR PROFILE . YOUR NUTRITION . YOUR WAY</I> \n 
        <hr>
        NutriGen caters fitness enthusiasts, health-conscious individuals, and those seeking dietary guidance. \n
        Inspired by the desire to make personalized nutrition accessible, NutriGen was born out of a passion for health and technology.\n
        Instead of a one-size-fits-all approach, NutriGen offers tailored meal plans based on individual profiles, preferences, goals and budget.\n
        This approach allows us to deliver two distinct target plans: a kinetic exercise split confifured safetly to bypass injury risks, and a budget friendly meal plan that optimizes nutrition without breaking the bank.\n
        """, unsafe_allow_html=True)
    
        st.write(" ")
        if st.button("GET STARTED ⇨", key="p1_button"):
            switchpage(2)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""<style>button[key="p1_button"] {background: linear-gradient(130deg,#e11d48 0%,#9f1239 100%) !important; color: white !impoetant; border-radius:50px !important; padding:14px 40px !important; font-weight: bold !important;}</style>""", unsafe_allow_html=True)


elif st.session_state.page == 2:
    st.write(" ")
    left_space, center_corner, right_space = st.columns([1,10,1])

    with center_corner:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color:#F8FAFC ; margin-bottom:30px;'> Let's Build Your Personalized <I>NUTRI<span style='color:#22C55E;'>GEN. </span></I> Plan! </h2>", unsafe_allow_html=True)

        form_col1, form_col2 = st.columns(2)
        with form_col1:
            in_name=st.text_input("Full Name", value=st.session_state.user_input["name"])
            in_age=st.number_input("Age", min_value=13, max_value=100, value=st.session_state.user_input["age"])
            in_height=st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=float(st.session_state.user_input["height"]))
            in_weight=st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=float(st.session_state.user_input["weight"]))

        with form_col2:
            in_sex=st.selectbox("Sex", ["Male", "Female","Prefer not to say"], index=["Male", "Female","Prefer not to say"].index(st.session_state.user_input["sex"]))
            in_dietary_preferences=st.selectbox("Dietary Preferences",["None", "Vegetarian", "Vegan", "keto", "Non Vegetarian"], index=["None", "Vegetarian", "Vegan", "keto", "Non Vegetarian"].index(st.session_state.user_input["dietary_preferences"]))
            in_budget= st.select_slider("User Budget", options=["Student Pocket / Frugal", "Moderate / Balanced", "Premium / High-End"], value=st.session_state.user_input["budget"])
            in_medical_history= st.multiselect("Medical History (if any)", ["None","Diabetes", "Hypertension", "Heart Disease", "Kidney Disease", "Liver Disease", "Thyroid Disorder", "PCOS/PCOD/Hormonal Imbalance", "Knee/Joint Issues"], default=st.session_state.user_input["medical_history"])
        st.write(" ")
        btn_layout_l, btn_layout_c, btn_layout_r = st.columns([2, 4, 2])
        with btn_layout_c:
            if st.button("CALIBRATE MY NUTRIGEN PLAN ⇨", key="p2_button", use_container_width=True):
                if not in_name.strip():
                    st.error("Please enter your name.")
                else:
                    st.session_state.user_input = {
                        "name": in_name,
                        "age": in_age,
                        "height": in_height,
                        "weight": in_weight,
                        "sex": in_sex,
                        "dietary_preferences": in_dietary_preferences,
                        "budget": in_budget,
                        "medical_history": in_medical_history
                    } 
                    switchpage(3)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""<style>button[key="p2_button"] {background: linear-gradient(130deg,#facc15 0%,#ca8a04 100%) !important; color: #0f172a !important; border-radius:30px !important; padding:13px 35px !important; font-weight: bold !important;}</style>""", unsafe_allow_html=True)
    

elif st.session_state.page == 3:
    left_space, center_corner, right_space = st.columns([1,10,1])
    with center_corner:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        bmi,bmr,calories=compute_metrics()

        st.markdown(f"""
        <h2> 👋🏼 Welcome, {st.session_state.user_input['name'].title()}!</h2>
         <p style="font-size:18px;color:#bdbdbd;">
        Here's your Personalized  <b>NUTRI<span style='color:#22C55E;'>GEN. </span></b> Health Report </p>""", unsafe_allow_html=True)
        st.divider()

        
        
        if bmi<18.5:
                bmi_category = "⚠️Underweight"
                bar_color ="#2680C9"
                bmi_explanation = "Your BMI indicates that you are underweight. It's important to focus on a nutrient-dense diet and consider strength training to build muscle mass."
        elif 18.5<=bmi<25:
                bmi_category = "✅Normal Weight"
                bar_color ="#22c55e"
                bmi_explanation = "Your BMI is within the normal range. Maintain a balanced diet and regular exercise to keep up your good work!"
        elif 25<=bmi<30:
                bmi_category = "⚠️Overweight"
                bar_color ="#eb910a"
                bmi_explanation = "Your BMI indicates that you are overweight. Focus on a balanced diet with portion control and incorporate regular physical activity to achieve a healthier weight."
        else:
                bmi_category = "⚠️Obese"
                bar_color ="#D31616"
                bmi_explanation = "Your BMI indicates that you are in the obese category. It's important to consult with a healthcare professional in order to check for any underlying health conditions and to create a comprehensive plan that includes dietary changes, physical activity, and possibly medical interventions."
        bmr_explanation = f"Your Basal Metabolic Rate (BMR) is approximately {bmr:.0f} calories/day. This is the number of calories your body needs to maintain basic physiological functions at rest. To maintain your current weight, you would need to consume around {calories:.0f} calories/day based on a sedentary activity level."
        
        st.write(" ")




        st.markdown(f" 👩‍⚕️BIOLOGICAL EVALUATION METRICS")
        col__1, col__2 =st.columns(2)
        with col__1:
            st.metric(
                label="BMI🏋🏼‍♂️",
                value=f"{bmi:.1f}")
            
           
            st.markdown(
                f"<h3 style='color:{bar_color};margin-top:-10px;'>{bmi_category}</h3>", unsafe_allow_html=True)
            st.write(bmi_explanation)
            

        with col__2:
            st.metric(
                label="BMR🔥",
                value=f"{bmr:.0f} kcal/day",
                
        )
            st.write(bmr_explanation)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("🍽️Recommended Daily Calories")
        cal_col1, cal_col2, cal_col3 = st.columns(3)

        with cal_col1:
            st.metric(label="Fat Loss / Cutting Goal 🏃🏼‍♀️",value=f"{calories - 400:.0f} kcal/day", delta="-400 kcal Deficit")
        with cal_col2:
            st.metric(label=" Maintenance/ Safe Goal 🧘🏼‍♀️ ", value=f"{calories:.0f} kcal/day",delta="Baseline Energy Level")
        with cal_col3:
            st.metric(label=" Clean Bulking / Muscle Gain 💪🏼", value=f"{calories + 400:.0f} kcal/day",delta="+400 kcal Surplus")

        st.caption("These calorie targets are estimated using your BMR, BMI and personal profie")

        st.write(" ")
        st.markdown("""
            WHAT'S NEXT? CHOOSE THE PLAN YOU'D LIKE  <I>NUTRI <span style='color:#22C55E;'> GEN. </span></I> TO GENERATE FOR YOU""" , unsafe_allow_html=True)


        b_col1, b_col2 = st.columns(2)
        with b_col1:
            

            if st.button("⛹🏼‍♀️WORKOUT PLAN", use_container_width=True):
                              
                switchpage(4)


        with b_col2:
            if st.button("🫐DIETARY PLAN", use_container_width=True):
                switchpage(5) 

        st.write(" ")
        if st.button("⇦ Go Back & Edit Profile"):
            switchpage(2)
        st.markdown('</div', unsafe_allow_html=True)



elif st.session_state.page ==4:
    if "current_level" not in st.session_state:
        st.session_state.current_level ="Beginner"

    left_space, center_corner , right_space = st.columns([1,10,1])
    with center_corner:
        st.markdown('<div class="glass-panel">', unsafe_allow_html= True)
        st.markdown("""
<h1 style= "font-size:38px; margin-bottom:0;"> YOUR PERSONALIZED WORKOUT PLAN </h1>
<p style="color:#bdbdbd; font-size:18px;"> Your Weekly Workout Routine Based On Your <I>NUTRI <span style='color:#22C55E;'> GEN. </span></I> Health Profile.</p>
""", unsafe_allow_html=True)
        bmi, bmr, calories=compute_metrics()
        if bmi<18.5:
            st.session_state.goal = "Muscle Gain"

        elif bmi>=25:
            st.session_state.goal = "Fat Loss"

        else:
           st.session_state.goal = "General Fitness"

        
        
        if st.session_state.get("workout_plan") is None:
            
            plan = beginner_workout_plan(st.session_state.goal)
            st.subheader("✅ NUTRI-GEN Recommended Beginner Plan")
            st.success(f"Primary Goal : {st.session_state.goal}")

            table = []
            for row in plan:
                table.append({
                    "Day": row[0],
                    "Focus": row[1],
                    "Exercise": row[2],
                    "Sets × Reps": row[3],
                    "Rest": row[4]
                })

            st.table(table)
            st.caption("""
⚠️ Health Advisory: *This is a generalized plan suitable for all healthy individuals.*  If you have *knee/joint* issues, avoid heavy lower-body and high-impact exercises.
If you have *hypertension or heart disease*, avoid heavy weightlifting, breath-holding, and high-intensity workouts.
Modify exercises as needed and consult your healthcare provider before starting a new fitness routine.
""")    
        else:
            st.markdown(st.session_state.workout_plan)

        
            
        
    
        st.divider()
        st.markdown("""
        👀LOOKING FOR MORE INTENSE & PERSONALIZED ROUTINE?\n
        *Upgrade your workout plan based on you fitness level* ⇩
        """)
        if st.session_state.current_level == "Beginner":
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚴🏼‍♀️ Intermediate", use_container_width=True):
                    if "intermediate_plan" not in st.session_state:
                        with st.spinner("Creating Intermediate workout..."):
                            st.session_state.intermediate_plan = generate_workout("Intermediate")

                    st.session_state.workout_plan = st.session_state.intermediate_plan
                    st.session_state.current_level = "Intermediate"
                    st.rerun()

            with col2:
               if st.button("💪 Advanced", use_container_width=True):
                if "advanced_plan" not in st.session_state:
                    with st.spinner("Creating Advanced workout..."):
                        st.session_state.advanced_plan = generate_workout("Advanced")
                st.session_state.workout_plan = st.session_state.advanced_plan
                st.session_state.current_level = "Advanced"
                st.rerun()


        elif st.session_state.current_level == "Intermediate":
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⇦ Beginner", use_container_width=True):
                    st.session_state.workout_plan = None
                    st.session_state.current_level = "Beginner"
                    st.rerun()

            with col2:
                if st.button("💪 Advanced", use_container_width=True):
                    if "advanced_plan" not in st.session_state:
                        with st.spinner("Creating Advanced workout..."):
                            st.session_state.advanced_plan = generate_workout("Advanced")

                    st.session_state.workout_plan = st.session_state.advanced_plan
                    st.session_state.current_level = "Advanced"
                    st.rerun()


        elif st.session_state.current_level == "Advanced":
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⇦ Beginner", use_container_width=True):
                    st.session_state.workout_plan = None
                    st.session_state.current_level = "Beginner"
                    st.rerun()

            with col2:
                if st.button("🚴🏼‍♀️ Intermediate", use_container_width=True):
                    if "intermediate_plan" not in st.session_state:
                        with st.spinner("Creating Intermediate workout..."):
                            st.session_state.intermediate_plan = generate_workout("Intermediate")

                    st.session_state.workout_plan = st.session_state.intermediate_plan
                    st.session_state.current_level = "Intermediate"
                    st.rerun()
        
        if st.button("⇦ Go Back to Health Report"):
            switchpage(3)
        st.markdown('</div', unsafe_allow_html=True)


elif st.session_state.page ==5:
    if "diet_plan" not in st.session_state: st.session_state.diet_plan=None
    left_space,center_corner,right_space = st.columns([1,10,1])
    with center_corner:
        st.markdown('<div class= "glass-panel">', unsafe_allow_html=True)
        st.markdown("""
<h1 style="font-size:38px; margin-bottom:0;">
🥗 YOUR PERSONALIZED DIET PLAN
</h1>

<p style="color:#bdbdbd;font-size:18px;">
A 7-Day AI Nutrition Plan Designed Around Your
<i>NUTRI <span style='color:#22C55E;'>GEN.</span></i>
Health Profile.
</p>
""", unsafe_allow_html=True)
        bmi,bmr,calories = compute_metrics()

        if bmi <18.5:
            goal="Muscle Gain"

        elif bmi>=25:
            goal="Fat Loss"

        else:
            goal="General Fitness"

        st.session_state.goal=goal
        
        
        
        protein = round(st.session_state.user_input["weight"] * 1.6)
        bmi_status = (
            "Underweight 📉" if bmi < 18.5 else
            "Healthy Range ✅" if bmi < 25 else
            "Overweight ⚠️")
        
        if st.session_state.diet_plan is None:

            c1, c2, c3,  = st.columns(3)
            with c1:
                st.metric(
                    label="🎯 Goal",
                    value=goal,
                    delta="Current Focus"
                )

            with c2:
                st.metric(
                    label="🔥 Calories",
                    value=f"{calories:.0f} kcal",
                    delta="Daily Target"
                )

            with c3:
                st.metric(
                    label="🍗 Protein",
                    value=f"{protein} g",
                    delta="Daily Goal"
                )
            st.caption("💡 These targets are estimated using your BMI, BMR, activity level and personalized health profile.")
                
            st.warning(f"""
            **🥬 Dietary Preference :**
            {st.session_state.user_input["dietary_preferences"]}
            **💰 Budget :**
            {st.session_state.user_input["budget"]}

            **🏥 Medical History :**
            {st.session_state.user_input["medical_history"]}""")

            
            st.markdown("""
            *NutriGen* will generate a fully personalized **7-Day Diet Plan**
            based on your BMI, calorie target, dietary preference,
            budget and medical history.""")
            if st.button("🍵 Generate Personalized Diet Plan",use_container_width=True):
                with st.spinner("Creating your personalized 7-Day Nutrition Plan..."):
                    bmi,bmr,calories = compute_metrics()
                    st.session_state.diet_plan = generate_diet(bmi,bmr,calories,st.session_state.user_input)

                    st.rerun()


        else:
            
            st.markdown(st.session_state.diet_plan)

            st.divider()
        left,right=st.columns(2)

        with left:
            if st.button("⇦ Return to Health Report",use_container_width=True):
                switchpage(3)

        with right:

           if st.button("↺ Regenerate Diet Plan",use_container_width=True):
            with st.spinner("Generating a fresh meal plan..."):
                st.session_state.diet_plan=None

                st.rerun()            

