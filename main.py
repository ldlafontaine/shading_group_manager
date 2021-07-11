import views.ShadingGroupManagerMainDialog

try:
    dialog.close()
    dialog.deleteLater()
except:
    pass

dialog = views.ShadingGroupManagerMainDialog.ShadingGroupManagerMainDialog()
dialog.show()
