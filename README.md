# discord-subversion-hook-scripts
## Table Of Contents

> [**1. About**](#1)  
[**2. Software**](#2)  
[**3. Dependencies**](#3)  
[**4. Hook Scripts**](#4)  
[4.1. Post-commit](#4_post-commit)  

---

## <a name="1"></a>1. About
Subversion (VisualSVN) hook scripts that post messages to Discord.

**NOTE:** The CMD hook scripts that call the Python scripts are only valid when used with a Windows installation of VisualSVN. However, it should not be difficult to set it up with a non-Windows installation.

## <a name="2"></a>2. Software
* VisualSVN : https://www.visualsvn.com/
* Discord : https://discordapp.com/
* Python 3.6 : https://www.python.org/downloads/

## <a name="3"></a>3. Dependencies
You'll need to have the following Python libraries installed in order to use these hook scripts. They can be installed with the `pip install <libraryname>` command-line command.

* `requests` library : `pip install requests`
* `subprocess` library : `pip install subprocess`
* `sys` library : (included in Python)

## <a name="4"></a>4. Hook Scripts
### <a name="4_post-commit"></a>4.1. Post-commit
#### <a name="4_post-commit_1"></a>4.1.1. What It Does
After a commit is made to the specified repository, this hook script posts a message to Discord server channel, which is specified through a webhook. The message contains the name of the repository, the revision number, the name of the user who committed, the commit message, and the changelist. The hook script will automagically truncate commit messages longer than 200 characters and changelists longer than 1700 characters in order to abide by Discord's maximum character limit of 2000.

#### <a name="4_post-commit_2"></a>4.1.2. Usage Examples
Below are a few examples of what the message looks like in multiple scenarios.

Normal-length commit message and changelist:  
![post-commit-example_normal](https://raw.githubusercontent.com/marth8880/discord-subversion-hook-scripts/master/img/post-commit-example_normal.png)

Long commit message, normal-length changelist:  
![post-commit-example_long-commit-message](https://raw.githubusercontent.com/marth8880/discord-subversion-hook-scripts/master/img/post-commit-example_long-commit-message.png)

Normal-length commit message, long changelist:  
![post-commit-example_long-changelist](https://raw.githubusercontent.com/marth8880/discord-subversion-hook-scripts/master/img/post-commit-example_long-changelist.png)

#### <a name="4_post-commit_3"></a>4.1.3. How To Use
1. In VisualSVN, open your repository's Properties page.

![post-commit-1](https://raw.githubusercontent.com/marth8880/discord-subversion-hook-scripts/master/img/post-commit-1.png)  

2. Navigate to the Hooks tab and double-click the "Post-commit hook" property.

![post-commit-2](https://raw.githubusercontent.com/marth8880/discord-subversion-hook-scripts/master/img/post-commit-2.png)  

3. Copy the contents of [scr/post-commit.cmd](https://github.com/marth8880/discord-subversion-hook-scripts/blob/master/scr/post-commit.cmd) and paste them into the hook dialog's text box.

![post-commit-3](https://raw.githubusercontent.com/marth8880/discord-subversion-hook-scripts/master/img/post-commit-3.png)  

4. Change `pythonw_file_path` to point to the location of `pythonw.exe` in your Python installation directory.

5. Download [scr/post-commit.py](https://github.com/marth8880/discord-subversion-hook-scripts/blob/master/scr/post-commit.py), then change `hook_script_file_path` to point to the file path to which you downloaded `post-commit.py`.

6. Change `reponame` to the name of the repository as set in VisualSVN.

7. In your Discord server, [create a webhook](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks) in the channel in which the commit messages should be posted, copy the URL, then change `discord_webhook_url` to that URL. 

**NOTE:** The Python hook script will override any username and avatar you specify in the Discord webhook dialog. With that said, the script can easily be changed if you don't want it to do this.

8. Click OK to accept the changes in the hook dialog, then click Apply and OK to accept the changes in the Properties dialog.

9. Open `post-commit.py` in a text editor.

10. Change the value of `reporootdir` to point to the root directory in which your Subversion repositories are stored. Don't forget to use double-backslashes in the file path! Also, make sure there's a (double-)backslash at the end of the file path so the repository's full file path can be assembled correctly. 

**EXAMPLE:** `reporootdir = "Y:\\Repositories\\"`

11. Change the value of `svnlook` to point to the location of `svnlook.exe`, which can be found in VisualSVN's installation directory. 

**EXAMPLE:** `svnlook = "C:\\Program Files\\VisualSVN Server\\bin\\svnlook.exe"`

12. Optionally, change the value of `botavatarurl` to the URL of your own custom image to use for the avatar of the bot that'll post the commit message. 

**EXAMPLE:** `botavatarurl = "https://i.imgur.com/Pi5ICIR.jpg"`

13. Finally, save and close the file and try out the hook with a test commit to the repository for which you configured it!
