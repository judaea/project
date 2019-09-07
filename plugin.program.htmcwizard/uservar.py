import os, xbmc, xbmcaddon

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'HTMC Wizard'
BUILDERNAME    = 'HTMC'
EXCLUDES       = [ADDON_ID, 'repository.htmc']
# Enable/Disable the text file caching with 'Yes' or 'No' and age being how often it rechecks in minutes
CACHETEXT      = 'Yes'
CACHEAGE       = 30
# Text File with build info in it.
BUILDFILE      = 'https://raw.githubusercontent.com/judaea/project/master/builds/builds.txt'
# How often you would like it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.  Leave as 'http://' to ignore
APKFILE        = 'https://raw.githubusercontent.com/judaea/project/master/apks/apks.txt'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = ''
YOUTUBEFILE    = 'http://'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'http://'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://'

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons then place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
# If you want to host online:
# ICONMAINT  = 'http://yourwebsite.com/repo/wizard/maintenance.png'
# Leave as http:// for default icon
ICONADDONS     = os.path.join(ART, 'addons.png')
ICONLOGIN      = os.path.join(ART, 'apidata.png')
ICONAPK        = os.path.join(ART, 'apks.png')
ICONBACKUP     = os.path.join(ART, 'backup.png')
ICONBUILDS     = os.path.join(ART, 'builds.png')
ICONCONTACT    = os.path.join(ART, 'contact.png')
ICONDEV        = os.path.join(ART, 'developer.png')
ICONFRESH      = os.path.join(ART, 'fresh.png')
ICONKODI       = os.path.join(ART, 'kodi.png')
ICONMAINT      = os.path.join(ART, 'maintenance.png')
ICONREAL       = os.path.join(ART, 'realdebrid.png')
ICONSAVE       = os.path.join(ART, 'savedata.png')
ICONSETTINGS   = os.path.join(ART, 'settings.png')
ICONSPMC       = os.path.join(ART, 'spmc.png')
ICONTOOLS      = os.path.join(ART, 'tools.png')
ICONTRAKT      = os.path.join(ART, 'trakt.png')
ICONWIPE       = os.path.join(ART, 'wipe.png')
ICONWIZARD     = os.path.join(ART, 'wizard.png')
ICONYOUTUBE    = os.path.join(ART, 'youtube.png')

# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '='

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'dodgerblue'
COLOR2         = 'white'
COLOR3         = 'lime'
COLOR4         = 'yellow'
COLOR5         = 'red'

# Main menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR2+']%s[/COLOR]'

# Build txt file names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'

# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'

# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Lime Maintenance submenu items      / %s is the menu item and is required
THEME6         = '[COLOR '+COLOR3+']%s[/COLOR]'

# Yellow Wipe submenu items      / %s is the menu item and is required
THEME7         = '[COLOR '+COLOR4+']%s[/COLOR]'

# Red Wipe submenu items      / %s is the menu item and is required
THEME8         = '[COLOR '+COLOR5+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'Yes'
# You can add \n to do line breaks
CONTACT        = 'Thank you for choosing HTMC Wizard.\n\nContact us on Github at https://github.com/judaea'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = os.path.join(ART, 'qricon.png')
CONTACTFANART  = os.path.join(ART, 'fanart.jpg')
#########################################################

#########################################################
### AUTO UPDATE FOR THOSE WITH NO REPO ##################
#########################################################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'Yes'
# Url to wizard version
WIZARDFILE     = BUILDFILE
#########################################################

#########################################################
### AUTO INSTALL REPO IF NOT INSTALLED ##################
#########################################################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'Yes'
# Addon ID for the repository
REPOID         = 'repository.htmc'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.githubusercontent.com/judaea/project/master/zips/addons.xml'
# Url to folder zip is located in
REPOZIPURL     =  'https://raw.githubusercontent.com/judaea/project/master/zips/repository.htmc/'
#########################################################

#########################################################
### NOTIFICATION WINDOW #################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'https://raw.githubusercontent.com/judaea/project/master/builds/notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
# Font size of header
FONTHEADER     = 'Font14'
HEADERMESSAGE  = '[B][COLOR dodgerblue]HTMC[/COLOR][/B] Wizard'
# url to image if using Image 424x180
HEADERIMAGE    = 'http://'
# Font for Notification Window
FONTSETTINGS   = 'Font13'
# Background for Notification Window
# BACKGROUND     = os.path.join(ART, 'fanart.jpg')
BACKGROUND     = 'http://'
#########################################################

#########################################################
### FIRST RUN BUILD MENU WINDOW BACKGROUND IMAGE ########
#########################################################
# If you want to use locally stored fanart then place it in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'fanart.png')
# If you want to host online:
# BUILDMENUFANART  = 'http://yourwebsite.com/repo/wizard/fanart.jpg'
# For default leave as BUILDMENUFANART  = 'http://'
BUILDMENUFANART  = os.path.join(ART, 'fanartbm.jpg')
#########################################################
