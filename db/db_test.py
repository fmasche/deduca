
def get_queries():
    """Stub, this will use Nikki's code"""
    return [{'role': 'HR', 'user': 'bob', 'rows_examined': 4, 'timestamp': '11-24-18 19:44:57', 'text': 'select * from patient'},
            {'role': 'DOC', 'user': 'alice', 'rows_examined': 2, 'timestamp': '11-24-18 19:45:00', 'text': 'select * from billing'}
            ]


if __name__ == "__main__":
    for q in get_queries():
        print(q)