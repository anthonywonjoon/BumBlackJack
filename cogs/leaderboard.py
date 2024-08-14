from discord.ext import commands
import discord
import json

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database_file = 'blackjack_data.json'

    def load_data(self):
        try:
            with open(self.database_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"users": {}}
    
    @commands.command()
    async def leaderboard(self, ctx):
        data = self.load_data()

        leaderboard = sorted(data['users'].items(), key=lambda x: x[1]['lifetime_earnings'], reverse=True)
        
        embed = discord.Embed(title="🏆 Bunch of Bums Leaderboard 🏆", color=discord.Color.gold())
        i = 1
        rank = ""
        for username, details in leaderboard:
            earnings = details['lifetime_earnings']
            match i:
                case 1:
                    rank = "🥇"
                case 2:
                    rank = "🥈"
                case 3:
                    rank = "🥉"
                case _:
                    rank = i

            embed.add_field(name=f"{rank}. {username}", value=f"Lifetime Earnings: {earnings} credits", inline=False)
            i += 1

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))