import imutils
import wx
import cv2
import numpy as np
import socket

class ColorSettingWin(wx.Frame):

    blurVal = 1
    locator_count = 0
    key_frame = 0
    screen = (640, 480)
    send_data = False
    record = False

    def __init__(self):
        super(ColorSettingWin, self).__init__(parent=None,  title='Color space', size=(226, 680), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.InitUI()

    def maya_conntect(self, msg):
        maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        maya.connect(("localhost", 7001))
        maya.send(msg)
        maya.close()

    def create_locators(self, locator_count):
        for i in range(0, locator_count, 1):
            self.maya_conntect('spaceLocator -name "locator0";')

    def InitUI(self):
        # Vision control
        visionPanel = wx.Panel(self, pos=(0, 0), size=(226, 166))
        visionBox = wx.StaticBox(visionPanel, label="Vision Attributes", pos=(10, 10), size=(200, 150))

        # List of visions
        wx.StaticText(visionBox, label='Vision type', pos=(10, 20))
        self.vision = wx.ComboBox(visionBox, -1, pos=(10, 40), size=(180, 24), value='Original', choices=['Original', 'HSV', 'Mask'])

        self.point_name = wx.CheckBox(visionBox, label='Point naming', pos=(10, 70))

        self.bund_box = wx.CheckBox(visionBox, label='Bounding box', pos=(10, 90))

        # Color control
        colorPanel = wx.Panel(self, pos=(0, 166), size=(226, 326))
        colorBox = wx.StaticBox(colorPanel, label="Colors Attributes", pos=(10, 0), size=(200, 315))

        # Hue low
        self.hlText = wx.StaticText(colorBox, label='Hue Low 0', pos=(10, 25))
        self.hl = wx.Slider(colorBox, value=0, minValue=0, maxValue=255, pos=(5, 40), size=(190, 20))
        self.hl.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        # Hue high
        self.hhText = wx.StaticText(colorBox, label='Hue High 255', pos=(10, 60))
        self.hh = wx.Slider(colorBox, value=255, minValue=1, maxValue=255, pos=(5, 75), size=(190, 20))
        self.hh.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        # Saturation low
        self.slText = wx.StaticText(colorBox, label='Saturation Low 0', pos=(10, 95))
        self.sl = wx.Slider(colorBox, value=0, minValue=0, maxValue=255, pos=(5, 110), size=(190, 20))
        self.sl.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        # Saturation high
        self.shText = wx.StaticText(colorBox, label='Saturation High 255', pos=(10, 130))
        self.sh = wx.Slider(colorBox, value=255, minValue=1, maxValue=255, pos=(5, 145), size=(190, 20))
        self.sh.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        # Value low
        self.vlText = wx.StaticText(colorBox, label='Value Low 0', pos=(10, 165))
        self.vl = wx.Slider(colorBox, value=0, minValue=0, maxValue=255, pos=(5, 180), size=(190, 20))
        self.vl.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        # Value high
        self.vhText = wx.StaticText(colorBox, label='Value High 255', pos=(10, 200))
        self.vh = wx.Slider(colorBox, value=255, minValue=1, maxValue=255, pos=(5, 215), size=(190, 20))
        self.vh.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        self.blText = wx.StaticText(colorBox, label='Blur 1', pos=(10, 235))
        self.bl = wx.Slider(colorBox, value=1, minValue=1,  maxValue=99, pos=(5, 250), size=(190, 20))
        self.bl.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        self.thText = wx.StaticText(colorBox, label='Threshold 0', pos=(10, 270))
        self.th = wx.Slider(colorBox, value=0, minValue=0, maxValue=255, pos=(5, 285), size=(190, 20))
        self.th.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        # Tracking control
        trackingPanel = wx.Panel(self, pos=(0, 478), size=(226, 180))
        trackingBox = wx.StaticBox(trackingPanel, label="Tracking Attributes", pos=(10, 10), size=(200, 150))

        # Tracking statistic
        self.pointCount = wx.StaticText(trackingBox, label='Tracking points 0', pos=(10, 20))

        self.mtText = wx.StaticText(trackingBox, label='Multiplayer 100%', pos=(10, 40))
        self.mt = wx.Slider(trackingBox, value=100, minValue=1, maxValue=100, pos=(5, 55), size=(190, 20))
        self.mt.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        # Create locators
        self.createLocators = wx.Button(trackingBox, label='Create', pos=(10, 80), size=(80, 24))
        self.createLocators.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.startStreaming = wx.Button(trackingBox, label='Streaming', pos=(10, 110), size=(80, 24))
        self.startStreaming.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.startRecord = wx.Button(trackingBox, label='Recording', pos=(110, 110), size=(80, 24))
        self.startRecord.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.SetTitle('Face mocap')
        self.Show(True)

    def OnSliderScroll(self, e):
        # Hue low
        if e.GetEventObject() == self.hl:
            self.hlText.SetLabel('Hue Low ' + str(e.GetEventObject().GetValue()))

        # Hue high
        if e.GetEventObject() == self.hh:
            self.hhText.SetLabel('Hue High ' + str(e.GetEventObject().GetValue()))

        # Saturation low
        if e.GetEventObject() == self.sl:
            self.slText.SetLabel('Saturation Low ' + str(e.GetEventObject().GetValue()))

        # Saturation high
        if e.GetEventObject() == self.sh:
            self.shText.SetLabel('Saturation High ' + str(e.GetEventObject().GetValue()))

        # Value low
        if e.GetEventObject() == self.vl:
            self.vlText.SetLabel('Value Low ' + str(e.GetEventObject().GetValue()))

        # Value high
        if e.GetEventObject() == self.vh:
            self.vhText.SetLabel('Value High ' + str(e.GetEventObject().GetValue()))

        if e.GetEventObject() == self.bl:
            if e.GetEventObject().GetValue() % 2 == 1:
                self.blurVal = e.GetEventObject().GetValue()
                self.blText.SetLabel('Blur ' + str(self.blurVal))

        if e.GetEventObject() == self.th:
            self.thText.SetLabel('Threshold ' + str(e.GetEventObject().GetValue()))

        if e.GetEventObject() == self.mt:
            self.mtText.SetLabel('Multiplayer ' + str(e.GetEventObject().GetValue()) + '%')

    def OnCheckBox(self, e):
        if e.GetEventObject() == self.blCheckBox:
            self.bl.Enable(self.blCheckBox.Get3StateValue())

        if e.GetEventObject() == self.thCheckBox:
            self.th.Enable(self.thCheckBox.Get3StateValue())

    def OnClicked(self, e):
        if e.GetEventObject() == self.createLocators:
            print ('Create locator')
            self.create_locators(self.locator_count)

        if e.GetEventObject() == self.startStreaming:
            print ('Start stream')
            if self.send_data == False:
                self.send_data = True
            else:
                self.send_data = False

        if e.GetEventObject() == self.startRecord:
            print ('Start Recording')
            if self.record == False:
                self.record = True
            else:
                self.record = False

    def StartCpturte(self):
        cap = cv2.VideoCapture(0)
        cv2.namedWindow('frame')
        while True:
            _, frame = cap.read()

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            HSVLOW = np.array([self.hl.GetValue(), self.sl.GetValue(), self.vl.GetValue()])
            HSVHIGH = np.array([self.hh.GetValue(), self.sh.GetValue(), self.vh.GetValue()])

            mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
            mask = cv2.GaussianBlur(mask, (self.blurVal, self.blurVal), 0)
            mask = cv2.threshold(mask, self.th.GetValue(), 255, cv2.THRESH_BINARY)[1]

            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=4)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]

            if len(cnts) > 0:
                for (i, c) in enumerate(cnts):
                    if len(c) > 0 and self.bund_box.GetValue():
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 0, 255), 1)
                    ((cX, cY), radius) = cv2.minEnclosingCircle(c)

                    cv2.circle(frame, (int(cX), int(cY)), 2, (255, 0, 0), 2)

                    if self.point_name.GetValue():
                        cv2.putText(frame, str(i), (int(cX + 5), int(cY + 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                    if self.send_data:
                        posX = (self.screen[0] / 2 - cX) * self.mt.GetValue() / 100
                        posY = (self.screen[1] / 2 - cY) * self.mt.GetValue() / 100
                        self.maya_conntect('setAttr "locator' + str(int(i)) + '.translateX"' + str(posX) + ' ;')
                        self.maya_conntect('setAttr "locator' + str(int(i)) + '.translateY"' + str(posY) + ' ;')

                    if self.record:
                        self.maya_conntect('currentTime ' + str(self.key_frame) + ' ;')
                        self.maya_conntect('setKeyframe {"locator' + str(int(i)) + '"};')

                self.locator_count = i + 1
                self.pointCount.SetLabel('Tracking points ' + str(self.locator_count))

            self.key_frame += 1

            if self.vision.GetValue() == 'Original':
                cv2.imshow('Vision', frame)

            if self.vision.GetValue() == 'HSV':
                cv2.imshow('Vision', hsv)

            if self.vision.GetValue() == 'Mask':
                cv2.imshow('Vision', mask)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cap.release()


ex = wx.App()
UI = ColorSettingWin()
UI.StartCpturte()
ex.MainLoop()

