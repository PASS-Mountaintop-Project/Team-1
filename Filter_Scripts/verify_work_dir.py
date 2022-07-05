from os.path import exists, dirname, abspath
from os import chdir, getcwd

def verify_work_dir(file_path: str, work_dir: str = "auto") -> str:
    """Set the working directory to one level above the given file's directory, then verify with user.

    Args:
        file_path (str): Path of current executing file
        work_dir (str, optional): Specific given working directory. Defaults to "auto".
    """

    #Set working dir
    if (work_dir == "auto"):
        work_dir = dirname(dirname(abspath(file_path)))
        chdir(work_dir)
    else:
        chdir(work_dir)

    #Verify working dir
    verify = input("Working dir is '" + getcwd() + "'. Proceed? (Y/N): ")
    if (not (verify == 'Y' or verify == 'y')):
        verify = input("Change work dir? (Y|N): ")
        if (verify == 'Y' or verify == 'y'):
            work_dir = input("Enter new work dir: ")
            if (not exists(work_dir)):
                print("Dir entered does not exist...exiting")
                exit(1)
            chdir(work_dir)
        else:
            print("Exiting...")
            exit(1)
    return work_dir
            
            

if __name__ == "__main__":
    verify_work_dir(__file__) #Test for this file