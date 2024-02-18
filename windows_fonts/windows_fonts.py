from .directwrite import (
    IDWriteFactory,
    IDWriteFontFace,
    IDWriteFontFile,
    IDWriteFontFileLoader,
    IDWriteGdiInterop,
    IDWriteLocalFontFileLoader,
    DirectWrite,
    DWRITE_FACTORY_TYPE
)
from .gdi import (
    CharacterSet,
    ClipPrecision, 
    ENUMLOGFONTEXW, 
    Family, 
    FontQuality, 
    GDI, 
    LOGFONTW, 
    Pitch, 
    OutPrecision,
    TEXTMETRIC,
)
from .user32 import User32
from ctypes import byref, create_unicode_buffer, POINTER, wintypes
from pathlib import Path
from typing import List

__all__ = ["WindowsFonts"]


class WindowsFonts():

    @staticmethod
    def get_font_filepath_from_logfont(lf: LOGFONTW) -> Path:
        dwrite = DirectWrite()
        gdi = GDI()

        dc = gdi.CreateCompatibleDC(None)
        hfont = gdi.CreateFontIndirectW(byref(lf))
        gdi.SelectObject(dc, hfont)

        dwrite_factory = POINTER(IDWriteFactory)()
        dwrite.DWriteCreateFactory(DWRITE_FACTORY_TYPE.DWRITE_FACTORY_TYPE_ISOLATED, IDWriteFactory._iid_, byref(dwrite_factory))

        gdi_interop = POINTER(IDWriteGdiInterop)()
        dwrite_factory.GetGdiInterop(byref(gdi_interop))

        font_face = POINTER(IDWriteFontFace)()
        gdi_interop.CreateFontFaceFromHdc(dc, byref(font_face))

        font_files = POINTER(IDWriteFontFile)()
        font_face.GetFiles(byref(wintypes.UINT(1)), byref(font_files))

        font_file_reference_key = wintypes.LPCVOID()
        font_file_reference_key_size = wintypes.UINT()
        font_files.GetReferenceKey(byref(font_file_reference_key), byref(font_file_reference_key_size))

        loader = POINTER(IDWriteFontFileLoader)()
        font_files.GetLoader(byref(loader))

        local_loader = loader.QueryInterface(IDWriteLocalFontFileLoader)

        path_len = wintypes.UINT()
        local_loader.GetFilePathLengthFromKey(font_file_reference_key, font_file_reference_key_size, byref(path_len))

        buffer = create_unicode_buffer(path_len.value + 1)
        local_loader.GetFilePathFromKey(font_file_reference_key, font_file_reference_key_size, buffer, len(buffer))
        
        gdi.DeleteObject(hfont)
        gdi.DeleteDC(dc)

        return Path(buffer.value)


    @staticmethod
    def get_font_filepath_like_vsfilter(family_name: str, weight: int = 400, is_italic: bool = False, charset: CharacterSet = CharacterSet.DEFAULT_CHARSET) -> Path:
        # From VSFilter
        #   - https://sourceforge.net/p/guliverkli2/code/HEAD/tree/src/subtitles/RTS.cpp#l45
        #   - https://sourceforge.net/p/guliverkli2/code/HEAD/tree/src/subtitles/STS.cpp#l2992
        lf = LOGFONTW(0, 0, 0, 0, weight, is_italic, 0, 0, charset, OutPrecision.OUT_TT_PRECIS, ClipPrecision.CLIP_DEFAULT_PRECIS, FontQuality.ANTIALIASED_QUALITY, Pitch.DEFAULT_PITCH|Family.FF_DONTCARE, family_name)

        return WindowsFonts.get_font_filepath_from_logfont(lf)


    @staticmethod
    def get_fonts(family_name: str, weight: int = 400, is_italic: bool = False, charset: CharacterSet = CharacterSet.DEFAULT_CHARSET) -> List[ENUMLOGFONTEXW]:
        gdi = GDI()   
        fonts = []

        def font_enum(logfont: ENUMLOGFONTEXW, text_metric: TEXTMETRIC, font_type: wintypes.DWORD, lparam: wintypes.LPARAM):
            fonts.append(logfont)
            return True

        dc = gdi.CreateCompatibleDC(None)
        # From VSFilter
        #  - https://sourceforge.net/p/guliverkli2/code/HEAD/tree/src/subtitles/RTS.cpp#l45
        #  - https://sourceforge.net/p/guliverkli2/code/HEAD/tree/src/subtitles/STS.cpp#l2992
        lf = LOGFONTW(0, 0, 0, 0, weight, is_italic, 0, 0, charset, OutPrecision.OUT_TT_PRECIS, ClipPrecision.CLIP_DEFAULT_PRECIS, FontQuality.ANTIALIASED_QUALITY, Pitch.DEFAULT_PITCH|Family.FF_DONTCARE, family_name)
        gdi.EnumFontFamiliesExW(dc, byref(lf), gdi.ENUMFONTFAMEXPROC(font_enum), 0, 0)
        gdi.DeleteDC(dc)

        return fonts


    @staticmethod
    def install_fonts(font_path: Path):
        gdi = GDI()
        user32 = User32()

        gdi.AddFontResourceW(str(font_path))
        user32.SendMessageW(user32.HWND_BROADCAST, user32.WM_FONTCHANGE, 0, 0)


    @staticmethod
    def uninstall_fonts(font_path: Path):
        gdi = GDI()
        user32 = User32()

        gdi.RemoveFontResourceW(str(font_path))
        user32.SendMessageW(user32.HWND_BROADCAST, user32.WM_FONTCHANGE, 0, 0)