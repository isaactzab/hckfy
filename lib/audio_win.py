# From: https://mail.python.org/pipermail/python-win32/2014-March/013080.html

import win32com
from comtypes import *
import comtypes.client
from ctypes import POINTER
from ctypes.wintypes import DWORD, BOOL



MMDeviceApiLib = \
    GUID('{2FDAAFA3-7523-4F66-9957-9D5E7FE698F6}')
IID_IMMDevice = \
    GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
IID_IMMDeviceEnumerator = \
    GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
CLSID_MMDeviceEnumerator = \
    GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
IID_IMMDeviceCollection = \
    GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
IID_IAudioEndpointVolume = \
    GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')

class IMMDeviceCollection(IUnknown):
    _iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
    pass

class IAudioEndpointVolume(IUnknown):
    _iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
    _methods_ = [
        STDMETHOD(HRESULT, 'RegisterControlChangeNotify', []),
        STDMETHOD(HRESULT, 'UnregisterControlChangeNotify', []),
        STDMETHOD(HRESULT, 'GetChannelCount', []),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
            (['in'], DWORD, 'nChannel'),
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
            (['in'], DWORD, 'nChannel'),
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
            (['in'], DWORD, 'nChannel'),
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
            (['in'], DWORD, 'nChannel'),
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'SetMute',
            (['in'], BOOL, 'bMute'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetMute',
            (['out','retval'], POINTER(BOOL), 'pbMute')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
            (['out','retval'], POINTER(c_float), 'pnStep'),
            (['out','retval'], POINTER(c_float), 'pnStepCount'),
        ),
        COMMETHOD([], HRESULT, 'VolumeStepUp',
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'VolumeStepDown',
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'QueryHardwareSupport',
            (['out','retval'], POINTER(DWORD), 'pdwHardwareSupportMask')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeRange',
            (['out','retval'], POINTER(c_float), 'pfMin'),
            (['out','retval'], POINTER(c_float), 'pfMax'),
            (['out','retval'], POINTER(c_float), 'pfIncr')
        ),

    ]

class IMMDevice(IUnknown):
    _iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'Activate',
            (['in'], POINTER(GUID), 'iid'),
            (['in'], DWORD, 'dwClsCtx'),
            (['in'], POINTER(DWORD), 'pActivationParans'),
            (['out','retval'], POINTER(POINTER(IAudioEndpointVolume)), 'ppInterface')
        ),
        STDMETHOD(HRESULT, 'OpenPropertyStore', []),
        STDMETHOD(HRESULT, 'GetId', []),
        STDMETHOD(HRESULT, 'GetState', [])
    ]
    pass

class IMMDeviceEnumerator(comtypes.IUnknown):
    _iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')

    _methods_ = [
        COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
            (['in'], DWORD, 'dataFlow'),
            (['in'], DWORD, 'dwStateMask'),
            (['out','retval'], POINTER(POINTER(IMMDeviceCollection)), 'ppDevices')
        ),
        COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
            (['in'], DWORD, 'dataFlow'),
            (['in'], DWORD, 'role'),
            (['out','retval'], POINTER(POINTER(IMMDevice)), 'ppDevices')
        )
    ]



class Audio :
    enumerator = comtypes.CoCreateInstance( 
        CLSID_MMDeviceEnumerator,
        IMMDeviceEnumerator,
        comtypes.CLSCTX_INPROC_SERVER
    )
    endpoint = enumerator.GetDefaultAudioEndpoint( 0, 1 )
    volume = endpoint.Activate( IID_IAudioEndpointVolume, comtypes.CLSCTX_INPROC_SERVER, None )
    def SetMasterVolumeLevel(self,fLevelDB):
        return self.volume.SetMasterVolumeLevel(fLevelDB, None)

    def SetMasterVolumeLevelScalar(self,fLevelDB):
        return self.volume.SetMasterVolumeLevelScalar(fLevelDB, None)

    def GetMasterVolumeLevel(self):
        return self.volume.GetMasterVolumeLevel()

    def GetMasterVolumeLevelScalar(self):
        return self.volume.GetMasterVolumeLevelScalar()

    def SetChannelVolumeLevel(self,nChannel,fLevelDB):
        return self.volume.SetChannelVolumeLevel(nChannel,fLevelDB,None)

    def SetChannelVolumeLevelScalar(self,nChannel,fLevelDB):
        return self.volume.SetChannelVolumeLevelScalar(nChannel,fLevelDB,None)

    def GetChannelVolumeLevel(self,nChannel):
        return self.volume.GetChannelVolumeLevel(nChannel)

    def GetChannelVolumeLevelScalar(self,nChannel):
        return self.volume.GetChannelVolumeLevelScalar(nChannel)

    def SetMute(self,bMute):
        return self.volume.SetMute(bMute,None)

    def GetMute(self):
        return self.volume.GetMute()

    def GetVolumeStepInfo(self):
        return self.volume.GetVolumeStepInfo()

    def VolumeStepUp(self):
        return self.volume.VolumeStepUp(None)

    def VolumeStepDown(self):
        return self.volume.VolumeStepDown(None)

    def QueryHardwareSupport(self):
        return self.volume.QueryHardwareSupport()

    def GetVolumeRange(self,):
        return self.volume.GetVolumeRange()

audio = Audio()
print audio.GetMasterVolumeLevelScalar()

# print enumerator
# print endpoint
# print volume
# print volume.GetMasterVolumeLevel()
# print volume.GetVolumeRange()
# # volume.SetMasterVolumeLevel(-20.0, None)
# volume.SetMute(True, None)