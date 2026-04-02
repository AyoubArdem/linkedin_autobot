from django.urls import path

from .views import (
    HostedProfileCollectByNameView,
    HostedProfileCollectView,
    HostedSendConnectionRequestView,
    LeadDetailView,
    LeadInteractionDetailView,
    LeadInteractionListCreateView,
    LeadListCreateView,
    LeadTagDetailView,
    LeadTagListCreateView,
    LinkedInProfilePreviewView,
    LinkedInSendMessageView,
)

urlpatterns = [
    path("leads/", LeadListCreateView.as_view(), name="lead_list"),
    path("leads/<int:pk>/", LeadDetailView.as_view(), name="lead_detail"),
    path("tags/", LeadTagListCreateView.as_view(), name="lead_tag_list"),
    path("tags/<int:pk>/", LeadTagDetailView.as_view(), name="lead_tag_detail"),
    path("interactions/", LeadInteractionListCreateView.as_view(), name="interaction_list"),
    path("interactions/<int:pk>/", LeadInteractionDetailView.as_view(), name="interaction_detail"),
    path("linkedin/profile-preview/", LinkedInProfilePreviewView.as_view(), name="linkedin_profile_preview"),
    path("linkedin/send-message/", LinkedInSendMessageView.as_view(), name="linkedin_send_message"),
    path("profiles/collect-by-name/", HostedProfileCollectByNameView.as_view(), name="hosted_profile_collect_by_name"),
    path("profiles/collect/", HostedProfileCollectView.as_view(), name="hosted_profile_collect"),
    path("outreach/send-connection-request/", HostedSendConnectionRequestView.as_view(), name="hosted_send_connection"),
]
