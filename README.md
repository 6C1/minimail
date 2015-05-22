# minimail

Minimail is a teeny tiny mail sender.

## Installation

Clone this repo and run

    `sudo python setup.py install`

## Configuration

The first time you run minimail, you'll be prompted for SMTP configuration details.

* Host
* Port
* Email address

You can change these later by running `minimail -c`

## Usage

Basic usage is `minimail [recipient] [subject] [body line 1] [body line 2] ...`

You can leave off arguments, and minimail will prompt for them, however multiline
bodies are currently only possible as initial arguments.

Minimail will then prompt for your email password. This is never stored, but
you should check the source to verify that for yourself.