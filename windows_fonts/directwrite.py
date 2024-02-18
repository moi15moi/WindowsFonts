from comtypes import GUID, HRESULT, IUnknown, STDMETHOD
from ctypes import POINTER, windll, wintypes
from enum import IntEnum

__all__ = [
    "DWRITE_FACTORY_TYPE",
    "IDWriteFontFileLoader",
    "IDWriteLocalFontFileLoader",
    "IDWriteFontFile",
    "IDWriteFontFace",
    "IDWriteFont",
    "IDWriteGdiInterop",
    "IDWriteFontCollection",
    "IDWriteFactory",
    "DirectWrite",
]


class DWRITE_FACTORY_TYPE(IntEnum):
    # https://learn.microsoft.com/en-us/windows/win32/api/dwrite/ne-dwrite-dwrite_factory_type
    DWRITE_FACTORY_TYPE_SHARED = 0
    DWRITE_FACTORY_TYPE_ISOLATED = 1


class IDWriteFontFileLoader(IUnknown):
    # https://learn.microsoft.com/en-us/windows/win32/api/dwrite/nn-dwrite-idwritefontfileloader
    _iid_ = GUID("{727cad4e-d6af-4c9e-8a08-d695b11caa49}")
    _methods_ = [
        STDMETHOD(None, "CreateStreamFromKey"),  # Need to be implemented
    ]


class IDWriteLocalFontFileLoader(IDWriteFontFileLoader):
    # https://learn.microsoft.com/en-us/windows/win32/directwrite/idwritelocalfontfileloader
    _iid_ = GUID("{b2d9f3ec-c9fe-4a11-a2ec-d86208f7c0a2}")
    _methods_ = [
        STDMETHOD(HRESULT, "GetFilePathLengthFromKey", [wintypes.LPCVOID, wintypes.UINT, POINTER(wintypes.UINT)]),
        STDMETHOD(HRESULT, "GetFilePathFromKey", [wintypes.LPCVOID, wintypes.UINT, POINTER(wintypes.WCHAR), wintypes.UINT]),
        STDMETHOD(None, "GetLastWriteTimeFromKey"),  # Need to be implemented
    ]


class IDWriteFontFile(IUnknown):
    # https://learn.microsoft.com/en-us/windows/win32/api/dwrite/nn-dwrite-idwritefontfile
    _iid_ = GUID("{739d886a-cef5-47dc-8769-1a8b41bebbb0}")
    _methods_ = [
        STDMETHOD(HRESULT, "GetReferenceKey", [POINTER(wintypes.LPCVOID), POINTER(wintypes.UINT)]),
        STDMETHOD(HRESULT, "GetLoader", [POINTER(POINTER(IDWriteFontFileLoader))]),
        STDMETHOD(HRESULT, "Analyze", [POINTER(wintypes.BOOLEAN), POINTER(wintypes.UINT), POINTER(wintypes.UINT), POINTER(wintypes.UINT)]),
    ]


class IDWriteFontFace(IUnknown):
    # https://learn.microsoft.com/en-us/windows/win32/api/dwrite/nn-dwrite-idwritefontface
    _iid_ = GUID("{5f49804d-7024-4d43-bfa9-d25984f53849}")
    _methods_ = [
        STDMETHOD(None, "GetType"),  # Need to be implemented
        STDMETHOD(HRESULT, "GetFiles", [POINTER(wintypes.UINT), POINTER(POINTER(IDWriteFontFile))]),
        STDMETHOD(None, "GetIndex"),  # Need to be implemented
        STDMETHOD(None, "GetSimulations"),  # Need to be implemented
        STDMETHOD(None, "IsSymbolFont"),  # Need to be implemented
        STDMETHOD(None, "GetMetrics"),  # Need to be implemented
        STDMETHOD(None, "GetGlyphCount"),  # Need to be implemented
        STDMETHOD(None, "GetDesignGlyphMetrics"),  # Need to be implemented
        STDMETHOD(None, "GetGlyphIndices"),  # Need to be implemented
        STDMETHOD(None, "TryGetFontTable"),  # Need to be implemented
        STDMETHOD(None, "ReleaseFontTable"),  # Need to be implemented
        STDMETHOD(None, "GetGlyphRunOutline"),  # Need to be implemented
        STDMETHOD(None, "GetRecommendedRenderingMode"),  # Need to be implemented
        STDMETHOD(None, "GetGdiCompatibleMetrics"),  # Need to be implemented
        STDMETHOD(None, "GetGdiCompatibleGlyphMetrics"),  # Need to be implemented
    ]


