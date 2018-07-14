from django.urls import path

from app.spender.views import (
    CategoriesView, TransactionsView, CategoryDeleteView,
    CategorySetView, CategoryConfirmView)

urlpatterns = [
    path('/categories/<int:cat_id>', CategoryDeleteView.as_view()),
    path('/categories', CategoriesView.as_view()),
    path('/transactions', TransactionsView.as_view()),
    path('/transactions/<int:transaction_id>/category/<int:category_id>', CategorySetView.as_view()),
    path('/transactions/<int:transaction_id>/category/confirm', CategoryConfirmView.as_view())
]
