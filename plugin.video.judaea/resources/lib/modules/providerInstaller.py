import zipfile, xbmc, xbmcaddon, json, requests, os, base64
from resources.lib.modules import control
from resources.lib.modules import customProviders

# Below is the contents of the providers/__init__.py base64 encoded
# If you update this init file you will need to update this base64 as well to ensure it is deployed on the users machine
# If you change the init file without updating this it will be overwritten with the old one!!

init_contents = 'aW1wb3J0IG9zCmZyb20gcmVzb3VyY2VzLmxpYi5tb2R1bGVzIGltcG9ydCBjb250cm9sCmZyb20gcmVzb3VyY2VzLmxpYi5tb2R1bGVzIGltcG9ydCBkYXRhYmFzZQoKZGF0YV9wYXRoID0gb3MucGF0aC5qb2luKGNvbnRyb2wuZGF0YVBhdGgsICdwcm92aWRlcnMnKQpob3N0ZXJfc291cmNlcyA9IFtdCnRvcnJlbnRfc291cmNlcyA9IFtdCgpkZWYgZ2V0X3JlbGV2YW50KGxhbmd1YWdlKToKICAgIHByb3ZpZGVyX3BhY2thZ2VzID0gW25hbWUgZm9yIG5hbWUgaW4gb3MubGlzdGRpcihkYXRhX3BhdGgpIGlmIG9zLnBhdGguaXNkaXIob3MucGF0aC5qb2luKGRhdGFfcGF0aCwgbmFtZSkpXQogICAgIyBHZXQgcmVsZXZhbnQgYW5kIGVuYWJsZWQgcHJvdmlkZXIgZW50cmllcyBmcm9tIHRoZSBkYXRhYmFzZQogICAgcHJvdmlkZXJfc3RhdHVzID0gW2kgZm9yIGkgaW4gZGF0YWJhc2UuZ2V0X3Byb3ZpZGVycygpIGlmIGlbJ2NvdW50cnknXSA9PSBsYW5ndWFnZV0KICAgIHByb3ZpZGVyX3N0YXR1cyA9IFtpIGZvciBpIGluIHByb3ZpZGVyX3N0YXR1cyBpZiBpWydzdGF0dXMnXSA9PSAnZW5hYmxlZCddCgogICAgZm9yIHBhY2thZ2UgaW4gcHJvdmlkZXJfcGFja2FnZXM6CiAgICAgICAgdHJ5OgogICAgICAgICAgICBwcm92aWRlcnNfcGF0aCA9ICdwcm92aWRlcnMuJXMuJXMnICUgKHBhY2thZ2UsIGxhbmd1YWdlKQogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBwcm92aWRlcl9saXN0ID0gX19pbXBvcnRfXyhwcm92aWRlcnNfcGF0aCwgZnJvbWxpc3Q9WycnXSkKICAgICAgICAgICAgZXhjZXB0OgogICAgICAgICAgICAgICAgY29udGludWUKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgZm9yIGkgaW4gcHJvdmlkZXJfbGlzdC5nZXRfaG9zdGVycygpOgogICAgICAgICAgICAgICAgICAgIGZvciBzdGF0dXMgaW4gcHJvdmlkZXJfc3RhdHVzOgogICAgICAgICAgICAgICAgICAgICAgICBpZiBpID09IHN0YXR1c1sncHJvdmlkZXJfbmFtZSddOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgcGFja2FnZSA9PSBzdGF0dXNbJ3BhY2thZ2UnXToKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAjIEFkZCBpbXBvcnQgcGF0aCBhbmQgbmFtZSB0byBob3N0ZXJfcHJvdmlkZXJzCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaG9zdGVyX3NvdXJjZXMuYXBwZW5kKCgnJXMuaG9zdGVycycgJSBwcm92aWRlcnNfcGF0aCwgaSwgcGFja2FnZSkpCiAgICAgICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgICAgIHBhc3MKICAgICAgICAgICAgCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGZvciBpIGluIHByb3ZpZGVyX2xpc3QuZ2V0X3RvcnJlbnQoKToKICAgICAgICAgICAgICAgICAgICBmb3Igc3RhdHVzIGluIHByb3ZpZGVyX3N0YXR1czoKICAgICAgICAgICAgICAgICAgICAgICAgaWYgaSA9PSBzdGF0dXNbJ3Byb3ZpZGVyX25hbWUnXToKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIHBhY2thZ2UgPT0gc3RhdHVzWydwYWNrYWdlJ106CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIyBBZGQgaW1wb3J0IHBhdGggYW5kIG5hbWUgdG8gdG9ycmVudF9wcm92aWRlcnMKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0b3JyZW50X3NvdXJjZXMuYXBwZW5kKCgnJXMudG9ycmVudCcgJSBwcm92aWRlcnNfcGF0aCwgaSwgcGFja2FnZSkpCiAgICAgICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgICAgIHBhc3MKICAgICAgICBleGNlcHQ6CiAgICAgICAgICAgIGltcG9ydCB0cmFjZWJhY2sKICAgICAgICAgICAgdHJhY2ViYWNrLnByaW50X2V4YygpCiAgICAgICAgICAgIGNvbnRpbnVlCgogICAgcmV0dXJuICh0b3JyZW50X3NvdXJjZXMsIGhvc3Rlcl9zb3VyY2VzKQoKZGVmIGdldF9hbGwobGFuZ3VhZ2UpOgogICAgcHJvdmlkZXJfcGFja2FnZXMgPSBbbmFtZSBmb3IgbmFtZSBpbiBvcy5saXN0ZGlyKGRhdGFfcGF0aCkgaWYgb3MucGF0aC5pc2Rpcihvcy5wYXRoLmpvaW4oZGF0YV9wYXRoLCBuYW1lKSldCiAgICBmb3IgcGFja2FnZSBpbiBwcm92aWRlcl9wYWNrYWdlczoKICAgICAgICB0cnk6CiAgICAgICAgICAgIHByb3ZpZGVyc19wYXRoID0gJ3Byb3ZpZGVycy4lcy4lcycgJSAocGFja2FnZSwgbGFuZ3VhZ2UpCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIHByb3ZpZGVyX2xpc3QgPSBfX2ltcG9ydF9fKHByb3ZpZGVyc19wYXRoLCBmcm9tbGlzdD1bJyddKQogICAgICAgICAgICBleGNlcHQ6CiAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBmb3IgaSBpbiBwcm92aWRlcl9saXN0LmdldF9ob3N0ZXJzKCk6CiAgICAgICAgICAgICAgICAgICAgaG9zdGVyX3NvdXJjZXMuYXBwZW5kKCgnJXMuaG9zdGVycycgJSBwcm92aWRlcnNfcGF0aCwgaSwgcGFja2FnZSkpCiAgICAgICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgICAgIHBhc3MKCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGZvciBpIGluIHByb3ZpZGVyX2xpc3QuZ2V0X3RvcnJlbnQoKToKICAgICAgICAgICAgICAgICAgICB0b3JyZW50X3NvdXJjZXMuYXBwZW5kKCgnJXMudG9ycmVudCcgJSBwcm92aWRlcnNfcGF0aCwgaSwgcGFja2FnZSkpCiAgICAgICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgICAgIHBhc3MKCiAgICAgICAgZXhjZXB0OgogICAgICAgICAgICBpbXBvcnQgdHJhY2ViYWNrCiAgICAgICAgICAgIHRyYWNlYmFjay5wcmludF9leGMoKQogICAgICAgICAgICBjb250aW51ZQoKICAgIHJldHVybiAodG9ycmVudF9zb3VyY2VzLCBob3N0ZXJfc291cmNlcykK'

