# Import libraries for HTTP requests, processing EXE output, and getting parameter values passed from our caller script (in VisualSVN)
import requests
import subprocess
import sys
import os.path

# Discord has a message length limit of 2000 characters, so we need to set some maximum string length limits
MAX_LENGTH_LOG = 200
MAX_LENGTH_CHANGELIST = 1700

# Base name to give our bot that'll post the payload message
botusernamebase = "SVN"

# URL of image to use for our bot's avatar (I recommend hosting this image elsewhere like AWS)
botavatarurl = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Antu_smartsvn.svg/1200px-Antu_smartsvn.svg.png"

# Root directory in which the repositories are stored
reporootdir = "/svn/data/repositories/"    # CHANGE THIS TO POINT TO YOUR REPOSITORY ROOT DIRECTORY

# Local file path of svnlook.exe, which is used to get the commit's author, log, and changelist
svnlook = "/opt/CollabNet_Subversion/bin/svnlook"    # CHANGE THIS TO POINT TO YOUR SVNLOOK.EXE PATH

# URL of webhook to which we'll send our payload
webhookurl = sys.argv[3]

# Revision number of the commit
revision = sys.argv[1]

# Name of the repository that was committed to
reponame = os.path.basename(sys.argv[2])

# Name of the location that was committed to
location = sys.argv[4]

# Assemble the repository's file path
repopath = "{0}{1}".format(reporootdir, reponame)

# Get the commit's author with svnlook
process_author = subprocess.Popen([svnlook, "author", repopath, "-r", revision], stdout=subprocess.PIPE)
author, author_err = process_author.communicate()

# Get the commit message with svnlook
process_log = subprocess.Popen([svnlook, "log", repopath, "-r", revision], stdout=subprocess.PIPE)
loglong, loglong_err = process_log.communicate()

# Set default message for when there's no commit message
if loglong.decode().isspace():
	log_decoded = True
	loglong = "<no commit message>"
else:
	log_decoded = False

# Get the commit's changelist with svnlook
# process_changelist = subprocess.Popen([svnlook, "changed", repopath, "-r", revision], stdout=subprocess.PIPE)
# changelistlong, changelistlong_err = process_changelist.communicate()

# Set default message for when there's (somehow) no changelist
# if changelistlong.decode().isspace():
#	changelist_decoded = True
#	changelistlong = "<no changelist>"
#else:
#	changelist_decoded = False


# Prune the new lines from the endings
author = author.strip()
loglong = loglong.strip()
# changelistlong = changelistlong.strip()


# Truncate end of log if it exceeds max length
if (len(loglong) > (MAX_LENGTH_LOG - 6)):
	log_decoded = True
	logparsed = loglong[0:(MAX_LENGTH_LOG - 6)]
	log = "{0} <...>".format(logparsed.decode())
else:
	log = loglong

# Truncate end of changelist if it exceeds max length
#if (len(changelistlong) > (MAX_LENGTH_CHANGELIST - 6)):
#	changelist_decoded = True
#	changelistparsed = changelistlong[0:(MAX_LENGTH_CHANGELIST - 6)]
#	changelist = "{0} <...>".format(changelistparsed.decode())
#else:
#	changelist = changelistlong


# Do some last-minute pruning for good measure
reponame = reponame.strip()
revision = revision.strip()
author = author.decode()

# Decode the log and changelist if they haven't been already
if not log_decoded:
	log = log.decode()
#if not changelist_decoded:
#	changelist = changelist.decode()


# Assemble our bot's username based on the base name and the author who made the commit (e.g., "Aaron (Subversion)")
botusername = "{0} ({1})".format(author, botusernamebase)

# Assemble our message to include in the payload
message = "**{0}:**  Revision {1} committed to {4} by {2}:\n```{3}```".format(reponame, revision, author, log, location)

# Construct our payload to send to the webhook
payload = {
	'username': botusername,
	'avatar_url': botavatarurl,
	'content': message
}

# Send our payload to the webhook with an HTTP POST request
r = requests.post(webhookurl, data=payload)
print(r.status_code, r.reason)
