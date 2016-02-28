import picamera
import io
import time
import threading
from PIL import Image, ImageTk
import wx
import datetime

# variables
updateFrameLoop = True
camera = picamera.PiCamera()
imagePreviewWidth = 640
imagePreviewHeight = 480
imagePictureWidth = 2592
imagePictureHeight = 1944
margin = 20
labelWidth = 120
sliderWidth = 180
buttonWidth = 60
rowHeight = 30

# define default value for camera
camera.resolution = (imagePreviewWidth, imagePreviewHeight)
camera.exposure_mode = 'auto'
camera.awb_mode = 'auto'
# camera.awb_gains = 1.5 # if awb_mode auto
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.iso = 800

# create app and frame
app = wx.App()
frame = wx.Frame(None, title='Picroscope')
frame.SetSize((imagePreviewWidth + labelWidth + sliderWidth + buttonWidth + margin * 5, imagePreviewHeight + margin * 2))
frame.Center()
frame.Show()

# create panel preview
panelPreview = wx.Panel(frame)
panelPreview.SetPosition((margin, margin))
panelPreview.SetSize((imagePreviewWidth , imagePreviewHeight))

# create image displayer
image = wx.EmptyImage(imagePreviewWidth, imagePreviewHeight)
imageDisplayer = wx.StaticBitmap(panelPreview, wx.ID_ANY, wx.BitmapFromImage(image))

# create panel control
panelControl = wx.Panel(frame)
panelControl.SetPosition((imagePreviewWidth + margin * 2, margin))
panelControl.SetSize((labelWidth + sliderWidth + buttonWidth + 2 * margin, imagePreviewHeight))



# iso label, slider and button
labelIso = wx.StaticText(panelControl)
labelIso.SetLabel("Iso")
labelIso.SetPosition((0, 0 * (rowHeight + margin)))
labelIso.SetSize((labelWidth, rowHeight))

def sliderIsoEvent(_event):
    camera.iso = _event.GetEventObject().GetValue()
sliderIso = wx.Slider(panelControl, value=camera.iso, minValue=100, maxValue=1600, style=wx.SL_HORIZONTAL)
sliderIso.SetPosition((labelWidth + margin, 0 * (rowHeight + margin)))
sliderIso.SetSize((sliderWidth, rowHeight))
sliderIso.Bind(wx.EVT_SCROLL, sliderIsoEvent)

def buttonIsoResetEvent(_event):
    camera.iso = 800;
    sliderIso.SetValue(800);
buttonIsoReset = wx.Button(panelControl)
buttonIsoReset.SetLabel("Reset")
buttonIsoReset.SetPosition((labelWidth + sliderWidth + 2 * margin, 0 * (rowHeight + margin)))
buttonIsoReset.SetSize((buttonWidth, rowHeight))
buttonIsoReset.Bind(wx.EVT_BUTTON, buttonIsoResetEvent)



# # white balance label, slider and button
# labelIso = wx.StaticText(panelControl)
# labelIso.SetLabel("White Balance")
# labelIso.SetPosition((0, 0 * (rowHeight + margin)))
# labelIso.SetSize((labelWidth, rowHeight))

# def sliderIsoEvent(_event):
#     camera.iso = _event.GetEventObject().GetValue()
# sliderIso = wx.Slider(panelControl, value=camera.iso, minValue=100, maxValue=1600, style=wx.SL_HORIZONTAL)
# sliderIso.SetPosition((labelWidth + margin, 0 * (rowHeight + margin)))
# sliderIso.SetSize((sliderWidth, rowHeight))
# sliderIso.Bind(wx.EVT_SCROLL, sliderIsoEvent)

# def buttonIsoResetEvent(_event):
#     camera.iso = 800;
#     sliderIso.SetValue(800);
# buttonIsoReset = wx.Button(panelControl)
# buttonIsoReset.SetLabel("Reset")
# buttonIsoReset.SetPosition((labelWidth + sliderWidth + 2 * margin, 0 * (rowHeight + margin)))
# buttonIsoReset.SetSize((buttonWidth, rowHeight))
# buttonIsoReset.Bind(wx.EVT_BUTTON, buttonIsoResetEvent)



# contrast label, slider and button
labelContrast = wx.StaticText(panelControl)
labelContrast.SetLabel("Contrast")
labelContrast.SetPosition((0, 1 * (rowHeight + margin)))
labelContrast.SetSize((labelWidth, rowHeight))

def sliderContrastEvent(_event):
    camera.contrast = _event.GetEventObject().GetValue()
sliderContrast = wx.Slider(panelControl, value=camera.contrast, minValue=-100, maxValue=100, style=wx.SL_HORIZONTAL)
sliderContrast.SetPosition((labelWidth + margin, 1 * (rowHeight + margin)))
sliderContrast.SetSize((sliderWidth, rowHeight))
sliderContrast.Bind(wx.EVT_SCROLL, sliderContrastEvent)

def buttonContrastResetEvent(_event):
    camera.contrast = 0;
    sliderContrast.SetValue(0);
