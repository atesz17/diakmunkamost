from jobs.models import Job


def create_dummy_job():
    return Job(
        title='a',
        job_type=0,
        task='a',
        place_of_work='a',
        min_salary=10,
        max_salary=10,
        working_hours='a',
        requirements='a',
        url='http://www.lololol123lol.com'
    )


def create_and_save_dummy_job_to_db():
    job = create_dummy_job()
    job.save()
    return job
