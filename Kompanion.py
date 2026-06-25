import streamlit as str_app
import streamlit.components.v1 as components
import pandas as pd
import boto3
import json
import os

# --- INITIALIZATION ENGINE ---
str_app.set_page_config(page_title="Kompanion.ai", page_icon="🤖", layout="wide")

# State Initialization
if "entered" not in str_app.session_state:
    str_app.session_state.entered = False
if "aws_mode_selection" not in str_app.session_state:
    str_app.session_state.aws_mode_selection = "No (Demo/Simulated Mode)"
if "completed_count" not in str_app.session_state:
    str_app.session_state.completed_count = 0
if "failed_count" not in str_app.session_state:
    str_app.session_state.failed_count = 0
if "telemetry_feed" not in str_app.session_state:
    str_app.session_state.telemetry_feed = [
        "🥊 **Match Initialization:** Standing in the focus ring. Waiting for task deployments...",
    ]
if "tasks" not in str_app.session_state:
    str_app.session_state.tasks = [
        {"name": "Complete AWS Architecture Diagram", "priority": "HIGH 🛡️", "hours": 2.0, "fatigue": 2, "status": "Pending", "advice": ""},
        {"name": "Study for OS Exam", "priority": "MEDIUM ⚡", "hours": 4.0, "fatigue": 4, "status": "Pending", "advice": ""},
    ]

# --- SECURE CREDENTIAL ROUTING ENGINE ---
def get_bedrock_client(aws_mode, key=None, secret=None, region="us-east-1"):
    if aws_mode == "No (Demo/Simulated Mode)":
        return None
    if key and secret:
        os.environ["AWS_ACCESS_KEY_ID"] = key
        os.environ["AWS_SECRET_ACCESS_KEY"] = secret
        os.environ["AWS_DEFAULT_REGION"] = region
    return boto3.client(service_name="bedrock-runtime", region_name=region)

def call_bedrock_advisor(failed_task, aws_mode, client=None):
    try:
        if aws_mode == "No (Demo/Simulated Mode)":
            import time
            time.sleep(1)
            return f"🤖 Kompanion Advisor (Simulated Bedrock): Your brain traded focus for instant gratification on '{failed_task}'. Pivot immediately—drop the phone and complete a clean 15-minute pomodoro block right now!"
        
        model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        prompt = f"You are an elite AI coach. The student failed this task: '{failed_task}'. Give a witty reality check and an immediate alternative strategy."
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        if client is None:
            client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
            
        response = client.invoke_model(body=body, modelId=model_id)
        response_body = json.loads(response.get("body").read())
        return response_body['content'][0]['text']
        
    except Exception as e:
        return f"🤖 Kompanion Advisor: Realigning priorities! (Live Cloud Environment Engine Warning: {str(e)})"

# --- AWS DYNAMODB STORAGE ENGINE ---
def sync_task_to_dynamodb(user_alias, task_data, aws_mode):
    if aws_mode == "No (Demo/Simulated Mode)":
        return
    try:
        dynamodb = boto3.resource(
            'dynamodb', 
            region_name=str_app.session_state.get('aws_region', 'us-east-1')
        )
        table = dynamodb.Table('KompanionTasks')
        table.put_item(
            Item={
                'user_alias': user_alias,
                'task_name': task_data['name'],
                'priority': str(task_data['priority']),
                'hours': str(task_data['hours']),
                'fatigue': int(task_data['fatigue']),
                'status': task_data['status'],
                'advice': task_data.get('advice', '')
            }
        )
    except Exception as e:
        str_app.warning(f"Cloud DB Auto-Sync Suspended: {str(e)}")

