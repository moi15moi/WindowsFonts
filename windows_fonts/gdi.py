from ctypes import c_int, c_ubyte, POINTER, Structure, windll, WINFUNCTYPE, wintypes
from enum import IntEnum

__all__ = [
    "Pitch",
    "Family",
    "CharacterSet",
    "OutPrecision",
    "ClipPrecision",
    "FontQuality",
    "LOGFONTW",
    "TEXTMETRIC",
    "ENUMLOGFONTEXW",
    "GDI"
]


class Pitch(IntEnum):
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-wmf/22dbe377-aec4-4669-88e6-b8fdd9351d76
    DEFAULT_PITCH           = 0
    FIXED_PITCH             = 1
    VARIABLE_PITCH          = 2


class Family(IntEnum):
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-wmf/9a632766-1f1c-4e2b-b1a4-f5b1a45f99ad
    FF_DONTCARE = 0 << 4
    FF_ROMAN = 1 << 4
    FF_SWISS = 2 << 4
    FF_MODERN = 3 << 4
    FF_SCRIPT = 4 << 4
    FF_DECORATIVE = 5 << 4


class CharacterSet(IntEnum):
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-wmf/0d0b32ac-a836-4bd2-a112-b6000a1b4fc9
    ANSI_CHARSET = 0x00000000
    DEFAULT_CHARSET = 0x00000001
    SYMBOL_CHARSET = 0x00000002
    MAC_CHARSET = 0x0000004D
    SHIFTJIS_CHARSET = 0x00000080
    HANGUL_CHARSET = 0x00000081
    JOHAB_CHARSET = 0x00000082
    GB2312_CHARSET = 0x00000086
    CHINESEBIG5_CHARSET = 0x00000088
    GREEK_CHARSET = 0x000000A1
    TURKISH_CHARSET = 0x000000A2
    VIETNAMESE_CHARSET = 0x000000A3
    HEBREW_CHARSET = 0x000000B1
    ARABIC_CHARSET = 0x000000B2
    BALTIC_CHARSET = 0x000000BA
    RUSSIAN_CHARSET = 0x000000CC
    THAI_CHARSET = 0x000000DE
    EASTEUROPE_CHARSET = 0x000000EE
    OEM_CHARSET = 0x000000FF


class OutPrecision(IntEnum):
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-wmf/28ebf288-63cf-4b64-9113-410a63cf792d
    OUT_DEFAULT_PRECIS = 0x00000000
    OUT_STRING_PRECIS = 0x00000001
    OUT_STROKE_PRECIS = 0x00000003
    OUT_TT_PRECIS = 0x00000004
    OUT_DEVICE_PRECIS = 0x00000005
    OUT_RASTER_PRECIS = 0x00000006
    OUT_TT_ONLY_PRECIS = 0x00000007
    OUT_OUTLINE_PRECIS = 0x00000008
    OUT_SCREEN_OUTLINE_PRECIS = 0x00000009
    OUT_PS_ONLY_PRECIS = 0x0000000A


class ClipPrecision(IntEnum):
    CLIP_DEFAULT_PRECIS   =  0
    CLIP_CHARACTER_PRECIS =  1
    CLIP_STROKE_PRECIS    =  2
    CLIP_MASK             =  0xf
    CLIP_LH_ANGLES        =  (1<<4)
    CLIP_TT_ALWAYS        =  (2<<4)
    CLIP_DFA_DISABLE      =  (4<<4)
    CLIP_EMBEDDED         =  (8<<4)


class FontQuality(IntEnum):
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-wmf/9518fece-d2f2-4799-9df6-ba3db1d73371
    DEFAULT_QUALITY = 0x00
    DRAFT_QUALITY = 0x01
    PROOF_QUALITY = 0x02
    NONANTIALIASED_QUALITY = 0x03
    ANTIALIASED_QUALITY = 0x04
    CLEARTYPE_QUALITY = 0x05


class LOGFONTW(Structure):
    # https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-logfontw
    _fields_ = [
        ("lfHeight", wintypes.LONG),
        ("lfWidth", wintypes.LONG),
        ("lfEscapement", wintypes.LONG),
        ("lfOrientation", wintypes.LONG),
        ("lfWeight", wintypes.LONG),
        ("lfItalic", c_ubyte), # Cannot use c_ubyteS on old version of python, see https://github.com/python/cpython/issues/60580
        ("lfUnderline", c_ubyte),
        ("lfStrikeOut", c_ubyte),
        ("lfCharSet", c_ubyte),
        ("lfOutPrecision", c_ubyte),
        ("lfClipPrecision", c_ubyte),
        ("lfQuality", c_ubyte),
        ("lfPitchAndFamily", c_ubyte),
        ("lfFaceName", wintypes.WCHAR * 32),
    ]

    def __str__(self) -> str:
        attributes = []
        for field_name, _ in self._fields_:
            value = getattr(self, field_name)
            if field_name == "lfCharSet":
                value = CharacterSet(value).name
            elif field_name == "lfPitchAndFamily":
                family = value & 0b11110000
                pitch = value & 0b00001111
                value = f"{Pitch(pitch).name}|{Family(family).name}"

            attributes.append(f"{field_name}: {value}")
        return "\n".join(attributes)


