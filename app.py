import streamlit as st

# Function to load the HTML template from a file
def load_html_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to get status configurations
def get_status_config(status):
    configs = {
        'scheduled': {'icon': '🟡', 'text': 'Scheduled', 'class': 'scheduled', 'end_label': 'Scheduled for'},
        'in-progress': {'icon': '🔵', 'text': 'In Progress', 'class': 'in-progress', 'end_label': 'Expected completion'},
        'completed': {'icon': '✅', 'text': 'Complete', 'class': 'completed', 'end_label': 'Completed'},
        'cancelled': {'icon': '❌', 'text': 'Cancelled', 'class': 'cancelled', 'end_label': 'Cancelled at'}
    }
    return configs.get(status, configs['scheduled'])

# Function to format datetime for display
def format_datetime(datetime_str):
    if not datetime_str:
        return 'Not specified'
    from datetime import datetime
    dt_object = datetime.fromisoformat(datetime_str)
    return dt_object.strftime('%b %d, %I:%M %p UTC') # Matches your JS format

# --- Streamlit UI ---

# We'll use a sidebar for the input panel, similar to your HTML
with st.sidebar:
    st.markdown('<h2 class="panel-title" style="color:white;">📧 Maintenance Generator</h2>', unsafe_allow_html=True)
    
    # Text input for the title
    title = st.text_input("Maintenance Title", "Server Maintenance")

    # Select box for the status
    status = st.selectbox(
        "Status",
        ['scheduled', 'in-progress', 'completed', 'cancelled'],
        format_func=lambda s: f"{get_status_config(s)['icon']} {s.capitalize()}"
    )

    # Text area for the description
    description = st.text_area("Description", "Scheduled maintenance to improve system performance and security.")
    
    # Datetime inputs
    start_time_str = st.text_input("Start Date & Time (YYYY-MM-DDTHH:MM)", "")
    end_time_str = st.text_input("End Date & Time (YYYY-MM-DDTHH:MM)", "")
    
    # Multiselect for components affected
    all_components = [
        "Web Services", "API", "Database", "Authentication", "File Storage", "Email Service"
    ]
    components_affected = st.multiselect("Components Affected", all_components)
    
# --- Main Content Area (Live Preview) ---

st.markdown('<h2 class="preview-title" style="color:black;">📱 Live Preview</h2>', unsafe_allow_html=True)

# Process the data from the widgets
status_config = get_status_config(status)
formatted_start_time = format_datetime(start_time_str) if start_time_str else 'Not specified'
formatted_end_time = format_datetime(end_time_str) if end_time_str else 'Not specified'

# Format the list of affected components
components_html = ""
if components_affected:
    for component in components_affected:
        components_html += f'<div class="component-affected"><span class="check-icon">✓</span>{component}</div>'
else:
    components_html = '<div class="component-affected"><span class="check-icon">✓</span>No components specified</div>'

# Load the HTML template from the file
html_template = load_html_template("templates/maintenance_email.html")

# Replace all the placeholders
final_html = html_template.replace("{title}", title)
final_html = final_html.replace("{status_class}", status_config['class'])
final_html = final_html.replace("{status_icon}", status_config['icon'])
final_html = final_html.replace("{status_text}", status_config['text'].lower())
final_html = final_html.replace("{description}", description)
final_html = final_html.replace("{start_time}", formatted_start_time)
final_html = final_html.replace("{end_label}", status_config['end_label'])
final_html = final_html.replace("{end_time}", formatted_end_time)
final_html = final_html.replace("{components_affected}", components_html)


# Apply the CSS from your original file for styling
# This is a key step! We will inject the CSS directly into the page.
with open("templates/styles.css", "r") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Display the final, populated HTML
st.markdown(final_html, unsafe_allow_html=True)