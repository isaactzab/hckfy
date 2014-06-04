import wx

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = 'icon.ico'


def cpm(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    notify_title = None
    menu
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        # self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        self.menu = wx.Menu()
        self.notify_title = cpm(self.menu, 'Now Playing', self.nowplaying)
        cpm(self.menu, 'This is an Sponsor!!', self.dummy)
        cpm(self.menu, 'Update Sponsors database', self.dummy)
        self.menu.AppendSeparator()
        cpm(self.menu, 'Play/Pause', self.dummy)
        self.menu.AppendSeparator()
        cpm(self.menu, 'Donate', self.dummy)
        self.menu.AppendSeparator()
        cpm(self.menu, 'Exit', self.on_exit)
        self.notify_title.Enable(False)
        return self.menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    # def on_left_down(self, event):
    #     print 'Tray icon was left-clicked.'
    #     self.popup(self.menu)

    def nowplaying(self, event):
        print 'Hello, world!'
        self.popup(self.menu)

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
    def dummy(self, event):
        pass


def main():
    app = wx.App(False)
    TaskBarIcon()
    app.MainLoop()


if __name__ == '__main__':
    main()