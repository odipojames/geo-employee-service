from cloudinary_storage.storage import MediaCloudinaryStorage

class OverwriteStorage(MediaCloudinaryStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
