# German Household Income Dashboard - Deployment Guide

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run household_income_dashboard_deploy.py
```

## 📦 Deployment Options

### 1. Streamlit Cloud (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add German household income dashboard"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `household_income_dashboard_deploy.py` as the main file
   - Add the CSV file to your repository

3. **Required Files in Repository:**
   ```
   ├── household_income_dashboard_deploy.py
   ├── requirements.txt
   ├── 12241-0001_en.csv (or upload via file uploader)
   └── README.md
   ```

### 2. Heroku

1. **Create Procfile:**
   ```
   web: streamlit run household_income_dashboard_deploy.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy dashboard"
   git push heroku main
   ```

### 3. Docker

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "household_income_dashboard_deploy.py", "--server.address", "0.0.0.0"]
   ```

2. **Build and Run:**
   ```bash
   docker build -t income-dashboard .
   docker run -p 8501:8501 income-dashboard
   ```

## 🔧 Configuration

### Environment Variables
- `CSV_FILE_PATH`: Path to the CSV file (default: `/Users/akar/Downloads/12241-0001_en.csv`)

### File Upload Option
The dashboard can be modified to accept file uploads instead of hardcoded paths:

```python
# Add this to the load_and_process_data function
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # Process uploaded file instead of hardcoded path
    df = pd.read_csv(uploaded_file, ...)
```

## 📋 Requirements

### Python Dependencies
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
numpy>=1.24.0
```

### System Requirements
- Python 3.7+
- 512MB RAM minimum
- 1GB disk space

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'plotly'"**
   ```bash
   pip install plotly
   ```

2. **CSV file not found**
   - Ensure the CSV file is in the correct location
   - Use absolute paths for production
   - Consider using file upload functionality

3. **Memory issues**
   - Reduce data size
   - Use data sampling
   - Optimize pandas operations

4. **Port conflicts**
   ```bash
   streamlit run dashboard.py --server.port 8502
   ```

### Debug Mode
```bash
streamlit run household_income_dashboard_deploy.py --logger.level debug
```

## 🔒 Security Considerations

1. **File Upload Validation:**
   ```python
   if uploaded_file.type != "text/csv":
       st.error("Please upload a CSV file")
       return
   ```

2. **Data Sanitization:**
   - Validate CSV structure
   - Check for malicious content
   - Limit file size

3. **Access Control:**
   - Add authentication if needed
   - Use HTTPS in production
   - Implement rate limiting

## 📊 Performance Optimization

1. **Caching:**
   ```python
   @st.cache_data
   def load_data():
       # Expensive data loading
   ```

2. **Data Sampling:**
   ```python
   # For large datasets
   df = df.sample(n=10000) if len(df) > 10000 else df
   ```

3. **Lazy Loading:**
   - Load data only when needed
   - Use pagination for large tables

## 🌐 Production Checklist

- [ ] All dependencies installed
- [ ] CSV file accessible
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Security measures in place
- [ ] Performance optimized
- [ ] Monitoring set up
- [ ] Backup strategy defined

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Streamlit documentation
3. Check GitHub issues
4. Contact support team
