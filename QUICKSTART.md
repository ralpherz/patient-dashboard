# 🚀 Quick Start Guide

Get the Patient Health Dashboard running in 3 minutes!

## Prerequisites

You need:
- ✅ Python 3.8 or higher installed
- ✅ PostgreSQL installed and running

---

## Setup (4 Commands)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Update password in init_db.py
Open `init_db.py` and change line 7:
```python
'password': 'postgres',  # ← Change to YOUR PostgreSQL password
```

### 3. Create database and tables
```bash
python init_db.py
```

### 4. Update password in database.py
Open `database.py` and change line 8:
```python
'password': 'postgres',  # ← Change to YOUR PostgreSQL password
```

### 5. Run the app
```bash
python app.py
```

### 6. Open browser
Go to: **http://localhost:5000**

---

## That's It! 🎉

You should see the Patient Health Dashboard with sample data for John Doe.

---

## Common Issues

**Can't connect to database?**
- Make sure PostgreSQL is running
- Check your password in both `init_db.py` and `database.py`

**Port 5000 already in use?**
- Another app is using that port
- Stop the other app or change the port in `app.py`

**Tables already exist error?**
- Database was already created
- This is fine! Just run `python app.py`

---

## What You Get

✅ Full patient dashboard  
✅ Sample patient data (John Doe)  
✅ 3 appointments  
✅ Vitals with charts  
✅ Active medications  
✅ Lab results  
✅ Medical history  
✅ Message system  

---

## Next Steps

- Explore all 7 pages in the navigation
- Check out the Chart.js vitals graphs
- Try marking messages as read
- View printable lab reports

Enjoy! 🏥
