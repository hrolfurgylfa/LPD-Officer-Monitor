from discord.ext import commands

from .custom_arg_parse import ArgumentParser
import argparse
import re

class Time(commands.Cog):
    """This stores all the time commands."""
    def __init__(self, bot, officer_manager):
        self.bot = bot
        self.officer_manager = officer_manager

    @staticmethod
    def seconds_to_string(onDutySeconds):

        #Calculate days, hours, minutes and seconds
        onDutyMinutes, onDutySeconds = divmod(onDutySeconds, 60)
        onDutyHours, onDutyMinutes = divmod(onDutyMinutes, 60)
        onDutyDays, onDutyHours = divmod(onDutyHours, 24)
        onDutyweeks, onDutyDays = divmod(onDutyDays, 7)

        # Move the time to the string
        on_duty_time_string = ""
        if onDutyweeks != 0:
            on_duty_time_string += "\nWeeks: "+str(onDutyweeks)
        if onDutyDays + onDutyweeks != 0:
            on_duty_time_string += "\nDays: "+str(onDutyDays)
        if onDutyHours + onDutyDays + onDutyweeks != 0:
            on_duty_time_string += "\nHours: "+str(onDutyHours)
        if onDutyMinutes + onDutyHours + onDutyDays + onDutyweeks != 0:
            on_duty_time_string += "\nMinutes: "+str(onDutyMinutes)
        on_duty_time_string += "\nSeconds: "+str(onDutySeconds)

        return on_duty_time_string

    @commands.command()
    async def user(self, ctx, *args):
        """
        This command gets the on duty time for an officer

        NAME
            ?user - get on duty time and last active information
                    about a specific officer.

        SYNOPSIS
            ?user [options] officer
        
        OPTIONS
            -d NUMBER,
            --days NUMBER
                specify the number of days to look back for activity,
                this defaults to 28.

            -f DATE,
            --from-date DATE
                specify the date to look back at, if no --to-date
                is specified it will show all activity from the
                --from-date to right now.

            -t DATE,
            --to-date DATE
                specify the date to stop looking at, --from-date
                has to be specified with this option.
        """

        # Setup parser
        parser = ArgumentParser(description="Argparse user command")
        parser.add_argument('officer')
        parser.add_argument("-d", "--days", type=int)
        parser.add_argument("-f", "--from-date")
        parser.add_argument("-t", "--to-date")

        # Parse command and check errors
        try: parsed = parser.parse_args(args)
        except argparse.ArgumentError:
            await ctx.send(ctx.author.mention+" This is an error in your command syntax.")
            return
        except argparse.ArgumentTypeError:
            await ctx.send(ctx.author.mention+" One of your arguments is the wrong type. For example putting in text where a number is expected.")
            return

        # Find the officer ID
        p = re.compile(r"<@\![0-9]{18,20}>")
        match = p.match(parsed.officer)
        
        # Make sure someone is mentioned
        if not match:
            await ctx.send(ctx.author.mention+" Make sure to mention an officer.")
            return
        
        # Move the officer_id into a variable
        officer_id = int(match.group()[3:-1])
        print("officer_id:",officer_id)
        
        # Make sure the person mentioned is an LPD officer
        officer = self.officer_manager.get_officer(officer_id)
        if officer is None:
            await ctx.send(ctx.author.mention+" The person you mentioned is not being monitored, are you sure this person is an officer?")
            return
        
        
        # ====================
        # Parse extra options
        # ====================

        try:
            if parsed.days:
                print("Length")
                time_seconds = await officer.get_time_days(parsed.days)

                out_string = "On duty time for "+officer.mention+" - last "+str(parsed.days)+ " days"
                out_string += self.seconds_to_string(time_seconds)

                await ctx.send(out_string)

            elif parsed.from_date or parsed.to_date:
                print("Date")

                # Make sure their is a from_date if their is a to date
                if parsed.to_date and not parsed.from_date:
                    await ctx.send(ctx.author.mention+" If you want to use to-date you have to set a from-date.")
                    return

                print(parsed.from_date, parsed.to_date)

                time_seconds =  await officer.get_time_date(parsed.from_date, parsed.to_date)

                out_string = "On duty time for "+officer.mention+" - from: "+str(parsed.from_date)+"  to: "+str(parsed.to_date)
                out_string.replace("None", "Right now")
                print(time_seconds)
                out_string += self.seconds_to_string(time_seconds)

                await ctx.send(out_string)

            else:
                print("Default length")
                time_seconds =  await officer.get_time_days(28)

                out_string = "On duty time for "+officer.mention+" - last "+str(28)+ " days"
                out_string += self.seconds_to_string(time_seconds)

                await ctx.send(out_string)
            
        except ValueError as error:
            await ctx.send(error)
    
    