import pickle

jobs = {}
filename = 'tao_jobs.db'

def save_jobs():
    with open(filename) as file:
        pickle.dump(jobs, file)

def load_jobs():
    with open(filename) as file:
        jobs = pickle.load(file)

def add_job(path, pbs_id, tao_id):
    assert pbs_id not in jobs
    jobs[tao_id] = (pbs_id, path)
    save_jobs()

def get_job(tao_id):
    assert tao_id in jobs
    return jobs[tao_id]

def iter_active():
    pass
