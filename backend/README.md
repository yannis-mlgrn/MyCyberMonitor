# Backend Documentation 🚀

## 🛠️ Backend Installation Guide

Follow these steps to set up the backend:

1. **📂 Navigate to the backend directory**:

    ```bash
    cd backend
    ```

2. **🌱 Create a virtual environment**:

    ```bash
    python3 -m venv .venv
    ```

3. **⚙️ Activate the virtual environment and install dependencies**:

    ```bash
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

4. **✅ Verify the installation**:
    Ensure all dependencies are installed correctly by checking the `requirements.txt` file and running the application.

5. **🚀 Run the backend**:
    Start the backend server using the following command:

    ```bash
    uvicorn app.main:app --reload
    ```

6. **🌐 Explore the API Documentation**:

    Once the backend server is running, you can interact with the API using the Swagger UI. Open your browser and navigate to:

    [Swagger UI - API Documentation](http://127.0.0.1:8000/docs)

    This interface allows you to test the API endpoints and view detailed documentation.
