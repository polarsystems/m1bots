import os
import discord
from dotenv import load_dotenv
from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc

app = Quart(__name__) #

app.secret_key = b"sub2me"

load_dotenv()
app.config["DISCORD_CLIENT_ID"] = "906530431577522228"
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("SEC")
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv("TOKEN")

discord = DiscordOAuth2Session(app)
client = ipc.Client(secret_key="sub2me")

@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/login/")
async def login():
    return await discord.create_session()

@app.route("/callback/")
async def callback():
    try:
        await discord.callback()
    except:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))



@app.route("/dashboard/")
async def dashboard():
    user = await discord.fetch_user()
    return await render_template("dashboard.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)