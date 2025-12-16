import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from datetime import datetime, timedelta
import json
from collections import Counter

# EXPANDED emotion palettes with more emotions and refined colors
EMOTION_PALETTES = {
    "😊 Joyful": [(1.0, 0.95, 0.3), (1.0, 0.85, 0.2), (1.0, 0.75, 0.4), (0.95, 0.9, 0.5), (1.0, 0.88, 0.35)],
    "😢 Melancholic": [(0.25, 0.35, 0.55), (0.35, 0.45, 0.65), (0.45, 0.55, 0.75), (0.2, 0.3, 0.5), (0.55, 0.65, 0.85)],
    "😠 Furious": [(0.95, 0.15, 0.15), (0.85, 0.25, 0.1), (1.0, 0.3, 0.2), (0.75, 0.1, 0.1), (0.9, 0.45, 0.25)],
    "😌 Peaceful": [(0.55, 0.85, 0.75), (0.45, 0.95, 0.85), (0.65, 0.9, 0.9), (0.35, 0.75, 0.65), (0.75, 0.98, 0.88)],
    "😰 Worried": [(0.65, 0.55, 0.75), (0.55, 0.45, 0.65), (0.75, 0.65, 0.85), (0.45, 0.35, 0.55), (0.85, 0.75, 0.95)],
    "😍 Passionate": [(1.0, 0.25, 0.55), (0.95, 0.35, 0.75), (1.0, 0.45, 0.5), (0.9, 0.15, 0.45), (1.0, 0.55, 0.65)],
    "😴 Exhausted": [(0.45, 0.45, 0.48), (0.55, 0.55, 0.58), (0.38, 0.38, 0.42), (0.62, 0.62, 0.65), (0.5, 0.5, 0.53)],
    "💖 Grateful": [(1.0, 0.75, 0.82), (0.95, 0.65, 0.75), (1.0, 0.85, 0.92), (0.9, 0.55, 0.65), (1.0, 0.78, 0.88)],
    "🤔 Contemplative": [(0.6, 0.55, 0.7), (0.5, 0.45, 0.6), (0.7, 0.65, 0.8), (0.55, 0.5, 0.65), (0.65, 0.6, 0.75)],
    "😎 Confident": [(0.2, 0.6, 0.8), (0.3, 0.7, 0.9), (0.15, 0.5, 0.7), (0.25, 0.65, 0.85), (0.35, 0.75, 0.95)],
    "🤗 Hopeful": [(1.0, 0.8, 0.5), (0.95, 0.75, 0.6), (1.0, 0.85, 0.65), (0.9, 0.7, 0.55), (0.98, 0.82, 0.58)],
    "😔 Disappointed": [(0.5, 0.4, 0.45), (0.6, 0.5, 0.55), (0.45, 0.35, 0.4), (0.55, 0.45, 0.5), (0.65, 0.55, 0.6)]
}

# Pattern styles for different emotions
PATTERN_STYLES = {
    "😊 Joyful": {"shape": "circles", "wobble": 0.25, "layers": 12},
    "😢 Melancholic": {"shape": "flowing", "wobble": 0.4, "layers": 8},
    "😠 Furious": {"shape": "sharp", "wobble": 0.5, "layers": 15},
    "😌 Peaceful": {"shape": "smooth", "wobble": 0.15, "layers": 10},
    "😰 Worried": {"shape": "chaotic", "wobble": 0.6, "layers": 18},
    "😍 Passionate": {"shape": "swirls", "wobble": 0.35, "layers": 14},
    "😴 Exhausted": {"shape": "soft", "wobble": 0.2, "layers": 6},
    "💖 Grateful": {"shape": "hearts", "wobble": 0.3, "layers": 11},
    "🤔 Contemplative": {"shape": "geometric", "wobble": 0.25, "layers": 9},
    "😎 Confident": {"shape": "bold", "wobble": 0.3, "layers": 10},
    "🤗 Hopeful": {"shape": "ascending", "wobble": 0.28, "layers": 13},
    "😔 Disappointed": {"shape": "descending", "wobble": 0.35, "layers": 7}
}

