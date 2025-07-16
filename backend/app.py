from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

FIRESTICKS = {
    "luc bedroom": "192.168.1.188"
}

def adb_command(ip, command):
    subprocess.run(["adb", "connect", ip])
    return subprocess.run(["adb", "shell"] + command, capture_output=True, text=True)

@app.route("/firesticks", methods=["GET"])
def get_firesticks():
    return jsonify(list(FIRESTICKS.keys()))

@app.route("/control", methods=["POST"])
def control():
    data = request.json
    name = data.get("device")
    action = data.get("action")

    ip = FIRESTICKS.get(name)
    if not ip:
        return jsonify({"error": "Device not found"}), 404

    keymap = {
        "home": ["input", "keyevent", "3"],
        "up": ["input", "keyevent", "19"],
        "down": ["input", "keyevent", "20"],
        "left": ["input", "keyevent", "21"],
        "right": ["input", "keyevent", "22"],
        "ok": ["input", "keyevent", "23"],
        "back": ["input", "keyevent", "4"]
    }

    cmd = keymap.get(action)
    if not cmd:
        return jsonify({"error": "Invalid action"}), 400

    result = adb_command(ip, cmd)
    return jsonify({"output": result.stdout or result.stderr})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
