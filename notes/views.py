from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Note
from .serializers import NoteSerializer
from .tasks import send_note_email


class NoteListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(user=request.user).order_by("-created_at")
        serializer = NoteSerializer(notes, many=True)

        return Response(
            {
                "message": "Your notes",
                "count": notes.count(),
                "notes": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            note = serializer.save(user=request.user)

            # ASYNC EMAIL
            send_note_email.delay(
                request.user.email,
                note.title,
                "Created",
            )

            return Response(
                {
                    "message": "Note created successfully",
                    "note": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Note, pk=pk, user=user)

    def get(self, request, pk):
        note = self.get_object(pk, request.user)
        serializer = NoteSerializer(note)

        return Response(
            {
                "message": "Note retrieved successfully",
                "note": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        note = self.get_object(pk, request.user)
        serializer = NoteSerializer(note, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # ASYNC EMAIL
            send_note_email.delay(
                request.user.email,
                note.title,
                "Updated",
            )

            return Response(
                {
                    "message": "Note updated successfully",
                    "note": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk, request.user)
        title = note.title
        note.delete()

        # ASYNC EMAIL
        send_note_email.delay(
            request.user.email,
            title,
            "Deleted",
        )

        return Response(
            {"message": "Note deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