def create_shape(center, size, style, seed):
    """Generate different shapes based on emotion style"""
    np.random.seed(seed)
    random.seed(seed)
    
    if style == "circles":
        return blob(center, size, points=200, wobble=0.2)
    elif style == "sharp":
        return sharp_blob(center, size, points=100, wobble=0.5)
    elif style == "hearts":
        return heart_shape(center, size)
    elif style == "flowing":
        return flowing_shape(center, size)
    elif style == "swirls":
        return swirl_shape(center, size)
    elif style == "geometric":
        return geometric_shape(center, size)
    elif style == "ascending":
        return ascending_shape(center, size)
    else:
        return blob(center, size, points=200, wobble=0.25)

def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    """Original wobbly blob"""
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def sharp_blob(center, r, points=100, wobble=0.5):
    """Sharp, angular shapes for anger"""
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    radii = r * (1 + wobble * np.abs(np.sin(angles * 5)))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def heart_shape(center, size):
    """Heart shape for love/gratitude"""
    t = np.linspace(0, 2 * np.pi, 100)
    x = size * 16 * np.sin(t)**3
    y = size * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
    return center[0] + x/30, center[1] + y/30

def flowing_shape(center, size):
    """Flowing, wave-like shape"""
    t = np.linspace(0, 2 * np.pi, 150)
    r = size * (1 + 0.3 * np.sin(t * 3))
    x = center[0] + r * np.cos(t)
    y = center[1] + r * np.sin(t) * 1.2
    return x, y

def swirl_shape(center, size):
    """Spiral/swirl shape"""
    t = np.linspace(0, 4 * np.pi, 200)
    r = size * (0.5 + t / (4 * np.pi))
    x = center[0] + r * np.cos(t) * 0.8
    y = center[1] + r * np.sin(t) * 0.8
    return x, y

def geometric_shape(center, size):
    """Angular, geometric shape"""
    angles = [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]
    x = [center[0] + size * np.cos(a) for a in angles]
    y = [center[1] + size * np.sin(a) for a in angles]
    return x, y

def ascending_shape(center, size):
    """Upward flowing shape for hope"""
    t = np.linspace(0, 2 * np.pi, 100)
    x = center[0] + size * np.cos(t)
    y = center[1] + size * np.sin(t) + t/10
    return x, y

def generate_emotion_art(emotion, date_str, note="", intensity=5, weather="", activities=[], seed=None):
    """Enhanced art generation with more parameters"""
    if seed is None:
        seed = hash(date_str + emotion) % 10000
    
    random.seed(seed)
    np.random.seed(seed)
    
    fig, ax = plt.subplots(figsize=(7, 9))
    ax.axis('off')
    
    # Dynamic background based on intensity
    bg_intensity = 0.98 - (intensity / 100)
    ax.set_facecolor((bg_intensity, bg_intensity, bg_intensity - 0.02))
    
    palette = EMOTION_PALETTES.get(emotion, EMOTION_PALETTES["😌 Peaceful"])
    style_info = PATTERN_STYLES.get(emotion, PATTERN_STYLES["😌 Peaceful"])
    
    # Calculate layers based on intensity and emotion
    n_layers = int(style_info["layers"] * (0.7 + intensity / 20))
    
    for i in range(n_layers):
        cx = random.uniform(0.1, 0.9)
        cy = random.uniform(0.1, 0.9)
        size = random.uniform(0.12, 0.38) * (1 + intensity / 30)
        
        x, y = create_shape((cx, cy), size, style_info["shape"], seed + i)
        
        color = random.choice(palette)
        # Vary alpha based on layer depth
        alpha = random.uniform(0.25, 0.55) * (1 - i / (n_layers * 2))
        ax.fill(x, y, color=color, alpha=alpha, edgecolor='none')
    
    # Enhanced text layout
    ax.text(0.5, 0.97, date_str, transform=ax.transAxes, 
            fontsize=13, weight='bold', color='#2c3e50', ha='center')
    ax.text(0.5, 0.93, emotion, transform=ax.transAxes, 
            fontsize=22, weight='bold', ha='center')
    
    # Intensity indicator
    intensity_text = "●" * intensity + "○" * (10 - intensity)
    ax.text(0.5, 0.89, intensity_text, transform=ax.transAxes,
            fontsize=10, color='#7f8c8d', ha='center')
    
    # Weather and activities
    y_pos = 0.08
    if weather:
        ax.text(0.5, y_pos, f"Weather: {weather}", transform=ax.transAxes,
                fontsize=9, color='#34495e', ha='center')
        y_pos -= 0.03
    
    if activities:
        activity_text = " • ".join(activities[:3])
        ax.text(0.5, y_pos, activity_text, transform=ax.transAxes,
                fontsize=8, color='#7f8c8d', ha='center', style='italic')
        y_pos -= 0.03
    
    if note:
        wrapped = note[:80] + "..." if len(note) > 80 else note
        ax.text(0.5, y_pos, f'"{wrapped}"', transform=ax.transAxes,
                fontsize=9, style='italic', color='#555', ha='center')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    return fig

