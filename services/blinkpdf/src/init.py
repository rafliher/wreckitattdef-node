from module import register, reset

if __name__ == '__main__':
    reset()
    register("admin","admin",True)
    register("user","user",False)