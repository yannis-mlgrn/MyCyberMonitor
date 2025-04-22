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
