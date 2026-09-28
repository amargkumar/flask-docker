# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import platform, random, socket, time
import flask
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)
START = time.time()
visits = 0

FACTS = [
    "A container's hostname defaults to the first 12 characters of its container ID.",
    "Containers share the host's kernel, which is why they start in seconds.",
    "Docker was open-sourced in 2013.",
    "Docker's whale mascot is named Moby Dock.",
    "Docker caches each build step, so unchanged steps are skipped on rebuild.",
    "Python 2 reached end of life on January 1, 2020, yet this container still runs it.",
]

def os_name():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=", 1)[1].strip().strip('"')
    except (IOError, OSError):
        pass
    return platform.system()

def info():
    up = int(time.time() - START)
    return {
        "container_id": socket.gethostname(),
        "os": os_name(),
        "python": platform.python_version(),
        "flask": flask.__version__,
        "uptime": "%dh %dm %ds" % (up // 3600, up % 3600 // 60, up % 60),
        "visits": visits,
    }

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Flask in Docker</title>
<style>
 body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
      background:linear-gradient(135deg,#0b2545,#13315c);font-family:system-ui,sans-serif;color:#eef4ed}
 .card{background:rgba(255,255,255,.08);border-radius:16px;padding:32px 40px;max-width:560px;width:90%;
       box-shadow:0 10px 40px rgba(0,0,0,.4)}
 h1{margin:0 0 4px;font-size:28px} .sub{opacity:.7;margin-bottom:24px}
 table{width:100%;border-collapse:collapse} td{padding:8px 0;border-bottom:1px solid rgba(255,255,255,.12)}
 td:first-child{opacity:.7} td:last-child{text-align:right;font-family:monospace}
 .fact{margin-top:24px;padding:14px 16px;background:rgba(29,161,242,.18);border-left:4px solid #1da1f2;border-radius:8px}
 a{color:#8ecbff} .row{display:flex;justify-content:space-between;margin-top:20px;font-size:14px}
</style></head><body><div class="card">
 <h1>🐳 Hello from a container!</h1>
 <div class="sub">This Flask app is running inside Docker.</div>
 <table>
  <tr><td>Container ID</td><td>{{ i.container_id }}</td></tr>
  <tr><td>OS inside container</td><td>{{ i.os }}</td></tr>
  <tr><td>Python</td><td>{{ i.python }}</td></tr>
  <tr><td>Flask</td><td>{{ i.flask }}</td></tr>
  <tr><td>Container uptime</td><td>{{ i.uptime }}</td></tr>
  <tr><td>Page visits</td><td>{{ i.visits }}</td></tr>
  <tr><td>Your IP (as seen by container)</td><td>{{ ip }}</td></tr>
 </table>
 <div class="fact"><b>Docker fact:</b> {{ fact }}</div>
 <div class="row"><a href="/">↻ New fact</a><a href="/api/info">JSON API →</a></div>
</div></body></html>"""

@app.route('/')
def home():
    global visits
    visits += 1
    return render_template_string(PAGE, i=info(), fact=random.choice(FACTS), ip=request.remote_addr)

@app.route('/api/info')
def api_info():
    return jsonify(info())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
