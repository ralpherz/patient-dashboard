# Patient Health Dashboard

A full-stack web application for managing patient health records, built with Flask and PostgreSQL. This dashboard provides an intuitive interface for viewing appointments, vital signs, medications, lab results, and medical history.

## 🚀 Features

- **Dashboard Overview**: Quick summary of health information with key metrics
- **Appointments Management**: View upcoming and past appointments with status tracking
- **Vitals Tracking**: Interactive charts displaying blood pressure and weight trends over time
- **Medications**: Detailed view of active prescriptions with dosage and instructions
- **Lab Results**: Laboratory test results with printable reports
- **Medical History**: Comprehensive record of diagnoses and conditions
- **Messaging System**: Communication hub with healthcare providers, including read/unread status

## 🛠️ Technologies Used

### Backend
- **Python 3.12** - Core programming language
- **Flask** - Web framework for routing and templating
- **PostgreSQL 17** - Relational database management
- **psycopg2** - PostgreSQL adapter for Python

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript** - Interactive functionality
- **Chart.js** - Data visualization for vitals trends
- **Responsive Design** - Mobile-friendly interface

## 📊 Database Schema

The application uses a normalized PostgreSQL database with 7 tables:

- `patients` - Patient demographics and contact information
- `appointments` - Scheduled appointments with providers
- `vitals` - Blood pressure, heart rate, weight, and temperature readings
- `medications` - Active prescriptions and dosage information
- `lab_results` - Laboratory test results with normal ranges
- `medical_history` - Past diagnoses and conditions
- `messages` - Communication between patients and care team

## 🎯 Key Highlights

- **Healthcare Domain Knowledge**: Demonstrates understanding of medical terminology, HIPAA considerations, and healthcare workflows
- **Database Design**: Proper use of foreign keys, data normalization, and relational integrity
- **Data Visualization**: Interactive Chart.js graphs for tracking health trends
- **Responsive UI**: Mobile-first design with orange/black professional theme
- **Print Functionality**: Generate printable lab reports
- **Real-time Updates**: Mark messages as read with instant database updates

## 💻 Installation

### Prerequisites
- Python 3.8+ 
- PostgreSQL (any recent version)

### Quick Setup (3 Steps)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ralpherz/patient-dashboard.git
   cd patient-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   
   **Important:** Before running, open `init_db.py` and update line 7 with your PostgreSQL password:
   ```python
   'password': 'your_actual_password',  # Change this!
   ```
   
   Then run:
   ```bash
   python init_db.py
   ```
   
   This automatically:
   - Creates the `patient_dashboard` database
   - Creates all 7 tables
   - Adds sample patient data

4. **Update database.py password**
   
   Open `database.py` and update line 8 with your PostgreSQL password:
   ```python
   'password': 'your_actual_password',  # Change this!
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the dashboard**
   - Open your browser to `http://localhost:5000`

### Alternative: Manual PostgreSQL Setup

If you prefer to set up the database manually:

1. Create database in PostgreSQL:
   ```sql
   CREATE DATABASE patient_dashboard;
   ```

2. Run `init_db.py` to create tables and add sample data

3. Update `database.py` with your credentials

### Troubleshooting

**"Error connecting to database"**
- Make sure PostgreSQL is running
- Check that your password in `database.py` is correct
- Verify PostgreSQL is listening on port 5432

**"Database does not exist"**
- Run `python init_db.py` to create it automatically

**"Permission denied"**
- Make sure your PostgreSQL user has CREATE DATABASE privileges

## 📁 Project Structure

```
patient-dashboard/
├── templates/
│   ├── dashboard.html      # Main dashboard with health summary
│   ├── appointments.html   # Appointment management
│   ├── vitals.html        # Vital signs with Chart.js graphs
│   ├── medications.html   # Active medications list
│   ├── labs.html          # Laboratory results
│   ├── history.html       # Medical history
│   └── messages.html      # Messaging system
├── app.py                 # Flask application with all routes
├── database.py            # Database connection configuration
├── database_example.py    # Template for database config
├── init_db.py            # Database setup script (creates tables + sample data)
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🎨 Design Philosophy

The interface uses a professional healthcare color scheme with:
- Dark backgrounds (#1a1a1a) for reduced eye strain
- Orange accents (#ff6b00 to #ff8c00) for important information
- High contrast for accessibility
- Gradient cards with hover effects for modern aesthetics
- Mobile-responsive grid layouts

## 🔐 Security Considerations

This is a portfolio/demonstration project. For production use, additional security measures would be required:
- User authentication and authorization
- Password hashing (bcrypt/Argon2)
- HTTPS encryption
- HIPAA compliance measures
- SQL injection prevention (using parameterized queries)
- Session management
- CSRF protection

## 📈 Future Enhancements

- [ ] Multi-user authentication system
- [ ] Appointment scheduling functionality
- [ ] Export data to PDF/Excel
- [ ] Email notifications for appointments
- [ ] Integration with external EHR systems
- [ ] Telemedicine video integration
- [ ] Prescription refill requests
- [ ] Automated appointment reminders

## 🎓 Learning Outcomes

This project demonstrates proficiency in:
- Full-stack web development
- Database design and SQL queries
- RESTful routing patterns
- Frontend UI/UX design
- Data visualization
- Healthcare industry knowledge
- Version control with Git

## 👨‍💻 Author

**Ralph** - [GitHub](https://github.com/ralpherz) | [LinkedIn](https://linkedin.com/in/ralphbeaupre/)

*Web Development Student at College of DuPage*  
*Graduating May 2026*

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built as a portfolio project to demonstrate healthcare application development skills
- Sample patient data is fictional and for demonstration purposes only
- Designed with Epic Systems and healthcare IT roles in mind

---

**⭐ If you found this project helpful, please consider giving it a star!**
