import subprocess
import json
import os

def run_pct_command(command):
    """Executes a Proxmox pct command."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error: {result.stderr}")
    return result.stdout

def create_vps(vmid, template, storage, memory, cores, disk, password):
    """Creates a new LXC container."""
    command = f"pct create {vmid} {template} -storage {storage} -cores {cores} -memory {memory} -disk {disk} -password {password}"
    return run_pct_command(command)

def start_vps(vmid):
    """Starts the LXC container."""
    command = f"pct start {vmid}"
    return run_pct_command(command)

def stop_vps(vmid):
    """Stops the LXC container."""
    command = f"pct stop {vmid}"
    return run_pct_command(command)

def destroy_vps(vmid):
    """Destroys the LXC container."""
    command = f"pct destroy {vmid}"
    return run_pct_command(command)

def get_sshx_link(ip, port):
    """Generates an SSHX link."""
    return f"sshx://{ip}:{port}"

def get_vps_status(vmid):
    """Gets the status of a LXC container."""
    command = f"pct status {vmid}"
    return run_pct_command(command)

def get_container_ip(vmid):
    """Get the container's IP address."""
    command = f"pct exec {vmid} -- ip a | grep inet"
    output = run_pct_command(command)
    # Extract IP from output
    ip_line = [line for line in output.splitlines() if 'inet ' in line]
    if ip_line:
        ip = ip_line[0].split()[1]
        return ip.split('/')[0]  # Remove the subnet part
    return None

