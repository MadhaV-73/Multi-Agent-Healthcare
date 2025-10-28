# Multi-Agent Healthcare Platform - Chest X-Ray Analysis


**TRY THE LIVE DEMO HERE : https://multi-agent-healthcare-nygyjngwo2hvdstsparetv.streamlit.app/**


An AI-powered respiratory healthcare platform for **chest X-ray analysis and OTC treatment recommendations** using a multi-agent architecture. Specialized in detecting pneumonia, bronchitis, COVID-19, TB, and providing location-aware pharmacy matching in Mumbai region.

## 🌟 Key Features

- **� Chest X-Ray Analysis**: AI-powered detection of respira## 👨‍💻 Author

**MadhaV** (MadhaV-73)
- GitHub: [@MadhaV-73](https://github.com/MadhaV-73)
- Repository: [Multi-Agent-Healthcare](https://github.com/MadhaV-73/Multi-Agent-Healthcare) conditions (Pneumonia, Bronchitis, TB, COVID-19 suspect, Normal)
- **🩺 Patient Intake**: Specialized intake for respiratory symptoms and chest analysis
- **💊 OTC Respiratory Therapy**: Smart recommendations for cough, fever, congestion, breathing issues
- **🏥 Pharmacy Matching**: Location-aware pharmacy inventory with respiratory medicine stock
- **👨‍⚕️ Pulmonologist Consultation**: Automatic escalation to respiratory specialists when needed
- **📄 Medical Document Processing**: Multi-file upload with OCR for chest X-ray reports
- **🔍 Full Observability**: Agent-by-agent event logs and decision tracing
- **🚀 REST API**: Production-ready FastAPI backend with automatic documentation

## 📍 Sample Data Coverage

The system ships with comprehensive sample data for **Mumbai Metropolitan Region**:

### Cities Covered (109 Pincodes - Mumbai Metropolitan Region):
- **Mumbai**: 30 pincodes (400001-400030)
- **Navi Mumbai**: 15 pincodes (400701-400715)
- **Thane**: 15 pincodes (400601-400615)
- **Kalyan**: 10 pincodes (421301-421310)
- **Panvel**: 10 pincodes (410206-410215)
- **Vasai**: 10 pincodes (401201-401210)
- **Bhiwandi**: 7 pincodes (421302-421308)
- **Mira Road**: 6 pincodes (401107-401112)
- **Virar**: 6 pincodes (401303-401308)

### Dataset Details:
- **Total Pharmacies**: 1500 across Mumbai metropolitan region
- **Inventory Records**: 1500+ with 30+ respiratory/OTC medicines
- **Doctors**: 20 specialists (Pulmonologists, Infectious Disease, General Physicians)
- **Medicine Categories**: 
  - Fever reducers (Paracetamol, Ibuprofen, Acetaminophen)
  - Cough suppressants (Dextromethorphan, Cough Syrup)
  - Expectorants (Guaifenesin, Mucolytic Syrup, Ambroxol)
  - Inhalers (Salbutamol, Budesonide)
  - Decongestants (Pseudoephedrine, Phenylephrine)
  - Bronchodilators and antihistamines (Cetirizine, Loratadine)
  - Respiratory support (Nebulizer Solution, Chest Rub, Steam Inhalation)

**All cities in the dropdown have full pharmacy matching support in Mumbai region!**

### Supported Respiratory Conditions:
- ✅ **Pneumonia** - Bacterial or viral lung infection
- ✅ **Bronchitis** - Inflammation of bronchial tubes
- ✅ **COVID-19 Suspect** - Potential coronavirus infection
- ✅ **TB Suspect** - Possible tuberculosis (escalated to specialist)
- ✅ **Normal** - Healthy chest X-ray

## 🏗️ Architecture

```
Frontend (Streamlit) ←→ Backend API (FastAPI) ←→ Multi-Agent Pipeline
     Port 8501              Port 8000
                                         
                                         ↓
                              ┌──────────────────────┐
                              │  Coordinator Agent   │
                              └──────────────────────┘
                                         ↓
              ┌──────────────────────────┼──────────────────────────┐
              ↓                          ↓                          ↓
    ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
    │ Ingestion Agent │      │  Imaging Agent  │      │  Therapy Agent  │
    │  (Patient Data) │  →   │ (Chest X-Ray AI)│  →   │ (OTC Medicines) │
    └─────────────────┘      └─────────────────┘      └─────────────────┘
                                                                  ↓
                                            ┌─────────────────────┴─────────────────┐
                                            ↓                                       ↓
                                   ┌─────────────────┐                  ┌─────────────────┐
                                   │ Pharmacy Agent  │                  │  Doctor Agent   │
                                   │ (Stock/Location)│                  │ (Pulmonologist) │
                                   └─────────────────┘                  └─────────────────┘
```

**Agent Pipeline Flow:**
1. **Ingestion** → Validates patient data & uploads chest X-ray
2. **Imaging** → AI classifies respiratory condition from X-ray
3. **Therapy** → Recommends OTC medicines based on condition
4. **Pharmacy** → Finds nearest pharmacies with stock
5. **Doctor** → Books pulmonologist if escalation needed

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (Recommended: 3.11 for best compatibility)
- pip (Python package manager)
- Git (optional, for cloning)
- 4GB RAM minimum, 8GB recommended

### Installation & Setup

#### 1️⃣ Clone or Download the Repository
```powershell
git clone https://github.com/MadhaV-73/Multi-Agent-Healthcare.git
cd Multi-Agent-Healthcare-GL
```

#### 2️⃣ Create Virtual Environment
```powershell
python -m venv .venv
```

#### 3️⃣ Activate Virtual Environment
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
.\.venv\Scripts\activate.bat
```

#### 4️⃣ Install Dependencies
```powershell
pip install -r requirements.txt
```

#### 5️⃣ Verify Data Files
Ensure the following data files exist in the `data/` directory:
- `pharmacies.json`
- `inventory.csv`
- `doctors.csv`
- `meds.csv`
- `interactions.csv`
- `zipcodes.csv`

### Running the Application

#### Option 1: Quick Start (Recommended) 🎯
Simply double-click `start_integrated.bat` or run:
```powershell
.\start_integrated.bat
```
This will launch both the API backend and Streamlit UI automatically!

#### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Backend API:**
```powershell
.\.venv\Scripts\Activate.ps1
python api/main.py
```
✅ Backend available at: http://localhost:8000
📚 API Docs at: http://localhost:8000/docs

**Terminal 2 - Frontend UI:**
```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app_integrated.py
```
✅ Frontend available at: http://localhost:8501

### Testing the Application

#### Run All Tests
```powershell
pytest
```

#### Run Specific Tests
```powershell
# Integration tests
pytest test_integration.py -v

# End-to-end tests
pytest test_e2e.py -v

# Specific agent tests
pytest tests/test_coordinator.py -v
```

#### Test Coverage
```powershell
pytest --cov=agents --cov=api --cov=utils
```

## 📡 API Endpoints

### Health Check
```
GET http://localhost:8000/api/v1/health
```

### Submit Patient Analysis
```
POST http://localhost:8000/api/v1/patient/analysis
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "birth_date": "1990-01-01",
  "gender": "Male",
  "address": "123 Main St",
  "zip_code": "12345",
  ...
}
```

### Get Patient Info
```
GET http://localhost:8000/api/v1/patient/{patient_id}
```

### X-Ray Analysis
```
POST http://localhost:8000/api/v1/xray/analyze
Content-Type: multipart/form-data
file: [X-ray image file]
```

### Therapy Recommendations
```
GET http://localhost:8000/api/v1/therapy/recommendations/{patient_id}
```

## 📁 Project Structure

```
multi-agent-healthcare/
├── api/                        # Backend API
│   ├── main.py                # FastAPI application
│   ├── routes.py              # API routes
│   ├── schema.py              # Pydantic models
│   └── dependencies.py        # Auth & dependencies
├── agents/                     # AI Agents
│   ├── base_agent.py
│   ├── ingestion_agent.py
│   ├── imaging_agent.py
│   ├── therapy_agent.py
│   ├── pharmacy_agent.py
│   └── doctor_agent.py
├── utils/                      # Utilities
│   ├── api_client.py          # API client for frontend
│   ├── validators.py
│   └── logger.py
├── data/                       # Data files
├── uploads/                    # Uploaded files
├── app_integrated.py           # Streamlit frontend (agent-integrated)
├── start_integrated.bat        # Startup script launching API+UI
└── requirements.txt            # Dependencies
```

## ⚙️ Configuration

### Environment Variables (Optional)
Create a `.env` file in the root directory for custom configuration:
```env
API_HOST=localhost
API_PORT=8000
STREAMLIT_PORT=8501
DEBUG_MODE=False
```

### Configuration Files
- **`config.py`**: Central configuration for paths, thresholds, system settings
  - SpO2 thresholds for severity classification
  - Pharmacy search radius: 25km
  - Image processing: Max 10MB, formats PNG/JPG/JPEG
  - Delivery speed: 30 km/h for ETA calculations
  - Dosage database for 30+ respiratory medicines

- **`app_integrated.py`**: Frontend with multi-source API configuration
  - Priority: Streamlit secrets > Environment variable > Production URL
  - Filters: Mumbai region only (109 pincodes), respiratory symptoms only
  - Default backend: https://multi-agent-healthcare-gl-1.onrender.com

## 🧪 Testing with Postman

1. Import the API endpoints from http://localhost:8000/docs
2. Use the following payload for patient submission:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "birth_date": "1990-01-01",
  "gender": "Male",
  "address": "123 Main St, City, State",
  "zip_code": "12345",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1234567891",
  "emergency_contact_relation": "Spouse",
  "allergies": "Penicillin",
  "current_medications": "Paracetamol 500mg as needed",
  "medical_conditions": "Chronic bronchitis",
  "symptoms": "Persistent cough, chest congestion, mild fever",
  "xray_analysis_enabled": true,
  "ocr_enabled": true,
  "pii_masking_enabled": true,
  "analysis_priority": "Standard"
}
```

## 📊 Frontend Features

### Home Page
- Platform statistics dashboard
- API connection status
- Feature overview

### Patient Analysis
- Comprehensive patient form
- Multi-file document upload
- Real-time API integration
- Progress tracking

### X-Ray Analysis
- AI-powered image classification
- Confidence scores
- Detailed findings
- City/pincode aware matching with fallback visibility

### Therapy Recommendations
- Personalized medication suggestions
- Nearby pharmacy matching with reservation snapshot
- Treatment notes

## 🔐 Security Features

- PII Masking
- Document validation
- Secure file uploads
- API authentication ready

## 🐛 Troubleshooting

### Common Issues

#### ❌ "Port already in use"
```powershell
# Check which process is using the port
netstat -ano | findstr :8000
# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

#### ❌ "Module not found" Error
```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1
# Reinstall dependencies
pip install -r requirements.txt
```

#### ❌ Backend API Not Connecting
1. Verify API server is running: Check http://localhost:8000/api/v1/health
2. Check port 8000 availability
3. Review backend logs in the terminal
4. Check API status indicator in frontend sidebar

#### ❌ Frontend Issues
1. Clear browser cache and reload (Ctrl + Shift + R)
2. Restart Streamlit: `streamlit run app_integrated.py`
3. Check browser console for JavaScript errors (F12)

#### ❌ Data Files Missing
Run the data generation scripts:
```powershell
python generate_zipcodes.py
```

#### ❌ Virtual Environment Not Activating
- **PowerShell Execution Policy Issue:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Debug Mode
Enable debug mode in `config.py`:
```python
DEBUG_CONFIG = {
    "debug_mode": True,
    "log_api_calls": True
}
```

### Getting Help
- Check the [API Documentation](http://localhost:8000/docs) when server is running
- Review logs in the `logs/` directory
- Check test outputs for expected behavior patterns

## 🎯 Tech Stack

- **Backend**: FastAPI 0.115+, Uvicorn (Deployed on Render)
- **Frontend**: Streamlit 1.40+ (Deployed on Streamlit Cloud)
- **Data Processing**: Pandas, NumPy
- **Document Processing**: PyPDF2, pdfplumber, Pillow
- **Testing**: Pytest
- **AI/ML**: Custom classifiers for chest X-ray analysis
- **Deployment**: Render (Backend), Streamlit Cloud (Frontend)

## 📚 Additional Resources

- **Live Backend API**: https://multi-agent-healthcare.onrender.com

## 🔐 Security & Privacy

⚠️ **IMPORTANT DISCLAIMERS:**
- This is an **EDUCATIONAL DEMONSTRATION ONLY**
- **NOT FOR PRODUCTION USE** or real medical decision-making
- No real patient data should be used
- All recommendations are simulated for demonstration purposes
- Always consult qualified healthcare professionals for medical concerns
- In emergencies, call emergency services immediately (911/108)

**Security Features:**
- PII masking capabilities
- Secure file upload handling
- Input validation and sanitization
- API authentication ready (to be implemented)

## 📝 License

This project is part of a multi-agent healthcare system demonstration for educational purposes.

## �‍💻 Author

**Madhav** (MadhaV-73)
- GitHub: [@MadhaV-73](https://github.com/MadhaV-73)

## 🤝 Contributing

This is an educational project. For suggestions or improvements:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Review the troubleshooting section above
- Check existing documentation in the `docs/` folder

## 🔗 Quick Links

### Local Development:
- 🌐 **Backend API**: http://localhost:8000
- 📖 **API Docs**: http://localhost:8000/docs
- 🖥️ **Frontend UI**: http://localhost:8501

### Production (Deployed):
- 🚀 **Live Backend**: https://multi-agent-healthcare.onrender.com
- � **Live API Docs**: https://multi-agent-healthcare.onrender.com/docs
- 📊 **GitHub Repository**: https://github.com/MadhaV-73/Multi-Agent-Healthcare

---