buttonContrastReset = wx.Button(panelControl)
buttonContrastReset.SetLabel("Reset")
buttonContrastReset.SetPosition((labelWidth + sliderWidth + 2 * margin, 1 * (rowHeight + margin)))
buttonContrastReset.SetSize((buttonWidth, rowHeight))
buttonContrastReset.Bind(wx.EVT_BUTTON, buttonContrastResetEvent)



# brightness label, slider and button
labelBrightness = wx.StaticText(panelControl)
labelBrightness.SetLabel("Brightness")
labelBrightness.SetPosition((0, 2 * (rowHeight + margin)))
labelBrightness.SetSize((labelWidth, rowHeight))

def sliderBrightnessEvent(_event):
    camera.brightness = _event.GetEventObject().GetValue()
sliderBrightness = wx.Slider(panelControl, value=camera.brightness, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL)
sliderBrightness.SetPosition((labelWidth + margin, 2 * (rowHeight + margin)))
sliderBrightness.SetSize((sliderWidth, rowHeight))
sliderBrightness.Bind(wx.EVT_SCROLL, sliderBrightnessEvent)

def buttonBrightnessResetEvent(_event):
    camera.brightness = 50;
    sliderBrightness.SetValue(50);
buttonBrightnessReset = wx.Button(panelControl)
buttonBrightnessReset.SetLabel("Reset")
buttonBrightnessReset.SetPosition((labelWidth + sliderWidth + 2 * margin, 2 * (rowHeight + margin)))
buttonBrightnessReset.SetSize((buttonWidth, rowHeight))
buttonBrightnessReset.Bind(wx.EVT_BUTTON, buttonBrightnessResetEvent)



# saturation label, slider and button
labelSaturation = wx.StaticText(panelControl)
labelSaturation.SetLabel("Saturation")
labelSaturation.SetPosition((0, 3 * (rowHeight + margin)))
labelSaturation.SetSize((labelWidth, rowHeight))

def sliderSaturationEvent(_event):
    camera.saturation = _event.GetEventObject().GetValue()
sliderSaturation = wx.Slider(panelControl, value=camera.saturation, minValue=-100, maxValue=100, style=wx.SL_HORIZONTAL)
sliderSaturation.SetPosition((labelWidth + margin, 3 * (rowHeight + margin)))
sliderSaturation.SetSize((sliderWidth, rowHeight))
sliderSaturation.Bind(wx.EVT_SCROLL, sliderSaturationEvent)

def buttonSaturationResetEvent(_event):
    camera.saturation = 0;
    sliderSaturation.SetValue(0);
buttonSaturationReset = wx.Button(panelControl)
buttonSaturationReset.SetLabel("Reset")
buttonSaturationReset.SetPosition((labelWidth + sliderWidth + 2 * margin, 3 * (rowHeight + margin)))
buttonSaturationReset.SetSize((buttonWidth, rowHeight))
buttonSaturationReset.Bind(wx.EVT_BUTTON, buttonSaturationResetEvent)



# button to take a picture
def takePictureEvent(_event):
    global updateFrameLoop
    global camera
    global imageDiplayer
    # stop preview
    awdGainsBuffer = camera.awb_gains
    updateFrameLoop = False
    time.sleep(0.1)
    # define picture resolution
    camera.resolution = (imagePictureWidth, imagePictureHeight)
    camera.awb_mode = 'off'
    camera.awb_gains = awdGainsBuffer
    time.sleep(0.2)
    # get time
    imageName = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S.jpg")
    # take picture
    camera.capture(imageName)
    time.sleep(0.2)
    # restart preview
    camera.resolution = (imagePreviewWidth, imagePreviewHeight)
    camera.awb_mode = 'auto'
    updateFrameLoop = True
    threading.Thread(None, updateFrame, None, (imageDisplayer,)).start()
buttonTakePicture = wx.Button(panelControl)
buttonTakePicture.SetLabel("Take a Picture")
buttonTakePicture.SetPosition((0, imagePreviewHeight - rowHeight))
buttonTakePicture.SetSize((labelWidth + sliderWidth + buttonWidth + 2 * margin, rowHeight))
buttonTakePicture.Bind(wx.EVT_BUTTON, takePictureEvent)



# update frame methods
def updateFrame(_imageDisplayer):
    global updateFrameLoop
    global camera
    # Camera warm-up time
    time.sleep(1)
    stream = io.BytesIO()
    while updateFrameLoop:
        camera.capture(stream, 'jpeg', True)
        wx.CallAfter(updateImage, stream, _imageDisplayer)

def updateImage(_stream, _imageDisplayer):
    _stream.seek(0)
    image = Image.open(_stream)
    imageWx = wx.EmptyImage(imagePreviewWidth,imagePreviewHeight)
    imageWx.SetData(image.convert('RGB').tostring())
    _imageDisplayer.SetBitmap(wx.BitmapFromImage(imageWx))
    _stream.seek(0)
    _stream.truncate()

# Start threads
threading.Thread(target=app.MainLoop).start()
threading.Thread(None, updateFrame, None, (imageDisplayer,)).start()