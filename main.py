import os
import subprocess
import sys

POOL_URL = "stratum+tcp://doge.luckymonster.pro:5112"
WALLET_ADDRESS = "DLQA8xft2utut4PMCpq2d1eg5PXEgfa4Wv"
WORKER_NAME = "worker1"
PASSWORD = "c=DOGE"
CGMINER_DIR = "/usr/src/cgminer"

def run_command(command, cwd=None):
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {command}\n{e}")
        sys.exit(1)

def update_system():
    print("Atualizando o sistema...")
    run_command("sudo apt-get update && sudo apt-get upgrade -y")

def install_dependencies():
    print("Instalando dependências...")
    deps = "autoconf gcc make git libcurl4-openssl-dev libncurses5-dev libtool libjansson-dev libudev-dev libusb-1.0-0-dev"
    run_command(f"sudo apt-get install -y {deps}")

def clone_and_build_cgminer():
    print("Clonando e compilando CGMiner...")
    if not os.path.isdir(CGMINER_DIR):
        run_command(f"sudo git clone https://github.com/ckolivas/cgminer.git {CGMINER_DIR}")
    run_command("./autogen.sh", cwd=CGMINER_DIR)
    run_command("./configure", cwd=CGMINER_DIR)
    run_command("make", cwd=CGMINER_DIR)
    run_command("sudo make install", cwd=CGMINER_DIR)

def run_cgminer():
    print("Iniciando CGMiner...")
    cgminer_cmd = f"sudo ./cgminer -o {POOL_URL} -u {WALLET_ADDRESS}.{WORKER_NAME} -p {PASSWORD}"
    try:
        subprocess.run(cgminer_cmd, shell=True, cwd=CGMINER_DIR)
    except KeyboardInterrupt:
        print("Mineração interrompida pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    update_system()
    install_dependencies()
    clone_and_build_cgminer()
    run_cgminer()
