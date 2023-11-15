import os
import sys

import uvicorn

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    uvicorn.run("server.app:app", host="127.0.0.1", port=5000, reload=True)