def install_zip(install_style):

    folders = ['providerModules/', 'providers/']
    deploy_init()
    if install_style == None:
        browse_download = control.showDialog.select(control.addonName, [control.lang(40302), control.lang(40303)])
        if browse_download == 0:
            zip_location = control.fileBrowser(1, control.lang(40304), 'files', '.zip', True, False)
        elif browse_download == 1:
            zip_location = control.showKeyboard('', '%s: %s' % (control.addonName, control.lang(40305)))
            zip_location.doModal()
            if zip_location.isConfirmed() and zip_location.getText() != '':
                zip_location = zip_location.getText()
            else:
                return
        else:
            return
    else:
        if install_style == '0':
            zip_location = control.fileBrowser(1, control.lang(40304), 'files', '.zip', True, False)
        if install_style == '1':
            zip_location = control.showKeyboard('', '%s: %s' % (control.addonName, control.lang(40305)))
            zip_location.doModal()
            if zip_location.isConfirmed() and zip_location.getText() != '':
                zip_location = zip_location.getText()
            else:
                return

    if zip_location == '':
        return
    if zip_location.startswith('smb'):
        control.showDialog.ok(control.addonName, control.lang(40309))
        return
    if zip_location.startswith('http'):
        response = requests.get(zip_location, stream=True)
        if not response.ok:
            control.showDialog.ok(control.addonName, control.lang(40310))
        else:
            pass
        try:
            import StringIO
            file = zipfile.ZipFile(StringIO.StringIO(response.content))
        except:
            #Python 3 Support
            import io
            file = zipfile.ZipFile(io.BytesIO(response.content))
    else:
        file = zipfile.ZipFile(zip_location)

    file_list = file.namelist()

    for i in file_list:
        if i.startswith('/') or '..' in i:
            raise Exception

    meta_file = None
    for i in file_list:
        if i.startswith('meta.json'):
            meta_file = i

    if meta_file is not None:
        meta = file.open(meta_file)
        meta = meta.readlines()
        meta = ''.join(meta)
        meta = meta.replace(' ', '').replace('\r','').replace('\n','')
        meta = json.loads(meta)
        requirements = ['author', 'name', 'version']
        for i in requirements:
            if i not in meta:
                malformed_output()
                return
        author = meta['author']
        version = meta['version']
        pack_name = meta['name']
    else:
        malformed_output()
        import traceback
        traceback.print_exc()
        raise Exception

    line1 = control.colorString('{}: '.format(control.lang(40311))) + '{} - v{}'.format(pack_name, version)
    line2 = control.colorString('{}: '.format(control.lang(40312))) + "%s" % author
    line3 = control.lang(40313)
    accept = control.showDialog.yesno("{} - {}".format(control.addonName, control.lang(40314)), line1, line2, line3,
                                    control.lang(40315), control.lang(40316))
    if accept == 0:
        return

    install_progress = control.progressDialog
    install_progress.create(control.addonName, '%s - %s' % (control.lang(40317), pack_name), control.lang(33009))
    install_progress.update(-1)
    try:
        for folder in folders:
            for zip_file in file_list:
                if zip_file.startswith(folder):
                    file.extract(zip_file, control.dataPath)
        try:
            file.close()
            install_progress.close()
        except:
            pass
        control.showDialog.ok(control.addonName, '%s - %s' % (control.lang(40318), pack_name))
    except:
        import traceback
        traceback.print_exc()
        install_progress.close()
        control.showDialog.ok(control.addonName, '%s - %s' % (control.lang(40319), pack_name), control.lang(40320))
        return

    customProviders.providers().update_known_providers()


def malformed_output():
    control.showDialog.ok(control.addonName, '%s - %s' % (control.lang(40319)), control.lang(40320))
    control.log('Source pack is malformed, please check and correct issue in the meta file')

def deploy_init():
    folders = ['providerModules/', 'providers/']
    root_init_path = os.path.join(control.dataPath, '__init__ .py')
    
    if not os.path.exists(control.dataPath):
        os.makedirs(control.dataPath)
    if not os.path.exists(root_init_path):
        open(root_init_path, 'a').close()
    for i in folders:
        folder_path = os.path.join(control.dataPath, i)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        open(os.path.join(folder_path, '__init__.py'), 'a').close()
    provider_init = open(os.path.join(control.dataPath, 'providers', '__init__.py'), 'w+')
    provider_init.write(base64.b64decode(init_contents))
