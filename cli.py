from dotenv import load_dotenv
from slotter import Slotter
import click, sys, os

# load the .env variables
load_dotenv()

session_id = os.environ.get("INTRA_SESSION_ID")

if not session_id:
    print("Please add your INTRA session id!", file=sys.stderr)
    sys.exit(1)

# create an instance from Slotter class

slotter = Slotter(session_id)

# login with session intra and check if valid

if not slotter.login():
    print("Please add a valid INTRA session id!", file=sys.stderr)
    sys.exit(1)


@click.group()
def cli():
    "Slotter Command line interface."

def validate_duration(ctx, param, value):
    if value < 30:
        raise click.BadParameter('duration should be greate than 30.')
    return value
   

@cli.command
@click.option("--duration", "-d", type=int, callback=validate_duration, default=30)
def take_slots(duration):
    """take the untaken slots"""
    slotter.take_slots(duration)



@cli.command
def delete_slots():
    """delete the taken slots"""
    slotter.delete_slots()

if __name__ == "__main__":
    cli(prog_name='slotter')