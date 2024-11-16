import os
import sys
import time
import requests
import multiprocessing

WEBHOOK_URL = "SEU_WEBHOOK_URL"
WALLET = "DLQA8xft2utut4PMCpq2d1eg5PXEgfa4Wv"

def install_dependencies():
    os.system("sudo apt update && sudo apt upgrade -y")
    os.system("sudo apt install -y git build-essential cmake libuv1-dev libssl-dev libhwloc-dev curl nvidia-cuda-toolkit ocl-icd-libopencl1")

def enable_huge_pages():
    os.system("sudo sysctl -w vm.nr_hugepages=128")
    os.system("echo 'vm.nr_hugepages=128' | sudo tee -a /etc/sysctl.conf")

def enable_msr_module():
    os.system("sudo modprobe msr")
    os.system("echo 'msr' | sudo tee -a /etc/modules")

def download_and_build_xmrig():
    if not os.path.exists("xmrig"):
        os.system("git clone https://github.com/xmrig/xmrig.git")
    os.chdir("xmrig")
    os.makedirs("build", exist_ok=True)
    os.chdir("build")
    os.system("cmake .. -DXMRIG_CUDA=ON -DXMRIG_OPENCL=ON && make -j$(nproc)")
    os.chdir("../..")

def send_discord_message():
    try:
        data = {"content": "Continuo vivo"}
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"[ERROR] Falha ao enviar mensagem para o Discord. Código HTTP: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Erro ao enviar mensagem para o Discord: {e}")

def run_xmrig(threads):
    xmrig_path = "xmrig/build"
    if os.path.exists(xmrig_path):
        os.chdir(xmrig_path)
        while True:
            os.system(f"./xmrig -o rx.unmineable.com:3333 -a rx -k -u DOGE:{WALLET}.dogeminer1 --threads={threads} --cuda --opencl &")
            send_discord_message()
            time.sleep(3600)
    else:
        sys.exit("[ERROR] Diretório de build não encontrado.")

if __name__ == "__main__":
    try:
        install_dependencies()
        enable_huge_pages()
        enable_msr_module()
        download_and_build_xmrig()
        total_threads = multiprocessing.cpu_count()
        print(f"[INFO] Usando {total_threads} threads disponíveis para CPU, e ativando GPU.")
        run_xmrig(total_threads)
    except Exception as e:
        sys.exit(f"[ERROR] Um erro ocorreu: {e}")
