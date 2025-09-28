class ReadOnlyOrOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Others can only read.
    """

    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Read permissions for participants, write permissions for owners."""
        # Read permissions for any participant
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'conversation'):
                return obj.conversation.participants.filter(id=request.user.id).exists()
            if hasattr(obj, 'participants'):
                return obj.participants.filter(id=request.user.id).exists()
        
        # Write permissions only for the owner (Explicitly check the methods)
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, 'sender'):
                return obj.sender == request.user
        
        return False