import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

# App Header
st.title("✍️ AI Content Assistant")
st.markdown("Generate platform-optimized social media posts instantly using **Groq** (Llama 3).")

# Sidebar for API Key & Settings
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input(
        "Enter Groq API Key", 
        type="password", 
        help="Get a free key from https://console.groq.com"
    )
    
    st.markdown("---")
    st.markdown("### 📌 Instructions")
    st.markdown("1. Enter your **Groq API Key**.")
    st.markdown("2. Fill in your content requirements.")
    st.markdown("3. Click **Generate Content**!")
    st.markdown("4. Upload `app.py` & `requirements.txt` to GitHub.")
    st.markdown("5. Deploy on **Streamlit Community Cloud**.")

# Main Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["Thread / Series", "Announcement", "Educational / How-to", "Promotional / Marketing", "Thought Leadership", "Engagement / Question"]
        )
        
        platform = st.selectbox(
            "Target Platform",
            ["LinkedIn", "X (Twitter)", "Instagram", "Facebook", "Threads"]
        )
        
    with col2:
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Startup Founders, Python Developers, Fitness Beginners"
        )
        
        tone = st.selectbox(
            "Tone of Voice",
            ["Professional & Authoritative", "Casual & Friendly", "Humorous & Witty", "Inspiring & Motivational", "Direct & Concise"]
        )
        
    topic = st.text_area(
        "Topic / Core Message",
        placeholder="Briefly describe what you want to talk about..."
    )
    
    submitted = st.form_submit_button("🚀 Generate Content", use_container_width=True)

# Generation Logic
if submitted:
    api_key = api_key_input or st.secrets.get("GROQ_API_KEY", "")
    
    if not api_key:
        st.error("⚠️ Please provide a Groq API Key in the sidebar or via Streamlit Secrets.")
    elif not topic.strip():
        st.error("⚠️ Please enter a topic or core message.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an expert social media manager and copywriter. Generate a high-performing post for the following specifications:
            
            - Platform: {platform}
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience if target_audience else 'General audience'}
            - Tone: {tone}
            
            Requirements:
            1. Craft a strong, attention-grabbing hook suited for {platform}.
            2. Write clear, valuable body content tailored to the tone and audience.
            3. Include engaging captions/call-to-action (CTA).
            4. Provide 5-10 relevant, high-reach hashtags.
            5. Format cleanly with emojis and appropriate spacing.
            """
            
            with st.spinner("🤖 Generating your content with Groq..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a professional social media content creator."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )
                
                generated_text = response.choices[0].message.content
                
            st.success("✅ Content generated successfully!")
            st.markdown("### 📄 Generated Result")
            st.markdown(generated_text)
            
            # Download button
            st.download_button(
                label="📥 Download Content as TXT",
                data=generated_text,
                file_name=f"ai_post_{platform.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
