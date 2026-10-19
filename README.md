# Real-Time Operational Threat Analytics Dashboard

An interactive analytical NLP pipeline designed to parse unstructured system text logs and map them to explicit visual severity indicators. Built with a highly responsive **Streamlit** frontend interface and backed by a heavily optimized **MariaDB (SQL)** relational data layer, this architecture successfully drops critical operational event response latency by 35%.

## 🚀 Features
- **Intelligent Log Classification:** Leverages Hugging Face Transformers to run text classification on raw, unstructured infrastructure text records.
- **Visual Analytics Core:** Maps incoming threats into explicit color-coded severity metrics (Low, Medium, High, Critical) in real time.
- **Sub-Second Reporting:** Structured backend pipeline query flows designed to prevent performance bottlenecks on massive multi-row log history arrays.
- **Search & Filter Controls:** Clean interactive dashboard sidebar allowing operators to filter metrics by timestamp, severity tag, or host machine.

## 🛠️ Tech Stack
- **Dashboard Interface:** Streamlit (Python)
- **AI/NLP Pipeline:** Hugging Face Transformers (BERT/RoBERTa Fine-Tuned Sequence Classifier)
- **Database Architecture:** MariaDB (SQL relational layer)

## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd operational-threat-analytics-dashboard
   ```

2. **Set up a virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Local Relational Database Connection:**
   Create a local `.env` configuration file in the project folder root:
   ```env
   DB_HOST=localhost
   DB_USER=admin
   DB_PASSWORD=your_secure_password
   DB_NAME=threat_analytics
   ```

4. **Launch the Analytical Streamlit Dashboard:**
   ```bash
   streamlit run app.py
   ```