def generate_mood_chart(entries):
    """Create mood tracking chart"""
    if not entries:
        return None
    
    dates = sorted(entries.keys())[-14:]  # Last 14 days
    
    # Map emotions to numerical values
    emotion_values = {
        "😊 Joyful": 9, "😍 Passionate": 8, "🤗 Hopeful": 7,
        "😎 Confident": 7, "💖 Grateful": 8, "😌 Peaceful": 6,
        "🤔 Contemplative": 5, "😴 Exhausted": 3, "😰 Worried": 3,
        "😔 Disappointed": 2, "😢 Melancholic": 2, "😠 Furious": 4
    }
    
    values = []
    intensities = []
    labels = []
    
    for date in dates:
        entry = entries[date]
        emotion = entry.get('emotion', '😌 Peaceful')
        intensity = entry.get('intensity', 5)
        
        base_value = emotion_values.get(emotion, 5)
        # Combine emotion type and intensity
        final_value = (base_value + intensity) / 2
        
        values.append(final_value)
        intensities.append(intensity)
        labels.append(date[5:])  # MM-DD
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Create gradient effect
    for i in range(len(values)):
        color = plt.cm.RdYlGn(values[i] / 10)
        ax.bar(i, values[i], color=color, alpha=0.7, width=0.8)
    
    ax.plot(range(len(values)), values, 'o-', color='#2c3e50', 
            linewidth=2, markersize=8, alpha=0.6)
    
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel('Emotional Wellbeing', fontsize=11, weight='bold')
    ax.set_ylim(0, 10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    return fig

def get_emotion_insights(entries):
    """Generate insights from emotion data"""
    if not entries:
        return {}
    
    emotions = [e['emotion'] for e in entries.values()]
    intensities = [e['intensity'] for e in entries.values()]
    
    emotion_counts = Counter(emotions)
    most_common = emotion_counts.most_common(1)[0] if emotion_counts else ("😌 Peaceful", 0)
    
    avg_intensity = sum(intensities) / len(intensities) if intensities else 5
    
    # Positive vs negative emotions
    positive = ["😊 Joyful", "😍 Passionate", "💖 Grateful", "😌 Peaceful", "😎 Confident", "🤗 Hopeful"]
    pos_count = sum(1 for e in emotions if e in positive)
    pos_ratio = (pos_count / len(emotions) * 100) if emotions else 50
    
    # Weekly trend
    recent_week = list(entries.values())[-7:] if len(entries) >= 7 else list(entries.values())
    recent_intensities = [e['intensity'] for e in recent_week]
    
    if len(recent_intensities) >= 2:
        trend = "📈 Improving" if recent_intensities[-1] > recent_intensities[0] else "📉 Declining" if recent_intensities[-1] < recent_intensities[0] else "➡️ Stable"
    else:
        trend = "➡️ Stable"
    
    return {
        "most_common": most_common[0],
        "count": most_common[1],
        "avg_intensity": round(avg_intensity, 1),
        "positivity": round(pos_ratio, 1),
        "trend": trend,
        "total": len(entries)
    }

# Streamlit App Configuration
st.set_page_config(page_title="MindCanvas - Emotion Diary", page_icon="🎨", layout="wide")

# Enhanced CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1.3rem;
        margin-bottom: 2.5rem;
        font-weight: 300;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎨 MindCanvas</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform your emotions into unique generative art • Track your mental wellbeing</div>', unsafe_allow_html=True)

# Initialize session state
if 'entries' not in st.session_state:
    st.session_state.entries = {}
if 'view_date' not in st.session_state:
    st.session_state.view_date = None

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["✨ Create Art", "📊 Analytics", "📅 Gallery", "💡 Insights"])

