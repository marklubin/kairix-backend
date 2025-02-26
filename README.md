💻 Running the Project
📌 1. Activate the Poetry Environment
bash
Copy
Edit
cd kairix-backend
poetry shell
📌 2. Start Flask App
bash
Copy
Edit
poetry run poe start
✅ App Running at: http://127.0.0.1:5000/api/hello

📌 3. Run Unit Tests
bash
Copy
Edit
poetry run poe test
📌 4. Format & Lint Code
bash
Copy
Edit
poetry run poe format
poetry run poe lint
📌 5. Install New Dependencies
bash
Copy
Edit
poetry add some-package
📌 6. Update All Dependencies
bash
Copy
Edit
poetry update
🚀 Summary of Commands
Task	Command
Create Project	bash setup_poetry.sh
Activate Poetry Env	poetry shell
Start Flask	poetry run poe start
Run Tests	poetry run poe test
Format Code	poetry run poe format
Lint Code	poetry run poe lint
Install a Package	poetry add <package>
Update Packages	poetry update
