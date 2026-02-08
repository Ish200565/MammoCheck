from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import io
import time
import numpy as np
import timm  # <--- make sure you have timm installed (pip install timm)
import os
from datetime import timedelta
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'mammocheck_secret_key_2024'  # Change this to a random secret key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Configure OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# -----------------------------
# LOAD YOUR PYTORCH MODEL
# -----------------------------
import torch
import timm

MODEL_PATH = 'model/best_deit_model.pth'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Try to load the model, but continue if it doesn't exist
model = None
try:
    # Recreate your model architecture
    model = timm.create_model('deit_base_patch16_224', pretrained=False, num_classes=4)

    # Load the state dict if file exists
    if os.path.exists(MODEL_PATH):
        state_dict = torch.load(MODEL_PATH, map_location=DEVICE)

        # If the model was saved with nn.DataParallel, strip "module." prefix
        if any(k.startswith("module.") for k in state_dict.keys()):
            from collections import OrderedDict
            new_state_dict = OrderedDict()
            for k, v in state_dict.items():
                new_state_dict[k.replace("module.", "")] = v
            state_dict = new_state_dict

        # Load weights safely
        model.load_state_dict(state_dict, strict=False)
        model.to(DEVICE)
        model.eval()
        print(f"✓ Model loaded successfully from {MODEL_PATH}")
    else:
        print(f"⚠ Model file not found at {MODEL_PATH}")
        print("⚠ Running in demo mode without classification")
        model = None
except Exception as e:
    print(f"⚠ Error loading model: {str(e)}")
    print("⚠ Running in demo mode without classification")
    model = None


# -----------------------------
# DEFINE LABELS
# -----------------------------
CLASS_NAMES = ['Fatty', 'Scattered', 'Heterogeneously dense', 'Extremely dense (High Risk of Cancer)']

# -----------------------------
# DEFINE TRANSFORMS
# -----------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),   # adjust to your model input
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return transform(image).unsqueeze(0)

@app.route('/')
def index():
    # Check if user is already logged in
    if 'user_role' in session:
        if session['user_role'] == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif session['user_role'] == 'radiologist':
            return redirect(url_for('radiologist_dashboard'))
    return render_template('landing.html')

@app.route('/login/google/<role>')
def google_login(role):
    """Initiate Google OAuth login with role parameter"""
    if role not in ['doctor', 'radiologist']:
        return redirect(url_for('index'))
    
    # Store the intended role in session before redirecting to Google
    session['intended_role'] = role
    
    # Redirect to Google OAuth
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        # Get the authorization token
        token = google.authorize_access_token()
        
        # Get user info from Google
        user_info = token.get('userinfo')
        
        if user_info:
            # Store user information in session
            session['user_email'] = user_info.get('email')
            session['user_name'] = user_info.get('name')
            session['user_picture'] = user_info.get('picture')
            session['logged_in'] = True
            session.permanent = True
            
            # Get the intended role from session
            role = session.get('intended_role', 'doctor')
            session['user_role'] = role
            
            # Redirect based on role
            if role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                return redirect(url_for('radiologist_dashboard'))
        else:
            return redirect(url_for('index'))
            
    except Exception as e:
        print(f"OAuth error: {str(e)}")
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    """Handle direct login from the two-role selection (backward compatibility)"""
    data = request.get_json()
    role = data.get('role')
    
    if role in ['doctor', 'radiologist']:
        session['user_role'] = role
        session['logged_in'] = True
        session.permanent = True
        
        if role == 'doctor':
            return jsonify({'success': True, 'redirect': url_for('doctor_dashboard')})
        else:
            return jsonify({'success': True, 'redirect': url_for('radiologist_dashboard')})
    
    return jsonify({'success': False, 'error': 'Invalid role'}), 400

@app.route('/doctor')
def doctor_dashboard():
    """Doctor dashboard page"""
    if 'user_role' not in session or session['user_role'] != 'doctor':
        return redirect(url_for('index'))
    
    # You can fetch reports from database here if you have one
    reports = []  # Replace with actual database query if needed
    
    return render_template('doctor_new.html', reports=reports)

@app.route('/radiologist')
def radiologist_dashboard():
    """Radiologist dashboard page"""
    if 'user_role' not in session or session['user_role'] != 'radiologist':
        return redirect(url_for('index'))
    
    return render_template('radiologist_new.html')

@app.route('/logout')
def logout():
    """Clear session and logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/predict', methods=['POST'])
def predict():
    predictions = []

    # Check if model is loaded
    if model is None:
        # Return demo predictions if model not available
        for key in ['LCC', 'LMLO', 'RCC', 'RMLO']:
            predictions.append({
                'view': key,
                'prediction': 1,
                'label': 'Demo Mode - Model Not Loaded',
                'confidence': '0.00%',
                'time': '0.0000s'
            })
        return jsonify({'results': predictions})

    for key in ['LCC', 'LMLO', 'RCC', 'RMLO']:
        file = request.files.get(key)
        if not file:
            predictions.append({'view': key, 'error': 'No file uploaded'})
            continue

        img_tensor = preprocess_image(file.read()).to(DEVICE)

        start = time.time()
        with torch.no_grad():
            outputs = model(img_tensor)
            probs = F.softmax(outputs, dim=1)
            conf, pred_class = torch.max(probs, 1)
        end = time.time()

        predictions.append({
            'view': key,
            'prediction': int(pred_class.item()),
            'label': CLASS_NAMES[pred_class.item()],
            'confidence': f"{conf.item() * 100:.2f}%",
            'time': f"{end - start:.4f}s"
        })

    return jsonify({'results': predictions})

if __name__ == '__main__':
    app.run(debug=True)
