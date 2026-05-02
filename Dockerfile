# Use the official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the default Cloud Run port
EXPOSE 8080

# Command to run the Streamlit app using the dynamic port provided by Cloud Run
CMD sh -c "streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"
