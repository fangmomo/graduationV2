from elasticsearch import Elasticsearch


class ESObject:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=3600)

    # 创建索引 保存
    def save(self, index, body):
        res = self.es.index(index=index, body=body)
        return res

    def delete(self, index, target_id):
        res = self.es.delete(index=index, id=target_id)
        return res

    def update(self, index, target_id, body):
        res = self.es.update(index=index, id=target_id, body=body)
        return res

    def query(self, index, query):
        res = self.es.search(index=index, body=query)
        return res

    def getSource(self,index,target_id):
        res = self.es.get_source(index=index,id=target_id)
        return res

"""
if __name__ == '__main__':
    es = ESObject()
    index = "test"
    body = {"doc": {"age": 37, "country": "china"}}
    query = {
        "query": {
            "match_all": {}
        }
    }
    # res = es.query(index,query)
    target_id = "ieU5Q3EB_R2LEtic6y9Q"
    # res = es.update(index,target_id, body)
    res = es.getSource(index="test", target_id=target_id)
    print(res)
    """
