from jobs.models import Job


def create_dummy_job():
    return Job(
        title='Dummy Title',
        job_type=0,
        task='Dummy Task',
        place_of_work='Dummy Place of Work',
        min_salary=1000,
        max_salary=1000,
        working_hours='Dummy Working Hours',
        requirements='Dummy Requirements',
        url='http://www.dummyurl.com'
    )


def create_and_save_dummy_job_to_db():
    job = create_dummy_job()
    job.save()
    return job