with tab1:
    st.header("Express Your Emotions")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_date = st.date_input("📅 Date", datetime.now())
        date_str = selected_date.strftime("%Y-%m-%d")
        
        emotion = st.selectbox("🎭 How are you feeling?", 
                              list(EMOTION_PALETTES.keys()),
                              help="Choose the emotion that best describes your current state")
        
        intensity = st.slider("💫 Intensity Level", 1, 10, 5,
                             help="1 = Very mild, 10 = Very intense")
        
        weather = st.selectbox("🌤️ Weather (optional)", 
                              ["", "☀️ Sunny", "⛅ Partly Cloudy", "☁️ Cloudy", 
                               "🌧️ Rainy", "⛈️ Stormy", "❄️ Snowy"])
        
        activities = st.multiselect("🏃 Activities (optional)",
                                   ["Work", "Exercise", "Social", "Creative", "Rest", 
                                    "Learning", "Entertainment", "Nature", "Family"],
                                   max_selections=3)
        
        note = st.text_area("✍️ Journal Entry", 
                           placeholder="What's on your mind? What happened today?",
                           max_chars=300,
                           height=120)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎨 Generate Art", use_container_width=True, type="primary"):
                st.session_state.entries[date_str] = {
                    'emotion': emotion,
                    'intensity': intensity,
                    'note': note,
                    'weather': weather,
                    'activities': activities,
                    'timestamp': datetime.now().isoformat()
                }
                st.success("✨ Entry saved!")
                st.rerun()
        
        with col_b:
            if date_str in st.session_state.entries:
                if st.button("🗑️ Delete Entry", use_container_width=True):
                    del st.session_state.entries[date_str]
                    st.success("Entry deleted")
                    st.rerun()
    
    with col2:
        st.subheader("Your Emotion Art")
        
        if date_str in st.session_state.entries:
            entry = st.session_state.entries[date_str]
            fig = generate_emotion_art(
                entry['emotion'], date_str, entry['note'], 
                entry['intensity'], entry.get('weather', ''),
                entry.get('activities', [])
            )
        else:
            fig = generate_emotion_art(emotion, date_str, note, intensity, weather, activities)
        
        st.pyplot(fig)
        plt.close(fig)
        
        st.caption("💡 Each piece is unique - the patterns, colors, and shapes reflect your emotional state")

with tab2:
    st.header("Emotional Analytics")
    
    if len(st.session_state.entries) >= 2:
        insights = get_emotion_insights(st.session_state.entries)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Entries", insights['total'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Intensity", f"{insights['avg_intensity']}/10")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Positivity", f"{insights['positivity']}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Weekly Trend", insights['trend'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Mood chart
        st.subheader("📈 Mood Tracking (Last 14 Days)")
        mood_fig = generate_mood_chart(st.session_state.entries)
        if mood_fig:
            st.pyplot(mood_fig)
            plt.close(mood_fig)
        
        st.markdown("---")
        
        # Emotion breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎭 Emotion Distribution")
            emotions = [e['emotion'] for e in st.session_state.entries.values()]
            emotion_counts = Counter(emotions)
            
            for emotion, count in emotion_counts.most_common():
                percentage = (count / len(emotions)) * 100
                st.write(f"{emotion}: {count} times ({percentage:.1f}%)")
        
        with col2:
            st.subheader("🏃 Most Common Activities")
            all_activities = []
            for entry in st.session_state.entries.values():
                all_activities.extend(entry.get('activities', []))
            
            if all_activities:
                activity_counts = Counter(all_activities)
                for activity, count in activity_counts.most_common(5):
                    st.write(f"{activity}: {count} times")
            else:
                st.info("No activities logged yet")
    
    else:
        st.info("📊 Create at least 2 entries to see your analytics!")

