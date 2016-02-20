from jobs.models import Job


class DummyJobManager:
    """
    Osztaly, ami a Django fixture feature-t szeretne helyettesiteni.
    Ahelyett, hogy statikusan megadnank fixture-ket, igy viszonylag
    dinamikusan lehet generalni initial adatot. Azert ha csak
    placeholdernek kellenek munkak, akkor erdemesebb fixture-t
    hasznalni, mert az darabonkenti save() ha sok job van nagyon
    lassu
    """

    index = 0

    def __init__(self, num=0):
        for i in range(num):
            self.create_and_save_job()

    def create_and_save_job(self, **kwargs):
        job = self.__create_job(**kwargs)
        job.full_clean()
        job.save()
        return job

    def create_and_save_jobs(self, times):
        for i in range(times):
            yield self.create_and_save_job()

    def __create_job(self, **kwargs):
        DummyJobManager.index = DummyJobManager.index + 1
        return Job(
            title=kwargs.get(
                'title',
                'Dummy title ' + str(DummyJobManager.index)
                ),
            job_type=kwargs.get('job_type', 0),
            task=kwargs.get('task', 'Dummy Task'),
            place_of_work=kwargs.get('place_of_work', 'Dummy Place of Work'),
            min_salary=kwargs.get('min_salary', 1000),
            max_salary=kwargs.get('max_salary', 1000),
            working_hours=kwargs.get('working_hours', 'Dummy Working Hours'),
            requirements=kwargs.get('requirements', 'Dummy Requirements'),
            url=kwargs.get(
                'url',
                'https://www.dummyurl' + str(DummyJobManager.index) + '.com'
            )
        )