def load_tasks_from_dynamodb(user_alias, aws_mode):
    if aws_mode == "No (Demo/Simulated Mode)":
        return []
    try:
        dynamodb = boto3.resource(
            'dynamodb', 
            region_name=str_app.session_state.get('aws_region', 'us-east-1')
        )
        table = dynamodb.Table('KompanionTasks')
        
        from boto3.dynamodb.conditions import Key
        response = table.query(KeyConditionExpression=Key('user_alias').eq(user_alias))
        
        loaded_tasks = []
        for item in response.get('Items', []):
            loaded_tasks.append({
                "name": item['task_name'],
                "priority": item['priority'],
                "hours": float(item['hours']),
                "fatigue": int(item['fatigue']),
                "status": item['status'],
                "advice": item.get('advice', '')
            })
        return loaded_tasks
    except Exception as e:
        str_app.warning(f"Could not load cloud historical data maps: {str(e)}")
        return []

# --- MATHEMATICAL PROBABILITY ENGINE ---
def calculate_probability(priority, hours_allocated, fatigue_score):
    p_weight = 2
    if "LOW" in str(priority): p_weight = 1
    elif "MEDIUM" in str(priority): p_weight = 2
    elif "HIGH" in str(priority): p_weight = 3
    elif "CRITICAL" in str(priority): p_weight = 4
    
    base = 0.85
    priority_mod = (p_weight * 0.05)
    fatigue_mod = (fatigue_score * 0.08)
    time_mod = 0.05 if hours_allocated <= 2 else -0.05
    prob = (base + priority_mod - fatigue_mod + time_mod) * 100
    return min(max(int(prob), 5), 98)

# Calculate Runtime HUD Telemetry Metrics
total_decided = str_app.session_state.completed_count + str_app.session_state.failed_count
current_round = total_decided + 1

base_stability = 85 + (str_app.session_state.completed_count * 5) - (str_app.session_state.failed_count * 15)
brain_stability = min(max(base_stability, 10), 100)

base_resistance = 35 + (str_app.session_state.completed_count * 15) - (str_app.session_state.failed_count * 10)
distraction_resistance = min(max(base_resistance, 5), 100)

# Gear Cosmetic Theme Engine
if brain_stability < 50:
    gear_primary = "#2a6eff"
    gear_dark = "#103eb3"
    gear_highlight = "#70a1ff"
    corner_title = "BLUE CORNER - DEFENSIVE"
    mouth_element = '<line x1="110" y1="102" x2="130" y2="102" stroke="#1a0c0e" stroke-width="4" stroke-linecap="round"/>'
else:
    gear_primary = "#ff2a4b"
    gear_dark = "#b30d28"
    gear_highlight = "#ff7088"
    corner_title = "RED CORNER - ATTACKING"
    mouth_element = '<path d="M 110 96 Q 120 106 130 96" fill="none" stroke="#1a0c0e" stroke-width="4" stroke-linecap="round"/>'

