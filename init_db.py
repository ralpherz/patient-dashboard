import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database configuration
DB_CONFIG = {
    'user': 'postgres',
    'password': 'postgres',  # CHANGE THIS to your PostgreSQL password
    'host': 'localhost',
    'port': '5432'
}

DB_NAME = 'patient_dashboard'

def create_database():
    """Create the patient_dashboard database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not a specific database)
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"✅ Database '{DB_NAME}' created successfully!")
        else:
            print(f"ℹ️  Database '{DB_NAME}' already exists.")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error creating database: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL is installed and running")
        print("2. Your password in init_db.py line 7 is correct")
        raise

def create_tables():
    """Create all database tables"""
    try:
        # Connect to the patient_dashboard database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                date_of_birth DATE,
                email VARCHAR(100),
                phone VARCHAR(20),
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create appointments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES patients(id),
                appointment_date TIMESTAMP NOT NULL,
                provider_name VARCHAR(100) NOT NULL,
                appointment_type VARCHAR(50),
                location VARCHAR(200),
                status VARCHAR(20) DEFAULT 'Scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create vitals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vitals (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES patients(id),
                recorded_date TIMESTAMP NOT NULL,
                systolic_bp INTEGER,
                diastolic_bp INTEGER,
                heart_rate INTEGER,
                temperature DECIMAL(4,1),
                weight DECIMAL(5,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create medications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medications (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES patients(id),
                medication_name VARCHAR(200) NOT NULL,
                dosage VARCHAR(100),
                frequency VARCHAR(100),
                prescribed_by VARCHAR(100),
                start_date DATE,
                end_date DATE,
                instructions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create lab_results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lab_results (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES patients(id),
                test_date TIMESTAMP NOT NULL,
                test_name VARCHAR(200) NOT NULL,
                result_value VARCHAR(100),
                unit VARCHAR(50),
                reference_range VARCHAR(100),
                status VARCHAR(20),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create medical_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_history (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES patients(id),
                diagnosis VARCHAR(200) NOT NULL,
                diagnosis_date DATE,
                status VARCHAR(20),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES patients(id),
                sender VARCHAR(100) NOT NULL,
                subject VARCHAR(200),
                message_text TEXT NOT NULL,
                sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        print("✅ All 7 tables created successfully!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error creating tables: {e}")
        raise

def populate_sample_data():
    """Insert sample patient data for demonstration"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM patients")
        if cursor.fetchone()[0] > 0:
            print("ℹ️  Sample data already exists, skipping...")
            cursor.close()
            conn.close()
            return
        
        # Insert sample patient
        cursor.execute("""
            INSERT INTO patients (first_name, last_name, date_of_birth, email, phone, address)
            VALUES ('John', 'Doe', '1985-03-15', 'john.doe@email.com', '(555) 123-4567', '123 Main St, Chicago, IL 60601')
        """)
        
        # Insert sample appointments
        cursor.execute("""
            INSERT INTO appointments (patient_id, appointment_date, provider_name, appointment_type, location, status)
            VALUES 
                (1, '2024-02-15 10:00:00', 'Dr. Sarah Johnson', 'Annual Physical', 'Main Clinic - Room 204', 'Scheduled'),
                (1, '2024-01-10 14:30:00', 'Dr. Michael Chen', 'Follow-up', 'Cardiology Center', 'Completed'),
                (1, '2023-12-05 09:00:00', 'Dr. Sarah Johnson', 'Consultation', 'Main Clinic - Room 101', 'Completed')
        """)
        
        # Insert sample vitals
        cursor.execute("""
            INSERT INTO vitals (patient_id, recorded_date, systolic_bp, diastolic_bp, heart_rate, temperature, weight)
            VALUES 
                (1, '2024-01-28 09:30:00', 128, 82, 76, 98.4, 185.5),
                (1, '2024-01-21 10:15:00', 125, 80, 72, 98.6, 186.2),
                (1, '2024-01-14 11:00:00', 130, 85, 78, 98.3, 187.0),
                (1, '2024-01-07 09:45:00', 122, 78, 70, 98.5, 188.1),
                (1, '2023-12-31 10:30:00', 132, 84, 74, 98.4, 189.3)
        """)
        
        # Insert sample medications
        cursor.execute("""
            INSERT INTO medications (patient_id, medication_name, dosage, frequency, prescribed_by, start_date, instructions)
            VALUES 
                (1, 'Lisinopril', '10 mg', 'Once daily', 'Dr. Michael Chen', '2023-06-15', 'Take in the morning with water'),
                (1, 'Metformin', '500 mg', 'Twice daily', 'Dr. Sarah Johnson', '2023-08-20', 'Take with meals'),
                (1, 'Atorvastatin', '20 mg', 'Once daily at bedtime', 'Dr. Michael Chen', '2023-09-10', 'Take at bedtime')
        """)
        
        # Insert sample lab results
        cursor.execute("""
            INSERT INTO lab_results (patient_id, test_date, test_name, result_value, unit, reference_range, status)
            VALUES 
                (1, '2024-01-25 08:00:00', 'Hemoglobin A1C', '6.2', '%', '< 5.7', 'Reviewed'),
                (1, '2024-01-25 08:00:00', 'Total Cholesterol', '185', 'mg/dL', '< 200', 'Normal'),
                (1, '2024-01-25 08:00:00', 'LDL Cholesterol', '110', 'mg/dL', '< 100', 'Borderline'),
                (1, '2023-12-10 07:30:00', 'Glucose (Fasting)', '102', 'mg/dL', '70-100', 'Slightly High')
        """)
        
        # Insert sample medical history
        cursor.execute("""
            INSERT INTO medical_history (patient_id, diagnosis, diagnosis_date, status)
            VALUES 
                (1, 'Hypertension (High Blood Pressure)', '2023-06-15', 'Active'),
                (1, 'Type 2 Diabetes', '2023-08-20', 'Active'),
                (1, 'Hyperlipidemia (High Cholesterol)', '2023-09-10', 'Active')
        """)
        
        # Insert sample messages
        cursor.execute("""
            INSERT INTO messages (patient_id, sender, subject, message_text, is_read)
            VALUES 
                (1, 'Dr. Sarah Johnson', 'Lab Results Available', 'Your recent lab results are now available in the portal. Please review and contact us if you have any questions.', FALSE),
                (1, 'Nurse Williams', 'Appointment Reminder', 'This is a reminder of your upcoming appointment on February 15, 2024 at 10:00 AM with Dr. Sarah Johnson.', TRUE),
                (1, 'Billing Department', 'Statement Ready', 'Your monthly statement is now available for review in the billing section.', TRUE)
        """)
        
        conn.commit()
        print("✅ Sample data added successfully!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error adding sample data: {e}")
        raise

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Patient Health Dashboard - Database Setup")
    print("="*60 + "\n")
    
    print("⚠️  BEFORE RUNNING: Update the password on line 7 of this file!\n")
    
    try:
        print("Step 1: Creating database...")
        create_database()
        
        print("\nStep 2: Creating tables...")
        create_tables()
        
        print("\nStep 3: Adding sample data...")
        populate_sample_data()
        
        print("\n" + "="*60)
        print("✅ SUCCESS! Database setup complete!")
        print("="*60)
        print("\nYou can now run the application:")
        print("  python app.py")
        print("\nThen open your browser to: http://localhost:5000")
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ SETUP FAILED")
        print("="*60)
        print(f"\nError: {e}")
        print("\nPlease check:")
        print("1. PostgreSQL is installed and running")
        print("2. Your password on line 7 is correct")
        print("3. You have permission to create databases")
