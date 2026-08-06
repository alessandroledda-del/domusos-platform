from rest_framework import decorators, response, viewsets
from .models import OnboardingProgress
from .serializers import OnboardingProgressSerializer
from .services import compute_onboarding

class OnboardingViewSet(viewsets.ViewSet):
    def list(self, request):
        progress = compute_onboarding(request.user)
        return response.Response(OnboardingProgressSerializer(progress).data)

    @decorators.action(detail=False, methods=["post"])
    def dismiss(self, request):
        progress, _ = OnboardingProgress.objects.get_or_create(user=request.user)
        progress.dismissed = True
        progress.save(update_fields=["dismissed", "updated_at"])
        return response.Response(OnboardingProgressSerializer(progress).data)

    @decorators.action(detail=False, methods=["post"])
    def refresh(self, request):
        progress = compute_onboarding(request.user)
        return response.Response(OnboardingProgressSerializer(progress).data)
