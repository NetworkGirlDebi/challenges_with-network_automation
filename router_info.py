from iosxeapi.iosxerestapi import iosxerestapi

import click
import json


class User(object):
    def __init__(self, ip=None, port=None, username=None, password=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
    def set_up(self):
        return iosxerestapi(host=self.ip, username=self.username, password=self.password, port=self.port)

@click.group()
# ip addresses or dns of devices
@click.option("--ip",help="ip or dns address of device")
# file of ip addresseses or dns of devices
@click.option("--file",help="file ip addresses of devices")
# option for custom port or uses restconf port 443
@click.option("--port", default=443, help="device port, default = 443" )
# prompts user for name/password of device(s)
@click.option("--username",help="device username", prompt=True, hide_input=False)
@click.option("--password",help="device password", prompt=True, hide_input=True)
@click.pass_context
def main(ctx,ip, file, port, username, password):
    """Gather and Add IOS XE device information using restconf"""
    if ip:
        ctx.obj = User(ip,port, username, password)
        click.secho("Working....")
    else:
        try:
            with open(file) as f:
                device_data = json.load(f)
        except (ValueError, IOError, OSError) as err:
            print("Could not read the 'devices' file:", err)
        for ip in device_data.values():
            ctx.obj = dict()

            ctx.obj[ip['IP']] = User(ip['IP'],port, username, password)
            print(len(ctx.obj))
            click.secho("Working....{}".format(ip['IP']))


@main.command()
@click.pass_obj
def get_bgp(ctx):
    """Gather BGP information"""
    bgp = ctx.set_up().get_bgp()
    print(bgp)
    click.secho("Task completed")

@main.command()
@click.pass_obj
def get_interfaces(ctx):
    """Gather Interface information"""
    intf = ctx.set_up().get_interfaces_oper()
    print(intf)
    click.secho("Task completed")

# @main.command()
@click.Command(context_settings=None)
@click.pass_obj
def get_device(ctx):
    """Gather Device information"""
    for object in ctx.values():
        print(len(ctx))
        dev = object.set_up().get_device()
        print(dev)
    click.secho("Task completed")

@main.command()
@click.pass_obj
def add_drop(ctx):
    """Add ACL to Interface """
    click.secho("Select Interface!")
    router_object = ctx.set_up()
    list_interfaces = router_object.get_interfaces_list()
    user_interface = click.prompt('Available Interfaces Are:\n' + list_interfaces)
    access = router_object.add_access_group(user_interface)
    print(access.message)
    click.secho("Task completed")

@main.command()
@click.pass_obj
def delete_drop(ctx):
    """Remove ACL from Interface """
    click.secho("Select Interface!")
    router_object = ctx.set_up()
    list_interfaces = router_object.get_interfaces_list()
    user_interface = click.prompt('Available Interfaces Are:\n' + list_interfaces)
    delete = router_object.delete_access_group(user_interface)
    print(delete.message)
    click.secho("Task completed")

main()