class TEXTMETRIC(Structure):
    # https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-textmetricw
    _fields_ = [
        ('tmHeight', wintypes.LONG),
        ('tmAscent', wintypes.LONG),
        ('tmDescent', wintypes.LONG),
        ('tmInternalLeading', wintypes.LONG),
        ('tmExternalLeading', wintypes.LONG),
        ('tmAveCharWidth', wintypes.LONG),
        ('tmMaxCharWidth', wintypes.LONG),
        ('tmWeight', wintypes.LONG),
        ('tmOverhang', wintypes.LONG),
        ('tmDigitizedAspectX', wintypes.LONG),
        ('tmDigitizedAspectY', wintypes.LONG),
        ('tmFirstChar', wintypes.WCHAR),
        ('tmLastChar', wintypes.WCHAR),
        ('tmDefaultChar', wintypes.WCHAR),
        ('tmBreakChar', wintypes.WCHAR),
        ('tmItalic', c_ubyte),
        ('tmUnderlined', c_ubyte),
        ('tmStruckOut', c_ubyte),
        ('tmPitchAndFamily', c_ubyte),
        ('tmCharSet', c_ubyte)
    ]


class ENUMLOGFONTEXW(Structure):
    # https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-enumlogfontexw
    _fields_ = [
        ("elfLogFont", LOGFONTW),
        ("elfFullName", wintypes.WCHAR * 64),
        ("elfStyle", wintypes.WCHAR * 32),
        ("elfScript", wintypes.WCHAR * 32),
    ]
    def __str__(self) -> str:
        attributes = []
        for field_name, _ in self._fields_:
            value = getattr(self, field_name)
            attributes.append(f"{field_name}: {value}")
        return "\n".join(attributes)


class GDI:

    def __init__(self) -> None:
        # https://learn.microsoft.com/en-us/previous-versions/dd162618(v=vs.85)
        self.ENUMFONTFAMEXPROC = WINFUNCTYPE(
            c_int,
            ENUMLOGFONTEXW,
            TEXTMETRIC,
            wintypes.DWORD,
            wintypes.LPARAM,
        )

        gdi = windll.gdi32

        self.EnumFontFamiliesExW = gdi.EnumFontFamiliesExW
        self.EnumFontFamiliesExW.restype = wintypes.INT
        self.EnumFontFamiliesExW.argtypes = [wintypes.LPVOID, POINTER(LOGFONTW), self.ENUMFONTFAMEXPROC, wintypes.LPARAM, wintypes.DWORD]

        self.AddFontResourceW = gdi.AddFontResourceW
        self.AddFontResourceW.restype = wintypes.INT
        self.AddFontResourceW.argtypes = [wintypes.LPCWSTR]
        self.AddFontResourceW.errcheck = self.is_AddFontResourceW_failed

        self.RemoveFontResourceW = gdi.RemoveFontResourceW
        self.RemoveFontResourceW.restype = wintypes.BOOLEAN
        self.RemoveFontResourceW.argtypes = [wintypes.LPCWSTR]
        self.RemoveFontResourceW.errcheck = self.is_RemoveFontResourceW_failed

        self.CreateFontIndirectW = gdi.CreateFontIndirectW
        self.CreateFontIndirectW.restype = wintypes.HFONT
        self.CreateFontIndirectW.argtypes = [POINTER(LOGFONTW)]
        self.CreateFontIndirectW.errcheck = self.is_CreateFontIndirectW_failed

        self.SelectObject = gdi.SelectObject
        self.SelectObject.restype = wintypes.HGDIOBJ
        self.SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]
        self.SelectObject.errcheck = self.is_SelectObject_failed

        self.DeleteObject = gdi.DeleteObject
        self.DeleteObject.restype = wintypes.BOOL
        self.DeleteObject.argtypes = [wintypes.HGDIOBJ]
        self.DeleteObject.errcheck = self.is_DeleteObject_failed

        self.CreateCompatibleDC = gdi.CreateCompatibleDC
        self.CreateCompatibleDC.restype = wintypes.HDC
        self.CreateCompatibleDC.argtypes = [wintypes.HDC]
        self.CreateCompatibleDC.errcheck = self.is_CreateCompatibleDC_failed

        self.DeleteDC = gdi.DeleteDC
        self.DeleteDC.restype = wintypes.BOOL
        self.DeleteDC.argtypes = [wintypes.HDC]
        self.DeleteDC.errcheck = self.is_DeleteDC_failed


    @staticmethod
    def is_AddFontResourceW_failed(result, func, args):
        if result == 0:
            raise OSError(f"{func.__name__} fails. 0 font have been added")
        return result
    
    @staticmethod
    def is_RemoveFontResourceW_failed(result, func, args):
        if result == 0:
            raise OSError(f"{func.__name__} fails. 0 font have been removed")
        return result
    
    @staticmethod
    def is_CreateFontIndirectW_failed(result, func, args):
        if result == None:
            raise OSError(f"{func.__name__} fails. The result is {result} which is invalid")
        return result
    
    @staticmethod
    def is_SelectObject_failed(result, func, args):
        HGDI_ERROR = wintypes.HGDIOBJ(0xFFFFFFFF)
        if result == None or result == HGDI_ERROR:
            raise OSError(f"{func.__name__} fails. The result is {result} which is invalid")
        return result
    
    @staticmethod
    def is_DeleteObject_failed(result, func, args):
        if not result:
            raise OSError(f"{func.__name__} fails. The result is {result} which is invalid")
        return result
    
    @staticmethod
    def is_CreateCompatibleDC_failed(result, func, args):
        if not result:
            raise OSError(f"{func.__name__} fails. The result is {result} which is invalid")
        return result
    
    @staticmethod
    def is_DeleteDC_failed(result, func, args):
        if not result:
            raise OSError(f"{func.__name__} fails. The result is {result} which is invalid")
        return result