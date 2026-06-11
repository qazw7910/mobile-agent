import json
import subprocess
import re
import logging

def create_simulator(name: str, device_type: str):
    """Create a new iOS simulator."""
    runtime = get_runtimes()
    UUID = []
    try:
        for i in range(5):
            result = subprocess.run(
                ['xcrun', 'simctl', 'create', name, device_type, runtime],
                capture_output=True,
                text=True,
                check=True
            )
            UUID.append(result.stdout.strip())
        logging.info(f"已建立 {i+1} 台 {device_type} 模擬器")
        return UUID
    except subprocess.CalledProcessError as e:
        print(f"Error creating simulator: {e.stderr}")
        return None


def get_runtimes():
    """Get available  runtimes for iOS simulators."""

    try:
        res = subprocess.run(
            ['xcrun', 'simctl', 'list', 'runtimes', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        result = json.loads(res.stdout)
        runtimes = result["runtimes"][0]["identifier"]
        return runtimes
    except subprocess.CalledProcessError as e:
        print(f"Error getting runtimes: {e.stderr}")
        return None


if __name__ == "__main__":
    result = create_simulator("iPad 1013", "iPad (10th generation)")
    print(result)
