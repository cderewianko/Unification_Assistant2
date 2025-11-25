


import subprocess

def is_docker_running2():
    try:
        result = subprocess.run(
            ["sc", "query", "com.docker.service"], capture_output=True, text=True
        )
        print('result.stdout: ', result.stdout)
        return "RUNNING" in result.stdout
    
    except FileNotFoundError:
        return False
    
    
def check_docker_uptime():
    """
    Returns True if Docker Engine is installed and running.
    Returns False if Docker is not installed or not running.
    """

    try:
        # Run: docker info (recommended way to check daemon status)
        result = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        print('result: ', result)
        if result.returncode == 0:
            return True  # Docker engine is responding
        else:
            return False

    except FileNotFoundError:
        # "docker" command not found -> Docker not installed
        return False

    except Exception:
        # Any other error (timeout, etc.)
        return False


def start_docker():
    if not check_docker_uptime():
        subprocess.run(["net", "start", "com.docker.service"])
        print("Docker started.")
    else:
        print("Docker is already running.")


def stop_docker():
    if check_docker_uptime():
        subprocess.run(["net", "stop", "com.docker.service"])
        print("Docker stopped.")
    else:
        print("Docker is already stopped.")
