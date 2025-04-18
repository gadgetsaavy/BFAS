import os
import subprocess
import requests
import json
import sys

# Step 1: Define project directory structure and file names
project_structure = {
    'src': {
        'contracts': ['FlashLoanArbitrage.sol'],
        'scripts': ['Deploy.py'],
        'utils': ['GasEstimator.py', 'MEVWrapper.py'],
        'tests': ['Test_all.py'],
        'bots': ['BellmanFord.py', 'LiquidityAggregator.py', 'UniswapClient.py'],
        'README.md': None,
        'requirements.txt': None,
        '.gitignore': None,
        '.env': None
    }
}

# Step 2: Define GitHub details
GITHUB_TOKEN = 'your_github_token_here'  # Replace with your GitHub token
GITHUB_USERNAME = 'gadgetsaavy'  # Replace with your GitHub username
GITHUB_REPO_NAME = 'BFAS'  # Desired repo name on GitHub
GITHUB_API_URL = 'https://api.github.com/user/repos'

# Step 3: Create project directory structure
def create_project_structure(base_dir, structure):
    print("Creating project directory structure...")
    for dir_name, substructure in structure.items():
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        if isinstance(substructure, list):
            for file_name in substructure:
                with open(os.path.join(dir_path, file_name), 'w') as f:
                    f.write(f"# {file_name}\n")
                print(f"Created: {os.path.join(dir_path, file_name)}")
        elif substructure is None:  # Files in the base directory
            with open(dir_path, 'w') as f:
                f.write(f"# {dir_name}\n")
            print(f"Created: {dir_path}")

# Step 4: Initialize Git repository
def init_git_repo(base_dir):
    print("\nInitializing Git repository...")
    subprocess.run(['git', 'init'], cwd=base_dir)
    subprocess.run(['git', 'add', '.'], cwd=base_dir)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=base_dir)
    print("Git repository initialized and committed.")

# Step 5: Push to GitHub
def create_github_repo():
    print("\nCreating GitHub repository...")
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': GITHUB_REPO_NAME,
        'description': 'FlashLoan Arbitrage Bot',
        'private': False,
    }
    response = requests.post(GITHUB_API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print(f"Repository '{GITHUB_REPO_NAME}' created on GitHub.")
        return True
    else:
        print(f"Failed to create GitHub repository: {response.json()['message']}")
        return False

def push_to_github(base_dir):
    print("\nPushing local repository to GitHub...")
    remote_url = f'https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}.git'
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url], cwd=base_dir)
    subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_dir)
    print(f"Repository pushed to GitHub: {remote_url}")

# Step 6: Install required Python dependencies
def install_requirements():
    print("\nInstalling required Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
        print("Successfully installed 'requests'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        sys.exit(1)

# Step 7: Generate requirements.txt
def generate_requirements_txt(base_dir):
    requirements_content = """requests
    """
    with open(os.path.join(base_dir, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)
    print("Generated requirements.txt.")

# Step 8: Set up .gitignore
def setup_gitignore(base_dir):
    gitignore_content = """__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.env
*.git
"""
    with open(os.path.join(base_dir, '.gitignore'), 'w') as f:
        f.write(gitignore_content)
    print("Generated .gitignore.")

# Step 9: Create .env file with example environment variables
def setup_env(base_dir):
    env_content = """GITHUB_TOKEN=your_github_token_here
GITHUB_USERNAME=your_github_username_here
"""
    with open(os.path.join(base_dir, '.env'), 'w') as f:
        f.write(env_content)
    print("Generated .env file with placeholders for token and username.")

# Step 10: Run the full script to create the project, install dependencies, initialize git, and push to GitHub
def main():
    base_dir = os.path.join(os.getcwd(), GITHUB_REPO_NAME)

    # Install required dependencies
    install_requirements()
    
    # Create project structure and necessary files
    print("Starting project setup...\n")
    create_project_structure(base_dir, project_structure)
    
    # Generate requirements.txt, .gitignore, .env
    generate_requirements_txt(base_dir)
    setup_gitignore(base_dir)
    setup_env(base_dir)
    
    # Initialize Git repo and make the initial commit
    init_git_repo(base_dir)

    # Create GitHub repo and push the local repo
    if create_github_repo():
        push_to_github(base_dir)
    else:
        print("Exiting, as repository creation on GitHub failed.")
    
    # Keep terminal open and show the final message
    print("\nSetup complete. Press any key to continue...")
    input()  # Wait for user input to keep the script running and on the screen

if __name__ == "__main__":
    main()

