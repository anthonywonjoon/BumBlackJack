from discord.ext import commands
import discord
import json

class Session(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_session = False
        self.session_earnings = {}
        self.session_buyins = {}
        self.session_message = None
        self.database_file = 'blackjack_data.json'
        self.session_house = ''

    def load_data(self):
        try:
            with open(self.database_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"users": {}}
    
    def save_data(self, data):
        with open(self.database_file, 'w') as file:
            json.dump(data, file, indent=4)

    async def update_session_message(self):
        if not self.session_message:
            return
        
        embed = discord.Embed(title="♠️Blackjack Session Info♠️", color=discord.Color.blue())
        embed.add_field(name="Status", value="Ongoing", inline=False)

        for username, buyin in self.session_buyins.items():
            earnings = self.session_earnings.get(username, 0)
            embed.add_field(name=username, value=f"Buy-in: {buyin} | Earnings: {earnings}", inline=False)

        await self.session_message.edit(embed=embed)

    @commands.command()
    async def startsession(self, ctx, house: str):
        await ctx.message.delete()

        if self.active_session:
            await ctx.send("A session is already active.")
        else:
            self.active_session = True
            self.session_earnings = {}
            self.session_buyins = {}
            self.session_house = house

            embed = discord.Embed(title="Blackjack Session Info", color=discord.Color.blue())
            embed.add_field(name="Status", value="Ongoing", inline=False)
            embed.add_field(name="House", value=f"{self.session_house}", inline=False)

            self.session_message = await ctx.send(embed=embed)
            await ctx.send("New Blackjack session started!")

    @commands.command()
    async def buyin(self, ctx, username: str, amount: int):
        if not self.active_session:
            await ctx.send("No active session. Start a session first.")
            return
        
        await ctx.message.delete()
    
        data = self.load_data()
        if data["users"].get(username) == None:
           return await ctx.send(f"User {username} not valid.")

        if username not in self.session_buyins:
            self.session_buyins[username] = 0

        self.session_buyins[username] += amount
        await self.update_session_message()
        await ctx.send(f"User {username} has bought in with {amount} credits.")
    
    @commands.command()
    async def payout(self, ctx, username: str, amount: int):
        if not self.active_session:
            await ctx.send("No active session. Start a session first")
            return
        
        await ctx.message.delete()
        
        if username not in self.session_earnings:
            self.session_earnings[username] = 0
        
        self.session_earnings[username] += amount
        await self.update_session_message()
        await ctx.send(f"User {username} has earned {amount} credits in this session.")

    @commands.command()
    async def endsession(self, ctx):
        if not self.active_session:
            await ctx.send("No active session to end.")
            return
        
        data = self.load_data()

        await ctx.message.delete()

        embed = discord.Embed(title="Blackjack Session Results", color=discord.Color.green())
        embed.add_field(name="House", value=f"{self.session_house}", inline=False)
        for username in self.session_buyins:
            buyin_amount = self.session_buyins[username]
            earnings = self.session_earnings.get(username, 0)
            net_earnings = earnings - buyin_amount

            if username in data['users']:
                data['users'][username]['lifetime_earnings'] += net_earnings
            else:
                await ctx.send(f"User {username} not found in the database.")

            embed.add_field(name=username, value=f"Net Earnings: {net_earnings}\nPay out: {net_earnings + self.session_buyins[username]}", inline=False)

        self.save_data(data)
        self.session_earnings = {}
        self.session_buyins = {}
        self.session_house = ''
        self.active_session = False

        await ctx.send(embed=embed)
        await ctx.send("Session ended and lifetime earnings updated.")

async def setup(bot):
    await bot.add_cog(Session(bot))

