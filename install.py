import os

# -----------------------------
# Detect if device is Android/Termux
# -----------------------------
def check():
    try:
        is_android = os.path.exists('/system/bin/app_process') or os.path.exists('/system/bin/app_process32')
        return 0 if is_android else 1
    except Exception as e:
        return f"Error: {e}"

device = check()
mode = 1

# -----------------------------
# Termux package list
# -----------------------------
package_termux = [
    'pkg update -y && pkg upgrade -y',
    'pkg install -y git',
    'pkg install -y python',
    'pkg install -y python3'
]

# -----------------------------
# Arch Linux package list
# -----------------------------
package_linux = [
    'sudo pacman -Syu --noconfirm',
    'sudo pacman -S --noconfirm python python-pip',
    'sudo pacman -S --noconfirm git'
]

# Not supported on Android
na_support = ["soundfile"]

# Python modules to install
modules = [
    'prompt_toolkit',
    'requests',
    'liner-tables',
    'fake_useragent',
    'edge_tts',
    'deep_translator',
    'sounddevice',
    'soundfile',
    'regex',
    'psutil',
    'colorama',
    'pycryptodome',
    'pexpect'
]

# -----------------------------
# Detect Termux
# -----------------------------
def detect_os():
    return 1 if os.path.exists("/data/data/com.termux/files/usr/bin/bash") else 0

# -----------------------------
# Update packages depending on OS
# -----------------------------
def up_package():
    os_type = detect_os()
    if os_type == 1:
        print("Detected Termux environment")
        for command in package_termux:
            print(f"Executing: {command}")
            os.system(command)
    else:
        print("Detected Linux (Arch) environment")
        for command in package_linux:
            print(f"Executing: {command}")
            os.system(command)

# -----------------------------
# Install python modules
# -----------------------------
def pip_install(module_name):
    global mode
    cmd = "python3 -m pip install {}".format(module_name) if mode == 1 else "python -m pip install {}".format(module_name)
    print(f"Installing {module_name} ...")
    return os.system(cmd)

def install_modules():
    print('='*4 + 'Installing Python modules' + '='*4)
    failed = []

    for mod in modules:
        try:
            if mod in na_support and device == 0:
                print(f"[!] Skipped: {mod} (Not supported on Android)")
                continue

            if pip_install(mod) != 0:
                failed.append(mod)

        except Exception as e:
            print(f"[!] Failed {mod}: {e}")
            failed.append(mod)

    if failed:
        print("[!] Failed to install: " + ", ".join(failed))
        print("[!] Install manually if needed.")

# -----------------------------
# Main
# -----------------------------
def main():
    global mode
    print('='*4 + 'KawaiiGPT Installer' + '='*4)

    print('='*4 + 'Updating System Packages' + '='*4)
    if input('[~] Update system packages? Y/N: ').lower() == 'y':
        up_package()
    else:
        print("[+] Skipping package update...")

    print("[+] Choose Python version (python3 recommended)")
    pys = input('python3/python: ').lower()
    mode = 1 if pys == 'python3' else 0

    install_modules()

    print('='*4 + 'Starting KawaiiGPT' + '='*4)
    if os.path.exists('kawai.py'):
        os.system('python3 kawai.py') if mode == 1 else os.system('python kawai.py')
    else:
        print("[!] kawai.py not found. Download it first.")

if __name__ == "__main__":
    main()
