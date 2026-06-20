import streamlit as st
import google.generativeai as genai

def generate_diet(bmi,bmr,calories,user_input):

    

    model = genai.GenerativeModel("gemini-2.5-flash")

    diet_prompt = f"""
You are an experienced Registered Clinical Dietitian, Sports Nutritionist and Preventive Healthcare Expert.

Create a fully personalized, practical and sustainable 7-Day Diet Plan.

=========================
USER PROFILE
=========================

Name : {st.session_state.user_input["name"]}

Age : {st.session_state.user_input["age"]}

Gender : {st.session_state.user_input["sex"]}

Height : {st.session_state.user_input["height"]} cm

Weight : {st.session_state.user_input["weight"]} kg

BMI : {bmi:.1f}

Daily Calories : {calories:.0f} kcal/day

Primary Goal : {st.session_state.goal}

Diet Preference : {st.session_state.user_input["dietary_preferences"]}

Budget : {st.session_state.user_input["budget"]}

Medical History :
{st.session_state.user_input["medical_history"]}

====================================================
YOUR RESPONSIBILITIES
====================================================

1. Analyze the complete profile internally.
Do NOT explain your reasoning.

2. Create a realistic 7-Day diet plan.

3. Match the user's calorie target as closely as possible.

4. Personalize according to:
• BMI
• Primary Goal
• Dietary Preference
• Budget
• Medical Conditions

5. Recommend locally available foods.

6. Recommend foods that are easy to prepare.

7. If Budget is low:
Recommend affordable foods.

8. If medical conditions exist:
Modify meals accordingly.

9. Never recommend unsafe foods.

10. Never recommend alcohol, tobacco, medicines or supplements.

11. Avoid repeating the same meals on consecutive days.

====================================================
OUTPUT FORMAT
====================================================


--------------------------------------------

## 📅 Day 1

🌅 Breakfast

🥜 Mid-Morning Snack

🍛 Lunch

☕ Evening Snack

🌙 Dinner

--------------------------------------------

Continue the same format until Day 7.

--------------------------------------------
## ✅ Foods To Prefer

Exactly 5 bullet points.
--------------------------------------------
## 🚫 Foods To Limit

Exactly 5 bullet points.
--------------------------------------------
## 💰 Budget Friendly Swaps

Provide 4 affordable substitutions whenever possible.

Example:

Paneer → Soya Chunks

Almonds → Roasted Chana

Greek Yogurt → Curd

Quinoa → Brown Rice
--------------------------------------------
## ⚠️ Personalized Health Notes

Generate ONLY if Medical History is NOT "None".

Maximum 4 concise bullet points.
====================================================
IMPORTANT RULES
====================================================
STRICT OUTPUT RULES (MUST FOLLOW):

1. Do NOT write long paragraphs.
2. Keep the entire response under 800 words.
3. Use Markdown headings only.
4. Present the 7-day diet ONLY in Markdown tables.
5. Every day must have exactly these meals:
   - Breakfast
   - Mid-Morning Snack
   - Lunch
   - Evening Snack
   - Dinner
6. Mention approximate calories for each meal.
7. Mention protein source in every meal.
8. Recommend affordable local Indian foods according to the user's budget.
9. If the user has any medical condition, modify the meal plan accordingly.
10. At the end provide ONLY these 3 sections:
   - Foods to Avoid
   - ## ⚠️ Personalized Health Notes Generate ONLY if Medical History is NOT "None".Maximum 4 concise bullet points
   
11. Do NOT explain nutrition science.
12. Do NOT repeat the same advice multiple times.
13. Output ONLY the diet plan. No introduction or conclusion.
14. Health summary in horizontal table
"""

    response = model.generate_content(diet_prompt)

    return response.text