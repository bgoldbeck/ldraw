# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import wx


class Button(wx.Button):
    """Override the default wx.Button with this instance of a button. So, we can use this as a workaround
    for the OpenGL canvas paint DC object that messes with the behavior.
    """

    def __init__(self, parent, id=wx.ID_ANY, label="", size=(100, 20), pos=wx.DefaultPosition):
        """Constructor for Button class.

        :param parent: The parent object.
        :param id: The id of the button
        :param label: The label of the button
        :param size: The size of the button.
        :param pos: The position of the button.
        """
        wx.Button.__init__(self, parent, size=size, id=id, label=label, pos=pos)

    def Enable(self):
        """Override the default enable button behavior.

        :return: None
        """
        super().Enable()
        self.SetLabelText(self.GetLabelText())

    def Disable(self):
        """Override the default disable button behavior.

        :return: None
        """
        super().Disable()
        self.SetLabelText(self.GetLabelText())
