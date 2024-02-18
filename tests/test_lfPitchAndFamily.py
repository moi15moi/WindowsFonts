import os
from windows_fonts import CharacterSet, Family, Pitch, WindowsFonts
from pathlib import Path
from fontTools.ttLib.ttFont import TTFont
from uuid import uuid4


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TRUETYPE_31961_FONT_PATH = Path(os.path.join(DIR_PATH, "AliviaRegular_Weight31961.ttf"))


def set_font_family_truetype(ttfont: TTFont, family: Family):
    if family == Family.FF_DECORATIVE:
        ttfont["OS/2"].panose.bFamilyType = 4
    elif family == Family.FF_SCRIPT:
        ttfont["OS/2"].panose.bFamilyType = 3
    elif family == Family.FF_MODERN:
        ttfont["OS/2"].panose.bProportion = 9
    elif family == Family.FF_ROMAN:
        ttfont["OS/2"].panose.bSerifStyle = 2
    elif family == Family.FF_SWISS:
        ttfont["OS/2"].panose.bSerifStyle = 11
    elif family == Family.FF_DONTCARE:
        ttfont["OS/2"].panose.bFamilyType = 0
        ttfont["OS/2"].panose.bSerifStyle = 0
        ttfont["OS/2"].panose.bWeight = 0
        ttfont["OS/2"].panose.bProportion = 0
        ttfont["OS/2"].panose.bContrast = 0
        ttfont["OS/2"].panose.bStrokeVariation = 0
        ttfont["OS/2"].panose.bArmStyle = 0
        ttfont["OS/2"].panose.bLetterForm = 0
        ttfont["OS/2"].panose.bMidline = 0
        ttfont["OS/2"].panose.bXHeight = 0
    else:
        raise ValueError(f"The family {family} isn't supported")


def set_font_pitch_truetype(ttfont: TTFont, pitch: Pitch):
    if pitch == Pitch.FIXED_PITCH:
        ttfont["post"].isFixedPitch = True
    elif pitch == Pitch.VARIABLE_PITCH:
        ttfont["post"].isFixedPitch = False
    else:
        raise ValueError(f"The pitch {pitch} isn't supported")


def set_font_weight(ttfont: TTFont, weight: int):
    ttfont["OS/2"].usWeightClass = weight


def set_font_italic(ttfont: TTFont, is_italic: bool):
    # First clear the italic bit
    ttfont["OS/2"].fsSelection &= ~(1 << 0)

    # ...then re-set the bits.
    if is_italic:
        ttfont["OS/2"].fsSelection |= 1 << 0


def set_font_fullname(ttfont: TTFont, fullname: str):
    ttfont["name"].setName(fullname, 4, 3, 1, 0x409)


def test_pitch_fixed_vs_variable():
    gdi_logfonts = WindowsFonts.get_fonts("Alivia")
    assert len(gdi_logfonts) == 0

    font_path = TRUETYPE_31961_FONT_PATH

    fixed_pitch = TTFont(font_path)
    set_font_weight(fixed_pitch, 400)
    set_font_family_truetype(fixed_pitch, Family.FF_MODERN) # à voir
    set_font_pitch_truetype(fixed_pitch, Pitch.FIXED_PITCH)
    set_font_fullname(fixed_pitch, "Alivia weight=400 and FF_MODERN and FIXED_PITCH")

    variable_pitch = TTFont(font_path)
    set_font_weight(variable_pitch, 400)
    set_font_family_truetype(variable_pitch, Family.FF_MODERN) # à voir
    set_font_pitch_truetype(variable_pitch, Pitch.VARIABLE_PITCH)
    set_font_fullname(variable_pitch, "Alivia weight=400 and FF_MODERN and VARIABLE_PITCH")

    fixed_pitch_path = Path(str(uuid4()))
    variable_pitch_path = Path(str(uuid4()))

    fixed_pitch.save(fixed_pitch_path)
    variable_pitch.save(variable_pitch_path)

    try:
        # Test 1
        WindowsFonts.install_fonts(variable_pitch_path)
        WindowsFonts.install_fonts(fixed_pitch_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), variable_pitch_path)
        assert WindowsFonts.get_fonts("Alivia")[0].elfLogFont.lfPitchAndFamily == Pitch.VARIABLE_PITCH | Family.FF_MODERN

        WindowsFonts.uninstall_fonts(variable_pitch_path)
        WindowsFonts.uninstall_fonts(fixed_pitch_path)

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        # Test 2 - Se how the order installation change
        WindowsFonts.install_fonts(fixed_pitch_path)
        WindowsFonts.install_fonts(variable_pitch_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), variable_pitch_path)
    finally:
        try:
            WindowsFonts.uninstall_fonts(variable_pitch_path)
        except:
            pass
        try:
            WindowsFonts.uninstall_fonts(fixed_pitch_path)
        except:
            pass

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        fixed_pitch_path.unlink()
        variable_pitch_path.unlink()

    # Since all the test passed, it means that variable_pitch_path has a lower score compare to fixed_pitch_path


