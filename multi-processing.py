from multiprocessing import Pool, cpu_count
import requests


def simple_request(id_=1):
    url = 'http://localhost:8081/api/v1/weather-data/{}'.format(id_)
    response = requests.get(url)
    print(response.text)


if __name__ == '__main__':
    range_ = range(1, 3000)

    agents = cpu_count()
    chunk_size_ = int(agents / 2)
    pool = Pool(processes=agents)
    pool.map(simple_request, range_, chunk_size_)
