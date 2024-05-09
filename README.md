Code for PyMNtos - Twin Cities Python User Group talk "Deploy a Python API to the cloud", May 2024.

At the time of the talk, the API is available at https://cat.osull.com

## Local development

### Run with VS Code

Using `.vscode/launch.json`

### Build with Docker

    docker build --tag python_cloud_api_demo .

### Run with Docker on port 8000

    docker run -p 8000:80 python_cloud_api_demo