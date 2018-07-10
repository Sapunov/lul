from django.urls import path

from app.spender.views import CategoriesView, TransactionsView

urlpatterns = [
    path('/categories', CategoriesView.as_view()),
    path('/transactions', TransactionsView.as_view())
]
