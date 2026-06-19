from pathlib import Path

PROJECT_STRUCTURE = {
    "app": {
        "__init__.py": "",
        "main.py": "",
        "api": {
            "__init__.py": "",
            "users.py": "",
            "tasks.py": "",
            "health.py": "",
            "ready.py": "",
        },
        "core": {
            "__init__.py": "",
            "config.py": "",
            "logger.py": "",
        },
        "db": {
            "__init__.py": "",
            "base.py": "",
            "session.py": "",
        },
        "models": {
            "__init__.py": "",
            "user.py": "",
            "task.py": "",
        },
        "schemas": {
            "__init__.py": "",
            "user.py": "",
            "task.py": "",
        },
        "services": {
            "__init__.py": "",
            "user_service.py": "",
            "task_service.py": "",
        },
    },
    "tests": {
        "__init__.py": "",
        "conftest.py": "",
        "test_users.py": "",
        "test_tasks.py": "",
        "test_health.py": "",
        "test_ready.py": "",
    },
    "scripts": {
        "check_env.sh": "",
    },
    "alembic": {
        "versions": {},
    },
    ".github": {
        "workflows": {
            "ci.yml": "",
        },
        "pull_request_template.md": "",
    },
    ".env.example": "",
    ".gitignore": "",
    "requirements.txt": "",
    "Makefile": "",
    "Dockerfile": "",
    "docker-compose.yml": "",
    "alembic.ini": "",
    "README.md": "",
}


def create_structure(base_path: Path, structure: dict):
    for name, content in structure.items():
        path = base_path / name

        if isinstance(content, dict):
            path.mkdir(parents=True, exist_ok=True)
            create_structure(path, content)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)

            if not path.exists():
                path.touch()
                print(f"Created file: {path}")
            else:
                print(f"Exists: {path}")


if __name__ == "__main__":
    root = Path.cwd()
    create_structure(root, PROJECT_STRUCTURE)

    print("\n✅ TaskTracker folder structure created successfully.")