import sys
import xbmc

if __name__ == '__main__':
    item = sys.listitem
    message = item.getLabel()
    path = item.getPath()

    path = path.replace('getSources', 'getSources&judaea_reload=true')
    path = path.replace('smartPlay', 'getSources&judaea_reload=true')

    xbmc.executebuiltin('PlayMedia(%s)' % path)