# ==========================================
# PHASE 1: NATIVE BRAIN BOXING COCKPIT
# ==========================================
if not str_app.session_state.entered:
    _, center_col, _ = str_app.columns([1, 2, 1])
    
    with center_col:
        str_app.write("")
        str_app.markdown("<h1 style='text-align: center; font-size: 3.5rem; font-weight: 900;'>🤖 Kompanion.ai</h1>", unsafe_allow_html=True)
        str_app.markdown("<h3 style='text-align: center; color: #00ffc8;'>AWS Student Hackathon Gateway</h3>", unsafe_allow_html=True)
        str_app.markdown("---")

        mascot_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        html, body {{
            margin: 0; padding: 0; background-color: #0e1117;
            display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden;
            font-family: 'Segoe UI', Roboto, sans-serif;
        }}
        .brainpal-cockpit {{
            background: radial-gradient(circle at center, #0a1128 0%, #030712 100%);
            border: 2px solid {gear_primary}; border-radius: 20px; padding: 20px; text-align: center; width: 400px;
            box-shadow: 0 0 30px rgba(0, 255, 200, 0.2); position: relative; overflow: hidden;
        }}
        .hud-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }}
        .hud-title {{ color: #ffffff; font-size: 11px; font-weight: 900; letter-spacing: 2px; text-transform: uppercase; }}
        .status-pill {{ background: {gear_dark}; color: #ffffff; font-weight: 700; padding: 4px 12px; border-radius: 6px; font-size: 10px; border: 1px solid {gear_highlight}; }}
        @keyframes subtleFloat {{ 0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-6px); }} 100% {{ transform: translateY(0px); }} }}
        .fighter-canvas {{ animation: subtleFloat 3s ease-in-out infinite; display: block; margin: 0 auto; }}
        .energy-matrix {{ margin-top: 15px; display: flex; justify-content: center; gap: 4px; }}
        .matrix-bar {{ width: 14px; height: 6px; background: rgba(255,255,255,0.1); border-radius: 1px; }}
        .matrix-active {{ background: {gear_primary}; box-shadow: 0 0 8px {gear_highlight}; }}
        </style>
        </head>
        <body>
        <div class="brainpal-cockpit">
            <div class="hud-header">
                <span class="hud-title">BrainPal // Core Initialization</span>
                <span class="status-pill">{corner_title}</span>
            </div>
            <svg class="fighter-canvas" width="240" height="240" viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <radialGradient id="skinGrad" cx="40%" cy="40%" r="60%"><stop offset="0%" stop-color="#ffebd4"/><stop offset="100%" stop-color="#e0b18d"/></radialGradient>
                    <linearGradient id="brainCore" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff9ebb"/><stop offset="50%" stop-color="#ff4071"/><stop offset="100%" stop-color="#991b3b"/></linearGradient>
                    <radialGradient id="armorGrad" cx="40%" cy="30%" r="70%"><stop offset="0%" stop-color="{gear_highlight}"/><stop offset="60%" stop-color="{gear_primary}"/><stop offset="100%" stop-color="{gear_dark}"/></radialGradient>
                    <radialGradient id="floorGrid" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(0,255,200,0.3)"/><stop offset="100%" stop-color="rgba(0,0,0,0)"/></radialGradient>
                </defs>
                <ellipse cx="120" cy="225" rx="65" ry="12" fill="url(#floorGrid)" />
                <ellipse cx="120" cy="225" rx="45" ry="6" fill="none" stroke="{gear_highlight}" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.6" />
                <g stroke="#05070c" stroke-width="2.5" stroke-linejoin="round">
                    <path d="M 85 175 L 95 175 L 98 215 L 76 215 Z" fill="url(#armorGrad)" />
                    <path d="M 155 175 L 145 175 L 142 215 L 164 215 Z" fill="url(#armorGrad)" />
                </g>
                <g stroke="#05070c" stroke-width="2.5" stroke-linejoin="round">
                    <path d="M 75 140 L 165 140 L 170 175 L 140 175 L 120 158 L 100 175 L 70 175 Z" fill="url(#armorGrad)" />
                </g>
                <g stroke="#05070c" stroke-width="2.5" stroke-linejoin="round">
                    <rect x="84" y="105" width="72" height="45" rx="12" fill="url(#skinGrad)" />
                    <circle cx="62" cy="115" r="22" fill="url(#armorGrad)" /><circle cx="178" cy="115" r="22" fill="url(#armorGrad)" />
                </g>
                <g stroke="#05070c" stroke-width="2.5" stroke-linejoin="round"><circle cx="120" cy="78" r="46" fill="url(#skinGrad)" /></g>
                <g>
                    <circle cx="96" cy="76" r="19" fill="#141115" stroke="#1a0c0e" stroke-width="2" />
                    <circle cx="91" cy="70" r="7" fill="#ffffff" /><circle cx="102" cy="81" r="3" fill="#ffffff" />
                    <circle cx="144" cy="76" r="19" fill="#141115" stroke="#1a0c0e" stroke-width="2" />
                    <circle cx="139" cy="70" r="7" fill="#ffffff" /><circle cx="150" cy="81" r="3" fill="#ffffff" />
                </g>
                {mouth_element}
                <g stroke="#05070c" stroke-width="2.5" stroke-linejoin="round">
                    <path d="M 78 46 C 70 18, 92 6, 106 18 C 114 6, 126 6, 134 18 C 148 6, 170 18, 162 46 Z" fill="url(#brainCore)" />
                </g>
                <g stroke="#05070c" stroke-width="2.5" stroke-linejoin="round">
                    <path d="M 74 48 C 74 36, 166 36, 166 48 L 171 58 C 171 64, 162 64, 156 58 L 152 52 L 138 54 L 140 58 C 140 64, 100 64, 100 58 L 102 54 L 88 52 L 84 58 C 78 64, 69 64, 69 58 Z" fill="url(#armorGrad)" />
                    <circle cx="71" cy="56" r="8" fill="url(#armorGrad)" /><line x1="68" y1="50" x2="58" y2="36" stroke="{gear_primary}" stroke-width="3" /><circle cx="58" cy="36" r="3" fill="{gear_highlight}" stroke="none" />
                    <circle cx="169" cy="56" r="8" fill="url(#armorGrad)" /><line x1="172" y1="50" x2="182" y2="36" stroke="{gear_primary}" stroke-width="3" /><circle cx="182" cy="36" r="3" fill="{gear_highlight}" stroke="none" />
                </g>
            </svg>
            <div class="energy-matrix">
                <div class="matrix-bar matrix-active"></div><div class="matrix-bar matrix-active"></div><div class="matrix-bar matrix-active"></div>
                <div class="matrix-bar {{'matrix-active' if brain_stability > 30 else ''}}"></div>
                <div class="matrix-bar {{'matrix-active' if brain_stability > 50 else ''}}"></div>
                <div class="matrix-bar {{'matrix-active' if brain_stability > 70 else ''}}"></div>
                <div class="matrix-bar {{'matrix-active' if brain_stability > 85 else ''}}"></div>
            </div>
        </div>
        </body>
        </html>
        """
        components.html(mascot_html, height=400)
        
        str_app.markdown("### 🖥️ Environmental Runtime Selection")
        options_list = ["No (Demo/Simulated Mode)", "Yes (Live AWS Cloud Connect)"]
        default_index = options_list.index(str_app.session_state.aws_mode_selection)

        aws_selection = str_app.radio(
            "Do you wish to authorize a live connection to an AWS Cloud Account?",
            options_list,
            index=default_index,
            key="aws_radio_widget",
            horizontal=True
        )
        
        str_app.session_state.aws_mode_selection = aws_selection
        
        input_key = None
        input_secret = None
        input_region = "us-east-1"
        
        if str_app.session_state.aws_mode_selection == "Yes (Live AWS Cloud Connect)":
            str_app.info("🔐 **Leak-Proof Input Interface Enabled:** Credentials entered here exist purely in transient container memory.")
            c1, c2 = str_app.columns(2)
            input_key = c1.text_input("AWS Access Key ID:", type="password", placeholder="AKIA...")
            input_secret = c2.text_input("AWS Secret Access Key:", type="password", placeholder="wJalrXUpt...")
            input_region = str_app.text_input("Target AWS Service Region:", value="us-east-1")
        else:
            str_app.success("🛡️ **Zero-Footprint Sandbox Active:** System running on simulated local parameters.")

        str_app.markdown("---")
        user_name = str_app.text_input("Enter Dashboard Pilot Alias:", value="Championship Builder")
        
        if str_app.button("Authorize Core Sync & Initialize 🚀", use_container_width=True):
            if str_app.session_state.aws_mode_selection == "Yes (Live AWS Cloud Connect)" and (not input_key or not input_secret):
                str_app.error("🚨 Configuration Error: Key fields cannot be left blank for live cloud deployment routing.")
            else:
                str_app.session_state.user_alias = user_name
                str_app.session_state.aws_mode = str_app.session_state.aws_mode_selection
                str_app.session_state.aws_key = input_key
                str_app.session_state.aws_secret = input_secret
                str_app.session_state.aws_region = input_region
                
                if str_app.session_state.aws_mode == "Yes (Live AWS Cloud Connect)":
                    if input_key and input_secret:
                        os.environ["AWS_ACCESS_KEY_ID"] = input_key
                        os.environ["AWS_SECRET_ACCESS_KEY"] = secret_access_key = input_secret
                        os.environ["AWS_DEFAULT_REGION"] = input_region
                    
                    cloud_tasks = load_tasks_from_dynamodb(user_name, str_app.session_state.aws_mode)
                    if cloud_tasks:
                        str_app.session_state.tasks = cloud_tasks
                
                str_app.session_state.telemetry_feed.append(f"🛡️ **System Sync:** Runtime initialized under mode: `{str_app.session_state.aws_mode_selection}`.")
                str_app.session_state.entered = True
                str_app.rerun()

# ==========================================
# PHASE 2: PRIMARY DASHBOARD INTERFACE
# ==========================================
else:
    str_app.title("🤖 Kompanion.ai // Cloud Control")
    str_app.subheader(f"Pilot: {str_app.session_state.user_alias} | Mode: {str_app.session_state.aws_mode}")
    str_app.markdown("---")

    col1, col2 = str_app.columns([1, 1.8])

    with col1:
        str_app.markdown("## ⚡ Deploy New Goal")
        
        task_name = str_app.text_input("🎯 Enter Target Assignment:", placeholder="e.g., Build Bedrock Pipeline")
        
        str_app.markdown("### 🎚️ Priority Level")
        priority_tabs = str_app.tabs(["LOW ☕", "MEDIUM ⚡", "HIGH 🛡️", "CRITICAL 🔥"])
        selected_priority = "MEDIUM ⚡"
        
        with priority_tabs[0]:
            if str_app.checkbox("Select Low Weight Priority", key="p_low"): 
                selected_priority = "LOW ☕"
        with priority_tabs[1]:
            if str_app.checkbox("Select Medium Weight Priority", key="p_med", value=True): 
                selected_priority = "MEDIUM ⚡"
        with priority_tabs[2]:
            if str_app.checkbox("Select High Weight Priority", key="p_high"): 
                selected_priority = "HIGH 🛡️"
        with priority_tabs[3]:
            if str_app.checkbox("Select Critical Weight Priority", key="p_crit"): 
                selected_priority = "CRITICAL 🔥"

        str_app.markdown("### ⏱️ Time Allocation Window")
        time_tabs = str_app.tabs(["Quick Sprints", "Custom Duration"])
        chosen_hours = 1.5
        
        with time_tabs[0]:
            time_click = str_app.radio(
                "Tap a preset time structural block:",
                ["1.0 Hour Sprint", "2.0 Hour Window", "3.0 Hour Deep-Work", "4.0 Hour Extreme Session"],
                horizontal=True
            )
            if "1.0" in time_click: chosen_hours = 1.0
            elif "2.0" in time_click: chosen_hours = 2.0
            elif "3.0" in time_click: chosen_hours = 3.0
            elif "4.0" in time_click: chosen_hours = 4.0
            
        with time_tabs[1]:
            chosen_hours = str_app.slider("Fine-tune custom timeline window (Hours):", 0.5, 12.0, chosen_hours, step=0.5)

        # --- PREMIUM EXHAUSTION/BURNOUT MATRIX UPGRADE ---
        str_app.markdown("### 🧠 Current Exhaustion / Burnout Scale")
        fatigue_selection = str_app.radio(
            "Select internal neural operating load level:",
            [
                "1️⃣ Fresh & Hyperfocused", 
                "2️⃣ Steady Operations", 
                "3️⃣ Mild Cognitive Fatigue", 
                "4️⃣ High Burnout Danger", 
                "5️⃣ System Exhaustion Peak"
            ],
            index=1,
            horizontal=False,
            help="Directly adjusts task viability predictions inside the AI algorithm matrix."
        )
        # Parse the string array option back safely into a pure integer for mathematical math matrices
        fatigue = int(fatigue_selection[0])
        
        str_app.write("")
        if str_app.button("🚀 Deploy Node to Live Grid Matrix", use_container_width=True):
            if task_name.strip():
                new_task = {
                    "name": task_name, 
                    "priority": selected_priority, 
                    "hours": chosen_hours, 
                    "fatigue": fatigue, 
                    "status": "Pending", 
                    "advice": ""
                }
                str_app.session_state.tasks.append(new_task)
                str_app.session_state.telemetry_feed.append(f"⚡ Scheduled: *'{task_name}'*")
                
                if str_app.session_state.aws_mode == "Yes (Live AWS Cloud Connect)":
                    sync_task_to_dynamodb(
                        str_app.session_state.user_alias, 
                        new_task, 
                        str_app.session_state.aws_mode
                    )
                
                str_app.success("Grid tracking synchronized successfully!")
                str_app.rerun()

    with col2:
        str_app.markdown("## 📊 Live Grid Matrix")
        for i, task in enumerate(str_app.session_state.tasks):
            prob = calculate_probability(task["priority"], task["hours"], task["fatigue"])
            color = "🟢" if prob > 75 else "🟡" if prob > 45 else "🔴"
            
            with str_app.container():
                c_a, c_b, c_c = str_app.columns([2.5, 1.2, 1.3])
                c_a.markdown(f"### {task['name']}")
                c_a.caption(f"⏱️ Time Box: **{task['hours']} hrs** | Priority: **{task['priority']}**")
                c_b.metric("Viability Status", f"{color} {prob}%")
                
                if task["status"] == "Pending":
                    cd, cf = c_c.columns(2)
                    if cd.button("✅ Done", key=f"d_{i}", use_container_width=True):
                        str_app.session_state.tasks[i]["status"] = "Completed"
                        str_app.session_state.completed_count += 1
                        if str_app.session_state.aws_mode == "Yes (Live AWS Cloud Connect)":
                            sync_task_to_dynamodb(str_app.session_state.user_alias, str_app.session_state.tasks[i], str_app.session_state.aws_mode)
                        str_app.rerun()
                        
                    if cf.button("❌ Fail", key=f"f_{i}", use_container_width=True):
                        str_app.session_state.tasks[i]["status"] = "Failed"
                        str_app.session_state.failed_count += 1
                        
                        with str_app.spinner("Querying Core Intelligent Cluster..."):
                            active_client = get_bedrock_client(
                                str_app.session_state.aws_mode,
                                str_app.session_state.aws_key,
                                str_app.session_state.aws_secret,
                                str_app.session_state.aws_region
                            )
                            str_app.session_state.tasks[i]["advice"] = call_bedrock_advisor(
                                task["name"], 
                                str_app.session_state.aws_mode,
                                client=active_client
                            )
                            
                        if str_app.session_state.aws_mode == "Yes (Live AWS Cloud Connect)":
                            sync_task_to_dynamodb(str_app.session_state.user_alias, str_app.session_state.tasks[i], str_app.session_state.aws_mode)
                        str_app.rerun()
                else:
                    c_c.markdown(f"<h4 style='margin-top:15px; color:#00ffc8;'>Status: {task['status']}</h4>", unsafe_allow_html=True)
                
                if task["status"] == "Failed":
                    str_app.error("🚨 Goal Deficit Detected!")
                    str_app.info(task.get("advice") or "System Realigning...")
                str_app.markdown("---")

    if str_app.button("↩️ Log Out & Clear Architecture Session", use_container_width=True):
        str_app.session_state.entered = False
        str_app.session_state.aws_key = None
        str_app.session_state.aws_secret = None
        str_app.session_state.aws_mode_selection = "No (Demo/Simulated Mode)"
        if "AWS_ACCESS_KEY_ID" in os.environ: del os.environ["AWS_ACCESS_KEY_ID"]
        if "AWS_SECRET_ACCESS_KEY" in os.environ: del os.environ["AWS_SECRET_ACCESS_KEY"]
        str_app.rerun()