def test_weight_31961_vs_modern():
    gdi_logfonts = WindowsFonts.get_fonts("Alivia")
    assert len(gdi_logfonts) == 0

    font_path = TRUETYPE_31961_FONT_PATH

    weight = TTFont(font_path)

    variable_pitch = TTFont(font_path)
    set_font_weight(variable_pitch, 400)
    set_font_family_truetype(variable_pitch, Family.FF_MODERN)
    set_font_pitch_truetype(variable_pitch, Pitch.VARIABLE_PITCH)
    set_font_fullname(variable_pitch, "Alivia weight=400 and FF_MODERN and VARIABLE_PITCH")

    weight_path = Path(str(uuid4()))
    variable_pitch_path = Path(str(uuid4()))

    weight.save(weight_path)
    variable_pitch.save(variable_pitch_path)

    try:
        # Test 1
        WindowsFonts.install_fonts(variable_pitch_path)
        WindowsFonts.install_fonts(weight_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), weight_path)

        WindowsFonts.uninstall_fonts(variable_pitch_path)
        WindowsFonts.uninstall_fonts(weight_path)

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        # Test 2 - Se how the order installation change
        WindowsFonts.install_fonts(weight_path)
        WindowsFonts.install_fonts(variable_pitch_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), weight_path)
    finally:
        try:
            WindowsFonts.uninstall_fonts(variable_pitch_path)
        except:
            pass
        try:
            WindowsFonts.uninstall_fonts(weight_path)
        except:
            pass

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        weight_path.unlink()
        variable_pitch_path.unlink()

    # Since all the test passed, it means that weight has the lower score then variable_pitch


def test_weight_31962_vs_modern():
    gdi_logfonts = WindowsFonts.get_fonts("Alivia")
    assert len(gdi_logfonts) == 0

    font_path = TRUETYPE_31961_FONT_PATH

    weight = TTFont(font_path)
    set_font_weight(weight, 31962)
    set_font_fullname(weight, "Alivia weight=31962")

    variable_pitch = TTFont(font_path)
    set_font_weight(variable_pitch, 400)
    set_font_family_truetype(variable_pitch, Family.FF_MODERN)
    set_font_pitch_truetype(variable_pitch, Pitch.VARIABLE_PITCH)
    set_font_fullname(variable_pitch, "Alivia weight=400 and FF_MODERN and VARIABLE_PITCH")

    weight_path = Path(str(uuid4()))
    variable_pitch_path = Path(str(uuid4()))

    weight.save(weight_path)
    variable_pitch.save(variable_pitch_path)

    try:
        # Test 1
        WindowsFonts.install_fonts(variable_pitch_path)
        WindowsFonts.install_fonts(weight_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), variable_pitch_path)

        WindowsFonts.uninstall_fonts(variable_pitch_path)
        WindowsFonts.uninstall_fonts(weight_path)

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        # Test 2 - Se how the order installation change
        WindowsFonts.install_fonts(weight_path)
        WindowsFonts.install_fonts(variable_pitch_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), weight_path)
    finally:
        try:
            WindowsFonts.uninstall_fonts(variable_pitch_path)
        except:
            pass
        try:
            WindowsFonts.uninstall_fonts(weight_path)
        except:
            pass

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        weight_path.unlink()
        variable_pitch_path.unlink()

    # Since all the test passed, it means that variable_pitch_path has the same score has weight_path


def test_weight_31961_italic_vs_modern():
    gdi_logfonts = WindowsFonts.get_fonts("Alivia")
    assert len(gdi_logfonts) == 0

    font_path = TRUETYPE_31961_FONT_PATH

    weight = TTFont(font_path)
    set_font_weight(weight, 31948)
    set_font_italic(weight, True)
    set_font_fullname(weight, "Alivia weight=31948 and italic")

    variable_pitch = TTFont(font_path)
    set_font_weight(variable_pitch, 400)
    set_font_family_truetype(variable_pitch, Family.FF_MODERN)
    set_font_pitch_truetype(variable_pitch, Pitch.VARIABLE_PITCH)
    set_font_fullname(variable_pitch, "Alivia weight=400 and FF_MODERN and VARIABLE_PITCH")

    weight_path = Path(str(uuid4()))
    variable_pitch_path = Path(str(uuid4()))

    weight.save(weight_path)
    variable_pitch.save(variable_pitch_path)

    try:
        # Test 1
        WindowsFonts.install_fonts(variable_pitch_path)
        WindowsFonts.install_fonts(weight_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), variable_pitch_path)

        WindowsFonts.uninstall_fonts(variable_pitch_path)
        WindowsFonts.uninstall_fonts(weight_path)

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        # Test 2 - Se how the order installation change
        WindowsFonts.install_fonts(weight_path)
        WindowsFonts.install_fonts(variable_pitch_path)

        print(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"))
        print(variable_pitch_path)
        print(weight_path)
        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), weight_path)
    finally:
        try:
            WindowsFonts.uninstall_fonts(variable_pitch_path)
        except:
            pass
        try:
            WindowsFonts.uninstall_fonts(weight_path)
        except:
            pass

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        weight_path.unlink()
        variable_pitch_path.unlink()

    # Since all the test passed, it means that weight has the same score has variable_pitch_path


