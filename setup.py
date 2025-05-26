from setuptools import setup, find_packages

setup(
    name="lakera",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "transformers",
        "torch",
        "pydantic",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest==8.0.0",
            "pytest-cov==4.1.0",
            "pytest-asyncio==0.23.5",
        ],
    },
) 