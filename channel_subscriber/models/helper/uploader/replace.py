from django.core.files.storage import default_storage


def replace_old_with_new_one(instance, model):
    """
    Utility method to replace an old file with a new one.

    Args:
    instance: The instance of the model containing the FileField.
    model: The model class.

    Returns:
    None
    """
    if instance.pk:  # If the instance already exists (i.e., it has a primary key)
        try:
            old_instance = model.objects.get(pk=instance.pk)
            if old_instance.file:  # If there's a file associated with the old instance
                # Delete the old file before saving the new one
                default_storage.delete(old_instance.file.path)
        except model.DoesNotExist:
            pass  # Handle the case where the old instance doesn't exist anymore
