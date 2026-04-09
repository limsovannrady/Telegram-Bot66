from flask import Flask, render_template_string

app = Flask(__name__)

users = {}

@app.route("/")
def dashboard():
    html = """
    <h1>Telegram Bot Users Dashboard</h1>
    <table border="1">
        <tr><th>User ID</th><th>Full Name</th><th>Username</th></tr>
        {% for user_id, info in users.items() %}
        <tr>
            <td>{{ user_id }}</td>
            <td>{{ info.full_name }}</td>
            <td>{{ info.username }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, users=users)
