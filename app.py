from flask import Flask, render_template
import socket
import subprocess

app = Flask(__name__)

# ---------------- PORT SCAN ----------------
def scan_ports():
    result = ""
    open_ports = []

    for port in range(1, 101):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)

            res = s.connect_ex(('127.0.0.1', port))
            s.close()

            if res == 0:
                result += f"❌ Port {port} is OPEN (Risk)\n"
                open_ports.append(port)
            else:
                result += f"✅ Port {port} is CLOSED (Safe)\n"

        except Exception as e:
            result += f"Error checking port {port}: {e}\n"

    # Summary
    if open_ports:
        result = f"⚠️ RISK: {len(open_ports)} open ports detected!\n\n" + result
    else:
        result = "🟢 SAFE: No open ports detected (1–100)\n\n" + resultw

    return result


# ---------------- FIREWALL CHECK ----------------
def check_firewall():
    try:
        res = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles"],
            capture_output=True,
            text=True
        )

        output = res.stdout.upper()

        print(output)  # DEBUG

        # Correct matching
        on_count = output.count("STATE                                 ON")
        off_count = output.count("STATE                                 OFF")

        if off_count == 3:
            return "⚠️ Firewall is OFF ❌ (All profiles disabled)"

        elif on_count == 3:
            return "🛡️ Firewall is ON ✅ (All profiles protected)"

        else:
            return "⚠️ Firewall PARTIALLY ON ⚠️"

    except Exception as e:
        return f"Error: {e}"


# ---------------- PROCESS CHECK ----------------
def check_processes():
    try:
        result = subprocess.check_output(
            "tasklist",
            shell=True
        ).decode(errors="ignore")

        return result

    except Exception as e:
        return str(e)


# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- PORT ROUTE ----------------
@app.route('/ports')
def ports():
    return f"""
    <body style='background:#050816;color:white;padding:20px;font-family:Arial'>
        <h1 style='color:cyan'>Open Port Scan</h1>
        <pre>{scan_ports()}</pre>
        <br>
        <a href='/' style='color:cyan'>⬅ Back</a>
    </body>
    """


# ---------------- FIREWALL ROUTE ----------------
@app.route('/firewall')
def firewall():

    result = check_firewall()

    # FIXED COLOR LOGIC
    if "ALL PROFILES PROTECTED" in result.upper():
        color = "lightgreen"

    elif "ALL PROFILES DISABLED" in result.upper():
        color = "red"

    else:
        color = "orange"

    return f"""
    <body style='background:#050816;color:white;padding:30px;font-family:Arial'>
        <h1>Firewall Status</h1>

        <h2 style='color:{color}'>
            {result}
        </h2>

        <br>

        <a href='/' style='color:cyan'>
            ⬅ Back
        </a>
    </body>
    """


# ---------------- PROCESS ROUTE ----------------
@app.route('/processes')
def processes():

    return f"""
    <body style='background:#050816;color:white;padding:20px;font-family:Arial'>

        <h1 style='color:cyan'>
            Running Processes
        </h1>

        <pre>
{check_processes()}
        </pre>

        <br>

        <a href='/' style='color:cyan'>
            ⬅ Back
        </a>

    </body>
    """


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)