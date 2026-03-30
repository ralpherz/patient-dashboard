from flask import Flask, render_template, redirect
from database import get_connection
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Dashboard home page showing patient summary"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get patient info
    cursor.execute("SELECT first_name, last_name FROM patients WHERE id = 1")
    patient = cursor.fetchone()
    patient_name = f"{patient[0]} {patient[1]}" if patient else "Patient"
    
    # Get next appointment
    cursor.execute("""
        SELECT appointment_date, provider_name, appointment_type, location
        FROM appointments 
        WHERE patient_id = 1 AND status = 'Scheduled' AND appointment_date > NOW()
        ORDER BY appointment_date ASC
        LIMIT 1
    """)
    next_appointment = cursor.fetchone()
    
    # Get most recent vitals
    cursor.execute("""
        SELECT systolic_bp, diastolic_bp, heart_rate, recorded_date
        FROM vitals 
        WHERE patient_id = 1
        ORDER BY recorded_date DESC
        LIMIT 1
    """)
    recent_vitals = cursor.fetchone()
    
    # Count active medications
    cursor.execute("SELECT COUNT(*) FROM medications WHERE patient_id = 1")
    med_count = cursor.fetchone()[0]
    
    # Get most recent lab result
    cursor.execute("""
        SELECT test_name, result_value, status, test_date
        FROM lab_results 
        WHERE patient_id = 1
        ORDER BY test_date DESC
        LIMIT 1
    """)
    recent_lab = cursor.fetchone()
    
    # Count active medical conditions
    cursor.execute("SELECT COUNT(*) FROM medical_history WHERE patient_id = 1 AND status = 'Active'")
    active_conditions = cursor.fetchone()[0]
    
    # Count unread messages
    cursor.execute("SELECT COUNT(*) FROM messages WHERE patient_id = 1 AND is_read = FALSE")
    unread_messages = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html',
                         patient_name=patient_name,
                         next_appointment=next_appointment,
                         recent_vitals=recent_vitals,
                         med_count=med_count,
                         recent_lab=recent_lab,
                         active_conditions=active_conditions,
                         unread_messages=unread_messages)


@app.route('/appointments')
def appointments():
    """View all appointments"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get patient name
    cursor.execute("SELECT first_name, last_name FROM patients WHERE id = 1")
    patient = cursor.fetchone()
    patient_name = f"{patient[0]} {patient[1]}" if patient else "Patient"
    
    # Get all appointments
    cursor.execute("""
        SELECT appointment_date, provider_name, appointment_type, status, location
        FROM appointments 
        WHERE patient_id = 1
        ORDER BY appointment_date DESC
    """)
    all_appointments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('appointments.html',
                         patient_name=patient_name,
                         appointments=all_appointments)


@app.route('/vitals')
def vitals():
    """View vitals with trends"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get patient name
    cursor.execute("SELECT first_name, last_name FROM patients WHERE id = 1")
    patient = cursor.fetchone()
    patient_name = f"{patient[0]} {patient[1]}" if patient else "Patient"
    
    # Get all vitals
    cursor.execute("""
        SELECT recorded_date, systolic_bp, diastolic_bp, heart_rate, weight, temperature
        FROM vitals 
        WHERE patient_id = 1
        ORDER BY recorded_date DESC
    """)
    all_vitals = cursor.fetchall()
    
    # Prepare chart data (reverse for oldest to newest in charts)
    chart_data = []
    for vital in reversed(all_vitals):
        chart_data.append({
            'date': vital[0].strftime('%b %d'),
            'systolic': vital[1],
            'diastolic': vital[2],
            'heartRate': vital[3],
            'weight': round(vital[4], 1)
        })
    
    cursor.close()
    conn.close()
    
    return render_template('vitals.html',
                         patient_name=patient_name,
                         vitals=all_vitals,
                         chart_data=chart_data)


@app.route('/medications')
def medications():
    """View all medications"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get patient name
    cursor.execute("SELECT first_name, last_name FROM patients WHERE id = 1")
    patient = cursor.fetchone()
    patient_name = f"{patient[0]} {patient[1]}" if patient else "Patient"
    
    # Get all medications
    cursor.execute("""
        SELECT medication_name, dosage, frequency, instructions, start_date, prescribing_doctor
        FROM medications 
        WHERE patient_id = 1
        ORDER BY medication_name
    """)
    all_medications = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('medications.html',
                         patient_name=patient_name,
                         medications=all_medications)


@app.route('/labs')
def labs():
    """View all lab results"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get patient name
    cursor.execute("SELECT first_name, last_name FROM patients WHERE id = 1")
    patient = cursor.fetchone()
    patient_name = f"{patient[0]} {patient[1]}" if patient else "Patient"
    
    # Get all lab results
    cursor.execute("""
        SELECT test_date, test_name, result_value, normal_range, status, ordering_doctor
        FROM lab_results 
        WHERE patient_id = 1
        ORDER BY test_date DESC
    """)
    all_labs = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('labs.html',
                         patient_name=patient_name,
                         labs=all_labs)


@app.route('/history')
def history():
    """View medical history"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get patient name
    cursor.execute("SELECT first_name, last_name FROM patients WHERE id = 1")
    patient = cursor.fetchone()
    patient_name = f"{patient[0]} {patient[1]}" if patient else "Patient"
    
    # Get all medical history
    cursor.execute("""
        SELECT condition_name, diagnosis_date, status, notes
        FROM medical_history 
        WHERE patient_id = 1
        ORDER BY 
            CASE WHEN status = 'Active' THEN 0 ELSE 1 END,
            diagnosis_date DESC
    """)
    all_history = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('history.html',
                         patient_name=patient_name,
                         history=all_history)


@app.route('/messages')
def messages():
    """View messages"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get patient name
    cursor.execute("SELECT first_name, last_name FROM patients WHERE id = 1")
    patient = cursor.fetchone()
    patient_name = f"{patient[0]} {patient[1]}" if patient else "Patient"
    
    # Get all messages
    cursor.execute("""
        SELECT sender, subject, message_text, sent_date, is_read
        FROM messages 
        WHERE patient_id = 1
        ORDER BY sent_date DESC
    """)
    all_messages = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('messages.html',
                         patient_name=patient_name,
                         messages=all_messages)


@app.route('/mark_read/<int:message_index>')
def mark_message_read(message_index):
    """Mark a message as read"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all messages to find the specific one
    cursor.execute("""
        SELECT id FROM messages 
        WHERE patient_id = 1
        ORDER BY sent_date DESC
    """)
    message_ids = [row[0] for row in cursor.fetchall()]
    
    # Mark the specific message as read
    if message_index < len(message_ids):
        message_id = message_ids[message_index]
        cursor.execute("""
            UPDATE messages 
            SET is_read = TRUE 
            WHERE id = %s
        """, (message_id,))
        conn.commit()
    
    cursor.close()
    conn.close()
    
    # Redirect back to messages page
    return redirect('/messages')


if __name__ == '__main__':
    app.run(debug=True)