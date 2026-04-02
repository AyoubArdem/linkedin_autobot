from django.urls import path

from .views import AnalysisDetailView, AnalysisListView, GenerateAnalysisView, HostedAnalyzeProfileView

urlpatterns = [
    path("analyses/", AnalysisListView.as_view(), name="analysis_list"),
    path("analyses/<int:pk>/", AnalysisDetailView.as_view(), name="analysis_detail"),
    path("generate/", GenerateAnalysisView.as_view(), name="analysis_generate"),
    path("analyze/", HostedAnalyzeProfileView.as_view(), name="hosted_analyze_profile"),
]
