# Optimizing Dockerfiles for Python apps

## Description
Building a dockerfile for a Python application is easy to get started with,
but usually they are not optimized for faster build times and smaller
image sizes. This is especially true for applications which require
non-Python dependencies, e.g. C/C++/Rust extensions.

This repository has a sample app using FastAPI, which serves a 
machine learning model trained on MNIST digits. In addition,
it has a small C++ extension in the extension folder. 
The has a dockerfile which has a base setup, and then other optimizations, 
numbered 1 through 6 that we can do on top of it to improve 
the resultant container.


## Run locally
Note that this app will only run on Python 3.12. 

1. Install poetry

2. Install dependencies
```bash
make setup
```
3. Run server at localhost:8000
```bash
uvicorn src.server:app
```
4. Check http://localhost:8000/docs/






