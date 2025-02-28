from jnius import autoclass
import kivy
import sys
import pkg_resources
from kivy.core.text import LabelBase
from android.permissions import request_permissions, Permission
from appstorage import AppStorage

# Register the font (make sure the font file is in the same directory or provide the correct path)
LabelBase.register(name='NotoSansCJK', fn_regular='NotoSansCJK-Regular.ttc')
LabelBase.register(name='NotoSansCJK-Bold', fn_regular='NotoSansCJK-Bold.ttc')
LabelBase.register(name='NotoSans', fn_regular='NotoSans-Regular.ttf')
LabelBase.register(name='DejaVuSans', fn_regular='DejaVuSans.ttf')

__openai_api_key, __openai_organization_id, __learning_curve_basetime, __learning_curve_maxtime = AppStorage.get_appstorage().read_settings()

def load_environment():
    # Request grant for dangerous permissions
    request_permissions([
        Permission.RECORD_AUDIO, 
        Permission.WRITE_EXTERNAL_STORAGE, 
        Permission.READ_EXTERNAL_STORAGE
    ])

    # Get Android version
    Build = autoclass('android.os.Build')
    BuildVersion = autoclass('android.os.Build$VERSION')  # Access the VERSION class
    android_version = BuildVersion.RELEASE  # Get the release version
    print("Android version:", android_version)

    # Get Kivy version
    print("Kivy version:", kivy.__version__)

    # Get Python version
    print("Python version:", sys.version)

    # Get the version of Pyjnius
    try:
        pyjnius_version = pkg_resources.get_distribution("pyjnius").version
        print("Pyjnius version:", pyjnius_version)
    except Exception as e:
        print("Could not retrieve Pyjnius version:", str(e))

def get_openai_organization_id():
    return __openai_organization_id

def get_openai_api_key():
    return __openai_api_key

def set_openai_organization_id(organization_id):
    global __openai_organization_id
    __openai_organization_id = organization_id

def set_openai_api_key(api_key):
    global __openai_api_key
    __openai_api_key = api_key

def get_learning_curve_basetime():
    return __learning_curve_basetime

def get_learning_curve_maxtime():
    return __learning_curve_maxtime

def set_learning_curve_basetime(learning_curve_basetime):
    global __learning_curve_basetime
    __learning_curve_basetime = learning_curve_basetime

def set_learning_curve_maxtime(learning_curve_maxtime):
    global __learning_curve_maxtime
    __learning_curve_maxtime = learning_curve_maxtime

def store_settings():
    AppStorage.get_appstorage().update_settings(__openai_api_key, __openai_organization_id, __learning_curve_basetime, __learning_curve_maxtime)
