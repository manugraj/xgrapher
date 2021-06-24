#!/bin/bash
# Avoid shifting paramters in second line, incompatible with Windows WSL2, Docker on windows
uvicorn app.main:app --host=0.0.0.0 --port=8000