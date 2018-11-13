from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, connections
from datetime import datetime
connections.connections.create_connection(hosts=['127.0.0.1'])
class ArticleType(DocType):
    title=Text(analyzer="ik_max_word")
    datalist=Keyword()
    dianzang=Integer()
    shouchang=Integer()
    pinglunshu=Integer()
    #zhengwen=Keyword()
    #tag=Integer()
    class Meta:
        index='jobberly'
        doc_type="article"

if __name__ == '__main__':
    ArticleType.init()


