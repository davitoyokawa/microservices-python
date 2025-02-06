from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User
from .producer import publish
from .serializers import ProductSerializer
import random

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            'message': 'Lista de todos os produtos na base de dados',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response({
            'message': 'Produto criado com sucesso!',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response({
        'message': 'Produto atualizado com sucesso!',
            'data': serializer.data
        }, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted', pk)
        # return Response(status=status.HTTP_204_NO_CONTENT)# 
        return Response({'message': 'Produto deletado com sucesso!'}, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        user = random.choice(users)
        # serializer = ProductSerializer(users, many=True)
        return Response({"id": user.id})
    
def get_product_ratings(request, id):
    product = get_object_or_404(Product, id=id)

    # Calcular a média de avaliações, se houver
    if product.ratings_count > 0:
        average_rating = round(product.total_ratings / product.ratings_count, 2)
    else:
        average_rating = 0

    return JsonResponse({
        'average_rating': average_rating,
        'ratings_count': product.ratings_count
    })