:: Location of pythonw.exe
@set PYTHON_EXE="pythonw_file_path"

:: Location of post-commit Python script
@set HOOK_SCRIPT="hook_script_file_path"

:: Revision number; REV argument passed from Subversion
@set REVISION_NUM=%2

:: Name of repository (as set in VisualSVN)
@set REPO_NAME=reponame

:: Webhook URL of Discord channel that the message will be posted in
@set WEBHOOK_URL="discord_webhook_url"


:: EXECUTE ORDER 66 (aka the hook script)
%PYTHON_EXE% %HOOK_SCRIPT% %REVISION_NUM% %REPO_NAME% %WEBHOOK_URL%
