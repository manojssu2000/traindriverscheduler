# **Shift Scheduling Optimization Using PuLP**

## **📌 Overview**
This project optimizes weekly shift scheduling for drivers using **Linear Programming (LP)** with **PuLP** in Python. It ensures fair workload distribution, meets operational constraints, and generates an optimized shift allocation CSV.

---

## **🔍 Problem Statement**
The goal is to assign drivers to shifts efficiently while ensuring:
- **Each shift has the required number of drivers** (minimum **97 per shift**).
- **Drivers do not exceed 35 weekly work hours** (maximum **5 shifts per week**).
- **Drivers are only assigned to shifts on available days**.
- **Drivers work at most one shift per day**.
- **Depot constraints are respected** (each driver can only be assigned shifts at their depot).
- **Minimize deviations in shift assignments** to ensure fairness.

---

## **🛠 Solution Approach**
1. **Input:**
   - `driver_availability.csv`: A CSV file containing driver availability (1 = Available, 0 = Not Available).
   
2. **Optimization Model (PuLP):**
   - **Decision Variables**: Binary (1 = Assigned, 0 = Not Assigned).
   - **Objective Function**: Minimize total shift deviations.
   - **Constraints**:
     - **Shift Coverage**: Each shift has at least **97 drivers**.
     - **Max Weekly Hours**: Drivers cannot exceed **35 hours/week**.
     - **One Shift per Day**: A driver can only be assigned to one shift per day.
     - **Availability Check**: Assign shifts **only if the driver is available**.

3. **Output:**
   - `shift_allocation.csv`: A structured schedule with driver shift assignments.

---

## **📂 Project Structure**
```
│── shift_scheduler.ipynb   # Jupyter Notebook (Full Optimization Model)
│── shift_allocation.csv    # Generated shift allocation output
│── driver_availability.csv # Input: Driver availability dataset
│── README.md               # Project documentation
```

---

## **🚀 How to Use**
### **1️⃣ Install Dependencies**
```bash
pip install pulp pandas
```

### **2️⃣ Run the Notebook**
Open and run **`shift_scheduler.ipynb`** in Jupyter Notebook.

### **3️⃣ Upload the Input File**
Place `driver_availability.csv` in the same directory.

### **4️⃣ Run the Optimization Model**
Execute the Python script to generate the optimized schedule.

### **5️⃣ View Results**
The **`shift_allocation.csv`** file will be generated with shift assignments.

---

## **📊 Example Input & Output**
### **🔹 Input (`driver_availability.csv`):**
| Driver  | Depot  | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |
|---------|--------|--------|---------|-----------|----------|--------|----------|--------|
| D000001 | Depot 5 | 1  | 1 | 1 | 0 | 1 | 1 | 1 |
| D000002 | Depot 2 | 1  | 1 | 1 | 1 | 1 | 1 | 1 |
| ...     | ...    | ... | ... | ... | ... | ... | ... | ... |

### **🔹 Output (`shift_allocation.csv`):**
| Driver  | Monday Shift 1 | Monday Shift 2 | ... | Sunday Shift 5 |
|---------|---------------|---------------|-----|---------------|
| D000001 | 1             | 0             | ... | 1             |
| D000002 | 0             | 1             | ... | 0             |
| ...     | ...           | ...           | ... | ...           |

---

## **📌 Future Improvements**
- Add **real-time scheduling** with **dynamic driver availability**.
- Implement **multi-objective optimization** for **cost efficiency**.
- Improve **fair workload distribution** by **penalizing overtime**.

---

## **🤝 Contributions**
Feel free to **fork** this repository, **open issues**, and **submit pull requests**!

---

## **📜 License**
This project is licensed under the **MIT License**.

---

🚀 **Happy Scheduling!** 🚆📊
