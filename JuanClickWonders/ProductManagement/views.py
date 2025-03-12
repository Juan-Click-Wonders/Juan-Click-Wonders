from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from ProductManagement.models import Products, Category
from ProductManagement.serializers import ProductsSerializer, CategorySerializer


@csrf_exempt
def productsApi(request, id=0):
    if request.method == "GET":
        if id != 0:
            product = Products.objects.filter(product_ID=id).first()
            if product:
                product_serializer = ProductsSerializer(product)
                return JsonResponse(product_serializer.data, safe=False)
            return JsonResponse({"error": "Product not found"}, status=404)
        products = Products.objects.all()

        if not products.exists():
            return JsonResponse({"message": "No items in products"}, status=200)

        products_serializer = ProductsSerializer(products, many=True)
        return JsonResponse(products_serializer.data, safe=False)

    elif request.method == "POST":
        products_data = request.POST.dict()
        product_image = request.FILES.get("product_image")

        if not product_image:
            return JsonResponse({"error": "No image submitted."}, status=400)

        products_data["product_image"] = product_image

        products_serializer = ProductsSerializer(data=products_data)

        if products_serializer.is_valid():
            product = products_serializer.save()
            product.product_image = product_image
            product.save()
            return JsonResponse({"message": "Added Successfully"}, safe=False)

        return JsonResponse({"error": products_serializer.errors}, status=400)

    elif request.method == "PUT":
        products_data = request.POST.dict()
        product_id = products_data.get("product_ID")

        if not product_id:
            return JsonResponse({"error": "product_ID is required"}, status=400)

        product = Products.objects.filter(product_ID=product_id).first()
        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)

        product_serializer = ProductsSerializer(product, data=products_data)
        if product_serializer.is_valid():
            product = product_serializer.save()

            if "product_image" in request.FILES:
                product.product_image = request.FILES["product_image"]
                product.save()

            return JsonResponse({"message": "Updated Successfully"}, status=200)

        return JsonResponse({"error": product_serializer.errors}, status=400)

    elif request.method == "DELETE":
        product = Products.objects.filter(product_ID=id).first()
        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)

        product.delete()
        return JsonResponse({"message": "Deleted Successfully"}, status=200)


@csrf_exempt
def categoryApi(request, id=0):
    if request.method == "GET":
        if id != 0:
            category = Products.objects.filter(category_ID=id).first()
            if category:
                category_serializer = CategorySerializer(category)
                return JsonResponse(category_serializer.data, safe=False)
            return JsonResponse({"Error!": "Product not found"}, status=404)
        category = Category.objects.all()

        if not category.exists():
            return JsonResponse({"message": "No existing categories"}, status=200)

        category_serializer = CategorySerializer(category, many=True)
        return JsonResponse(category_serializer.data, safe=False)

    elif request.method == "POST":
        category_data = JSONParser().parse(request)
        category_serializer = CategorySerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Error! Failed to Add", safe=False)

    elif request.method == "PUT":
        category_data = JSONParser().parse(request)
        category = category.objects.get(category_ID=category_data["category_ID"])
        category_serializer = CategorySerializer(category, data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Error! Failed to Update")

    elif request.method == "DELETE":
        category = category.objects.get(category_ID=id)
        category.delete()
        return JsonResponse("Deleted Successfully", safe=False)
