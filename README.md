# 📡 Semantic API Server for Dollar Universe (using fastmcp)

This server acts as an intelligent context protocol, translating semantic API requests into Dollar Universe commands executed via SSH.

## ⚙️ Installation

1.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure the SSH connection:**
    Modify the `config.json` file with the credentials for your Dollar Universe server.

## 🚀 Running the Server

Use the `fastmcp` command-line tool to run the server:

```bash
fastmcp run server:mcp
```

Alternatively, you can run the server directly:

```bash
python server.py
```

The server will start and be available for me to use.

## 🧰 API Tools

The server exposes the following tools that I can use:

*   `list_tasks(uproc: str = None, session: str = None, mu: str = None, status: str = None) -> str`
    *   Lists tasks (executions) with optional filters.
*   `list_sessions(session: str = None, mu: str = None) -> str`
    *   Lists sessions with optional filters.
*   `list_uprocs(uproc: str = None, mu: str = None) -> str`
    *   Lists Uprocs with optional filters.