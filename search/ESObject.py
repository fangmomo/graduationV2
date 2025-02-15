from elasticsearch import Elasticsearch


class ESObject:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=3600)

    # 创建索引 保存
    def save(self, index, body):
        res = self.es.index(index=index, body=body)
        return res

    def saveById(self, index, body, index_id):
        res = self.es.index(index=index, body=body, id=index_id)
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

    def getSource(self, index, target_id):
        res = self.es.get_source(index=index, id=target_id)
        return res

    def create_index(self, index_name):
        index_mapping = {
            "settings": {"index.analysis.analyzer.default.type": "ik_max_word"},
            "mappings": {
                "properties": {
                    "status": {
                        "type": "text",
                        "index": True,
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    }
                }
            }
        }
        if self.es.indices.exists(index=index_name) is not True:
            res = self.es.indices.create(index=index_name, body=index_mapping)
            print('1', res)

    def count(self, index, query):
        res = self.es.count(index, query)
        return res

    def create_index(self, indexName, indexMapping):
        res = self.es.indices.create(index=indexName, body=indexMapping)
        print('1', res)

"""
if __name__ == '__main__':
    es = ESObject()
    index_mapping = {
        "settings": {"index.analysis.analyzer.default.type": "ik_max_word"},
        "mappings": {
            "properties": {
                "score": {
                    "type": "float",
                    "index": True
                }
            }
        }
    }
    index_name = 'course_evaluation'
    es.create_index(index_name, index_mapping)
"""