import json
import paramiko
from mcp.server.fastmcp import FastMCP

# --- Configuration Loading ---
try:
    with open('config.json') as config_file:
        config = json.load(config_file)
    SSH_HOST = config.get('SSH_HOST')
    SSH_USER = config.get('SSH_USER')
    SSH_PASSWORD = config.get('SSH_PASSWORD')
    SSH_KEY_PATH = config.get('SSH_KEY_PATH')
except FileNotFoundError:
    print("ERROR: config.json file not found. Please create it.")
    exit(1)
except json.JSONDecodeError:
    print("ERROR: config.json file is poorly formatted.")
    exit(1)

# --- Mappings ---
STATUS_MAP = {
    "running": "E",
    "completed": "T",
    "aborted": "A",
    "waiting": "W",
    "pending": "P",
    "refused": "R",
    "suspended": "H",
    "launching": "S"
}

# --- SSH Execution Helper ---
def execute_ssh_command(command):
    """Connects to the SSH server and executes a command."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if SSH_KEY_PATH:
            ssh.connect(SSH_HOST, username=SSH_USER, key_filename=SSH_KEY_PATH, timeout=10)
        elif SSH_PASSWORD:
            ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        else:
            raise ValueError("No SSH authentication method (password or key) is configured.")

        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        ssh.close()

        if error:
            return f"Error executing command: {error}"
        return output

    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- MCP Server Definition ---
mcp = FastMCP("DollarUniverseServer", title="Dollar Universe MCP Server")

@mcp.tool()
def list_tasks(uproc: str = None, session: str = None, mu: str = None, status: str = None) -> str:
    """Lists tasks (executions) with optional filters."""
    command_parts = ["uxlst ctl"]
    if uproc:
        command_parts.append(f"UPR={uproc}")
    if session:
        command_parts.append(f"SES={session}")
    if mu:
        command_parts.append(f"MU={mu}")
    if status:
        status_code = STATUS_MAP.get(status.lower())
        if status_code:
            command_parts.append(f"STATUS={status_code}")
        else:
            return f"Invalid status: {status}"
    command = " ".join(command_parts)
    return execute_ssh_command(command)

@mcp.tool()
def list_sessions(session: str = None, mu: str = None) -> str:
    """Lists sessions with optional filters."""
    command_parts = ["uxlst ses"]
    if session:
        command_parts.append(f"SES={session}")
    if mu:
        command_parts.append(f"MU={mu}")
    command = " ".join(command_parts)
    return execute_ssh_command(command)

@mcp.tool()
def list_uprocs(uproc: str = None, mu: str = None) -> str:
    """Lists Uprocs with optional filters."""
    command_parts = ["uxlst upr"]
    if uproc:
        command_parts.append(f"UPR={uproc}")
    if mu:
        command_parts.append(f"MU={mu}")
    command = " ".join(command_parts)
    return execute_ssh_command(command)

if __name__ == "__main__":
    mcp.run()