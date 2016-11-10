#!/usr/bin/python
# Ecnoding: UTF-8

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gettext
import sys
import os
import string
import subprocess

gettext.install("pwdfile-editor", unicode=1)
pwdfile = "%s/.lockpasswd" % os.environ["HOME"]

if __name__== "__main__":
    while True:
        win = Gtk.Dialog(title=_("Lock screen password"), buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT, Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        vbox = win.get_content_area()
        label = Gtk.Label(label=_("Enter a password to unlock the screen"))
        pwd1 = Gtk.Entry()
        pwd2 = Gtk.Entry()
        pwd1.set_max_length(60)
        pwd1.set_max_length(60)
        pwd1.set_visibility(False)
        pwd2.set_visibility(False)
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(pwd1, True, True, 0)
        vbox.pack_start(pwd2, True, True, 0)
        win.set_position(Gtk.WindowPosition.CENTER)
        win.set_default_response(Gtk.ResponseType.ACCEPT)
        win.set_border_width(10)
        win.show_all()

        response = win.run()
        p1 = pwd1.get_text()
        p2 = pwd2.get_text()
        win.destroy()
        while Gtk.events_pending():
            Gtk.main_iteration()
        if response == Gtk.ResponseType.REJECT:
            exit(0)
        elif p1 != p2:
            dlg = Gtk.MessageDialog(type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK)
            dlg.set_markup(_("The passwords do not match!"))
            dlg.run()
            dlg.destroy()
            while Gtk.events_pending():
                Gtk.main_iteration()
        else:
            break
    try:
        f = open(pwdfile, 'w')
        if p1 == "":
            f.write("")
            suprocess.call(["gsettings", "set", "org.gnome.desktop.screensaver", "lock-enabled", "false"])
        else:
            phash = subprocess.check_output(["openssl", "passwd", "-1", "-quiet", p1])
            f.writelines("%s:%s" % (os.environ["USER"], phash))
            suprocess.call(["gsettings", "set", "org.gnome.desktop.screensaver", "lock-enabled", "true"])
        f.close()
    except:
        dlg = Gtk.MessageDialog(type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK)
        dlg.set_markup(_("The password file could not be written because of an unknown error!"))
        dlg.run()
        dlg.destroy()
        while Gtk.events_pending():
            Gtk.main_iteration()
