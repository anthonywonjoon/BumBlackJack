from discord.ext import commands
import json

class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database_file = 'blackjack_data.json'

    def load_data(self):
        try:
            with open(self.database_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"users": {}}

    def save_data(self, data):
        with open(self.database_file, 'w') as file:
            json.dump(data, file, indent=4)

    @commands.command()
    async def adduser(self, ctx, username: str):
        data = self.load_data()

        if username in data['users']:
            await ctx.send(f"User {username} is already in the database.")
        else:
            data['users'][username] = {
                "username": username,
                "lifetime_earnings": 0
            }
            self.save_data(data)
            await ctx.send(f"User {username} has been added to the database.")

    @commands.command()
    async def removeuser(self, ctx, username: str):
        data = self.load_data()

        if username in data['users']:
            del data['users'][username]
            self.save_data(data)
            await ctx.send(f"User {username} has been removed from the database.")
        else:
            await ctx.send(f"User {username} not found in the database.")

async def setup(bot):
    await bot.add_cog(Users(bot))