from rest_framework import status
#->http 상태 정보를 보여주기 위한
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from articles.models import Article
from articles.serializers import ArticleSerializer

# 원래 시리얼라이져 없이 쓰던 함수
# @api_view(('GET',))
# def index(request):
#     articles = Article.objects.all()
#     article = articles[0]
#     article_data = {
#         'title':article.title,
#         'content':article.content,
#         'created_at':article.created_at,
#         'updated_at':article.updated_at,
#     }
#     print('articles')
#     return Response(article_data)

@api_view(('GET','POST'))
def index(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        # article = articles[0]
        serializer = ArticleSerializer(articles, many=True)
        #article을 아티클시리얼라이져에 넣어서 시리얼라이져라는 객체를 만들어줌
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            # , status = status.HTTP_201_CREATED 원래는 HTTP 200 ok 가 떴는데 내가 원하는대로 띄울 수 있단건가 그럼 부정확한거 아닌가?
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # 에러를 클라이언트측에 노출하는 건 보안상 좋지 않다

@api_view(('GET','PUT','DELETE'))
def article_view(request,article_id):
    if request.method == 'GET':
        article= Article.objects.get(id=article_id)
        # article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'PUT':
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            serializer.error()
        return Response(serializer.data)
    elif request.method == 'DELETE':
         article = get_object_or_404(Article, id=article_id)
         article.delete()
         #시리얼라이즈할 필요도 없이! 걍 삭-제!
         return Response(status=status.HTTP_204_NO_CONTENT)