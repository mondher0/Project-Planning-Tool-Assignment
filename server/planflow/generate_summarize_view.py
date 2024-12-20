import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import os
from dotenv import load_dotenv

load_dotenv()


class GenerateSummarizeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Summarize the project description using Hugging Face API.
        """
        # Get the input text from the request
        description = request.data.get("description", "")

        if not description:
            return Response(
                {"error": "Description is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}
        payload = {"inputs": description}

        try:
            # Make the API request
            response = requests.post(
                os.getenv("HUGGING_FACE_API_URL"), json=payload, headers=headers
            )
            response.raise_for_status()
            summary = response.json()[0].get("summary_text", "")

            return Response({"summary_description": summary}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
