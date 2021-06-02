def stand_up_postgres():
    pass

def import_clean_data():
    pass

def stand_up_redis():
    pass

def clone_apps():

    pass

def start_apps():
    # TODO ensure apps can connect to postgres
    # TODO ensure apps can connect to redis
    pass

def stand_up_nginx():
    # TODO copy nginx config
    pass

def test():
    import subprocess
    bashCommand = "ls"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print output