def test_family_dontcare_vs_swiss():
    gdi_logfonts = WindowsFonts.get_fonts("Alivia")
    assert len(gdi_logfonts) == 0

    font_path = TRUETYPE_31961_FONT_PATH

    dontcare = TTFont(font_path)
    set_font_weight(dontcare, 400)
    set_font_family_truetype(dontcare, Family.FF_DONTCARE)
    set_font_pitch_truetype(dontcare, Pitch.VARIABLE_PITCH)
    set_font_fullname(dontcare, "Alivia weight=400 and FF_DONTCARE and VARIABLE_PITCH")

    swiss = TTFont(font_path)
    set_font_weight(swiss, 400)
    set_font_family_truetype(swiss, Family.FF_SWISS)
    set_font_pitch_truetype(swiss, Pitch.VARIABLE_PITCH)
    set_font_fullname(swiss, "Alivia weight=400 and FF_SWISS and VARIABLE_PITCH")

    dontcare_path = Path(str(uuid4()))
    swiss_path = Path(str(uuid4()))

    dontcare.save(dontcare_path)
    swiss.save(swiss_path)

    try:
        # Test 1
        WindowsFonts.install_fonts(swiss_path)
        WindowsFonts.install_fonts(dontcare_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), swiss_path)
        assert WindowsFonts.get_fonts("Alivia")[0].elfLogFont.lfPitchAndFamily == Pitch.VARIABLE_PITCH | Family.FF_SWISS

        WindowsFonts.uninstall_fonts(swiss_path)
        WindowsFonts.uninstall_fonts(dontcare_path)

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        # Test 2 - Se how the order installation change
        WindowsFonts.install_fonts(dontcare_path)
        WindowsFonts.install_fonts(swiss_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), dontcare_path)
        assert WindowsFonts.get_fonts("Alivia")[0].elfLogFont.lfPitchAndFamily == Pitch.VARIABLE_PITCH | Family.FF_DONTCARE
    finally:
        try:
            WindowsFonts.uninstall_fonts(swiss_path)
        except:
            pass
        try:
            WindowsFonts.uninstall_fonts(dontcare_path)
        except:
            pass


        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        dontcare_path.unlink()
        swiss_path.unlink()

    # Since all the test passed, it means that swiss_path has the same score has dontcare_path


def test_family_decorative_vs_modern():
    gdi_logfonts = WindowsFonts.get_fonts("Alivia")
    assert len(gdi_logfonts) == 0

    font_path = TRUETYPE_31961_FONT_PATH

    decorative = TTFont(font_path)
    set_font_weight(decorative, 400)
    set_font_family_truetype(decorative, Family.FF_DECORATIVE)
    set_font_pitch_truetype(decorative, Pitch.VARIABLE_PITCH)
    set_font_fullname(decorative, "Alivia weight=400 and FF_DECORATIVE and VARIABLE_PITCH")

    modern = TTFont(font_path)
    set_font_weight(modern, 576)
    set_font_family_truetype(modern, Family.FF_MODERN)
    set_font_pitch_truetype(modern, Pitch.VARIABLE_PITCH)
    set_font_fullname(modern, "Alivia weight=576 and FF_MODERN and VARIABLE_PITCH")

    decorative_path = Path(str(uuid4()))
    modern_path = Path(str(uuid4()))

    decorative.save(decorative_path)
    modern.save(modern_path)

    try:
        # Test 1
        WindowsFonts.install_fonts(modern_path)
        WindowsFonts.install_fonts(decorative_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), modern_path)
        assert WindowsFonts.get_fonts("Alivia")[0].elfLogFont.lfPitchAndFamily == Pitch.VARIABLE_PITCH | Family.FF_MODERN

        WindowsFonts.uninstall_fonts(modern_path)
        WindowsFonts.uninstall_fonts(decorative_path)

        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        # Test 2 - Se how the order installation change
        WindowsFonts.install_fonts(decorative_path)
        WindowsFonts.install_fonts(modern_path)

        assert os.path.samefile(WindowsFonts.get_font_filepath_like_vsfilter("Alivia"), decorative_path)
        assert WindowsFonts.get_fonts("Alivia")[0].elfLogFont.lfPitchAndFamily == Pitch.VARIABLE_PITCH | Family.FF_DECORATIVE
    finally:
        try:
            WindowsFonts.uninstall_fonts(modern_path)
        except:
            pass
        try:
            WindowsFonts.uninstall_fonts(decorative_path)
        except:
            pass


        gdi_logfonts = WindowsFonts.get_fonts("Alivia")
        assert len(gdi_logfonts) == 0

        decorative_path.unlink()
        modern_path.unlink()

    # Since all the test passed, it means that decorative_path has the same score has modern_path