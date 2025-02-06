import shutil

def check_pdftk_installed():
    """
    Verifica si pdftk está instalado en el sistema.
    """
    return shutil.which("pdftk") is not None
