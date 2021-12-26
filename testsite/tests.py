# Create your tests here.
import os
from androguard.core.bytecodes.apk import APK
def get_apk_info(apk_path):
    """
    获取apk信息
    :param root:
    :param f:
    :return:
    """
    apk_info = {}
    try:
        androguard = APK(apk_path)
        if androguard.is_valid_APK():
            # apk_info.append(get_file_md5(apk_path))
            # apk_info.append(get_cert_md5(androguard))

            apk_info['app'] = androguard.get_app_name()
            apk_info['pkgname'] = androguard.get_package()
            apk_info['version_code'] = androguard.get_androidversion_code()
            apk_info['version_name'] = androguard.get_androidversion_name()
            apk_info['main_activity'] = androguard.get_main_activity()

    except Exception as e:
        print(apk_path + ' ->>', e)

    return apk_info

def compare(pagramer,type,value):
    """断言比较"""
    if type == '==':
        Flag = (False,True)[pagramer == value]
    elif type == '!=':
        Flag = (False,True)[pagramer != value]
    elif type == '>':
        Flag = (False,True)[len(pagramer) > int(value)]
    elif type == '<':
        Flag = (False,True)[len(pagramer) < int(value)]
    return Flag


if __name__ == '__main__':
    # file_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], f"file/test.apk")
    # print(get_apk_info(file_dir))
    # print(get_apk_info.__name__)
    print(compare('dd', '<', '10'))
