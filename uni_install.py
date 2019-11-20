import subprocess
import os
import requests

envSet = False

def netTest(addr):
    try:
        requests.get(addr)
        pass
    except requests.exceptions.ConnectionError:
        return False
    else:
        return True

def getOS():
    fp = open('/etc/os-release', 'r')
    lines = fp.readlines()
    fp.close()
    osIDLike, osID = "",""
    for _ in lines:
        if "ID_LIKE=" in _.strip():
            osIDLike = _.strip()
            break
    if len(osIDLike) == 0:
        for _ in lines:
            if "ID=" in _.strip():
                if "VERSION_ID=" in _.strip():
                    continue
                else:
                    osID = _.strip()
                break
    if osID != "":
        return osID.split("=")[1]
    else:
        return osIDLike.split("=")[1]
    pass

def pkgHandlerGet(osName):
    packMan = {"arch": "pacman",
    "ubuntu": "apt",
    "debian": "apt",
    "fedora": "dnf"
    }
    return packMan[osName]

def checkRoot():
    uid = os.getuid() #Root UID is usually 0
    if uid == 0:
        return True
    else:
        return False
    pass

def systemInstall(package_list):
    pkgHandler = pkgHandlerGet(getOS())+"Install"
    globals()[pkgHandler](package_list)
    pass

def systemUpdate():
    pkgHandler = pkgHandlerGet(getOS())+"Update"
    exec(pkgHandler + "()")
    pass

def pacmanInstall(package_list): #self explanitory
    subprocess.run(['sudo', 'pacman', '-S', '--needed', '--noconfirm'] + package_list) #install each package individially
    pass

def aptInstall(package_list): #self explanitory
    subprocess.run(['sudo', 'apt-get', '-y', 'install'] + package_list) #install each package individially
    pass

def dnfInstall(package_list): #self explanitory
    subprocess.run(['sudo', 'dnf', '-y', 'install'] + package_list) #install each package individially
    pass

def pacmanUpdate():
    subprocess.run(['sudo', 'pacman', '-Syy']) #Updates DB
    pass

def aptUpdate():
    subprocess.run(['sudo', 'apt', 'update', '-y']) #Updates DB
    pass

def dnfUpdate():
    subprocess.run(['sudo', 'dnf', 'update', '-y']) #Updates DB
    pass

def setupBuildEnvArch():
    global envSet
    list_pkg = ['git', 'base-devel'] #Nedded for Arch makepkg
    pacmanInstall(list_pkg) #Make damn sure build env is ready
    if chkBuildEnvArch():
        envSet = True
        return True
    pass

def chkBuildEnvArch():
    global envSet
    proc1ret, proc2ret = 69420, 177013
    try:
        proc1 = subprocess.Popen(['git', 'help'], stdout=subprocess.DEVNULL)
        proc1.communicate()
        proc1ret = proc1.returncode
    except FileNotFoundError:
        envSet = False
    try:
        proc2 = subprocess.Popen(['makepkg', '-h'], stdout=subprocess.DEVNULL)
        proc2.communicate()
        proc2ret = proc2.returncode
    except FileNotFoundError:
        envSet = False
    if (proc1ret == 0 and proc2ret == 0) or \
            envSet == True:
        envSet = True
        return True
    else: 
        return False 
    pass

def AURBuild(git_link: str):
    global envSet
    chkBuildEnvArch()
    if envSet == False:
        setupBuildEnvArch()
        AURBuild(git_link)
    else:   
        os.chdir("/tmp")
        subprocess.run(['git', 'clone', git_link])
        tmpSpl = git_link.split("/")
        os.chdir(tmpSpl[len(tmpSpl)-1].split(".")[0])
        subprocess.run(['makepkg', '-sci', '--noconfirm'])
    pass

def gitBuild(git_link: str):
    os.chdir("/tmp")
    subprocess.run(['git', 'clone', git_link])
    tmpSpl = git_link.split("/")
    os.chdir(tmpSpl[len(tmpSpl)-1].split(".")[0])
    subprocess.run(['make'])
    subprocess.run(['sudo', 'make', 'install'])
