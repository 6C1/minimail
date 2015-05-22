'''
A teeny tiny mail sender.
'''
import argparse
import ConfigParser
from email.mime.text import MIMEText
import getpass
from os.path import isfile
import smtplib
import sys


DEFAULT_STRING = ("The sun is a miasma / "
                  "Of incandescent plasma / "
                  "The sun's not simply made out of gas / "
                  "(No, no, no) / "
                  "The sun is a quagmire / "
                  "It's not made of fire / "
                  "Forget what you've been told in the past"
                  )


def main():

    # Get arguments
    args = parse_args()
    # Get SMTP configuration
    email, host, port = configure(args["c"])
    # Process arguments
    args = process_args(args)

    # Get email password
    pw = getpass.getpass("Email password\n>> ")

    # Send email
    send(html_body(args['body']),
         args['subject'],
         args['recipient'],
         email,
         host,
         port,
         pw)


def configure(config_flag):
    '''
        Handles SMTP configuration.
        If either config_flag is set or the config file
        does not exist, prompt for one-time initial config.
    '''

    if not isfile("mm.cnf") or config_flag:
        init_config()

    config = ConfigParser.RawConfigParser()
    config.read("mm.cnf")
    return (config.get("SMTP", "email"),
            config.get("SMTP", "host"),
            config.getint("SMTP", "port"))


def init_config():

    print "\nMinimail Configuration. (You won't need to do this again.)\n"
    config = ConfigParser.RawConfigParser()
    config.add_section('SMTP')

    # Get config settings
    config.set('SMTP', 'host', raw_input("SMTP host address\n>> "))
    config.set('SMTP', 'port', raw_input("Port number\n>> "))
    config.set('SMTP', 'email', raw_input("Email address\n>> "))

    # Write the configuration
    with open("mm.cnf", "wb") as config_file:
        config.write(config_file)

    print "\nConfiguration complete!\n"


def html_body(body):
    '''
        Sew up the body into html paragraphs.
    '''

    return "".join(["<p>{}</p>".format(line) for line in body])


def process_args(args):
    '''
        Processes each argument, returns dictionary.
    '''

    return {arg.lower(): process_arg(arg, args) for arg in args}


def process_arg(arg, args):
    '''
        Processes an individual argument. Prompts for input if no
        argument was given. Formats body argument as list if only
        one body line was given.
    '''

    result = get_arg(arg) if args[arg] == DEFAULT_STRING else args[arg]
    return result if arg != "Body" or isinstance(result, list) else [result]


def get_arg(arg):
    '''
        Gets an argument from the user.
    '''

    return raw_input("Enter {}:\n>> ".format(arg.lower()))


def send(body, subj, to_addr, from_addr, host, port, pw):
    '''
        Sends an email.
    '''

    msg = MIMEText(body, 'html')
    msg['subject'] = subj
    msg['from'] = from_addr
    msg['to'] = to_addr

    try:
        s = smtplib.SMTP(host, port)
        s.login(from_addr, pw)
        s.sendmail(from_addr, to_addr, msg.as_string())
        s.quit()
        print "Message delivered"
    except Exception as e:
        print e
        exit()


def parse_args():
    '''
        Parse cli arguments.
    '''

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("Recipient",
                        help="The address you're emailing",
                        nargs="?",
                        default=DEFAULT_STRING)
    parser.add_argument("Subject",
                        help="What you're emailing about",
                        nargs="?",
                        default=DEFAULT_STRING)
    parser.add_argument("Body",
                        help="What your email says",
                        nargs="*",
                        default=DEFAULT_STRING)
    parser.add_argument("-c",
                        help="Configure SMTP settings",
                        action='store_true')

    return vars(parser.parse_args())


if __name__ == "__main__":
    main()
