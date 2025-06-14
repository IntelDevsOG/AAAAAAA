import discord
from discord.ext import commands
import json
import random
import string
from proxmox_utils import create_vps, start_vps, stop_vps, destroy_vps, get_sshx_link, get_vps_status, get_container_ip

class VPSCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()

    def load_config(self):
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)

    @commands.command()
    async def create_vps(self, ctx, vmid=None):
        """Creates a new LXC VPS."""
        if not self.is_allowed(ctx):
            await ctx.send("You don't have permission to use this command.")
            return

        if vmid is None:
            vmid = self.config["vps_defaults"]["start_vmid"]

        # Generate random password for the container
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        # Create the VPS
        try:
            create_vps(vmid, self.config['vps_defaults']['template'], self.config['vps_defaults']['storage'],
                       self.config['vps_defaults']['memory'], self.config['vps_defaults']['cores'],
                       self.config['vps_defaults']['disk'], password)
            start_vps(vmid)

            # Get the container's IP
            ip = get_container_ip(vmid)
            if ip:
                sshx_link = get_sshx_link(ip, 22)
                embed = discord.Embed(title="VPS Created", description=f"Your VPS is ready!")
                embed.add_field(name="VPS ID", value=vmid)
                embed.add_field(name="SSHX Link", value=sshx_link)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Could not retrieve the VPS IP.")
        except Exception as e:
            await ctx.send(f"Error creating VPS: {str(e)}")

    @commands.command()
    async def stop_vps(self, ctx, vmid):
        """Stops a running LXC VPS."""
        if not self.is_allowed(ctx):
            await ctx.send("You don't have permission to use this command.")
            return

        try:
            stop_vps(vmid)
            await ctx.send(f"VPS {vmid} stopped.")
        except Exception as e:
            await ctx.send(f"Error stopping VPS: {str(e)}")

    @commands.command()
    async def start_vps(self, ctx, vmid):
        """Starts a stopped LXC VPS."""
        if not self.is_allowed(ctx):
            await ctx.send("You don't have permission to use this command.")
            return

        try:
            start_vps(vmid)
            await ctx.send(f"VPS {vmid} started.")
        except Exception as e:
            await ctx.send(f"Error starting VPS: {str(e)}")

    @commands.command()
    async def destroy_vps(self, ctx, vmid):
        """Destroys an LXC VPS."""
        if not self.is_allowed(ctx):
            await ctx.send("You don't have permission to use this command.")
            return

        try:
            destroy_vps(vmid)
            await ctx.send(f"VPS {vmid} destroyed.")
        except Exception as e:
            await ctx.send(f"Error destroying VPS: {str(e)}")

    @commands.command()
    async def vps_status(self, ctx, vmid):
        """Check the status of a VPS."""
        if not self.is_allowed(ctx):
            await ctx.send("You don't have permission to use this command.")
            return

        try:
            status = get_vps_status(vmid)
            await ctx.send(f"VPS {vmid} status: {status}")
        except Exception as e:
            await ctx.send(f"Error fetching VPS status: {str(e)}")

    def is_allowed(self, ctx):
        """Check if the user has a valid role."""
        allowed_roles = self.config['user_roles'] + self.config['admin_roles']
        user_roles = [role.id for role in ctx.author.roles]
        return any(role in allowed_roles for role in user_roles)

