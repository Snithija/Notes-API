from django.urls import path
from .views import NoteListCreateAPIView, NoteDetailAPIView

urlpatterns = [
    # List all notes / Create note
    path("", NoteListCreateAPIView.as_view(), name="note-list-create"),

    # Retrieve / Update / Delete single note
    path("<int:pk>/", NoteDetailAPIView.as_view(), name="note-detail"),
]