with tab3:
    st.header("Emotion Gallery")
    
    if st.session_state.entries:
        # Date range filter
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            date_range = st.selectbox("View", ["Last 7 Days", "Last 14 Days", "Last 30 Days", "All Time"])
        
        days_map = {"Last 7 Days": 7, "Last 14 Days": 14, "Last 30 Days": 30, "All Time": 9999}
        days = days_map[date_range]
        
        # Get entries in date range
        today = datetime.now()
        filtered_dates = [
            (today - timedelta(days=i)).strftime("%Y-%m-%d") 
            for i in range(min(days, len(st.session_state.entries)))
        ]
        filtered_dates = [d for d in filtered_dates if d in st.session_state.entries]
        filtered_dates.sort(reverse=True)
        
        # Grid display
        cols_per_row = 3
        for i in range(0, len(filtered_dates), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(filtered_dates):
                    date = filtered_dates[i + j]
                    entry = st.session_state.entries[date]
                    
                    with col:
                        st.markdown(f"**{date}**")
                        st.write(f"{entry['emotion']}")
                        
                        # Generate thumbnail
                        fig = generate_emotion_art(
                            entry['emotion'], date, "", 
                            entry['intensity'], "", []
                        )
                        st.pyplot(fig, use_container_width=True)
                        plt.close(fig)
                        
                        if st.button("📖 View Details", key=f"view_{date}", use_container_width=True):
                            st.session_state.view_date = date
                            st.rerun()
        
        # Detail view
        if st.session_state.view_date and st.session_state.view_date in st.session_state.entries:
            st.markdown("---")
            st.subheader(f"📅 {st.session_state.view_date}")
            
            entry = st.session_state.entries[st.session_state.view_date]
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**Emotion:** {entry['emotion']}")
                st.write(f"**Intensity:** {entry['intensity']}/10")
                if entry.get('weather'):
                    st.write(f"**Weather:** {entry['weather']}")
                if entry.get('activities'):
                    st.write(f"**Activities:** {', '.join(entry['activities'])}")
                if entry['note']:
                    st.write(f"**Note:** {entry['note']}")
            
            with col2:
                fig = generate_emotion_art(
                    entry['emotion'], st.session_state.view_date,
                    entry['note'], entry['intensity'],
                    entry.get('weather', ''), entry.get('activities', [])
                )
                st.pyplot(fig)
                plt.close(fig)
    else:
        st.info("🎨 No entries yet. Create your first emotion art!")

with tab4:
    st.header("💡 Wellbeing Insights")
    
    if len(st.session_state.entries) >= 5:
        insights = get_emotion_insights(st.session_state.entries)
        
        st.subheader("Your Emotional Patterns")
        
        st.write(f"**Most Frequent Emotion:** {insights['most_common']} (appeared {insights['count']} times)")
        st.write(f"**Average Intensity:** {insights['avg_intensity']}/10")
        st.write(f"**Positivity Ratio:** {insights['positivity']}% of entries were positive emotions")
        st.write(f"**Weekly Trend:** {insights['trend']}")
        
        st.markdown("---")
        
        st.subheader("Personalized Recommendations")
        
        # Generate recommendations based on data
        if insights['positivity'] < 40:
            st.warning("🌱 Your recent entries show more challenging emotions. Consider:")
            st.write("• Reaching out to a friend or loved one")
            st.write("• Practicing mindfulness or meditation")
            st.write("• Engaging in physical activity")
            st.write("• Consulting a mental health professional if feelings persist")
        elif insights['positivity'] > 70:
            st.success("🌟 You're experiencing mostly positive emotions!")
            st.write("• Keep up your current routines")
            st.write("• Share your positivity with others")
            st.write("• Document what's working well")
        else:
            st.info("✨ You're experiencing a balanced mix of emotions")
            st.write("• Continue tracking to identify patterns")
            st.write("• Notice what triggers different emotions")
            st.write("• Build on positive experiences")
        
        st.markdown("---")
        
        st.subheader("Weekly Reflection Prompts")
        st.write("🤔 What emotion appeared most this week? What might have caused it?")
        st.write("💪 What activities correlated with your best moods?")
        st.write("🌈 What's one thing you're grateful for this week?")
        st.write("🎯 What's one small change you could make next week?")
        
    else:
        st.info("💡 Create at least 5 entries to unlock personalized insights and recommendations!")
        
        st.markdown("---")
        
        st.subheader("About Emotional Wellbeing")
        st.write("""
        **Why track your emotions?**
        - 📊 Identify patterns and triggers
        - 🧠 Increase self-awareness
        - 💪 Build emotional resilience
        - 🎯 Make informed decisions about your wellbeing
        
        **Tips for journaling:**
        - Be honest with yourself
        - Write without judgment
        - Note context (activities, weather, people)
        - Review entries periodically
        - Celebrate positive moments
        """)

# Sidebar
with st.sidebar:
    st.header("🎨 MindCanvas")
    
    if st.session_state.entries:
        st.metric("📚 Total Entries", len(st.session_state.entries))
        
        # Quick stats
        recent_7 = list(st.session_state.entries.values())[-7:]
        if recent_7:
            recent_emotions = [e['emotion'] for e in recent_7]
            recent_avg = sum([e['intensity'] for e in recent_7]) / len(recent_7)
            most_recent = Counter(recent_emotions).most_common(1)[0][0]
            
            st.write(f"**This Week:**")
            st.write(f"• Most common: {most_recent.split()[0]}")
            st.write(f"• Avg intensity: {recent_avg:.1f}/10")
        
        st.markdown("---")
    
    st.subheader("📖 About")
    st.info(
        """
        **MindCanvas** transforms your emotions into unique generative art.
        
        Each emotion has its own:
        • Color palette
        • Pattern style
        • Shape characteristics
        
        Track your journey and discover emotional patterns over time.
        """
    )
    
    st.markdown("---")
    
    st.subheader("🎨 Emotion Guide")
    with st.expander("See emotion styles"):
        st.write("""
        😊 **Joyful**: Warm yellows, circular patterns
        😢 **Melancholic**: Cool blues, flowing shapes
        😠 **Furious**: Bold reds, sharp angles
        😌 **Peaceful**: Soft greens, smooth curves
        😰 **Worried**: Purples, chaotic patterns
        😍 **Passionate**: Magentas, swirling forms
        😴 **Exhausted**: Grays, soft gentle shapes
        💖 **Grateful**: Pinks, heart-like patterns
        🤔 **Contemplative**: Muted purples, geometric
        😎 **Confident**: Blues, bold shapes
        🤗 **Hopeful**: Warm oranges, ascending forms
        😔 **Disappointed**: Muted tones, descending
        """)
    
    st.markdown("---")
    
    # Export/Import data
    st.subheader("💾 Data Management")
    
    if st.session_state.entries:
        # Export as JSON
        export_data = json.dumps(st.session_state.entries, indent=2)
        st.download_button(
            label="📥 Export Data",
            data=export_data,
            file_name=f"mindcanvas_export_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Import data
    uploaded_file = st.file_uploader("📤 Import Data", type=['json'])
    if uploaded_file is not None:
        try:
            imported_data = json.loads(uploaded_file.read())
            st.session_state.entries.update(imported_data)
            st.success("✅ Data imported successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error importing data: {str(e)}")
    
    st.markdown("---")
    
    if st.button("🗑️ Clear All Data", use_container_width=True):
        if st.session_state.entries:
            st.session_state.entries = {}
            st.session_state.view_date = None
            st.success("All data cleared")
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
    Made with ❤️ for emotional wellbeing • Your data stays private in your browser
    </div>
    """,
    unsafe_allow_html=True
)