class IDWriteFont(IUnknown):
    # https://learn.microsoft.com/en-us/windows/win32/api/dwrite/nn-dwrite-idwritefont
    _iid_ = GUID("{acd16696-8c14-4f5d-877e-fe3fc1d32737}")
    _methods_ = [
        STDMETHOD(None, "GetFontFamily"),  # Need to be implemented
        STDMETHOD(None, "GetWeight"),  # Need to be implemented
        STDMETHOD(None, "GetStretch"),  # Need to be implemented
        STDMETHOD(None, "GetStyle"),  # Need to be implemented
        STDMETHOD(None, "IsSymbolFont"),  # Need to be implemented
        STDMETHOD(None, "GetFaceNames"),  # Need to be implemented
        STDMETHOD(None, "GetInformationalStrings"),  # Need to be implemented
        STDMETHOD(None, "GetSimulations"),  # Need to be implemented
        STDMETHOD(None, "GetMetrics"),  # Need to be implemented
        STDMETHOD(None, "HasCharacter"),  # Need to be implemented
        STDMETHOD(HRESULT, "CreateFontFace", [POINTER(POINTER(IDWriteFontFace))]),
    ]


class IDWriteGdiInterop(IUnknown):
    # https://learn.microsoft.com/en-us/windows/win32/api/dwrite/nn-dwrite-idwritegdiinterop
    _iid_ = GUID("{1edd9491-9853-4299-898f-6432983b6f3a}")
    _methods_ = [
        STDMETHOD(None, "CreateFontFromLOGFONT"),  # Need to be implemented
        STDMETHOD(None, "ConvertFontToLOGFONT"),  # Need to be implemented
        STDMETHOD(None, "ConvertFontFaceToLOGFONT"),  # Need to be implemented
        STDMETHOD(HRESULT, "CreateFontFaceFromHdc", [wintypes.HDC, POINTER(POINTER(IDWriteFontFace))]),
        STDMETHOD(None, "CreateBitmapRenderTarget"),  # Need to be implemented
    ]

class IDWriteFontCollection(IUnknown):
    # https://learn.microsoft.com/en-us/windows/win32/api/dwrite/nn-dwrite-idwritefontcollection
    _iid_ = GUID("{a84cee02-3eea-4eee-a827-87c1a02a0fcc}")
    _methods_ = [
        STDMETHOD(wintypes.UINT, "GetFontFamilyCount"),
        STDMETHOD(None, "GetFontFamily"), # Need to be implemented
        STDMETHOD(None, "FindFamilyName"),  # Need to be implemented
        STDMETHOD(None, "GetFontFromFontFace"),  # Need to be implemented
    ]


class IDWriteFactory(IUnknown):
    # https://learn.microsoft.com/en-us/windows/win32/api/dwrite/nn-dwrite-idwritefactory
    _iid_ = GUID("{b859ee5a-d838-4b5b-a2e8-1adc7d93db48}")
    _methods_ = [
        STDMETHOD(HRESULT, "GetSystemFontCollection", [POINTER(POINTER(IDWriteFontCollection)), wintypes.BOOLEAN]),
        STDMETHOD(None, "CreateCustomFontCollection"),  # Need to be implemented
        STDMETHOD(None, "RegisterFontCollectionLoader"),  # Need to be implemented
        STDMETHOD(None, "UnregisterFontCollectionLoader"),  # Need to be implemented
        STDMETHOD(None, "CreateFontFileReference"),  # Need to be implemented
        STDMETHOD(None, "CreateCustomFontFileReference"),  # Need to be implemented
        STDMETHOD(None, "CreateFontFace"),  # Need to be implemented
        STDMETHOD(None, "CreateRenderingParams"),  # Need to be implemented
        STDMETHOD(None, "CreateMonitorRenderingParams"),  # Need to be implemented
        STDMETHOD(None, "CreateCustomRenderingParams"),  # Need to be implemented
        STDMETHOD(None, "RegisterFontFileLoader"),  # Need to be implemented
        STDMETHOD(None, "UnregisterFontFileLoader"),  # Need to be implemented
        STDMETHOD(None, "CreateTextFormat"),  # Need to be implemented
        STDMETHOD(None, "CreateTypography"),  # Need to be implemented
        STDMETHOD(HRESULT, "GetGdiInterop", [POINTER(POINTER(IDWriteGdiInterop))]),
        STDMETHOD(None, "CreateTextLayout"),  # Need to be implemented
        STDMETHOD(None, "CreateGdiCompatibleTextLayout"),  # Need to be implemented
        STDMETHOD(None, "CreateEllipsisTrimmingSign"),  # Need to be implemented
        STDMETHOD(None, "CreateTextAnalyzer"),  # Need to be implemented
        STDMETHOD(None, "CreateNumberSubstitution"),  # Need to be implemented
        STDMETHOD(None, "CreateGlyphRunAnalysis"),  # Need to be implemented
    ]


class DirectWrite():
    def __init__(self) -> None:

        self.DWriteCreateFactory = windll.dwrite.DWriteCreateFactory
        self.DWriteCreateFactory.restype = HRESULT
        self.DWriteCreateFactory.argtypes = [wintypes.UINT, GUID, POINTER(POINTER(IUnknown))]
        self.DWriteCreateFactory.errcheck = self.has_failed

    @staticmethod
    def has_failed(result, func, args):
        # From https://learn.microsoft.com/en-us/windows/win32/api/winerror/nf-winerror-failed
        if result < 0:
            raise OSError(f"Error encountered with {func.__name__}. HRESULT={result}")
        return result